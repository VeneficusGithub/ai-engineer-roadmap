"""The site knows its own address."""

from playwright.sync_api import Page, expect

SITE_URL = "https://veneficusgithub.github.io/ai-engineer-roadmap/"


def test_pages_name_their_address_on_the_live_site(page: Page) -> None:
    page.goto("")
    expect(page.locator('link[rel="canonical"]')).to_have_attribute("href", SITE_URL)
    page.goto("stages/rag/")
    expect(page.locator('link[rel="canonical"]')).to_have_attribute(
        "href", SITE_URL + "stages/rag/"
    )


def test_header_has_no_repository_link(page: Page) -> None:
    page.goto("")
    expect(page.locator(".md-header a.md-source")).to_have_count(0)
    expect(page.locator('a[href*="github.com"]')).to_have_count(0)
