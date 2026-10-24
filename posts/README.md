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

Optional header fields:

```
image: assets/blog/cover-xyz.jpg        # cover image, 1200x675 (16:9); shown on index, post hero and social previews
tags: Vacant land tax, Municipal finance
highlights:                             # rendered as an "In brief" box at the top of the post
  - First key point
  - Second key point
```

In the body: `**bold**` text is highlighted; a `> quote` line becomes a large pull-quote; an *italic* line
right after an image becomes its caption.
