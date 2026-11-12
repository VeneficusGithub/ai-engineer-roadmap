"""Courses that build on Anthropic API access, added next to the free material."""

import pytest
from playwright.sync_api import Page, expect

CLAUDE_API = "https://anthropic.skilljar.com/claude-with-the-anthropic-api/"
TOOL_USE = CLAUDE_API + "287747"
AGENTS_AND_WORKFLOWS = CLAUDE_API + "287796"
GETTING_STARTED = "https://www.coursera.org/learn/building-with-the-claude-api#modules"

NEEDS_API_KEY = [
    ("llm-foundations", GETTING_STARTED),
    ("agents", TOOL_USE),
    ("agents", AGENTS_AND_WORKFLOWS),
    ("mcp-skills", CLAUDE_API + "287780"),
    ("mcp-skills", "https://www.deeplearning.ai/courses/agent-skills-with-anthropic"),
    ("rag", CLAUDE_API + "287763"),
    ("evaluation", CLAUDE_API + "287731"),
]

OPEN_GAPS = {
    "agents": "Er ontbreekt nog materiaal over agent-frameworks.",
    "mcp-skills": (
        "De DataCamp-cursus, de workshop en de module van Anthropic Academy "
        "overlappen elkaar."
    ),
    "rag": "Er ontbreekt nog materiaal over vectordatabases en RAG-evaluatie.",
}


@pytest.mark.parametrize(("stage", "url"), NEEDS_API_KEY)
def test_resource_says_when_it_needs_an_api_key(
    page: Page, stage: str, url: str
) -> None:
    page.goto(f"stages/{stage}/")
    item = page.locator("li.rm-li", has=page.locator(f'a[href="{url}"]'))
    expect(item).to_contain_text("API-sleutel")


def test_first_stage_says_how_to_get_an_api_key(page: Page) -> None:
    page.goto("stages/llm-foundations/")
    note = page.locator(".admonition.curating")
    expect(note.locator(".admonition-title")).to_have_text(
        "Zo kom je aan je API-sleutel"
    )
    expect(note).to_contain_text("workspace")
    expect(note).to_contain_text("nog niet ingericht")


def test_later_module_points_back_to_the_key_note(page: Page) -> None:
    page.goto("stages/agents/")
    item = page.locator("li.rm-li", has=page.locator(f'a[href="{TOOL_USE}"]'))
    expect(item).to_contain_text("in fase 1 lees je hoe je die krijgt")


def test_course_modules_are_ticked_off_separately(page: Page) -> None:
    page.goto("stages/agents/")
    page.locator(f'.rm-check[data-id="r:{TOOL_USE}"]').check()
    page.reload()
    expect(page.locator(f'.rm-check[data-id="r:{TOOL_USE}"]')).to_be_checked()
    expect(
        page.locator(f'.rm-check[data-id="r:{AGENTS_AND_WORKFLOWS}"]')
    ).not_to_be_checked()


@pytest.mark.parametrize("stage", OPEN_GAPS)
def test_note_lists_only_what_is_still_open(page: Page, stage: str) -> None:
    page.goto(f"stages/{stage}/")
    note = page.locator(".admonition.curating p:not(.admonition-title)")
    expect(note).to_have_text(OPEN_GAPS[stage])


def test_multi_agent_stage_has_no_open_gaps_left(page: Page) -> None:
    page.goto("stages/multi-agent/")
    expect(page.locator(".admonition.curating")).to_have_count(0)


def test_home_page_gives_the_new_length_of_the_full_route(page: Page) -> None:
    page.goto("")
    expect(page.locator('[data-route="full"] span')).to_have_text("35–40 uur")
    expect(page.locator(".rm-steps")).to_contain_text("ongeveer 35–40 uur")
