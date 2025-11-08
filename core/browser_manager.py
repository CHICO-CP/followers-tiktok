"""
Advanced Browser Management with Anti-Detection
"""

import asyncio
import random
import logging
from typing import Optional, List, Dict
from pyppeteer import launch
from pyppeteer.browser import Browser
from pyppeteer.page import Page

class BrowserManager:
    def __init__(self, proxy_rotator):
        self.proxy_rotator = proxy_rotator
        self.logger = logging.getLogger(__name__)
        self.active_browsers: List[Browser] = []
        
    async def create_browser(self, account: Dict) -> Optional[Browser]:
        """Create stealth browser instance with anti-detection"""
        try:
            browser_args = await self._get_browser_args(account)
            
            browser = await launch(
                headless=False,  # Set to True for production
                args=browser_args,
                ignoreHTTPSErrors=True,
                autoClose=False
            )
            
            self.active_browsers.append(browser)
            self.logger.info(f"Browser created for {account['username']}")
            return browser
            
        except Exception as e:
            self.logger.error(f"Failed to create browser: {e}")
            return None
            
    async def _get_browser_args(self, account: Dict) -> List[str]:
        """Generate browser arguments for stealth"""
        args = [
            '--no-sandbox',
            '--disable-setuid-sandbox',
            '--disable-blink-features=AutomationControlled',
            '--disable-features=VizDisplayCompositor',
            '--disable-background-timer-throttling',
            '--disable-backgrounding-occluded-windows',
            '--disable-renderer-backgrounding',
            '--disable-dev-shm-usage',
            '--disable-web-security',
            '--disable-features=TranslateUI',
            '--disable-ipc-flooding-protection',
            f'--window-size={random.randint(1200, 1920)},{random.randint(800, 1080)}',
            f'--user-agent={await self._get_random_user_agent()}'
        ]
        
        # Add proxy if available
        proxy = await self.proxy_rotator.get_proxy(account)
        if proxy:
            args.append(f'--proxy-server={proxy}')
            
        return args
        
    async def _get_random_user_agent(self) -> str:
        """Get random user agent from file"""
        try:
            with open('config/user_agents.txt', 'r') as f:
                agents = [line.strip() for line in f if line.strip()]
                return random.choice(agents) if agents else self._get_default_user_agent()
        except:
            return self._get_default_user_agent()
            
    def _get_default_user_agent(self) -> str:
        """Get default user agent"""
        return "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        
    async def setup_page(self, page: Page):
        """Configure page for stealth browsing"""
        try:
            # Set viewport
            await page.setViewport({
                'width': random.randint(1200, 1920),
                'height': random.randint(800, 1080)
            })
            
            # Enable JavaScript
            await page.setJavaScriptEnabled(True)
            
            # Remove webdriver property
            await page.evaluateOnNewDocument('''
                () => {
                    delete navigator.__proto__.webdriver;
                    Object.defineProperty(navigator, 'webdriver', { get: () => false });
                    Object.defineProperty(navigator, 'plugins', { get: () => [1, 2, 3, 4, 5] });
                    Object.defineProperty(navigator, 'languages', { get: () => ['en-US', 'en'] });
                }
            ''')
            
            # Randomize other properties
            await self._randomize_page_properties(page)
            
        except Exception as e:
            self.logger.error(f"Page setup failed: {e}")
            
    async def _randomize_page_properties(self, page: Page):
        """Randomize page properties to avoid fingerprinting"""
        try:
            await page.evaluateOnNewDocument('''
                () => {
                    // Randomize screen resolution
                    Object.defineProperty(screen, 'width', { get: () => 1920 + Math.floor(Math.random() * 200) });
                    Object.defineProperty(screen, 'height', { get: () => 1080 + Math.floor(Math.random() * 200) });
                    
                    // Randomize timezone
                    Object.defineProperty(Intl.DateTimeFormat.prototype, 'resolvedOptions', {
                        value: () => ({
                            ...Intl.DateTimeFormat.prototype.resolvedOptions(),
                            timeZone: ['America/New_York', 'Europe/London', 'Asia/Tokyo'][Math.floor(Math.random() * 3)]
                        })
                    });
                }
            ''')
        except Exception as e:
            self.logger.warning(f"Property randomization failed: {e}")
            
    async def cleanup(self):
        """Close all active browsers"""
        for browser in self.active_browsers:
            try:
                await browser.close()
            except:
                pass
        self.active_browsers.clear()