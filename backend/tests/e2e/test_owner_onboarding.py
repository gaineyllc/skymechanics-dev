"""E2E tests for SkyMechanics owner onboarding flow."""

import pytest
from playwright.sync_api import Page, expect

pytestmark = pytest.mark.e2e


@pytest.mark.order(1)
def test_owner_onboarding_flow(page: Page) -> None:
    """Test the complete owner onboarding flow."""
    # Navigate to the registration page
    page.goto("http://localhost:8888/register")
    
    # Fill in owner registration form
    page.get_by_label("Email").fill("e2e-owner@example.com")
    page.get_by_label("Password").fill("Test123!")
    page.get_by_label("First Name").fill("E2E")
    page.get_by_label("Last Name").fill("Owner")
    page.get_by_label("Organization Name").fill("E2E Test Org")
    
    # Submit the form
    page.get_by_role("button", name="Register").click()
    
    # Verify success - should redirect or show success message
    expect(page).to_have_url("http://localhost:8888/login")
    
    # Verify user can login with new credentials
    page.goto("http://localhost:8888/login")
    page.get_by_label("Email").fill("e2e-owner@example.com")
    page.get_by_label("Password").fill("Test123!")
    page.get_by_role("button", name="Login").click()
    
    # Should redirect to dashboard
    expect(page).to_have_url("http://localhost:8888/dashboard")


@pytest.mark.order(2)
def test_login_with_invalid_credentials(page: Page) -> None:
    """Test that invalid login attempts are rejected."""
    page.goto("http://localhost:8888/login")
    page.get_by_label("Email").fill("nonexistent@example.com")
    page.get_by_label("Password").fill("wrongpassword")
    page.get_by_role("button", name="Login").click()
    
    # Should show error message
    expect(page.get_by_text("Invalid credentials")).to_be_visible()


@pytest.mark.order(3)
def test_heartbeat_endpoint(page: Page) -> None:
    """Test that the health endpoint returns successfully."""
    response = page.request.get("http://localhost:8200/")
    assert response.status == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "version" in data
