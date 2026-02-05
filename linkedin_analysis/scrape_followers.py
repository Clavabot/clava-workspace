import csv
import json
import time
import subprocess
import re

# Load high priority supernodes
high_priority = []
with open('potential_supernodes.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        high_priority.append(row)

# Filter for tier 1 (YC, notable companies, etc)
tier1_keywords = ['yc', 'y combinator', 'airwallex', 'mercury', 'stripe', 'openai', 'llamaindex', 
                  'anthropic', 'coinbase', 'circle', 'plaid', 'brex', 'ramp', 'deel', 'wise',
                  'general partner', 'managing partner', 'bitcoin']

top_profiles = []
for p in high_priority:
    combined = f"{p['company']} {p['position']}".lower()
    if any(kw in combined for kw in tier1_keywords):
        top_profiles.append(p)

# Also add some founders/CEOs from notable companies
for p in high_priority:
    if len(top_profiles) >= 50:
        break
    pos_lower = p['position'].lower()
    if ('ceo' in pos_lower or 'co-founder' in pos_lower) and p not in top_profiles:
        top_profiles.append(p)

print(f"Selected {len(top_profiles)} profiles to scrape (will do first 30)")
print("\nProfiles to scrape:")
for i, p in enumerate(top_profiles[:30]):
    print(f"{i+1}. {p['name']} - {p['position']} @ {p['company']}")
    print(f"   {p['url']}")

# Save the list for the scraper
with open('profiles_to_scrape.json', 'w') as f:
    json.dump(top_profiles[:30], f, indent=2)

print(f"\nSaved {min(30, len(top_profiles))} profiles to profiles_to_scrape.json")
