"""YouTube resources show a thumbnail preview that opens the video."""

import re
from urllib.parse import parse_qs, urlparse

import pytest
from playwright.sync_api import Page, expect

STAGES = [
    "llm-foundations",
    "agents",
    "mcp-skills",
    "rag",
    "multi-agent",
    "evaluation",
    "security",
    "deployment",
    "final-project",
]
YOUTUBE = 'a.rm-item[href*="youtube.com/watch"]'


def test_llm_foundations_has_a_refresh_video_from_the_start(page: Page) -> None:
    page.goto("stages/llm-foundations/")
    video = page.locator('a.rm-item[href*="LPZh9BOjkQs"]')
    expect(video).to_have_count(1)
    expect(video).to_have_attribute(
        "href", "https://www.youtube.com/watch?v=LPZh9BOjkQs"
    )
    expect(video).to_have_class("rm-item rm-refresh")


def test_mcp_skills_has_a_refresh_video_starting_at_0_48(page: Page) -> None:
    page.goto("stages/mcp-skills/")
    video = page.locator('a.rm-item[href*="6wdvSH61xGw"]')
    expect(video).to_have_count(1)
    expect(video).to_have_attribute(
        "href", "https://www.youtube.com/watch?v=6wdvSH61xGw&t=48s"
    )
    expect(video).to_have_class("rm-item rm-refresh")
    expect(video.locator("img.rm-thumb-img")).to_have_attribute(
        "src", "https://i.ytimg.com/vi/6wdvSH61xGw/hqdefault.jpg"
    )


def test_rag_has_a_refresh_video_from_the_start(page: Page) -> None:
    page.goto("stages/rag/")
    video = page.locator('a.rm-item[href*="T-D1OfcDW1M"]')
    expect(video).to_have_count(1)
    expect(video).to_have_attribute(
        "href", "https://www.youtube.com/watch?v=T-D1OfcDW1M"
    )
    expect(video).to_have_class("rm-item rm-refresh")
    expect(video.locator("img.rm-thumb-img")).to_be_visible()


def test_evaluation_has_a_refresh_video_from_the_start(page: Page) -> None:
    page.goto("stages/evaluation/")
    video = page.locator('a.rm-item[href*="-sL7QzDFW-4"]')
    expect(video).to_have_count(1)
    expect(video).to_have_attribute(
        "href", "https://www.youtube.com/watch?v=-sL7QzDFW-4"
    )
    expect(video).to_have_class("rm-item rm-refresh")
    expect(video.locator("img.rm-thumb-img")).to_be_visible()


def test_security_has_a_refresh_video_from_the_start(page: Page) -> None:
    page.goto("stages/security/")
    video = page.locator('a.rm-item[href*="gUNXZMcd2jU"]')
    expect(video).to_have_count(1)
    expect(video).to_have_attribute(
        "href", "https://www.youtube.com/watch?v=gUNXZMcd2jU"
    )
    expect(video).to_have_class("rm-item rm-refresh")
    expect(video.locator("img.rm-thumb-img")).to_be_visible()


def test_agents_has_a_refresh_video_from_the_start(page: Page) -> None:
    page.goto("stages/agents/")
    video = page.locator('a.rm-item[href*="EDb37y_MhRw"]')
    expect(video).to_have_count(1)
    expect(video).to_have_attribute(
        "href", "https://www.youtube.com/watch?v=EDb37y_MhRw"
    )
    expect(video).to_have_class("rm-item rm-refresh")
    expect(video.locator("img.rm-thumb-img")).to_be_visible()


@pytest.mark.parametrize(
    "stage",
    ["llm-foundations", "agents", "mcp-skills", "rag", "evaluation", "security"],
)
def test_stage_no_longer_asks_for_a_refresh_video(page: Page, stage: str) -> None:
    page.goto(f"stages/{stage}/")
    expect(page.get_by_text("Opfrisvideo nog te kiezen")).to_have_count(0)


@pytest.mark.parametrize("stage", STAGES)
def test_youtube_resources_show_their_thumbnail_inside_the_link(
    page: Page, stage: str
) -> None:
    page.goto(f"stages/{stage}/")
    for link in page.locator(YOUTUBE).all():
        query = urlparse(link.get_attribute("href") or "").query
        video_id = parse_qs(query)["v"][0]
        thumbnail = link.locator("img.rm-thumb-img")
        expect(thumbnail).to_be_visible()
        expect(thumbnail).to_have_attribute(
            "src", f"https://i.ytimg.com/vi/{video_id}/hqdefault.jpg"
        )


@pytest.mark.parametrize("stage", STAGES)
def test_other_resources_have_no_thumbnail(page: Page, stage: str) -> None:
    page.goto(f"stages/{stage}/")
    others = page.locator(f"a.rm-item:not({YOUTUBE.removeprefix('a.rm-item')})")
    expect(others.locator("img.rm-thumb-img")).to_have_count(0)


def test_both_youtube_videos_get_a_thumbnail(page: Page) -> None:
    for stage in ("llm-foundations", "multi-agent"):
        page.goto(f"stages/{stage}/")
        expect(page.locator(f"{YOUTUBE} img.rm-thumb-img")).to_have_count(1)


def test_thumbnail_keeps_the_checkbox_label_unchanged(page: Page) -> None:
    page.goto("stages/multi-agent/")
    checkbox = page.locator(".rm-check").first
    expect(checkbox).to_have_attribute(
        "aria-label", 'Markeer "Multi-Agent Systems Explained" als gedaan'
    )


@pytest.mark.parametrize("stage", ["llm-foundations", "mcp-skills", "multi-agent"])
def test_thumbnail_fills_its_frame_so_black_bars_are_cropped(
    page: Page, stage: str
) -> None:
    page.goto(f"stages/{stage}/")
    image = page.locator("img.rm-thumb-img").first
    frame = page.locator(".rm-thumb").first
    image_box, frame_box = image.bounding_box(), frame.bounding_box()
    assert image_box is not None and frame_box is not None
    assert abs(image_box["height"] - frame_box["height"]) <= 2
    assert abs(image_box["y"] - frame_box["y"]) <= 2


@pytest.mark.parametrize("stage", STAGES)
def test_video_is_the_first_resource(page: Page, stage: str) -> None:
    page.goto(f"stages/{stage}/")
    items = page.locator("a.rm-item")
    if page.locator(YOUTUBE).count() == 0:
        pytest.skip("stage has no video")
    expect(items.first).to_have_attribute("href", re.compile(r"youtube\.com/watch"))
