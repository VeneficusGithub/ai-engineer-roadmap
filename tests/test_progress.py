"""Progress tracking: everything a trainee does is kept in their own browser."""

import re

from playwright.sync_api import Page, expect

STAGE = "stages/agents/"


def first_item(page: Page) -> tuple[str, str]:
    """Return (id, selector) of the first tickable resource on the page."""
    item_id = page.locator(".rm-check").first.get_attribute("data-id")
    assert item_id
    return item_id, f'.rm-check[data-id="{item_id}"]'


def test_ticked_resource_stays_ticked_after_reload(page: Page) -> None:
    page.goto(STAGE)
    _, selector = first_item(page)
    page.locator(selector).check()
    page.reload()
    expect(page.locator(selector)).to_be_checked()


def test_question_rating_stays_after_reload(page: Page) -> None:
    page.goto(STAGE)
    question = page.locator("details.interview").first
    question.locator('.rm-rate[data-rating="review"]').click()
    page.reload()
    expect(
        page.locator("details.interview").first.locator(
            '.rm-rate[data-rating="review"]'
        )
    ).to_have_attribute("aria-pressed", "true")


def test_review_filter_shows_only_questions_to_review(page: Page) -> None:
    page.goto(STAGE)
    questions = page.locator("details.interview")
    assert questions.count() >= 2
    questions.nth(0).locator('.rm-rate[data-rating="review"]').click()
    questions.nth(1).locator('.rm-rate[data-rating="ok"]').click()
    page.locator(".rm-review-filter").click()
    expect(questions.nth(0)).to_be_visible()
    expect(questions.nth(1)).to_be_hidden()


def test_home_shows_stage_progress_and_review_count(page: Page) -> None:
    page.goto("")
    expect(page.locator("#rm-review-count")).to_have_text("0")
    page.goto(STAGE)
    _, selector = first_item(page)
    page.locator(selector).check()
    page.locator("details.interview").first.locator(
        '.rm-rate[data-rating="review"]'
    ).click()
    page.goto("")
    card = page.locator(f'.rm-stage-card[data-stage="{STAGE}"]')
    expect(card.locator(".rm-stage-progress")).to_have_text(re.compile(r"^1 / \d+$"))
    expect(page.locator("#rm-review-count")).to_have_text("1")


def test_refresh_route_hides_full_route_items(page: Page) -> None:
    page.goto("")
    page.locator('.rm-route-toggle [data-route="refresh"]').click()
    page.goto(STAGE)
    expect(page.locator("li.rm-li:not(.rm-refresh)").first).to_be_hidden()
    expect(page.locator("li.rm-li.rm-refresh").first).to_be_visible()
    expect(page.locator("details.interview:not(.rm-refresh)").first).to_be_hidden()


def test_continue_button_links_to_last_visited_stage(page: Page) -> None:
    page.goto(STAGE)
    page.goto("")
    expect(page.locator("#rm-continue")).to_have_attribute(
        "href", re.compile(re.escape(STAGE) + "$")
    )
