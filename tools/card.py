"""Share card, 1200x630, drawn as HTML and shot with headless Chrome (PIL here cannot stack Thai tone marks)."""
import math, pathlib, subprocess, tempfile
from PIL import Image

root = pathlib.Path(__file__).resolve().parent.parent
out = root / "docs" / "card.jpg"
vials = ""
for i in range(10):
    x = 660 + i * 50
    vials += f'<rect x="{x-15}" y="80" width="30" height="14" fill="#f0c23c" stroke="#eceae4" stroke-width="3"/>'
    vials += f'<rect x="{x-18}" y="94" width="36" height="70" rx="7" fill="#2a3440" stroke="#eceae4" stroke-width="3"/><rect x="{x-14}" y="138" width="28" height="22" fill="#cfc8b4"/>'
    if i == 0:
        vials += f'<path d="M{x-22} 76 L{x+22} 168 M{x+22} 76 L{x-22} 168" stroke="#e2685c" stroke-width="6"/>'
    if i in (1, 2):
        vials += f'<rect x="{x-25}" y="72" width="50" height="100" rx="10" fill="none" stroke="#7da2e6" stroke-width="5"/>'
pts = " ".join(f"{660 + k / 300 * 480:.1f},{520 - 260 * math.exp(-((k / 300 - 0.5) / 0.05) ** 2):.1f}" for k in range(301))
pts2 = " ".join(f"{660 + k / 300 * 480:.1f},{520 - 247 * math.exp(-((k / 300 - 0.5) / 0.05) ** 2):.1f}" for k in range(301))
html = f"""<!doctype html><meta charset="utf-8"><style>
body{{margin:0;width:1200px;height:630px;background:#121419;color:#eceae4;font-family:Arial,sans-serif;overflow:hidden;position:relative}}
.t{{position:absolute;left:62px}}
</style>
<svg width="1200" height="630" style="position:absolute;left:0;top:0">{vials}
<line x1="660" y1="520" x2="1140" y2="520" stroke="#a3a7b0" stroke-width="4"/>
<polyline points="{pts}" fill="none" stroke="#7da2e6" stroke-width="6"/>
<polyline points="{pts2}" fill="none" stroke="#e2685c" stroke-width="6" stroke-dasharray="14 12"/></svg>
<div class="t" style="top:100px;font:bold 28px 'Courier New',monospace;color:#f0c23c">THIRD-PARTY LAB TESTING</div>
<div class="t" style="top:150px;font:bold 92px/1.05 Arial">The Bridge<br>Vial</div>
<div class="t" style="top:370px;font:bold 58px Tahoma;color:#a3a7b0">ขวดเทียบ</div>
<div class="t" style="top:462px;font:bold 28px 'Courier New',monospace">Janoshik once, Thai labs after.</div>
<div class="t" style="top:502px;font:30px Tahoma;color:#a3a7b0">ตรวจที่ปรากครั้งเดียว ที่เหลือแล็บไทย</div>
<div class="t" style="top:566px;font:bold 28px 'Courier New',monospace;color:#f0c23c">nanobotco.github.io/bridge-vial</div>"""
with tempfile.TemporaryDirectory() as tmp:
    page, png = pathlib.Path(tmp) / "card.html", pathlib.Path(tmp) / "card.png"
    page.write_text(html, encoding="utf-8")
    subprocess.run(["/Applications/Google Chrome.app/Contents/MacOS/Google Chrome", "--headless=new", "--disable-gpu",
                    "--hide-scrollbars", "--window-size=1200,630", f"--screenshot={png}", page.as_uri()],
                   check=True, capture_output=True)
    Image.open(png).convert("RGB").crop((0, 0, 1200, 630)).save(out, quality=88)
print(out)
