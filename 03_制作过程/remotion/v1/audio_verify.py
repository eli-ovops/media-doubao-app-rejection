from pathlib import Path
import subprocess,json,sys
p=Path(__file__).resolve().parent
subprocess.run([sys.executable,str(p/'diagnose_audio.py')],check=True,capture_output=True)
rows=json.loads((p/'qc/final/audio-diagnosis.json').read_text())
result={'method':'All 7 retained clip interiors: full-sample FFT lag search +/-500 ms, 16 kHz mono. Original to prepared and prepared to final compared separately; no direct hearing or ASR correctness claim.','rows':rows,'audioTimelineCheck':'PASS' if all(r['sourceToFinal'][0]>.9 and abs(r['sourceToFinal'][1])<1 and r['preparedToFinal'][0]>.98 and abs(r['preparedToFinal'][1])<1 for r in rows) else 'REVIEW'}
(p/'qc/final/audio-correlation.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
