"""
Advanced Human Behavior Simulation
"""

import asyncio
import random
import math
import logging
from typing import Dict, Tuple
from pyppeteer.page import Page

class BehaviorSimulator:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.behavior_profiles = self._load_behavior_profiles()
        
    async def simulate_video_watching(self, page: Page):
        """Simulate natural video watching behavior"""
        try:
            # Random watch time (10-45 seconds)
            watch_time = random.uniform(10, 45)
            
            # Simulate occasional scrolling while watching
            scroll_chance = 0.3  # 30% chance to scroll during video
            
            elapsed = 0
            while elapsed < watch_time:
                # Random micro-pauses
                if random.random() < 0.2:  # 20% chance per second
                    await asyncio.sleep(random.uniform(0.5, 2))
                    
                # Occasional scroll during video
                if random.random() < scroll_chance:
                    await self._simulate_natural_scroll(page)
                    scroll_chance *= 0.5  # Reduce chance after scrolling
                    
                await asyncio.sleep(1)
                elapsed += 1
                
            # Random reaction after video
            await self._simulate_post_video_reaction(page)
            
        except Exception as e:
            self.logger.error(f"Video watching simulation failed: {e}")
            
    async def simulate_typing(self, page: Page, element, text: str):
        """Simulate human-like typing"""
        try:
            await element.click()
            await element.evaluate('(element) => element.value = ""')
            
            for char in text:
                # Type character
                await element.type(char)
                
                # Random typing speed variations
                base_delay = random.uniform(0.05, 0.15)
                
                # Occasional pauses (thinking time)
                if random.random() < 0.05:  # 5% chance per character
                    await asyncio.sleep(random.uniform(0.5, 1.5))
                    
                # Occasional typos and corrections (2% chance)
                if random.random() < 0.02:
                    await page.keyboard.press('Backspace')
                    await asyncio.sleep(random.uniform(0.1, 0.3))
                    await element.type(char)
                    
                await asyncio.sleep(base_delay)
                
        except Exception as e:
            self.logger.error(f"Typing simulation failed: {e}")
            # Fallback to normal typing
            await element.type(text)
            
    async def simulate_mouse_movement(self, page: Page, start_selector: str, end_selector: str):
        """Simulate natural mouse movement between elements"""
        try:
            start_element = await page.querySelector(start_selector)
            end_element = await page.querySelector(end_selector)
            
            if not start_element or not end_element:
                return
                
            # Get element positions
            start_rect = await start_element.boundingBox()
            end_rect = await end_element.boundingBox()
            
            if not start_rect or not end_rect:
                return
                
            # Generate curved mouse path
            path = self._generate_mouse_path(
                (start_rect['x'] + start_rect['width'] / 2, 
                 start_rect['y'] + start_rect['height'] / 2),
                (end_rect['x'] + end_rect['width'] / 2, 
                 end_rect['y'] + end_rect['height'] / 2)
            )
            
            # Move mouse along path
            for point in path:
                await page.mouse.move(point[0], point[1])
                await asyncio.sleep(random.uniform(0.01, 0.03))
                
        except Exception as e:
            self.logger.error(f"Mouse movement simulation failed: {e}")
            
    async def _simulate_natural_scroll(self, page: Page):
        """Simulate natural scrolling behavior"""
        try:
            # Random scroll distance and speed
            scroll_distance = random.randint(100, 400)
            scroll_steps = random.randint(3, 8)
            
            for step in range(scroll_steps):
                scroll_amount = scroll_distance / scroll_steps
                # Add some randomness to each step
                varied_scroll = scroll_amount * random.uniform(0.8, 1.2)
                
                await page.evaluate(f'window.scrollBy(0, {varied_scroll})')
                await asyncio.sleep(random.uniform(0.1, 0.3))
                
        except Exception as e:
            self.logger.error(f"Scroll simulation failed: {e}")
            
    async def _simulate_post_video_reaction(self, page: Page):
        """Simulate natural reactions after watching video"""
        try:
            # Random reactions (like, share, etc.)
            reactions = [
                self._simulate_like_reaction,
                self._simulate_share_consideration,
                self._simulate_replay_consideration
            ]
            
            # Perform 1-2 random reactions
            num_reactions = random.randint(1, 2)
            chosen_reactions = random.sample(reactions, num_reactions)
            
            for reaction in chosen_reactions:
                await reaction(page)
                await asyncio.sleep(random.uniform(1, 3))
                
        except Exception as e:
            self.logger.error(f"Post-video reaction simulation failed: {e}")
            
    async def _simulate_like_reaction(self, page: Page):
        """Simulate considering to like the video"""
        try:
            # Hover over like button
            like_icon = await page.querySelector('div[data-e2e="like-icon"]')
            if like_icon:
                await like_icon.hover()
                await asyncio.sleep(random.uniform(0.5, 1.5))
                
        except:
            pass
            
    async def _simulate_share_consideration(self, page: Page):
        """Simulate considering to share the video"""
        try:
            # Look for share button (varies by TikTok version)
            share_selectors = [
                '[data-e2e*="share"]',
                '[aria-label*="share"]',
                '.share-icon'
            ]
            
            for selector in share_selectors:
                share_btn = await page.querySelector(selector)
                if share_btn:
                    await share_btn.hover()
                    await asyncio.sleep(random.uniform(0.5, 1))
                    break
                    
        except:
            pass
            
    async def _simulate_replay_consideration(self, page: Page):
        """Simulate considering to replay the video"""
        try:
            # Small scroll to indicate replay consideration
            await page.evaluate('window.scrollBy(0, 50)')
            await asyncio.sleep(random.uniform(0.5, 1))
            await page.evaluate('window.scrollBy(0, -50)')
            
        except:
            pass
            
    def _generate_mouse_path(self, start: Tuple[float, float], end: Tuple[float, float]) -> list:
        """Generate curved mouse path between two points"""
        path = []
        
        # Number of points in path
        num_points = random.randint(20, 40)
        
        # Control points for Bezier curve
        control1 = (
            start[0] + (end[0] - start[0]) * random.uniform(0.3, 0.7),
            start[1] + random.uniform(-100, 100)
        )
        control2 = (
            start[0] + (end[0] - start[0]) * random.uniform(0.3, 0.7),
            end[1] + random.uniform(-100, 100)
        )
        
        for i in range(num_points):
            t = i / (num_points - 1)
            
            # Cubic Bezier curve calculation
            x = (1-t)**3 * start[0] + 3*(1-t)**2*t * control1[0] + 3*(1-t)*t**2 * control2[0] + t**3 * end[0]
            y = (1-t)**3 * start[1] + 3*(1-t)**2*t * control1[1] + 3*(1-t)*t**2 * control2[1] + t**3 * end[1]
            
            # Add some randomness to the path
            x += random.uniform(-3, 3)
            y += random.uniform(-3, 3)
            
            path.append((x, y))
            
        return path
        
    def _load_behavior_profiles(self) -> Dict:
        """Load different behavior profiles"""
        return {
            'casual': {
                'typing_speed_min': 50,
                'typing_speed_max': 150,
                'watch_time_min': 15,
                'watch_time_max': 30,
                'scroll_speed': 'medium'
            },
            'power_user': {
                'typing_speed_min': 80,
                'typing_speed_max': 200,
                'watch_time_min': 10,
                'watch_time_max': 25,
                'scroll_speed': 'fast'
            },
            'content_creator': {
                'typing_speed_min': 40,
                'typing_speed_max': 120,
                'watch_time_min': 20,
                'watch_time_max': 45,
                'scroll_speed': 'slow'
            }
        }