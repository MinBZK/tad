import pytest
from playwright.sync_api import Page, expect


@pytest.mark.slow()
def test_e2e_create_project(page: Page):
    page.goto("/projects/new")

    page.fill("#name", "My new project")

    impact_assesment = page.get_by_label("AI Impact Assessment (AIIA)")

    expect(impact_assesment).not_to_be_checked()

    impact_assesment.check()

    button = page.get_by_role("button", name="Create Project")
    button.click()

    expect(page.get_by_role("heading", name="My new project")).to_be_visible()


@pytest.mark.slow()
def test_e2e_create_project_invalid(page: Page):
    page.goto("/projects/new")

    button = page.get_by_role("button", name="Create Project")
    button.click()

    expect(page.get_by_role("heading", name="Request Validation Error")).to_be_visible()


@pytest.mark.slow()
def test_e2e_create_project_with_tasks(page: Page):
    page.goto("/projects/new")

    page.fill("#name", "My new filled project")

    impact_assesment = page.get_by_label("AI Impact Assessment (AIIA)")

    expect(impact_assesment).not_to_be_checked()

    impact_assesment.check()

    button = page.get_by_role("button", name="Create Project")
    button.click()

    expect(page.get_by_role("heading", name="My new filled project")).to_be_visible()
    card_1 = page.get_by_text("Geef een korte beschrijving van het beoogde AI-systeem")
    expect(card_1).to_be_visible()
    card_2 = page.get_by_text("Waarom is er voor de huidige techniek gekozen?")
    expect(card_2).to_be_visible()
