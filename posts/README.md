# Writing a blog post

Create a new file in this folder named `YYYY-MM-DD-short-slug.md`. Start it with a header block:

```
---
title: Why Indian cities under-tax land
date: 2026-11-02
author: Aviral Marwal
summary: One or two sentences shown on the blog index.
---
```

Then write the post in Markdown below the closing `---`. Run `python3 build.py` and push.
Images go in `site-src-assets/blog/` and are referenced as `../assets/blog/filename.jpg`.
