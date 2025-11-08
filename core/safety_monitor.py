"""
Advanced Safety Monitoring and Risk Management
"""

import asyncio
import time
import logging
from typing import Dict, List, Optional
from pyppeteer.page import Page

class SafetyMonitor:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.account_health = {}
        self.risk_thresholds = {
            'max_actions_per_hour': 30,
            'max_follows_per_day': 50,
            'max_comments_per_day': 30,
            'cooldown_period': 3600,  # 1 hour
            'suspicion_score_limit': 80
        }
        
    async def check_account_safety(self, account: Dict) -> bool:
        """Check if account is safe to use"""
        try:
            username = account['username']
            
            # Initialize account health tracking
            if username not in self.account_health:
                self.account_health[username] = {
                    'last_used': 0,
                    'action_count': 0,
                    'suspicion_score': 0,
                    'cooldown_until': 0
                }
                
            health = self.account_health[username]
            
            # Check cooldown period
            if time.time() < health['cooldown_until']:
                self.logger.warning(f"Account {username} is in cooldown")
                return False
                
            # Check action limits
            if health['action_count'] >= self.risk_thresholds['max_actions_per_hour']:
                self.logger.warning(f"Account {username} exceeded action limits")
                return False
                
            # Check suspicion score
            if health['suspicion_score'] >= self.risk_thresholds['suspicion_score_limit']:
                self.logger.warning(f"Account {username} has high suspicion score")
                return False
                
            return True
            
        except Exception as e:
            self.logger.error(f"Safety check failed: {e}")
            return False
            
    async def monitor_page_activity(self, page: Page, account: Dict):
        """Monitor page for suspicious activity"""
        try:
            # Detect shadowban indicators
            await self._check_shadowban_indicators(page, account)
            
            # Monitor rate limits
            await self._check_rate_limits(page, account)
            
            # Update account health
            self._update_health_metrics(account)
            
        except Exception as e:
            self.logger.error(f"Page monitoring failed: {e}")
            
    async def _check_shadowban_indicators(self, page: Page, account: Dict):
        """Check for shadowban indicators"""
        try:
            # Check if videos are visible
            video_count = await page.evaluate('''
                () => {
                    const videos = document.querySelectorAll('div[data-e2e="user-post-item"]');
                    return videos.length;
                }
            ''')
            
            # Check if follow button is disabled
            follow_disabled = await page.evaluate('''
                () => {
                    const followBtn = document.querySelector('button[data-e2e="user-follow"]');
                    return followBtn ? followBtn.disabled : false;
                }
            ''')
            
            if video_count == 0 or follow_disabled:
                self.account_health[account['username']]['suspicion_score'] += 20
                self.logger.warning(f"Shadowban indicators detected for {account['username']}")
                
        except Exception as e:
            self.logger.error(f"Shadowban check failed: {e}")
            
    async def _check_rate_limits(self, page: Page, account: Dict):
        """Check for rate limiting"""
        try:
            # Check for error messages
            error_elements = await page.querySelectorAll('[class*="error"], [class*="limit"]')
            if error_elements:
                self.account_health[account['username']]['suspicion_score'] += 10
                self.logger.warning(f"Rate limit indicators detected for {account['username']}")
                
        except Exception as e:
            self.logger.error(f"Rate limit check failed: {e}")
            
    def _update_health_metrics(self, account: Dict):
        """Update account health metrics"""
        username = account['username']
        health = self.account_health[username]
        
        health['action_count'] += 1
        health['last_used'] = time.time()
        
        # Gradually decrease suspicion score
        if health['suspicion_score'] > 0:
            health['suspicion_score'] -= 1
            
    async def trigger_cooldown(self, account: Dict, duration: int = None):
        """Trigger cooldown period for account"""
        username = account['username']
        cooldown_duration = duration or self.risk_thresholds['cooldown_period']
        
        self.account_health[username]['cooldown_until'] = time.time() + cooldown_duration
        self.account_health[username]['action_count'] = 0
        
        self.logger.info(f"Cooldown triggered for {username}: {cooldown_duration} seconds")
        
    def get_account_health(self, account: Dict) -> Dict:
        """Get account health status"""
        username = account['username']
        return self.account_health.get(username, {})