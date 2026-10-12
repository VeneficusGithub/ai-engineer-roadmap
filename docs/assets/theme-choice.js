/*
 * Keeps a visitor's light/dark choice after the theme button went from three
 * settings (0 = system, 1 = light, 2 = dark) to two (0 = light, 1 = dark).
 *
 * The theme stores the chosen position, so an old "light" would now mean dark.
 * This runs in <head> (see overrides/main.html), after the theme's storage
 * helpers exist but before the theme reads the stored choice.
 */
(() => {
  "use strict";
  try {
    const palette = __md_get("__palette");
    if (!palette || !palette.color) return;
    if (palette.color.media === "(prefers-color-scheme)") {
      // "System": forget the choice, so the theme follows the computer again.
      localStorage.removeItem(`${__md_scope.pathname}.__palette`);
      return;
    }
    const index = palette.color.scheme === "slate" ? 1 : 0;
    if (palette.index !== index) __md_set("__palette", { ...palette, index });
  } catch {
    // Storage unavailable or theme helpers missing: the theme uses its default.
  }
})();
