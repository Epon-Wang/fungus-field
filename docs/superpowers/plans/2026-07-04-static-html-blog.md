# Static HTML Blog Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a pure static HTML personal blog inspired by the structure of `/home/epon/lilianweng.github.io`, without requiring Jekyll, Hugo, Ruby, Bundler, or any build step.

**Architecture:** The site is plain HTML, CSS, and JavaScript served directly by GitHub Pages. Posts live under `posts/<slug>/index.html`; listing pages are manually maintained. Shared behavior such as theme toggling, search, and the back-to-top link is implemented in one small JavaScript file.

**Tech Stack:** HTML, CSS, vanilla JavaScript, GitHub Pages static hosting.

---

## File Structure

- Create `index.html`: home page with header, welcome section, and post cards.
- Create `archives.html`: chronological list of posts.
- Create `search.html`: client-side search page backed by a small inline post index.
- Create `faq.html`: short maintenance guide for adding Typora-exported HTML posts.
- Create `404.html`: simple not-found page.
- Create `posts/first-post/index.html`: example post page and template for future posts.
- Create `assets/css/style.css`: PaperMod-inspired layout, cards, typography, light/dark theme.
- Create `assets/js/main.js`: theme toggle, search filtering, and back-to-top behavior.

No Git commands should be run by the agent. The user will handle commit, push, and pull operations.

### Task 1: Red Structural Checks

**Files:**
- Check: `index.html`
- Check: `assets/css/style.css`
- Check: `assets/js/main.js`
- Check: `posts/first-post/index.html`

- [ ] **Step 1: Verify target files do not exist yet**

Run:

```bash
test -f index.html
test -f assets/css/style.css
test -f assets/js/main.js
test -f posts/first-post/index.html
```

Expected: each command exits non-zero before implementation.

### Task 2: Create Static Site Files

**Files:**
- Create: `index.html`
- Create: `archives.html`
- Create: `search.html`
- Create: `faq.html`
- Create: `404.html`
- Create: `posts/first-post/index.html`
- Create: `assets/css/style.css`
- Create: `assets/js/main.js`

- [ ] **Step 1: Create the static HTML pages and assets**

Use complete HTML documents for each page. Use root-relative links such as `/assets/css/style.css` and `/posts/first-post/` so GitHub Pages serves them correctly from `fungus-field.github.io`.

### Task 3: Verification

**Files:**
- Verify: all created files

- [ ] **Step 1: Verify required files exist**

Run:

```bash
test -f index.html
test -f archives.html
test -f search.html
test -f faq.html
test -f 404.html
test -f assets/css/style.css
test -f assets/js/main.js
test -f posts/first-post/index.html
```

Expected: each command exits zero after implementation.

- [ ] **Step 2: Verify key links and hooks exist**

Run:

```bash
rg -n "/posts/first-post/|theme-toggle|data-search-root|back-to-top|/assets/css/style.css|/assets/js/main.js" index.html archives.html search.html faq.html 404.html posts/first-post/index.html assets/css/style.css assets/js/main.js
```

Expected: output shows the post link, theme toggle, search root, back-to-top link, and asset references.

- [ ] **Step 3: Start a static preview server**

Run:

```bash
python3 -m http.server 4000
```

Expected: server listens on `http://127.0.0.1:4000/`.
