#!/usr/bin/env python3
"""
EmberAI email-signature generator.

Stamps out brand-consistent HTML email signatures from one template.
Edit PEOPLE below (or pass a JSON file) and run:

    python3 signatures/generate.py

Outputs one ready-to-install HTML file per person into signatures/out/.
Open the file in a browser, Select-All -> Copy, then paste into your
Outlook / mail-client signature editor.

Brand assets (logo, flame) are referenced from the public GitHub Pages CDN
so images render in every mail client without base64 bloat.
"""
import html
import json
import os
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out")

# Public CDN base (GitHub Pages on the Ember-AI-Co/brand-assets repo).
CDN = "https://ember-ai-co.github.io/brand-assets/assets"

# ---- Brand palette (from EmberAI_Brand_Guidelines) -------------------------
EMBER_DARK = "#C46A1A"   # burnt ember orange (labels, links)
EMBER_MID = "#E8913A"    # mid ember
EMBER_LIGHT = "#F0A855"  # light ember
INK = "#1A1714"          # near-black (name)
MUTE = "#5A5248"         # muted grey-brown (address, body)
FAINT = "#9A8E7F"        # faint grey (disclaimer, strapline)

TAGLINE = "BETTER DECISIONS START HERE."
COMPANY_LEGAL = "EmberAI Pty Ltd"
DISCLAIMER = (
    "This email and any files transmitted with it are confidential and intended solely for "
    "the use of the individual or entity to whom they are addressed. If you are not the "
    "addressee you must not read, copy, distribute this information or take action in reliance "
    "on it. If received in error, please delete all copies. "
    f"{COMPANY_LEGAL} accepts no liability for any damage caused in the transmission, receipt "
    "or opening of this message."
)

FONT = "Arial, Helvetica, sans-serif"

# ---- People ----------------------------------------------------------------
# Required: name, title, email, web, web_url, slug
# Optional: phone, mobile, address1, address2
PEOPLE = [
    {
        "slug": "richard-moore",
        "name": "Richard Moore",
        "title": "Director",
        "phone": "07 3808 9917",
        "mobile": "[redacted]",
        "email": "richard@emberai.ai",
        "web": "www.emberai.com.au",
        "web_url": "https://www.emberai.com.au",
        "address1": "21 Godwin Street",
        "address2": "Bulimba QLD 4171",
    },
    {
        "slug": "melissa-davin",
        "name": "Melissa Davin",
        "title": "Director",
        # Mel: mobile only, no landline.
        "mobile": "[redacted]",
        "email": "melissa@emberai.ai",
        "web": "www.emberai.com.au",
        "web_url": "https://www.emberai.com.au",
        "address1": "21 Godwin Street",
        "address2": "Bulimba QLD 4171",
    },
]


def _tel_href(num: str) -> str:
    """Australian E.164 tel: href from a display number."""
    digits = num.replace(" ", "")
    if digits.startswith("0"):
        digits = "+61" + digits[1:]
    return "tel:" + digits


def contact_row(label: str, value: str, href: str) -> str:
    return f"""
        <tr>
          <td style="padding:1px 10px 1px 0;font-family:{FONT};font-size:12px;font-weight:bold;color:{EMBER_DARK};vertical-align:top;">{label}</td>
          <td style="padding:1px 0;font-family:{FONT};font-size:12px;vertical-align:top;">
            <a href="{href}" style="color:{EMBER_DARK};text-decoration:underline;font-weight:bold;">{html.escape(value)}</a>
          </td>
        </tr>"""


def build_signature(p: dict) -> str:
    name = html.escape(p["name"])
    title = html.escape(p["title"]).upper()

    address_rows = ""
    for key in ("address1", "address2"):
        if p.get(key):
            address_rows += (
                f'<div style="font-family:{FONT};font-size:12px;color:{MUTE};'
                f'line-height:18px;">{html.escape(p[key])}</div>'
            )

    rows = ""
    if p.get("phone"):
        rows += contact_row("P", p["phone"], _tel_href(p["phone"]))
    if p.get("mobile"):
        rows += contact_row("M", p["mobile"], _tel_href(p["mobile"]))
    rows += contact_row("E", p["email"], "mailto:" + p["email"])
    rows += contact_row("W", p["web"], p["web_url"])

    # The signature itself: a single presentation table, all-inline styles.
    return f"""<table role="presentation" cellpadding="0" cellspacing="0" border="0" style="border-collapse:collapse;background:#ffffff;">
  <tr><td style="padding:0 0 2px 0;font-family:{FONT};font-size:20px;font-weight:bold;color:{INK};line-height:24px;">{name}</td></tr>
  <tr><td style="padding:0 0 6px 0;font-family:{FONT};font-size:11px;font-weight:bold;color:{EMBER_DARK};letter-spacing:2px;">{title}</td></tr>
  <tr><td style="padding:0 0 12px 0;">{address_rows}</td></tr>
  <tr><td style="padding:0 0 12px 0;">
    <table role="presentation" cellpadding="0" cellspacing="0" border="0" width="480" style="border-collapse:collapse;table-layout:fixed;">
      <tr>
        <td width="160" height="6" style="background:{EMBER_DARK};font-size:0;line-height:0;">&nbsp;</td>
        <td width="160" height="6" style="background:{EMBER_MID};font-size:0;line-height:0;">&nbsp;</td>
        <td width="160" height="6" style="background:{EMBER_LIGHT};font-size:0;line-height:0;">&nbsp;</td>
      </tr>
    </table>
  </td></tr>
  <tr><td style="padding:0 0 12px 0;">
    <table role="presentation" cellpadding="0" cellspacing="0" border="0" style="border-collapse:collapse;">{rows}
    </table>
  </td></tr>
  <tr><td style="padding:0 0 4px 0;">
    <img src="{CDN}/emberai-logo.png" alt="EmberAI" width="200" height="45" style="display:block;border:0;outline:none;">
  </td></tr>
  <tr><td style="padding:0 0 12px 0;font-family:{FONT};font-size:10px;font-weight:bold;color:{FAINT};letter-spacing:1.5px;">{TAGLINE}</td></tr>
  <tr><td style="border-top:1px solid #E8E2D8;padding:8px 0 0 0;">
    <div style="font-family:{FONT};font-size:9px;font-style:italic;color:{FAINT};line-height:13px;max-width:520px;">{DISCLAIMER}</div>
  </td></tr>
</table>"""


def build_page(p: dict, sig: str) -> str:
    """Full standalone HTML doc — open in a browser, Select-All, Copy, paste into mail client."""
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<title>EmberAI signature — {html.escape(p['name'])}</title></head>
<body style="margin:0;padding:24px;background:#ffffff;">
{sig}
</body></html>"""


def main():
    people = PEOPLE
    if len(sys.argv) > 1:
        with open(sys.argv[1]) as f:
            people = json.load(f)

    os.makedirs(OUT_DIR, exist_ok=True)
    for p in people:
        sig = build_signature(p)
        page = build_page(p, sig)
        path = os.path.join(OUT_DIR, p["slug"] + ".html")
        with open(path, "w") as f:
            f.write(page)
        print(f"  {p['name']:<18} -> {path}")


if __name__ == "__main__":
    print("Generating EmberAI signatures:")
    main()
