"""The site knows its own address and links to its repository."""

from playwright.sync_api import Page, expect

SITE_URL = "https://veneficusgithub.github.io/ai-engineer-roadmap/"
REPO_URL = "https://github.com/VeneficusGithub/ai-engineer-roadmap"


def test_pages_name_their_address_on_the_live_site(page: Page) -> None:
    page.goto("")
    expect(page.locator('link[rel="canonical"]')).to_have_attribute("href", SITE_URL)
    page.goto("stages/rag/")
    expect(page.locator('link[rel="canonical"]')).to_have_attribute(
        "href", SITE_URL + "stages/rag/"
    )


def test_header_links_to_the_repository(page: Page) -> None:
    page.goto("")
    expect(page.locator(".md-header a.md-source")).to_have_attribute("href", REPO_URL)
