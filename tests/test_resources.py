"""The resources on each stage page are exactly the ones selected in the review.

Only resources explicitly kept in the review count; rows that were left untouched
there are not a choice and must not appear. Each entry is
(url, is_exercise, is_refresh). Hours are what the stage page and its home-page
card should both say; "n.t.b." means the stage has no resources yet.
"""

import re

import pytest
from playwright.sync_api import Page, expect

DC = "https://www.datacamp.com/courses/"
TO_BE_DECIDED = "n.t.b."

EXPECTED: dict[str, dict[str, object]] = {
    "llm-foundations": {
        "hours": "3 uur",
        "items": [
            (DC + "working-with-the-openai-api", False, False),
            (DC + "understanding-prompt-engineering", False, False),
            ("https://www.youtube.com/watch?v=LPZh9BOjkQs", False, True),
        ],
    },
    "rag": {
        "hours": "2 uur",
        "items": [
            (DC + "retrieval-augmented-generation-rag-with-langchain", False, False),
            ("https://www.youtube.com/watch?v=T-D1OfcDW1M", False, True),
        ],
    },
    "agents": {
        "hours": "3 uur",
        "items": [
            (DC + "introduction-to-ai-agents", False, False),
            (
                "https://www.anthropic.com/engineering/building-effective-agents",
                False,
                True,
            ),
            (DC + "designing-agentic-systems-with-langchain", False, False),
            ("https://www.youtube.com/watch?v=EDb37y_MhRw", False, True),
        ],
    },
    "evaluation": {
        "hours": "3,5 uur",
        "items": [
            (DC + "llm-application-evaluation-with-langsmith", False, False),
            (
                "https://www.udemy.com/course/evaluation-for-llm-applications/",
                False,
                False,
            ),
            ("https://www.youtube.com/watch?v=-sL7QzDFW-4", False, True),
        ],
    },
    "deployment": {
        "hours": "4,5 uur",
        "items": [
            (DC + "deploying-ai-into-production-with-fastapi", False, False),
            ("https://www.udemy.com/course/mastering-aiml-with-docker/", False, False),
        ],
    },
    "security": {
        "hours": "3 uur",
        "items": [
            (
                "https://www.udemy.com/course/ai-security-defend-llm-apps-against-the-owasp-llm-top-10/",
                False,
                False,
            ),
            ("https://play.lakera.ai/agent-breaker", True, False),
            ("https://www.youtube.com/watch?v=gUNXZMcd2jU", False, True),
        ],
    },
    "mcp-skills": {
        "hours": "5,5 uur",
        "items": [
            (DC + "introduction-to-model-context-protocol-mcp", False, False),
            ("https://pamelafox.github.io/github-copilot-mcp-tutorial/", True, False),
            ("https://www.youtube.com/watch?v=6wdvSH61xGw&t=48s", False, True),
        ],
    },
    "multi-agent": {
        "hours": "10 min",
        "items": [
            ("https://www.youtube.com/watch?v=sWH0T4Zez6I", False, True),
        ],
    },
}


def page_items(page: Page) -> list[tuple[str, bool, bool]]:
    items = []
    for link in page.locator("a.rm-item").all():
        classes = link.get_attribute("class") or ""
        items.append(
            (
                link.get_attribute("href") or "",
                "rm-exercise" in classes,
                "rm-refresh" in classes,
            )
        )
    return items


@pytest.mark.parametrize("stage", EXPECTED)
def test_stage_lists_exactly_the_selected_resources(page: Page, stage: str) -> None:
    page.goto(f"stages/{stage}/")
    expected = EXPECTED[stage]["items"]
    assert isinstance(expected, list)
    assert sorted(page_items(page)) == sorted(expected)


@pytest.mark.parametrize("stage", EXPECTED)
def test_stage_has_no_extra_resource_links(page: Page, stage: str) -> None:
    """Every external link in the page content is one of the selected resources."""
    page.goto(f"stages/{stage}/")
    links = page.locator('.md-content article a[href^="http"]')
    for link in links.all():
        expect(link).to_have_class(re.compile(r"\brm-item\b"))


@pytest.mark.parametrize("stage", EXPECTED)
def test_stage_has_no_unrequested_sections(page: Page, stage: str) -> None:
    """Stage pages hold resources and interview questions, nothing else."""
    page.goto(f"stages/{stage}/")
    headings = page.locator(".md-content h2")
    expect(headings.filter(has_text="Wat je moet kunnen uitleggen")).to_have_count(0)
    expect(headings.filter(has_text="Check je begrip")).to_have_count(0)
    expect(page.locator("details.selfcheck")).to_have_count(0)
    # Learning material and exercises share one list under "Leren".
    expect(headings.filter(has_text="Oefenen")).to_have_count(0)
    if page.locator("a.rm-item").count():
        expect(headings.filter(has_text="Leren")).to_have_count(1)


REMOVED_QUESTIONS = [
    "Wat geeft een framework als LangGraph je ten opzichte van de loop zelf schrijven?",
    "Hoe test je een agent?",
]


def test_agents_page_drops_removed_interview_questions(page: Page) -> None:
    page.goto("stages/agents/")
    summaries = page.locator("details.interview summary")
    for question in REMOVED_QUESTIONS:
        expect(summaries.filter(has_text=question)).to_have_count(0)


@pytest.mark.parametrize("stage", EXPECTED)
def test_stage_hours_match_between_page_and_home_card(page: Page, stage: str) -> None:
    hours = str(EXPECTED[stage]["hours"])
    page.goto(f"stages/{stage}/")
    meta = "Tijd nog te bepalen" if hours == TO_BE_DECIDED else f"Ongeveer {hours}"
    expect(page.locator(".rm-meta")).to_contain_text(meta)
    page.goto("")
    card = page.locator(f'.rm-stage-card[data-stage="stages/{stage}/"]')
    expect(card.locator(".rm-stage-hours")).to_have_text(hours)


@pytest.mark.parametrize("stage", EXPECTED)
def test_resource_links_open_in_a_new_tab(page: Page, stage: str) -> None:
    page.goto(f"stages/{stage}/")
    for link in page.locator("a.rm-item").all():
        expect(link).to_have_attribute("target", "_blank")
        expect(link).to_have_attribute("href", re.compile(r"^https://"))
