#!/usr/bin/env python3
"""
Render the EmberAI flame+wordmark logo lockup (assets/emberai-logo.png).

Reads the in-repo transparent flame (assets/emberai-flame.png), composes the
"EmberAI" wordmark in DM Serif Display (fetched from Google Fonts at render
time), and screenshots a crisp, auto-cropped transparent PNG via headless
Chrome.

Requirements: macOS with Google Chrome, Python 3 + Pillow, network access
(for the DM Serif Display web font).

    python3 tools/render-logo.py
"""
import base64
import os
import subprocess

from PIL import Image

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FLAME = os.path.join(REPO, "assets", "emberai-flame.png")
OUT = os.path.join(REPO, "assets", "emberai-logo.png")
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

flame_b64 = base64.b64encode(open(FLAME, "rb").read()).decode()

html = f"""<!doctype html><html><head><meta charset="utf-8">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=DM+Serif+Display&display=block" rel="stylesheet">
<style>
  html,body{{margin:0;padding:0;background:transparent;}}
  #wrap{{display:inline-block;padding:24px;white-space:nowrap;}}
  img.flame{{height:96px;width:96px;vertical-align:middle;margin-right:14px;position:relative;top:-6px;}}
  span.word{{font-family:'DM Serif Display',Georgia,serif;font-size:104px;line-height:1;
            letter-spacing:0.5px;vertical-align:middle;}}
  .ember{{color:#1A1714;}}
  .ai{{color:#C46A1A;}}
</style></head>
<body><div id="wrap"><img class="flame" src="data:image/png;base64,{flame_b64}">
<span class="word"><span class="ember">Ember</span><span class="ai">AI</span></span></div></body></html>"""

html_path = os.path.join(REPO, "tools", ".logo.html")
raw_png = os.path.join(REPO, "tools", ".logo_raw.png")
open(html_path, "w").write(html)

subprocess.run(
    [CHROME, "--headless", "--disable-gpu", "--hide-scrollbars",
     "--force-color-profile=srgb", "--default-background-color=00000000",
     "--window-size=2400,600", "--virtual-time-budget=4000",
     f"--screenshot={raw_png}", f"file://{html_path}"],
    check=True, capture_output=True,
)

im = Image.open(raw_png).convert("RGBA")
im = im.crop(im.getbbox())
pad = 16
canvas = Image.new("RGBA", (im.width + pad * 2, im.height + pad * 2), (0, 0, 0, 0))
canvas.paste(im, (pad, pad), im)
canvas.save(OUT)
os.remove(html_path)
os.remove(raw_png)
print(f"logo: {canvas.width}x{canvas.height} -> {OUT}")
