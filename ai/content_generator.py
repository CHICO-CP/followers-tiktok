"""
AI-Powered Content Generation for Natural Interactions
"""

import random
import logging
from typing import List, Dict, Optional

class ContentGenerator:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.comment_templates = self._load_comment_templates()
        self.sentiment_keywords = self._load_sentiment_keywords()
        
    async def generate_comment(self, page) -> Optional[str]:
        """Generate context-aware comment for current video"""
        try:
            # Extract video context
            video_context = await self._extract_video_context(page)
            
            # Generate appropriate comment
            if video_context:
                comment = self._create_contextual_comment(video_context)
            else:
                comment = self._get_random_comment()
                
            return comment if self._validate_comment(comment) else None
            
        except Exception as e:
            self.logger.error(f"Comment generation failed: {e}")
            return self._get_random_comment()
            
    async def _extract_video_context(self, page) -> Optional[Dict]:
        """Extract context from current video"""
        try:
            context = {}
            
            # Extract video description
            description = await page.evaluate('''
                () => {
                    const desc = document.querySelector('[data-e2e="video-desc"]');
                    return desc ? desc.textContent.trim() : '';
                }
            ''')
            context['description'] = description
            
            # Extract hashtags
            hashtags = await page.evaluate('''
                () => {
                    const tags = document.querySelectorAll('[data-e2e*="hash"]');
                    return Array.from(tags).map(tag => tag.textContent).slice(0, 5);
                }
            ''')
            context['hashtags'] = hashtags
            
            # Extract like count for engagement level
            likes = await page.evaluate('''
                () => {
                    const likeCount = document.querySelector('[data-e2e="like-count"]');
                    return likeCount ? likeCount.textContent : '0';
                }
            ''')
            context['like_count'] = likes
            
            return context if context['description'] or context['hashtags'] else None
            
        except:
            return None
            
    def _create_contextual_comment(self, context: Dict) -> str:
        """Create comment based on video context"""
        try:
            description = context.get('description', '').lower()
            hashtags = context.get('hashtags', [])
            
            # Determine content type
            content_type = self._classify_content(description, hashtags)
            
            # Select appropriate template
            templates = self.comment_templates.get(content_type, [])
            if not templates:
                templates = self.comment_templates['general']
                
            template = random.choice(templates)
            
            # Fill template with context
            comment = self._fill_template(template, context)
            return comment
            
        except Exception as e:
            self.logger.error(f"Contextual comment creation failed: {e}")
            return self._get_random_comment()
            
    def _classify_content(self, description: str, hashtags: List[str]) -> str:
        """Classify content type"""
        text = description + ' ' + ' '.join(hashtags).lower()
        
        # Content classification logic
        if any(word in text for word in ['funny', 'comedy', 'lol', 'joke']):
            return 'funny'
        elif any(word in text for word in ['tutorial', 'how to', 'learn', 'guide']):
            return 'educational'
        elif any(word in text for word in ['dance', 'music', 'song', 'artist']):
            return 'music'
        elif any(word in text for word in ['challenge', 'trend', 'viral']):
            return 'trending'
        else:
            return 'general'
            
    def _fill_template(self, template: str, context: Dict) -> str:
        """Fill template with context data"""
        comment = template
        
        # Add relevant hashtags
        hashtags = context.get('hashtags', [])
        if hashtags and random.random() < 0.3:  # 30% chance to include hashtag
            hashtag = random.choice(hashtags)
            comment += f" {hashtag}"
            
        return comment.strip()
        
    def _get_random_comment(self) -> str:
        """Get random comment from templates"""
        all_templates = []
        for category in self.comment_templates.values():
            all_templates.extend(category)
            
        return random.choice(all_templates) if all_templates else "Great content! 👍"
        
    def _validate_comment(self, comment: str) -> bool:
        """Validate comment for safety and appropriateness"""
        if not comment or len(comment) < 5 or len(comment) > 150:
            return False
            
        # Check for inappropriate content
        blacklist = ['http', 'www.', '.com', 'follow', 'subscribe', 'check out']
        if any(phrase in comment.lower() for phrase in blacklist):
            return False
            
        return True
        
    def _load_comment_templates(self) -> Dict[str, List[str]]:
        """Load comment templates by category"""
        return {
            'general': [
                "This is amazing! 🔥",
                "Love this content! ❤️",
                "You're so talented! ✨",
                "This made my day! 😊",
                "Incredible work! 👏"
            ],
            'funny': [
                "I can't stop laughing! 😂",
                "This is hilarious! 🤣",
                "You're too funny! 😄",
                "My stomach hurts from laughing! 💀",
                "Comedy gold! 🥇"
            ],
            'educational': [
                "So informative! 📚",
                "Learned something new today! 🧠",
                "Great explanation! 👍",
                "This is really helpful! 💡",
                "Thanks for sharing this knowledge! 🙏"
            ],
            'music': [
                "This beat is fire! 🎵",
                "Amazing rhythm! 🎶",
                "You've got great taste in music! 🎧",
                "This song is stuck in my head now! 🎤",
                "Perfect vibes! 🌟"
            ],
            'trending': [
                "This is going viral! 🚀",
                "You're winning this challenge! 🏆",
                "Trendsetter! 💫",
                "This is so creative! 🎨",
                "You nailed this trend! ✅"
            ]
        }
        
    def _load_sentiment_keywords(self) -> Dict[str, List[str]]:
        """Load sentiment analysis keywords"""
        return {
            'positive': ['love', 'amazing', 'great', 'awesome', 'fantastic', 'perfect'],
            'supportive': ['proud', 'impressed', 'inspired', 'motivated', 'encouraging'],
            'curious': ['how', 'what', 'when', 'where', 'tell me more', 'explain'],
            'excited': ['wow', 'omg', 'incredible', 'unbelievable', 'mind blown']
        }