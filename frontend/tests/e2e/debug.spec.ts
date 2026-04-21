import { test, expect } from '@playwright/test'

test.describe('SkyMechanics Frontend', () => {
  test('check if app renders with network logs', async ({ page }) => {
    page.on('console', msg => console.log('Browser console:', msg.text()))
    page.on('pageerror', err => console.log('Page error:', err.message))
    page.on('requestfailed', req => console.log('Request failed:', req.url(), req.failure().errorText))

    // Capture all requests
    const requests = []
    page.on('request', req => {
      requests.push({
        url: req.url(),
        method: req.method(),
        headers: req.headers()
      })
    })

    await page.goto('http://localhost:3102');
    
    console.log('Requests made:', JSON.stringify(requests, null, 2))
    
    // Wait for network idle
    await page.waitForLoadState('networkidle')
    
    // Check root
    const root = await page.locator('#root')
    const hasChildren = await root.evaluate(el => el.children.length > 0)
    console.log('Root has children:', hasChildren)
    
    // List all JS resources
    const jsResources = await page.evaluate(() => {
      const scripts = Array.from(document.querySelectorAll('script'))
      return scripts.map(s => ({
        src: s.src || s.getAttribute('src'),
        type: s.type || s.getAttribute('type')
      }))
    })
    console.log('JS resources:', JSON.stringify(jsResources, null, 2))
    
    expect(hasChildren).toBe(true)
  });
});
