import { test, expect } from '@playwright/test';

test.describe('SkyMechanics Frontend', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('http://localhost:3002');
  });

  test('has correct title', async ({ page }) => {
    await expect(page).toHaveTitle(/SkyMechanics/);
  });

  test('has sidebar and brand text', async ({ page }) => {
    await expect(page.getByTestId('brand-link')).toBeVisible();
  });

  test('has navigation links in sidebar', async ({ page }) => {
    const mainNav = page.getByTestId('main-nav');
    await expect(mainNav.getByText('Dashboard', { exact: true })).toBeVisible();
    await expect(mainNav.getByText('Jobs', { exact: true })).toBeVisible();
    await expect(mainNav.getByText('Customers', { exact: true })).toBeVisible();
    await expect(mainNav.getByText('Mechanics', { exact: true })).toBeVisible();
  });
});
