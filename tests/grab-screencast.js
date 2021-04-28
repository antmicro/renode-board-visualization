const PuppeteerVideoRecorder = require('puppeteer-video-recorder');
const puppeteer = require('puppeteer');

(async () => {
    const browser = await puppeteer.launch({ headless: true, args: ['--no-sandbox'] })
    const page = (await browser.pages())[0]
    await page.setViewport({ width: 1280, height: 800});
    const recorder = new PuppeteerVideoRecorder()
    await recorder.init(page, __dirname)
    await page.goto('http://localhost:8000')
    await recorder.start()
    await page.waitForTimeout(10000)
    await recorder.stop()
    await browser.close()
  })()
