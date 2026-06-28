import json

with open('parametric_results.json') as f:
    results = json.load(f)

print(f'Total results: {len(results)}')
for r in results:
    label = r['label']
    if r['converged']:
        apex = r['dz_apex']
        track = r['dz_track']
        print(f"  {label:20s} | Apex: {apex:+8.2f} um | Track: {track:+8.2f} um")
    else:
        print(f"  {label:20s} | FALHA")
