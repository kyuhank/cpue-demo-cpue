"""Write a short CPUE report from the verified comparison outputs."""
import base64, csv, html, json, os
from pathlib import Path
out=Path('outputs');manifest=json.loads((out/'manifest.json').read_text())
rows=list(csv.DictReader((out/'comparison.csv').open()));last=rows[-1]
body=f'<p>Two alternative standardisations were fitted to the same synthetic longline records for {rows[0]["year"]}–{last["year"]}. Indices are relative measures of abundance.</p>'
body+=(out/'cpue.svg').read_text()
body+=f'<h2>Comparison</h2><p>In {last["year"]}, the relative index is {float(last["analysis_A"]):.3f} for analysis A and {float(last["analysis_B"]):.3f} for analysis B. Model choices alter the index supplied to the assessment; both series and their provenance are retained.</p>'
body+='<table><tr><th>Year</th><th>Analysis A</th><th>Analysis B</th></tr>'+''.join(f'<tr><td>{r["year"]}</td><td>{float(r["analysis_A"]):.3f}</td><td>{float(r["analysis_B"]):.3f}</td></tr>' for r in rows[-5:])+'</table>'
body+='<h2>Recorded sources</h2><p>Each assessment input uses its corresponding CPUE analysis directly.</p><details><summary>Data, code and settings</summary><pre>'+html.escape(json.dumps(manifest,indent=2))+'</pre></details>'
for name in ['cpue.csv','comparison.csv','manifest.json']:
    body+=f'<a download="{name}" href="data:application/octet-stream;base64,{base64.b64encode((out/name).read_bytes()).decode()}">{name}</a> '
text='<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>CPUE report</title><style>body{font:17px/1.6 Arial;color:#12304c;background:#f8fbfc;margin:auto;max-width:960px;padding:30px}h1{font:38px Georgia}h2{font-size:22px}svg{width:100%}table{border-collapse:collapse;width:100%}td,th{padding:8px;text-align:left;border-bottom:1px solid #dce5ea}a{color:#0085ca}pre{white-space:pre-wrap;overflow-wrap:anywhere;font-size:12px}small{color:#607984}</style><h1>Longline CPUE report</h1>'+body+'<p><small>Synthetic data and illustrative models. No management advice.</small></p></html>'
(out/'report.html').write_text(text);(out/'results.html').write_text(text)
print('CPUE REPORT complete: report.html; two analyses and recorded source manifests',flush=True)
