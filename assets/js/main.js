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

  const searchRoot = document.querySelector("[data-search-root]");
  if (searchRoot) {
    const input = document.getElementById("search-input");
    const items = Array.from(searchRoot.querySelectorAll("[data-search-item]"));

    if (input) {
      input.addEventListener("input", function () {
        const query = input.value.trim().toLowerCase();
        items.forEach(function (item) {
          const haystack = [
            item.dataset.title || "",
            item.dataset.summary || "",
            item.dataset.tags || ""
          ].join(" ");
          item.hidden = query.length > 0 && !haystack.includes(query);
        });
      });
    }
  }
})();
