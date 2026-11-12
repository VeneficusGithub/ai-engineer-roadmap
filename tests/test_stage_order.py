"""The stages appear in the agreed order everywhere the site lists or numbers them."""

import re

import pytest
from playwright.sync_api import Page, expect

ORDER = [
    "llm-foundations",
    "agents",
    "mcp-skills",
    "rag",
    "multi-agent",
    "evaluation",
    "security",
    "final-project",
]


def test_home_cards_follow_the_order(page: Page) -> None:
    page.goto("")
    cards = page.locator(".rm-stage-card")
    expect(cards).to_have_count(len(ORDER))
    for index, stage in enumerate(ORDER):
        card = cards.nth(index)
        expect(card).to_have_attribute("data-stage", f"stages/{stage}/")
        expect(card.locator(".rm-stage-number")).to_have_text(f"{index + 1:02d}")


def test_navigation_follows_the_order(page: Page) -> None:
    page.goto("")
    links = page.locator("nav.md-nav--primary a.md-nav__link[href*='stages/']")
    hrefs = [href for href in links.evaluate_all("els => els.map(e => e.href)")]
    stages = [href.rstrip("/").rsplit("/", 1)[-1] for href in hrefs]
    assert list(dict.fromkeys(stages)) == ORDER


@pytest.mark.parametrize("stage", ORDER)
def test_stage_page_shows_its_position(page: Page, stage: str) -> None:
    page.goto(f"stages/{stage}/")
    position = ORDER.index(stage) + 1
    expect(page.locator(".rm-meta")).to_contain_text(
        f"Fase {position} van {len(ORDER)}"
    )


# How each stage is named when another page says it builds on it.
STAGE_NAMES = {
    "llm-foundations": r"\bLLM-basiskennis\b",
    "agents": r"\bagents\b",
    "mcp-skills": r"\bMCP\b",
    "rag": r"\bRAG\b",
    "multi-agent": r"\bmulti-agent\b",
    "evaluation": r"\bevaluatie\b",
    "security": r"\bLLM-security\b",
}


@pytest.mark.parametrize("stage", ORDER)
def test_stage_builds_only_on_earlier_stages(page: Page, stage: str) -> None:
    page.goto(f"stages/{stage}/")
    meta = page.locator(".rm-meta span", has_text="Bouwt voort op:")
    builds_on = meta.inner_text().split(":", 1)[1]
    named = [s for s, name in STAGE_NAMES.items() if re.search(name, builds_on)]
    later = [s for s in named if ORDER.index(s) >= ORDER.index(stage)]
    assert later == [], f"{stage} builds on stages that come later: {later}"
