"""Branding, language and wording agreed with the traineeship."""

import re

import pytest
from playwright.sync_api import Page, expect

STAGES = [
    "llm-foundations",
    "rag",
    "agents",
    "evaluation",
    "deployment",
    "security",
    "mcp-skills",
    "multi-agent",
    "final-project",
]
ALL_PAGES = ["", *(f"stages/{stage}/" for stage in STAGES)]

# Stages are presented as equals: no labels or text ranking how urgent they are.
URGENCY = re.compile(
    r"biggest gap|less urgent|urgent|grootste gat|minder urgent|urgentie",
    re.IGNORECASE,
)

# Phrases from the English version that must not survive the translation.
ENGLISH_LEFTOVERS = re.compile(
    r"\b(Learn|Practise|Go deeper|Interview questions|Check your understanding"
    r"|Could answer|Need to review|Full route|Stage \d of|About \d)\b"
)

VENEFICUS_GREEN = "rgb(84, 182, 115)"


def test_hero_says_data_trainee_to_ai_engineer(page: Page) -> None:
    page.goto("")
    expect(page.locator(".rm-hero-title")).to_have_text(
        "Van Data Trainee naar AI Engineer"
    )


def test_hero_text_offers_preparation_next_to_the_programme(page: Page) -> None:
    page.goto("")
    expect(page.locator(".rm-hero-text")).to_have_text(
        "Deze pagina biedt naast het trainingsprogramma extra voorbereiding voor "
        "een rol als AI engineer: wat je moet leren, waar je het leert en welke "
        "interviewvragen je kunt oefenen. Je voortgang wordt in deze browser "
        "opgeslagen."
    )


@pytest.mark.parametrize("path", ALL_PAGES)
def test_no_urgency_wording(page: Page, path: str) -> None:
    page.goto(path)
    expect(page.locator(".md-content")).not_to_contain_text(URGENCY)


@pytest.mark.parametrize("path", ALL_PAGES)
def test_page_is_in_dutch(page: Page, path: str) -> None:
    page.goto(path)
    expect(page.locator("html")).to_have_attribute("lang", "nl")
    expect(page.locator(".md-content")).not_to_contain_text(ENGLISH_LEFTOVERS)


def test_progress_controls_are_in_dutch(page: Page) -> None:
    page.goto("stages/agents/")
    question = page.locator("details.interview").first
    expect(question.locator('.rm-rate[data-rating="ok"]')).to_have_text(
        "Kon ik beantwoorden"
    )
    expect(question.locator('.rm-rate[data-rating="review"]')).to_have_text(
        "Nog herhalen"
    )
    expect(page.locator(".rm-review-filter")).to_have_text(
        "Alleen vragen om te herhalen"
    )
    expect(page.locator('.rm-toolbar [data-route="full"]')).to_have_text(
        "Volledige route"
    )
    expect(page.locator(".rm-toolbar-count")).to_have_text(re.compile(r"afgerond$"))


def test_primary_button_uses_company_green(page: Page) -> None:
    page.goto("")
    expect(page.locator("#rm-continue")).to_have_css(
        "background-color", VENEFICUS_GREEN
    )
