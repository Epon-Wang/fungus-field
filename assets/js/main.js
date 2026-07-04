(function () {
  const storageKey = "fungus-field-theme";
  const body = document.body;
  const toggle = document.getElementById("theme-toggle");
  const icon = toggle ? toggle.querySelector(".theme-toggle__icon") : null;

  function prefersDark() {
    return window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches;
  }

  function applyTheme(theme) {
    const isDark = theme === "dark";
    body.classList.toggle("dark", isDark);
    if (icon) {
      icon.textContent = isDark ? "☀" : "☾";
    }
  }

  const savedTheme = localStorage.getItem(storageKey);
  applyTheme(savedTheme || (prefersDark() ? "dark" : "light"));

  if (toggle) {
    toggle.addEventListener("click", function () {
      const nextTheme = body.classList.contains("dark") ? "light" : "dark";
      localStorage.setItem(storageKey, nextTheme);
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
