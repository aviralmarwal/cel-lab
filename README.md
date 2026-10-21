# CEL Lab website

Source for https://cel-lab.in — City Experimentation and Learning Lab, IIT Roorkee.

- `data.py` — all site content (lab description, research themes, projects, people, publications, events, opportunities). Edit this.
- `build.py` — generates the static site into `docs/` from `data.py`. Run `python3 build.py` after editing.
- `site-src-assets/` — images (event posters, photos). Copied into `docs/assets/` on build.
- `docs/` — the built site, served by GitHub Pages. Do not edit by hand.

Workflow: edit `data.py` → `python3 build.py` → commit and push `data.py` and `docs/` together.
