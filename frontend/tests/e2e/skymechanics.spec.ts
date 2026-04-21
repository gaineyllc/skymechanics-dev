import { test, expect } from '@playwright/test'

const BASE_URL = process.env.PLAYWRIGHT_TEST_BASE_URL || 'http://localhost:3004'

test.describe('SkyMechanics E2E Tests', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto(`${BASE_URL}/`)
  })

  test('1. Dashboard loads with stats', async ({ page }) => {
    await page.goto(`${BASE_URL}/dashboard`)
    await expect(page.getByText('Dashboard')).toBeVisible()
    await expect(page.getByText('Active Jobs')).toBeVisible()
    await expect(page.getByText('Pending Approval')).toBeVisible()
    await expect(page.getByText('Customers')).toBeVisible()
    await expect(page.getByText('Mechanics')).toBeVisible()
    await expect(page.getByText('Recent Activity')).toBeVisible()
  })

  test('2. Customers list and create flow', async ({ page }) => {
    await page.goto(`${BASE_URL}/customers`)
    await expect(page.getByText('Customers')).toBeVisible()
    await expect(page.getByRole('button', { name: 'New Customer' })).toBeVisible()
  })

  test('3. Mechanics list and view details', async ({ page }) => {
    await page.goto(`${BASE_URL}/mechanics`)
    await expect(page.getByText('Mechanics')).toBeVisible()
  })

  test('4. Inspectors list and delete', async ({ page }) => {
    await page.goto(`${BASE_URL}/inspectors`)
    await expect(page.getByText('Inspectors')).toBeVisible()
  })

  test('5. Aircraft list and view', async ({ page }) => {
    await page.goto(`${BASE_URL}/aircraft`)
    await expect(page.getByText('Aircraft')).toBeVisible()
  })

  test('6. Jobs list and workflow', async ({ page }) => {
    await page.goto(`${BASE_URL}/jobs`)
    await expect(page.getByText('Jobs')).toBeVisible()
    await page.goto(`${BASE_URL}/workflow`)
    await expect(page.getByText('Workflow Builder')).toBeVisible()
  })

  test('7. Login page', async ({ page }) => {
    await page.goto(`${BASE_URL}/login`)
    await expect(page.getByText('Login')).toBeVisible()
    await expect(page.getByLabel('Email')).toBeVisible()
    await expect(page.getByLabel('Password')).toBeVisible()
    await expect(page.getByRole('button', { name: 'Login' })).toBeVisible()
  })

  test('8. Responsive layout', async ({ page }) => {
    await page.setViewportSize({ width: 375, height: 667 })
    await page.goto(`${BASE_URL}/`)
    await expect(page.getByText('SkyMechanics')).toBeVisible()
    
    await page.setViewportSize({ width: 1920, height: 1080 })
    await page.goto(`${BASE_URL}/`)
    await expect(page.getByText('SkyMechanics')).toBeVisible()
  })

  test('9. Brand text visible', async ({ page }) => {
    await page.goto(`${BASE_URL}/`)
    await expect(page.getByText('SkyMechanics')).toBeVisible()
    await expect(page.getByText('Aircraft Maintenance')).toBeVisible()
  })

  test('10. Navigation sidebar exists', async ({ page }) => {
    await page.goto(`${BASE_URL}/`)
    const navGroup = await page.locator('[data-testid="main-nav"]')
    await expect(navGroup).toBeVisible()
  })
})
