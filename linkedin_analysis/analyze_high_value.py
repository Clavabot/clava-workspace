import csv
from collections import Counter

# Load potential supernodes
supernodes = []
with open('potential_supernodes.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        supernodes.append(row)

# Prioritize by company recognition & role seniority
tier1_companies = ['stripe', 'airwallex', 'openai', 'anthropic', 'a16z', 'sequoia', 'yc', 'y combinator', 
                   'accel', 'benchmark', 'greylock', 'index', 'google', 'meta', 'nvidia', 'microsoft',
                   'amazon', 'mercury', 'brex', 'ramp', 'plaid', 'carta', 'gusto', 'rippling',
                   'deel', 'remote', 'wise', 'revolut', 'nubank', 'coinbase', 'circle', 'figma']

tier1_roles = ['ceo', 'founder', 'co-founder', 'cofounder', 'general partner', 'managing partner', 
               'managing director', 'partner at', 'investor at', 'gp']

high_priority = []
medium_priority = []
other = []

for sn in supernodes:
    company_lower = sn['company'].lower()
    position_lower = sn['position'].lower()
    
    is_tier1_company = any(tc in company_lower for tc in tier1_companies)
    is_tier1_role = any(tr in position_lower for tr in tier1_roles)
    
    if is_tier1_company or is_tier1_role:
        if is_tier1_company and is_tier1_role:
            high_priority.append(sn)
        else:
            medium_priority.append(sn)
    else:
        other.append(sn)

print(f"=== PRIORITY SUPER-NODES ===\n")
print(f"HIGH PRIORITY ({len(high_priority)}) - Tier 1 company + senior role:")
print("-" * 80)
for sn in high_priority[:40]:
    print(f"{sn['name']}")
    print(f"  {sn['position']} @ {sn['company']}")
    print(f"  {sn['url']}")
    print()

print(f"\nMEDIUM PRIORITY ({len(medium_priority)}) - Either tier1 company OR senior role:")
print("-" * 80)
for sn in medium_priority[:30]:
    print(f"{sn['name']}")
    print(f"  {sn['position']} @ {sn['company']}")
    print(f"  {sn['url']}")
    print()

# Save prioritized list
with open('supernodes_prioritized.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=['priority', 'name', 'position', 'company', 'url', 'email'])
    writer.writeheader()
    for sn in high_priority:
        writer.writerow({**sn, 'priority': 'HIGH'})
    for sn in medium_priority:
        writer.writerow({**sn, 'priority': 'MEDIUM'})
    for sn in other:
        writer.writerow({**sn, 'priority': 'OTHER'})

print(f"\nSaved prioritized list to supernodes_prioritized.csv")
print(f"  HIGH: {len(high_priority)}")
print(f"  MEDIUM: {len(medium_priority)}")
print(f"  OTHER: {len(other)}")
