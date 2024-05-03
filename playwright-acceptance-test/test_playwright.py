import re
from playwright.sync_api import Page, expect

def test_home_page_has_title(page:Page):
    page.goto("https://betafish-flask-backend-3asud65paa-uc.a.run.app/")
    expect(page).to_have_title(re.compile("Denver Crime Tracker"))

def test_click_analytics_changes_display(page:Page):
    page.goto("https://betafish-flask-backend-3asud65paa-uc.a.run.app/")

    page.get_by_text("Analytics").click()
    expect(page.locator("#first-chart")).to_be_visible()
    expect(page.locator("#second-chart")).to_be_visible()

def test_search_returns_results(page:Page):
    page.goto("https://betafish-flask-backend-3asud65paa-uc.a.run.app/")
    expect(page.locator("tbody")).to_contain_text("-")
    page.get_by_label("Start date").fill("2024-03-01")
    page.get_by_role("button", name="Search").click()
    expect(page.get_by_role("cell", name="4/25/").first).to_be_visible()

def test_search_adds_icon_to_map(page:Page):
    page.goto("https://betafish-flask-backend-3asud65paa-uc.a.run.app/")
    page.get_by_label("Start date").fill("2024-03-01")
    page.get_by_role("button", name="Search").click()
    expect(page.locator(".leaflet-pane > img:nth-child(2)")).to_be_visible()