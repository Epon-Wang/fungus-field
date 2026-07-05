# Post Index Generator Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Generate the home, archive, search, and topics pages from one post metadata file.

**Architecture:** Keep the site as plain static HTML. Store post metadata in `posts.json`, render the list sections into existing HTML shells, and verify generated pages are up to date with a check command.

**Tech Stack:** Python 3 standard library, POSIX shell, static HTML/CSS/JS.

---

### Task 1: Add The Generator Contract

**Files:**
- Create: `scripts/verify-generated-pages.sh`

- [ ] **Step 1: Write the failing verification script**

Create `scripts/verify-generated-pages.sh` that runs `python3 scripts/generate-list-pages.py --check` and verifies core generated links are present.

- [ ] **Step 2: Run the script to verify it fails**

Run: `bash scripts/verify-generated-pages.sh`
Expected: FAIL because `scripts/generate-list-pages.py` does not exist yet.

### Task 2: Add Metadata And Generator

**Files:**
- Create: `posts.json`
- Create: `scripts/generate-list-pages.py`
- Modify: `index.html`
- Modify: `archives.html`
- Modify: `search.html`
- Modify: `topics.html`

- [ ] **Step 1: Add `posts.json`**

Add metadata for `posts/2026-07-04_frege/` and `posts/first-post/`.

- [ ] **Step 2: Add the generator**

Create `scripts/generate-list-pages.py` to render generated sections into marker-delimited regions in the four list pages.

- [ ] **Step 3: Run the generator**

Run: `python3 scripts/generate-list-pages.py`
Expected: generated list pages contain both posts and topics from `posts.json`.

### Task 3: Verify

**Files:**
- Check: `posts.json`
- Check: `scripts/generate-list-pages.py`
- Check: `scripts/verify-generated-pages.sh`
- Check: generated list pages

- [ ] **Step 1: Run generated-page verification**

Run: `bash scripts/verify-generated-pages.sh`
Expected: PASS.

- [ ] **Step 2: Run existing tag navigation verification**

Run: `bash scripts/verify-tag-navigation.sh`
Expected: PASS.
