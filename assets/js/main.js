(function () {
  const storageKey = "fungus-field-theme";
  const body = document.body;
  const root = document.documentElement;
  const toggle = document.getElementById("theme-toggle");
  let transitionTimer = null;

  function prefersDark() {
    return window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches;
  }

  function applyTheme(theme) {
    const isDark = theme === "dark";
    body.classList.toggle("dark", isDark);
    if (toggle) {
      toggle.setAttribute("aria-label", isDark ? "Switch to light theme" : "Switch to dark theme");
      toggle.setAttribute("aria-pressed", String(isDark));
    }
  }

  function transitionTheme() {
    root.classList.add("transition");
    root.offsetWidth;
    window.clearTimeout(transitionTimer);
    transitionTimer = window.setTimeout(function () {
      root.classList.remove("transition");
    }, 750);
  }

  const savedTheme = localStorage.getItem(storageKey);
  applyTheme(savedTheme || (prefersDark() ? "dark" : "light"));

  if (toggle) {
    toggle.addEventListener("click", function () {
      const nextTheme = body.classList.contains("dark") ? "light" : "dark";
      localStorage.setItem(storageKey, nextTheme);
      transitionTheme();
      applyTheme(nextTheme);
    });
  }

  const backToTop = document.querySelector(".back-to-top");
  if (backToTop) {
    const syncBackToTop = function () {
      backToTop.classList.toggle("is-visible", window.scrollY > 360);
    };
    syncBackToTop();
    window.addEventListener("scroll", syncBackToTop, { passive: true });
  }

  const postContent = document.querySelector(".main--post .typora-content");
  if (postContent) {
    const headings = Array.from(postContent.querySelectorAll("h1, h2, h3, h4")).filter(function (heading) {
      return heading.textContent.trim().length > 0;
    });

    function slugifyHeading(text) {
      return text
        .trim()
        .toLowerCase()
        .replace(/[^a-z0-9]+/g, "-")
        .replace(/^-+|-+$/g, "") || "section";
    }

    function uniqueHeadingId(heading, usedIds) {
      if (heading.id) {
        usedIds.add(heading.id);
        return heading.id;
      }

      const baseId = slugifyHeading(heading.textContent);
      let nextId = baseId;
      let counter = 2;
      while (usedIds.has(nextId) || document.getElementById(nextId)) {
        nextId = baseId + "-" + counter;
        counter += 1;
      }
      heading.id = nextId;
      usedIds.add(nextId);
      return nextId;
    }

    if (headings.length > 0) {
      const toc = document.createElement("nav");
      const tocTitle = document.createElement("div");
      const tocList = document.createElement("ol");
      const usedIds = new Set(Array.from(document.querySelectorAll("[id]")).map(function (element) {
        return element.id;
      }));
      const baseLevel = Math.min.apply(null, headings.map(function (heading) {
        return Number(heading.tagName.slice(1));
      }));

      toc.className = "post-toc";
      toc.setAttribute("aria-label", "Post contents");
      tocTitle.className = "post-toc__title";
      tocTitle.textContent = "Contents";
      tocList.className = "post-toc__list";

      headings.forEach(function (heading) {
        const headingLevel = Number(heading.tagName.slice(1));
        const relativeLevel = Math.min(Math.max(headingLevel - baseLevel, 0), 3);
        const item = document.createElement("li");
        const link = document.createElement("a");

        link.className = "post-toc__link post-toc__link--level-" + relativeLevel;
        link.href = "#" + uniqueHeadingId(heading, usedIds);
        link.textContent = heading.textContent.trim();
        item.appendChild(link);
        tocList.appendChild(item);
      });

      toc.appendChild(tocTitle);
      toc.appendChild(tocList);
      document.body.appendChild(toc);
    }
  }

  const searchTagsRoot = document.querySelector("[data-search-tags-root]");
  if (searchTagsRoot) {
    const input = document.getElementById("search-input");
    const tags = Array.from(searchTagsRoot.querySelectorAll("[data-search-tag]"));
    const postResults = searchTagsRoot.querySelector("[data-search-post-results]");
    const posts = postResults ? Array.from(postResults.querySelectorAll("[data-search-post]")) : [];
    const emptyState = postResults ? postResults.querySelector("[data-search-empty]") : null;

    if (input) {
      const params = new URLSearchParams(window.location.search);
      const tagQuery = (params.get("tag") || "").trim().toLowerCase();

      function syncSearch(query) {
        const normalizedQuery = query.trim().toLowerCase();
        let visiblePostCount = 0;

        tags.forEach(function (tag) {
          const label = (tag.dataset.tagLabel || tag.textContent || "").toLowerCase();
          tag.hidden = normalizedQuery.length > 0 && !label.includes(normalizedQuery);
        });

        if (postResults) {
          postResults.hidden = normalizedQuery.length === 0;
        }

        posts.forEach(function (post) {
          const haystack = [
            post.dataset.title || "",
            post.dataset.summary || "",
            post.dataset.tags || ""
          ].join(" ").toLowerCase();
          const matches = normalizedQuery.length > 0 && haystack.includes(normalizedQuery);
          post.hidden = !matches;
          if (matches) {
            visiblePostCount += 1;
          }
        });

        if (emptyState) {
          emptyState.hidden = normalizedQuery.length === 0 || visiblePostCount > 0;
        }
      }

      if (tagQuery.length > 0) {
        input.value = tagQuery;
        syncSearch(tagQuery);
      }

      input.addEventListener("input", function () {
        syncSearch(input.value);
      });
    }
  }
})();
