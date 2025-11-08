"""
Advanced Proxy Rotation and Management
"""

import asyncio
import random
import aiohttp
import logging
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass

@dataclass
class Proxy:
    address: str
    protocol: str
    health_score: float = 100.0
    last_used: float = 0
    response_time: float = 0
    success_count: int = 0
    failure_count: int = 0

class ProxyRotator:
    def __init__(self, proxy_file: str = "config/proxies.txt"):
        self.proxy_file = proxy_file
        self.logger = logging.getLogger(__name__)
        self.proxies: List[Proxy] = []
        self.load_proxies()
        
    def load_proxies(self):
        """Load proxies from file"""
        try:
            if not os.path.exists(self.proxy_file):
                self.logger.warning(f"Proxy file not found: {self.proxy_file}")
                return
                
            with open(self.proxy_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        self._parse_proxy_line(line)
                        
            self.logger.info(f"Loaded {len(self.proxies)} proxies")
            
        except Exception as e:
            self.logger.error(f"Proxy loading failed: {e}")
            
    def _parse_proxy_line(self, line: str):
        """Parse proxy line and create Proxy object"""
        try:
            # Handle different proxy formats
            if line.startswith('http://') or line.startswith('https://'):
                protocol = 'http'
            elif line.startswith('socks5://'):
                protocol = 'socks5'
            else:
                protocol = 'http'
                line = f'http://{line}'  # Assume HTTP if no protocol
                
            proxy = Proxy(address=line, protocol=protocol)
            self.proxies.append(proxy)
            
        except Exception as e:
            self.logger.error(f"Proxy parsing failed for line '{line}': {e}")
            
    async def get_proxy(self, account: Dict) -> Optional[str]:
        """Get best available proxy for account"""
        if not self.proxies:
            return None
            
        # Filter healthy proxies
        healthy_proxies = [p for p in self.proxies if p.health_score > 50]
        
        if not healthy_proxies:
            self.logger.warning("No healthy proxies available")
            return None
            
        # Select proxy based on health score and recent usage
        proxy = self._select_optimal_proxy(healthy_proxies)
        
        if proxy:
            proxy.last_used = asyncio.get_event_loop().time()
            return proxy.address
            
        return None
        
    def _select_optimal_proxy(self, proxies: List[Proxy]) -> Optional[Proxy]:
        """Select optimal proxy based on multiple factors"""
        if not proxies:
            return None
            
        # Calculate scores for each proxy
        scored_proxies = []
        current_time = asyncio.get_event_loop().time()
        
        for proxy in proxies:
            score = proxy.health_score
            
            # Penalize recently used proxies
            time_since_use = current_time - proxy.last_used
            if time_since_use < 300:  # 5 minutes
                recency_penalty = (300 - time_since_use) / 300 * 20  # Up to 20% penalty
                score -= recency_penalty
                
            # Bonus for fast response times
            if proxy.response_time > 0:
                speed_bonus = max(0, 10 - (proxy.response_time / 1000))  # Up to 10% bonus
                score += speed_bonus
                
            scored_proxies.append((proxy, max(1, score)))  # Ensure minimum score of 1
            
        # Weighted random selection
        total_score = sum(score for _, score in scored_proxies)
        if total_score == 0:
            return random.choice(proxies)
            
        selection = random.uniform(0, total_score)
        current = 0
        
        for proxy, score in scored_proxies:
            current += score
            if current >= selection:
                return proxy
                
        return scored_proxies[0][0]  # Fallback to first proxy
        
    async def validate_proxy(self, proxy: Proxy) -> bool:
        """Validate proxy connectivity and speed"""
        try:
            timeout = aiohttp.ClientTimeout(total=10)
            
            async with aiohttp.ClientSession(timeout=timeout) as session:
                start_time = asyncio.get_event_loop().time()
                
                try:
                    async with session.get(
                        'https://httpbin.org/ip',
                        proxy=proxy.address
                    ) as response:
                        if response.status == 200:
                            response_time = (asyncio.get_event_loop().time() - start_time) * 1000
                            
                            # Update proxy metrics
                            proxy.response_time = response_time
                            proxy.success_count += 1
                            proxy.health_score = min(100, proxy.health_score + 5)
                            
                            self.logger.info(f"Proxy validated: {proxy.address} - {response_time:.0f}ms")
                            return True
                            
                except asyncio.TimeoutError:
                    self.logger.warning(f"Proxy timeout: {proxy.address}")
                    
        except Exception as e:
            self.logger.debug(f"Proxy validation failed for {proxy.address}: {e}")
            
        # Update failure metrics
        proxy.failure_count += 1
        proxy.health_score = max(0, proxy.health_score - 15)
        
        return False
        
    async def validate_all_proxies(self):
        """Validate all proxies and remove unhealthy ones"""
        self.logger.info("Starting proxy validation...")
        
        validation_tasks = []
        for proxy in self.proxies:
            task = self.validate_proxy(proxy)
            validation_tasks.append(task)
            
        results = await asyncio.gather(*validation_tasks, return_exceptions=True)
        
        healthy_count = sum(1 for result in results if result is True)
        self.logger.info(f"Proxy validation complete: {healthy_count}/{len(self.proxies)} healthy")
        
    def get_proxy_stats(self) -> Dict:
        """Get proxy statistics"""
        total_proxies = len(self.proxies)
        healthy_proxies = len([p for p in self.proxies if p.health_score > 70])
        average_health = sum(p.health_score for p in self.proxies) / total_proxies if total_proxies > 0 else 0
        
        return {
            'total_proxies': total_proxies,
            'healthy_proxies': healthy_proxies,
            'unhealthy_proxies': total_proxies - healthy_proxies,
            'average_health_score': average_health,
            'total_requests': sum(p.success_count + p.failure_count for p in self.proxies),
            'success_rate': (sum(p.success_count for p in self.proxies) / 
                           sum(p.success_count + p.failure_count for p in self.proxies) * 100 
                           if total_proxies > 0 else 0)
        }
        
    def remove_unhealthy_proxies(self, threshold: float = 30.0):
        """Remove proxies below health threshold"""
        initial_count = len(self.proxies)
        self.proxies = [p for p in self.proxies if p.health_score >= threshold]
        removed_count = initial_count - len(self.proxies)
        
        if removed_count > 0:
            self.logger.info(f"Removed {removed_count} unhealthy proxies")