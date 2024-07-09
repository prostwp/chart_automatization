const puppeteer = require('puppeteer');

(async () => {
    const browserURL = 'http://127.0.0.1:9222';  // Порт для подключения к Chrome

    try {
        console.log('Connecting to browser...');
        const browser = await puppeteer.connect({ browserURL, defaultViewport: null, timeout: 30000 });
        console.log('Connected to browser.');

        const pages = await browser.pages();
        console.log('Pages fetched:', pages.length);

        const targetUrl = 'https://cp.octafeed.com/panel/overview-posts/create';
        let page;
        if (pages.length === 0) {
            console.log('No pages found. Opening a new page...');
            page = await browser.newPage();
        } else {
            console.log('Pages found. Using existing page...');
            page = pages[0];
        }
        await page.goto(targetUrl);
        console.log('Navigated to target URL.');
    } catch (error) {
        console.error('Error occurred while connecting to the browser:', error);
    }
})();
