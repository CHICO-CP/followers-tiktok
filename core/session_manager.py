"""
Advanced Session Management with Cookie Persistence
"""

import asyncio
import json
import pickle
import hashlib
import time
import logging
from typing import Optional, Dict
from pyppeteer.page import Page

class SessionManager:
    def __init__(self, encryption_manager):
        self.encryption = encryption_manager
        self.logger = logging.getLogger(__name__)
        self.sessions = {}
        
    async def initialize_session(self, account: Dict, page: Page) -> Optional[Dict]:
        """Initialize or restore session for account"""
        try:
            username = account['username']
            
            # Try to load existing session
            session = await self._load_session(account)
            if session and await self._validate_session(page, session):
                self.logger.info(f"Session restored for {username}")
                return session
                
            # Create new session
            self.logger.info(f"Creating new session for {username}")
            return await self._create_new_session(account, page)
            
        except Exception as e:
            self.logger.error(f"Session initialization failed for {account['username']}: {e}")
            return None
            
    async def _load_session(self, account: Dict) -> Optional[Dict]:
        """Load session from storage"""
        try:
            session_file = self._get_session_filename(account['username'])
            with open(session_file, 'rb') as f:
                encrypted_data = pickle.load(f)
                
            session_data = self.encryption.decrypt(encrypted_data)
            return json.loads(session_data)
            
        except:
            return None
            
    async def _validate_session(self, page: Page, session: Dict) -> bool:
        """Validate if session is still active"""
        try:
            # Set cookies and check if logged in
            await page.setCookie(*session.get('cookies', []))
            await page.goto('https://www.tiktok.com/', waitUntil='networkidle2')
            
            # Check for login indicators
            await asyncio.sleep(3)
            logged_in = await page.querySelector('div[data-e2e="search-icon"]') is not None
            
            return logged_in
            
        except:
            return False
            
    async def _create_new_session(self, account: Dict, page: Page) -> Optional[Dict]:
        """Create new session by logging in"""
        try:
            login_success = await self._perform_login(account, page)
            if not login_success:
                return None
                
            # Get session data
            cookies = await page.cookies()
            session_data = {
                'username': account['username'],
                'cookies': cookies,
                'created_at': time.time(),
                'user_agent': await page.evaluate('() => navigator.userAgent')
            }
            
            await self._save_session(account, session_data)
            return session_data
            
        except Exception as e:
            self.logger.error(f"Session creation failed: {e}")
            return None
            
    async def _perform_login(self, account: Dict, page: Page) -> bool:
        """Perform TikTok login"""
        try:
            await page.goto('https://www.tiktok.com/login', waitUntil='networkidle2')
            
            # Wait for login form
            await page.waitForSelector('input[name="username"]', timeout=10000)
            
            # Fill credentials
            await page.type('input[name="username"]', account['username'])
            await asyncio.sleep(1)
            await page.type('input[type="password"]', account['password'])
            await asyncio.sleep(1)
            
            # Submit login
            await page.click('button[type="submit"]')
            
            # Wait for login completion
            await page.waitForSelector('div[data-e2e="search-icon"]', timeout=15000)
            
            self.logger.info(f"Login successful for {account['username']}")
            return True
            
        except Exception as e:
            self.logger.error(f"Login failed for {account['username']}: {e}")
            return False
            
    async def _save_session(self, account: Dict, session_data: Dict):
        """Save session to storage"""
        try:
            session_file = self._get_session_filename(account['username'])
            encrypted_data = self.encryption.encrypt(json.dumps(session_data))
            
            with open(session_file, 'wb') as f:
                pickle.dump(encrypted_data, f)
                
        except Exception as e:
            self.logger.error(f"Session save failed: {e}")
            
    def _get_session_filename(self, username: str) -> str:
        """Generate session filename"""
        username_hash = hashlib.md5(username.encode()).hexdigest()
        return f'sessions/{username_hash}.session'
        
    async def save_session(self, account: Dict, page: Page):
        """Save current session state"""
        try:
            cookies = await page.cookies()
            session_data = {
                'username': account['username'],
                'cookies': cookies,
                'updated_at': time.time()
            }
            
            await self._save_session(account, session_data)
            
        except Exception as e:
            self.logger.error(f"Session save failed: {e}")