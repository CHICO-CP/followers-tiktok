#!/usr/bin/env python3
"""
TikTok Automation Bot - Main Orchestrator
Advanced modular architecture for maximum efficiency and safety
"""

import asyncio
import logging
import sys
import os
from typing import Dict, List, Optional

# Add modules to path
sys.path.extend(['core', 'ai', 'analytics', 'security'])

from core.browser_manager import BrowserManager
from core.session_manager import SessionManager
from core.action_executor import ActionExecutor
from core.safety_monitor import SafetyMonitor
from ai.content_generator import ContentGenerator
from ai.behavior_simulator import BehaviorSimulator
from analytics.database import Database
from analytics.performance_tracker import PerformanceTracker
from security.encryption import EncryptionManager
from security.proxy_rotator import ProxyRotator

class TikTokBot:
    def __init__(self):
        self.setup_logging()
        self.load_configuration()
        self.initialize_modules()
        
    def setup_logging(self):
        """Configure advanced logging"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S',
            handlers=[
                logging.FileHandler('logs/bot_operation.log', encoding='utf-8'),
                logging.StreamHandler(sys.stdout)
            ]
        )
        self.logger = logging.getLogger(__name__)
        
    def load_configuration(self):
        """Load all configuration files"""
        self.config = self.load_json_config('config/settings.json')
        self.accounts = self.load_json_config('config/accounts.json')
        self.comments = self.load_json_config('config/comments.json')
        
    def load_json_config(self, filepath: str) -> Dict:
        """Load JSON configuration file"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            self.logger.error(f"Error loading {filepath}: {e}")
            return {}
            
    def initialize_modules(self):
        """Initialize all bot modules"""
        self.logger.info("Initializing TikTok Bot Modules...")
        
        # Security modules first
        self.encryption = EncryptionManager()
        self.proxy_rotator = ProxyRotator()
        
        # Core functionality
        self.browser_manager = BrowserManager(self.proxy_rotator)
        self.session_manager = SessionManager(self.encryption)
        self.action_executor = ActionExecutor()
        self.safety_monitor = SafetyMonitor()
        
        # AI intelligence
        self.content_generator = ContentGenerator()
        self.behavior_simulator = BehaviorSimulator()
        
        # Analytics
        self.database = Database()
        self.performance_tracker = PerformanceTracker()
        
        self.logger.info("All modules initialized successfully")
        
    async def run_account_cycle(self, account: Dict) -> bool:
        """Run complete cycle for one account"""
        try:
            self.logger.info(f"Starting cycle for account: {account['username']}")
            
            # Safety check
            if not await self.safety_monitor.check_account_safety(account):
                self.logger.warning(f"Account {account['username']} failed safety check")
                return False
                
            # Create browser instance
            browser = await self.browser_manager.create_browser(account)
            if not browser:
                return False
                
            # Create page and setup
            page = await browser.newPage()
            await self.browser_manager.setup_page(page)
            
            # Session management
            session = await self.session_manager.initialize_session(account, page)
            if not session:
                await browser.close()
                return False
                
            # Execute actions
            success = await self.execute_actions(account, page, session)
            
            # Cleanup
            await self.session_manager.save_session(account, page)
            await browser.close()
            
            return success
            
        except Exception as e:
            self.logger.error(f"Account cycle failed for {account['username']}: {e}")
            return False
            
    async def execute_actions(self, account: Dict, page, session) -> bool:
        """Execute TikTok actions for account"""
        try:
            target_username = self.get_target_username()
            if not target_username:
                return False
                
            # Search and follow
            if not await self.action_executor.search_and_follow(page, target_username):
                return False
                
            # Interact with videos
            await self.action_executor.interact_with_videos(
                page, 
                target_username,
                self.content_generator,
                self.behavior_simulator
            )
            
            # Track performance
            await self.performance_tracker.track_actions(account['username'])
            
            return True
            
        except Exception as e:
            self.logger.error(f"Action execution failed: {e}")
            return False
            
    def get_target_username(self) -> Optional[str]:
        """Get target username from user input"""
        try:
            target = input("Enter TikTok username to target: ").strip()
            return target if target else None
        except:
            return None
            
    async def run(self):
        """Main bot execution loop"""
        self.logger.info("🚀 Starting TikTok Automation Bot")
        
        try:
            successful_accounts = 0
            
            for account in self.accounts.get('accounts', []):
                if not account.get('enabled', True):
                    continue
                    
                if await self.run_account_cycle(account):
                    successful_accounts += 1
                    
                # Delay between accounts
                await asyncio.sleep(30)
                
            self.logger.info(f"✅ Bot completed. Successful accounts: {successful_accounts}/{len(self.accounts.get('accounts', []))}")
            
        except KeyboardInterrupt:
            self.logger.info("Bot stopped by user")
        except Exception as e:
            self.logger.error(f"Bot crashed: {e}")
        finally:
            await self.cleanup()
            
    async def cleanup(self):
        """Cleanup resources"""
        await self.browser_manager.cleanup()
        self.database.close()

async def main():
    """Application entry point"""
    bot = TikTokBot()
    await bot.run()

if __name__ == "__main__":
    # Import required for submodules
    import json
    asyncio.run(main())