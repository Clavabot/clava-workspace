import csv
import re
from collections import Counter

connections = []
with open('Connections.csv', 'r', encoding='utf-8') as f:
    lines = f.readlines()
    
# Find the header line
header_idx = None
for i, line in enumerate(lines):
    if line.startswith('First Name,'):
        header_idx = i
        break

if header_idx is None:
    print("Header not found!")
    exit(1)

# Parse from header onwards
import io
csv_content = ''.join(lines[header_idx:])
reader = csv.DictReader(io.StringIO(csv_content))

for row in reader:
    if row.get('First Name'):
        connections.append({
            'name': f"{row.get('First Name', '')} {row.get('Last Name', '')}".strip(),
            'url': row.get('URL', ''),
            'email': row.get('Email Address', ''),
            'company': row.get('Company', ''),
            'position': row.get('Position', ''),
            'connected_on': row.get('Connected On', '')
        })

print(f"Total connections: {len(connections)}")
print()

# Analyze by company
companies = Counter([c['company'] for c in connections if c['company']])
print("Top 25 companies in your network:")
for company, count in companies.most_common(25):
    print(f"  {count:3d} - {company}")
print()

# Analyze by position keywords
positions = [c['position'].lower() for c in connections if c['position']]
keywords = ['ceo', 'founder', 'cto', 'vp', 'vice president', 'director', 'head of', 'partner', 'investor', 'principal', 'managing']
print("Leadership roles in network:")
for kw in keywords:
    count = sum(1 for p in positions if kw in p)
    print(f"  {count:3d} - {kw}")
print()

# Find potential super-nodes (founders, CEOs, partners at notable firms)
super_node_keywords = ['ceo', 'founder', 'co-founder', 'partner', 'investor', 'vc', 'general partner', 'managing director']
potential_supernodes = []
for c in connections:
    pos_lower = c['position'].lower()
    if any(kw in pos_lower for kw in super_node_keywords):
        potential_supernodes.append(c)

print(f"\nPotential super-nodes (founders/CEOs/partners): {len(potential_supernodes)}")
print("\nTop 50 potential super-nodes:")
for c in potential_supernodes[:50]:
    print(f"  {c['name']} | {c['position']} @ {c['company']}")
    print(f"    {c['url']}")

# Save for further analysis
with open('potential_supernodes.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=['name', 'url', 'email', 'company', 'position', 'connected_on'])
    writer.writeheader()
    writer.writerows(potential_supernodes)

print(f"\nSaved {len(potential_supernodes)} potential super-nodes to potential_supernodes.csv")
