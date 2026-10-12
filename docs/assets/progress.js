/*
 * Progress tracking for the AI Engineer Roadmap.
 *
 * Everything is stored in the trainee's own browser (localStorage), so the
 * site needs no server. Content pages only need Markdown markup:
 *   - resources/exercises: links with class "rm-item" (plus "rm-exercise")
 *   - questions: "??? interview" or "??? selfcheck" admonitions
 *   - refresh route: add class "rm-refresh" to either
 */
(() => {
  "use strict";

  const KEY = "ai-engineer-roadmap:v1";

  // ---------- state ----------

  const emptyState = () => ({ done: {}, ratings: {}, route: "full", last: null });

  const isValidState = (value) =>
    value !== null &&
    typeof value === "object" &&
    typeof value.done === "object" &&
    value.done !== null &&
    typeof value.ratings === "object" &&
    value.ratings !== null;

  function loadState() {
    try {
      const parsed = JSON.parse(localStorage.getItem(KEY));
      return isValidState(parsed) ? { ...emptyState(), ...parsed } : emptyState();
    } catch {
      return emptyState();
    }
  }

  function saveState() {
    try {
      localStorage.setItem(KEY, JSON.stringify(state));
    } catch {
      // Storage can be unavailable (private windows, blocked site data).
      // The page keeps working; progress just isn't remembered.
    }
  }

  let state = loadState();

  // ---------- reading content ----------

  const slug = (text) =>
    text.trim().toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "");

  const itemId = (link) => link.dataset.id || `r:${link.getAttribute("href")}`;

  // Enhanced questions get rating buttons inside their summary, so the id is
  // remembered on the element before those buttons are added.
  const questionId = (details) =>
    details.dataset.rmId || `q:${slug(details.querySelector("summary").textContent)}`;

  const QUESTIONS = "details.interview, details.selfcheck";

  /** All trackable entries in a page, so the home page can count other pages. */
  function collectEntries(root) {
    const items = [...root.querySelectorAll("a.rm-item")].map((link) => ({
      id: itemId(link),
      kind: "item",
      refresh: link.classList.contains("rm-refresh"),
    }));
    const questions = [...root.querySelectorAll(QUESTIONS)].map((details) => ({
      id: questionId(details),
      kind: "question",
      refresh: details.classList.contains("rm-refresh"),
    }));
    return [...items, ...questions];
  }

  const isDone = (entry) =>
    entry.kind === "item" ? Boolean(state.done[entry.id]) : state.ratings[entry.id] === "ok";

  function progressOf(entries) {
    const inRoute = entries.filter((entry) => state.route === "full" || entry.refresh);
    return { done: inRoute.filter(isDone).length, total: inRoute.length };
  }

  const reviewCount = () =>
    Object.values(state.ratings).filter((rating) => rating === "review").length;

  // ---------- small DOM helpers ----------

  function el(tag, attributes = {}, children = []) {
    const node = document.createElement(tag);
    for (const [name, value] of Object.entries(attributes)) {
      if (name === "class") node.className = value;
      else if (name === "text") node.textContent = value;
      else node.setAttribute(name, value);
    }
    node.append(...children);
    return node;
  }

  function applyRoute() {
    document.documentElement.classList.toggle("rm-route-refresh", state.route === "refresh");
    for (const button of document.querySelectorAll(".rm-route-toggle [data-route]")) {
      button.setAttribute("aria-pressed", String(button.dataset.route === state.route));
    }
  }

  function bindRouteToggles(onChange) {
    for (const button of document.querySelectorAll(".rm-route-toggle [data-route]")) {
      button.addEventListener("click", () => {
        state.route = button.dataset.route;
        saveState();
        applyRoute();
        onChange();
      });
    }
  }

  const routeToggle = () =>
    el("div", { class: "rm-route-toggle", role: "group", "aria-label": "Kies een route" }, [
      el("button", { type: "button", "data-route": "full" }, ["Volledige route"]),
      el("button", { type: "button", "data-route": "refresh" }, ["Opfrissen"]),
    ]);

  // ---------- stage pages ----------

  function youtubeId(href) {
    try {
      const url = new URL(href);
      if (url.hostname.endsWith("youtube.com") && url.pathname === "/watch") return url.searchParams.get("v");
      if (url.hostname === "youtu.be") return url.pathname.slice(1) || null;
    } catch {
      // Not an absolute URL, so not a video.
    }
    return null;
  }

  // Videos get a preview inside their own link, so clicking it opens the video.
  // The image has no alt text: the link's title already names the video.
  function addThumbnail(link) {
    const id = youtubeId(link.href);
    if (!id) return;
    const image = el("img", {
      class: "rm-thumb-img",
      src: `https://i.ytimg.com/vi/${id}/hqdefault.jpg`,
      alt: "",
      loading: "lazy",
    });
    link.prepend(el("span", { class: "rm-thumb" }, [image]));
  }

  function enhanceItem(link) {
    const item = link.closest("li");
    if (!item) return;
    const id = itemId(link);
    item.classList.add("rm-li");
    if (link.classList.contains("rm-refresh")) item.classList.add("rm-refresh");
    if (link.classList.contains("rm-exercise")) item.classList.add("rm-exercise");
    link.target = "_blank";
    link.rel = "noopener";
    addThumbnail(link);

    const main = el("div", { class: "rm-li-main" });
    main.append(...item.childNodes);

    const checkbox = el("input", {
      type: "checkbox",
      class: "rm-check",
      "data-id": id,
      "aria-label": `Markeer "${link.textContent}" als gedaan`,
    });
    checkbox.checked = Boolean(state.done[id]);
    item.classList.toggle("is-done", checkbox.checked);
    checkbox.addEventListener("change", () => {
      if (checkbox.checked) state.done[id] = true;
      else delete state.done[id];
      item.classList.toggle("is-done", checkbox.checked);
      saveState();
      updateStageToolbar();
    });

    const meta = el("div", { class: "rm-li-meta" });
    if (link.classList.contains("rm-exercise")) {
      meta.append(el("span", { class: "rm-chip rm-chip--exercise", text: "Oefening" }));
    }
    if (link.dataset.source) meta.append(el("span", { class: "rm-chip", text: link.dataset.source }));
    if (link.dataset.time) meta.append(el("span", { class: "rm-chip rm-chip--time", text: link.dataset.time }));

    item.append(el("label", { class: "rm-check-wrap" }, [checkbox]), main, meta);
  }

  function enhanceQuestion(details) {
    const id = questionId(details);
    details.dataset.rmId = id;
    details.classList.add("rm-q");
    const buttons = [
      ["ok", "Kon ik beantwoorden"],
      ["review", "Nog herhalen"],
    ].map(([rating, label]) => {
      const button = el("button", {
        type: "button",
        class: "rm-rate",
        "data-rating": rating,
        "aria-pressed": "false",
        text: label,
      });
      button.addEventListener("click", (event) => {
        // The rating sits in the summary row: don't open or close the answer.
        event.preventDefault();
        event.stopPropagation();
        if (state.ratings[id] === rating) delete state.ratings[id];
        else state.ratings[id] = rating;
        saveState();
        renderRating();
        updateStageToolbar();
      });
      return button;
    });

    function renderRating() {
      const rating = state.ratings[id] || "";
      details.dataset.rating = rating;
      for (const button of buttons) {
        button.setAttribute("aria-pressed", String(button.dataset.rating === rating));
      }
    }

    details
      .querySelector("summary")
      .append(el("span", { class: "rm-rating", role: "group", "aria-label": "Beoordeel jezelf" }, buttons));
    renderRating();
  }

  let stageContent = null;

  function updateStageToolbar() {
    const toolbar = document.querySelector(".rm-toolbar");
    if (!toolbar || !stageContent) return;
    const { done, total } = progressOf(collectEntries(stageContent));
    toolbar.querySelector(".rm-toolbar-count").textContent = total
      ? `${done} / ${total} afgerond`
      : "Nog niets om af te vinken";
    toolbar.style.setProperty("--rm-progress", total ? done / total : 0);
  }

  // The toolbar sticks below the site header, so jumping to a section must
  // leave room for both. Its height changes when its buttons wrap.
  function keepSectionsClearOf(toolbar) {
    const root = document.documentElement;
    root.classList.add("rm-has-toolbar");
    const measure = () => root.style.setProperty("--rm-toolbar-height", `${toolbar.offsetHeight}px`);
    measure();
    if ("ResizeObserver" in window) new ResizeObserver(measure).observe(toolbar);
  }

  function initStagePage(content) {
    stageContent = content;
    state.last = location.href.split("#")[0];
    saveState();

    content.querySelectorAll("a.rm-item").forEach(enhanceItem);
    content.querySelectorAll(QUESTIONS).forEach(enhanceQuestion);

    const filter = el(
      "button",
      { type: "button", class: "rm-review-filter", "aria-pressed": "false" },
      ["Alleen vragen om te herhalen"],
    );
    filter.addEventListener("click", () => {
      const active = !document.documentElement.classList.contains("rm-filter-review");
      document.documentElement.classList.toggle("rm-filter-review", active);
      filter.setAttribute("aria-pressed", String(active));
    });

    const toolbar = el("div", { class: "rm-toolbar" }, [
      el("div", { class: "rm-toolbar-progress" }, [
        el("span", { class: "rm-toolbar-count" }),
        el("span", { class: "rm-bar" }, [el("span", { class: "rm-bar-fill" })]),
      ]),
      el("div", { class: "rm-toolbar-actions" }, [routeToggle(), filter]),
    ]);
    (content.querySelector(".rm-meta") || content.querySelector("h1")).after(toolbar);
    keepSectionsClearOf(toolbar);

    bindRouteToggles(updateStageToolbar);
    applyRoute();
    updateStageToolbar();
  }

  // ---------- home page ----------

  const stageCache = new Map();

  function stageEntries(url) {
    if (!stageCache.has(url)) {
      stageCache.set(
        url,
        fetch(url)
          .then((response) => response.text())
          .then((html) => {
            const doc = new DOMParser().parseFromString(html, "text/html");
            return collectEntries(doc.querySelector(".md-content") || doc);
          })
          .catch(() => []),
      );
    }
    return stageCache.get(url);
  }

  async function renderHome() {
    const cards = [...document.querySelectorAll(".rm-stage-card")];
    let stagesDone = 0;
    await Promise.all(
      cards.map(async (card) => {
        const { done, total } = progressOf(await stageEntries(card.href));
        const complete = total > 0 && done === total;
        if (complete) stagesDone += 1;
        card.querySelector(".rm-stage-progress").textContent = total ? `${done} / ${total}` : "–";
        card.style.setProperty("--rm-progress", total ? done / total : 0);
        card.classList.toggle("is-complete", complete);
        card.classList.toggle("is-started", done > 0 && !complete);
      }),
    );
    document.getElementById("rm-stages-done").textContent = `${stagesDone} / ${cards.length}`;
    document.getElementById("rm-items-done").textContent = String(Object.keys(state.done).length);
    document.getElementById("rm-review-count").textContent = String(reviewCount());

    const resume = document.getElementById("rm-continue");
    if (state.last) {
      resume.href = state.last;
      resume.textContent = "Ga verder waar je gebleven was";
    }
  }

  function initHomePage() {
    bindRouteToggles(renderHome);
    applyRoute();
    renderHome();
  }

  // ---------- start ----------

  function init() {
    if (document.querySelector(".rm-roadmap")) {
      initHomePage();
      return;
    }
    const content = document.querySelector(".md-content");
    if (content && location.pathname.includes("/stages/")) initStagePage(content);
    else applyRoute();
  }

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init);
  else init();
})();
