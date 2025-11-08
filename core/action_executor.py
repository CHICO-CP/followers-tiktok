"""
Advanced Action Execution with Human-like Behavior
"""

import asyncio
import random
import logging
from typing import Optional, List, Dict
from pyppeteer.page import Page

class ActionExecutor:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.action_delays = {
            'min_delay': 2,
            'max_delay': 8,
            'typing_speed': (50, 150)  # chars per minute range
        }
        
    async def search_and_follow(self, page: Page, target_username: str) -> bool:
        """Search for user and follow them"""
        try:
            self.logger.info(f"Searching for user: {target_username}")
            
            # Click search icon
            search_icon = await page.querySelector('div[data-e2e="search-icon"]')
            if search_icon:
                await search_icon.click()
                await self.random_delay(1, 3)
            
            # Find search input
            search_input = await page.querySelector('input[type="text"]')
            if not search_input:
                self.logger.error("Search input not found")
                return False
                
            # Type username with human-like behavior
            await self.human_type(page, search_input, target_username)
            await page.keyboard.press('Enter')
            await self.random_delay(2, 4)
            
            # Wait for results and click first user
            user_card = await page.waitForSelector(
                'a[data-e2e="search-user-card"]', 
                timeout=10000
            )
            if user_card:
                await user_card.click()
                await self.random_delay(2, 4)
                
                # Follow user
                follow_btn = await page.waitForSelector(
                    'button[data-e2e="user-follow"]', 
                    timeout=10000
                )
                if follow_btn:
                    await follow_btn.click()
                    self.logger.info(f"Successfully followed {target_username}")
                    await self.random_delay(2, 5)
                    return True
                    
            self.logger.error(f"User {target_username} not found or follow failed")
            return False
            
        except Exception as e:
            self.logger.error(f"Search and follow failed: {e}")
            return False
            
    async def interact_with_videos(self, page: Page, target_username: str, 
                                 content_generator, behavior_simulator):
        """Interact with user's videos"""
        try:
            self.logger.info(f"Starting video interaction for {target_username}")
            
            # Wait for videos to load
            await page.waitForSelector('div[data-e2e="user-post-item"]', timeout=10000)
            
            # Get video elements
            video_elements = await page.querySelectorAll('div[data-e2e="user-post-item"]')
            
            if not video_elements:
                self.logger.info("No videos found for user")
                return
                
            # Limit interactions to avoid spam
            max_interactions = min(3, len(video_elements))
            videos_to_interact = random.sample(
                range(len(video_elements)), 
                max_interactions
            )
            
            self.logger.info(f"Interacting with {max_interactions} videos")
            
            for i, video_index in enumerate(videos_to_interact):
                try:
                    self.logger.info(f"Processing video {i + 1}/{max_interactions}")
                    
                    # Scroll to video
                    await self.scroll_to_element(page, video_elements[video_index])
                    await self.random_delay(1, 3)
                    
                    # Click video
                    await video_elements[video_index].click()
                    await self.random_delay(2, 4)
                    
                    # Watch video with human-like behavior
                    await behavior_simulator.simulate_video_watching(page)
                    
                    # Like video
                    if await self.like_video(page):
                        self.logger.info("Liked video")
                        
                    # Comment on video (50% chance)
                    if random.random() < 0.5:
                        comment = await content_generator.generate_comment(page)
                        if comment and await self.comment_on_video(page, comment):
                            self.logger.info(f"Commented: {comment}")
                    
                    # Close video
                    await self.close_video_player(page)
                    await self.random_delay(2, 4)
                    
                except Exception as e:
                    self.logger.error(f"Video interaction {i + 1} failed: {e}")
                    await self.close_video_player(page)
                    continue
                    
        except Exception as e:
            self.logger.error(f"Video interaction failed: {e}")
            
    async def like_video(self, page: Page) -> bool:
        """Like the current video"""
        try:
            like_icon = await page.querySelector('div[data-e2e="like-icon"]')
            if like_icon:
                await like_icon.click()
                await self.random_delay(1, 2)
                return True
            return False
        except:
            return False
            
    async def comment_on_video(self, page: Page, comment: str) -> bool:
        """Comment on the current video"""
        try:
            comment_input = await page.querySelector('textarea[data-e2e="comment-input"]')
            if comment_input:
                await self.human_type(page, comment_input, comment)
                await page.keyboard.press('Enter')
                await self.random_delay(2, 4)
                return True
            return False
        except:
            return False
            
    async def close_video_player(self, page: Page) -> bool:
        """Close video player"""
        try:
            close_selectors = [
                'div[data-e2e="close-icon"]',
                'button[data-e2e="browse-close"]',
                'svg[data-e2e="browse-close"]'
            ]
            
            for selector in close_selectors:
                close_btn = await page.querySelector(selector)
                if close_btn:
                    await close_btn.click()
                    await self.random_delay(1, 2)
                    return True
                    
            # Fallback: press Escape
            await page.keyboard.press('Escape')
            return True
            
        except:
            return False
            
    async def human_type(self, page: Page, element, text: str):
        """Type text with human-like behavior"""
        try:
            await element.click()
            await element.evaluate('(element) => element.value = ""')
            
            for char in text:
                await element.type(char)
                # Random typing delay
                await asyncio.sleep(random.uniform(0.05, 0.2))
                
        except Exception as e:
            self.logger.error(f"Human typing failed: {e}")
            # Fallback: normal typing
            await element.type(text)
            
    async def scroll_to_element(self, page: Page, element):
        """Scroll to element with human-like behavior"""
        try:
            await page.evaluate('(element) => {
                element.scrollIntoView({behavior: "smooth", block: "center"});
            }', element)
        except:
            # Fallback scroll
            await element.hover()
            
    async def random_delay(self, min_seconds: float, max_seconds: float):
        """Random delay between actions"""
        delay = random.uniform(min_seconds, max_seconds)
        await asyncio.sleep(delay)