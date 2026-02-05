import csv
import json
import re

# Load all connections
connections = []
with open('Connections.csv', 'r', encoding='utf-8') as f:
    lines = f.readlines()
    
header_idx = None
for i, line in enumerate(lines):
    if line.startswith('First Name,'):
        header_idx = i
        break

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

# Niche keywords for fintech/BaaS/AI Compliance
niche_keywords = [
    'fintech', 'baas', 'bank', 'banking', 'compliance', 'regtech', 'kyc', 'aml',
    'payments', 'lending', 'credit', 'debit', 'card', 'issuing', 'acquiring',
    'sponsor bank', 'program manager', 'money transmitter', 'mtl', 'ledger',
    'embedded finance', 'banking as a service', 'treasury', 'wire', 'ach',
    'visa', 'mastercard', 'stripe', 'plaid', 'unit', 'synctera', 'treasury prime',
    'column', 'bond', 'marqeta', 'galileo', 'i2c', 'tabapay', 'dwolla',
    'cross river', 'sutton', 'evolve', 'blue ridge', 'coastal', 'celtic',
    'ai', 'artificial intelligence', 'machine learning', 'llm', 'agent'
]

# High-value company keywords
tier1_companies = [
    'stripe', 'plaid', 'unit', 'synctera', 'treasury prime', 'column', 'bond',
    'marqeta', 'galileo', 'airwallex', 'wise', 'revolut', 'mercury', 'brex', 'ramp',
    'deel', 'visa', 'mastercard', 'jpmorgan', 'goldman', 'morgan stanley',
    'cross river', 'evolve', 'sutton', 'coastal community', 'blue ridge',
    'a16z', 'sequoia', 'accel', 'index', 'ribbit', 'qed', 'nyca',
    'openai', 'anthropic', 'google', 'meta', 'microsoft', 'nvidia',
    'y combinator', 'yc'
]

# Senior roles that indicate influence
senior_roles = [
    'ceo', 'founder', 'co-founder', 'cofounder', 'chief', 'president',
    'general partner', 'managing partner', 'partner', 'managing director',
    'head of', 'vp', 'vice president', 'director', 'svp', 'evp'
]

# Known high-follower individuals (from public knowledge)
known_influencers = {
    'jeremiah owyang': {'followers': '38K', 'note': 'Verified - AI/Blitzscaling GP'},
    'jerry liu': {'followers': '~50K', 'note': 'LlamaIndex founder'},
    'jack zhang': {'followers': '~15K', 'note': 'Airwallex CEO'},
    'jason zhang': {'followers': '~8K', 'note': 'Mercury COO'},
    'immad akhund': {'followers': '~20K', 'note': 'Mercury CEO'},
}

def score_connection(c):
    score = 0
    reasons = []
    
    name_lower = c['name'].lower()
    company_lower = c['company'].lower()
    position_lower = c['position'].lower()
    combined = f"{company_lower} {position_lower}"
    
    # Known influencer bonus
    if name_lower in known_influencers:
        score += 100
        reasons.append(f"Known influencer: {known_influencers[name_lower]['note']}")
    
    # Tier 1 company
    for tc in tier1_companies:
        if tc in company_lower:
            score += 30
            reasons.append(f"Tier 1 company: {c['company']}")
            break
    
    # Senior role
    for sr in senior_roles:
        if sr in position_lower:
            score += 20
            reasons.append(f"Senior role")
            break
    
    # Niche relevance
    niche_matches = []
    for nk in niche_keywords:
        if nk in combined:
            niche_matches.append(nk)
    if niche_matches:
        score += len(niche_matches) * 10
        reasons.append(f"Niche match: {', '.join(niche_matches[:3])}")
    
    # Specific high-value roles
    if 'general partner' in position_lower or 'gp' in position_lower:
        score += 25
        reasons.append("VC General Partner")
    
    if 'compliance' in position_lower or 'regulatory' in position_lower:
        score += 15
        reasons.append("Compliance/Regulatory role")
    
    if ('head' in position_lower or 'director' in position_lower) and ('partnership' in position_lower or 'bd' in position_lower):
        score += 15
        reasons.append("BD/Partnerships leader")
    
    return score, reasons

# Score all connections
scored = []
for c in connections:
    score, reasons = score_connection(c)
    if score > 0:
        c['score'] = score
        c['reasons'] = reasons
        scored.append(c)

# Sort by score
scored.sort(key=lambda x: x['score'], reverse=True)

# Output top 50
print("=" * 100)
print("TOP 50 SUPER-NODES FOR FINTECH/BAAS/AI COMPLIANCE")
print("Ranked by: Company tier, Role seniority, Niche relevance")
print("=" * 100)
print()

for i, c in enumerate(scored[:50], 1):
    known = known_influencers.get(c['name'].lower(), {})
    followers = known.get('followers', 'TBD')
    
    print(f"{i:2d}. {c['name']}")
    print(f"    📍 {c['position']} @ {c['company']}")
    print(f"    👥 Followers: {followers}")
    print(f"    🎯 Score: {c['score']} | {'; '.join(c['reasons'])}")
    print(f"    🔗 {c['url']}")
    print()

# Save full ranked list
with open('ranked_supernodes.json', 'w') as f:
    json.dump(scored[:100], f, indent=2)

print(f"\nSaved top 100 to ranked_supernodes.json")

# Also create focused list for fintech/BaaS
baas_focused = [c for c in scored if any(kw in f"{c['company']} {c['position']}".lower() 
    for kw in ['bank', 'baas', 'compliance', 'sponsor', 'program manager', 'embedded', 
               'treasury', 'payments', 'issuing', 'ledger', 'synctera', 'unit', 'column',
               'cross river', 'evolve', 'sutton', 'marqeta', 'galileo'])]

print(f"\n{'=' * 100}")
print("BAAS/SPONSOR BANK FOCUSED (Your core niche)")
print("=" * 100)
for i, c in enumerate(baas_focused[:20], 1):
    print(f"{i:2d}. {c['name']} | {c['position']} @ {c['company']}")
    print(f"    {c['url']}")
