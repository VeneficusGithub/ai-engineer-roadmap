"""The setup-and-costs page and the progress export/import section are gone."""

import pytest
from playwright.sync_api import Page, expect
from test_branding import ALL_PAGES


def test_setup_page_no_longer_exists(page: Page) -> None:
    response = page.goto("setup/")
    assert response is not None and response.status == 404


@pytest.mark.parametrize("path", ALL_PAGES)
def test_no_page_links_to_the_setup_page(page: Page, path: str) -> None:
    page.goto(path)
    expect(page.locator('a[href*="setup"]')).to_have_count(0)
    expect(page.get_by_text("Setup en kosten")).to_have_count(0)


def test_home_has_no_export_or_import_section(page: Page) -> None:
    page.goto("")
    expect(page.locator(".rm-backup")).to_have_count(0)
    expect(page.locator("#rm-export")).to_have_count(0)
    expect(page.locator("#rm-import")).to_have_count(0)
    expect(page.get_by_text("Jouw voortgang")).to_have_count(0)


def test_home_steps_no_longer_mention_a_backup(page: Page) -> None:
    page.goto("")
    steps = page.locator(".rm-steps li")
    expect(steps).to_have_count(3)
    expect(page.locator(".rm-steps")).not_to_contain_text("back-up")


def test_home_still_tracks_progress_without_the_section(page: Page) -> None:
    errors: list[str] = []
    page.on("pageerror", lambda error: errors.append(str(error)))
    page.goto("")
    expect(page.locator("#rm-stages-done")).to_have_text("0 / 9")
    assert errors == []
