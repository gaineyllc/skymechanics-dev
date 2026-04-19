import { test, expect } from '@playwright/test';

test.describe('SkyMechanics Frontend', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('http://localhost:3002');
  });

  test('has correct title', async ({ page }) => {
    await expect(page).toHaveTitle(/SkyMechanics/);
  });

  test('has main heading', async ({ page }) => {
    await expect(page.getByRole('heading', { name: 'SkyMechanics' })).toBeVisible();
  });

  test('has navigation links', async ({ page }) => {
    await expect(page.getByRole('link', { name: 'Dashboard' })).toBeVisible();
    await expect(page.getByRole('link', { name: 'Jobs' })).toBeVisible();
    await expect(page.getByRole('link', { name: 'Customers' })).toBeVisible();
    await expect(page.getByRole('link', { name: 'Mechanics' })).toBeVisible();
    await expect(page.getByRole('link', { name: 'Admin' })).toBeVisible();
  });
});
