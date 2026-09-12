"""Combine the two verified CPUE analyses into a comparison table and figure."""
import csv, hashlib, html, json
from pathlib import Path
out=Path('outputs');out.mkdir(exist_ok=True)
series={};sources={}
for key,label in [('cpue_vessel','A'),('cpue_year','B')]:
    folder=Path('inputs')/key
    series[label]=list(csv.DictReader((folder/'cpue.csv').open()))
    sources[label]=json.loads((folder/'manifest.json').read_text())
assert [r['year'] for r in series['A']]==[r['year'] for r in series['B']], 'CPUE years differ'
assert sources['A']['source_sha256']==sources['B']['source_sha256'], 'CPUE source snapshots differ'
with (out/'cpue.csv').open('w') as f:
    writer=csv.writer(f);writer.writerow(['analysis','year','index'])
    for label,rows in series.items():writer.writerows((label,r['year'],r['index']) for r in rows)
with (out/'comparison.csv').open('w') as f:
    writer=csv.writer(f);writer.writerow(['year','analysis_A','analysis_B','difference'])
    writer.writerows((a['year'],a['index'],b['index'],float(a['index'])-float(b['index'])) for a,b in zip(series['A'],series['B']))
years=[int(r['year']) for r in series['A']]; ymax=max(float(r['index']) for rows in series.values() for r in rows)*1.12
svg='<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 330" role="img" aria-label="Comparison of CPUE analyses A and B"><rect width="900" height="330" fill="white"/><g font-family="Arial" font-size="16" fill="#536b7b">'
for v in [0,ymax/2,ymax]:
    y=265-215*v/ymax;svg+=f'<path d="M65 {y}H855" stroke="#e2ebee"/><text x="8" y="{y+5}">{v:.2f}</text>'
for label,color in [('A','#0085ca'),('B','#d87532')]:
    points=' '.join(f'{65+790*(int(r["year"])-min(years))/(max(years)-min(years) or 1):.2f},{265-215*float(r["index"])/ymax:.2f}' for r in series[label])
    svg+=f'<polyline points="{points}" fill="none" stroke="{color}" stroke-width="3"/><text x="{65 if label=="A" else 270}" y="25" fill="{color}">CPUE analysis {label}</text>'
svg+=f'<text x="65" y="305">{min(years)}</text><text x="813" y="305">{max(years)}</text></g></svg>'
(out/'cpue.svg').write_text(svg)
manifest={**sources['A'],'cpue_comparison':sources,'summary_files':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in out.iterdir() if p.name!='manifest.json'}}
(out/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
print(f'CPUE SUMMARY complete: two analyses; {len(years)} years; comparison.csv and cpue.svg',flush=True)
