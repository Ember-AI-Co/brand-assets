# EmberAI Brand Assets

Public CDN for EmberAI brand assets that need a stable, publicly reachable URL —
chiefly **email-signature images** (mail clients can't load images from our
private repos, and base64-embedded images get stripped by Outlook).

Served via **GitHub Pages**:

```
https://ember-ai-co.github.io/brand-assets/assets/<file>
```

## Assets

| File | Use |
|------|-----|
| [`assets/emberai-logo.png`](assets/emberai-logo.png) | Flame + "EmberAI" wordmark lockup (532×120, transparent). Email signatures, light backgrounds. |
| [`assets/emberai-flame.png`](assets/emberai-flame.png) | Flame mark only (512×512, transparent). Favicons, icons, app marks. |

## Email signatures

`signatures/generate.py` stamps out brand-consistent HTML signatures for the
whole team from one template.

Real team data (names + personal mobiles) is **not** committed — it lives in
the gitignored `signatures/people.json`. Copy the format from
`signatures/people.example.json`, then run:

```bash
python3 signatures/generate.py
```

Resolution order: CLI arg JSON > `signatures/people.json` > built-in (empty).
Output lands in the gitignored `signatures/out/<slug>.html` — one
ready-to-install file each (kept local, not pushed to this public repo).

**To install:** open the `.html` file in a browser → Select-All (⌘A / Ctrl-A) →
Copy → paste into your mail client's signature editor.

- **Outlook (New / Web / Mac):** Settings → Mail → Compose and reply →
  Signatures → paste.
- **Outlook (classic Windows):** File → Options → Mail → Signatures → paste.

Current signatures: `richard-moore.html`, `melissa-davin.html`.

## Regenerating the logo

The wordmark is rendered in **DM Serif Display** (brand serif) over the flame
mark. To rebuild after a flame/font change:

```bash
python3 tools/render-logo.py
```

Requires macOS + Google Chrome + Pillow + network (fetches the web font).

## Brand reference

- **Ember orange:** `#C46A1A` (dark) · `#E8913A` (mid) · `#F0A855` (light)
- **Ink:** `#1A1714` · **Muted:** `#5A5248` · **Faint:** `#9A8E7F`
- **Serif (display):** DM Serif Display · **Sans (body):** DM Sans → Arial
- **Tagline:** *Better decisions start here.*

Canonical brand guidelines live in the EmberAI OneDrive →
`Marketing/Brand/EmberAI_Brand_Guidelines.html`.
