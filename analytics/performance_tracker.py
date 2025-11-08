"""
Advanced Performance Tracking and Optimization
"""

import time
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from dataclasses import dataclass

@dataclass
class PerformanceMetrics:
    actions_completed: int = 0
    actions_failed: int = 0
    total_response_time: float = 0
    last_action_time: Optional[datetime] = None
    peak_performance: float = 0
    
class PerformanceTracker:
    def __init__(self, database):
        self.database = database
        self.logger = logging.getLogger(__name__)
        self.account_metrics: Dict[str, PerformanceMetrics] = {}
        self.optimization_rules = self._load_optimization_rules()
        
    async def track_action(self, username: str, action_type: str, success: bool, 
                          response_time: float, target_user: str = None):
        """Track action performance"""
        try:
            # Initialize metrics for new account
            if username not in self.account_metrics:
                self.account_metrics[username] = PerformanceMetrics()
                
            metrics = self.account_metrics[username]
            
            # Update metrics
            if success:
                metrics.actions_completed += 1
            else:
                metrics.actions_failed += 1
                
            metrics.total_response_time += response_time
            metrics.last_action_time = datetime.now()
            
            # Calculate current performance
            current_performance = self._calculate_performance_metrics(metrics)
            metrics.peak_performance = max(metrics.peak_performance, current_performance)
            
            # Log to database
            details = {
                'performance_score': current_performance,
                'peak_performance': metrics.peak_performance
            }
            
            self.database.log_interaction(
                username, action_type, target_user, success, response_time, details
            )
            
            # Check for optimization triggers
            await self._check_optimization_triggers(username, metrics)
            
            self.logger.info(f"Action tracked: {username} - {action_type} - {success}")
            
        except Exception as e:
            self.logger.error(f"Action tracking failed: {e}")
            
    def _calculate_performance_metrics(self, metrics: PerformanceMetrics) -> float:
        """Calculate performance score (0-100)"""
        if metrics.actions_completed + metrics.actions_failed == 0:
            return 0
            
        success_rate = (metrics.actions_completed / 
                       (metrics.actions_completed + metrics.actions_failed)) * 100
        
        # Adjust for response time (faster is better)
        avg_response_time = (metrics.total_response_time / 
                           (metrics.actions_completed + metrics.actions_failed))
        time_score = max(0, 100 - (avg_response_time * 10))  # Penalize slow responses
        
        # Combined score (70% success rate, 30% speed)
        performance_score = (success_rate * 0.7) + (time_score * 0.3)
        
        return min(100, performance_score)
        
    async def _check_optimization_triggers(self, username: str, metrics: PerformanceMetrics):
        """Check if optimization actions are needed"""
        performance_score = self._calculate_performance_metrics(metrics)
        
        # Check for performance degradation
        if performance_score < 60:  # Below 60% performance
            self.logger.warning(f"Performance degradation detected for {username}: {performance_score:.1f}%")
            
            # Log safety event
            self.database.log_safety_event(
                username, 
                'performance_degradation', 
                'medium',
                f'Performance score dropped to {performance_score:.1f}%'
            )
            
        # Check for suspicious patterns
        if self._detect_suspicious_patterns(username, metrics):
            self.database.log_safety_event(
                username,
                'suspicious_activity_pattern',
                'high',
                'Unusual activity pattern detected'
            )
            
    def _detect_suspicious_patterns(self, username: str, metrics: PerformanceMetrics) -> bool:
        """Detect suspicious activity patterns"""
        # Example detection logic
        failure_rate = (metrics.actions_failed / 
                       (metrics.actions_completed + metrics.actions_failed))
        
        # High failure rate
        if failure_rate > 0.5:  # More than 50% failures
            return True
            
        # Rapid successive actions (potential bot detection)
        if metrics.last_action_time:
            time_since_last = (datetime.now() - metrics.last_action_time).total_seconds()
            if time_since_last < 1:  # Actions less than 1 second apart
                return True
                
        return False
        
    def get_account_performance(self, username: str) -> Dict:
        """Get performance data for account"""
        if username not in self.account_metrics:
            return {}
            
        metrics = self.account_metrics[username]
        performance_score = self._calculate_performance_metrics(metrics)
        
        return {
            'username': username,
            'performance_score': performance_score,
            'peak_performance': metrics.peak_performance,
            'actions_completed': metrics.actions_completed,
            'actions_failed': metrics.actions_failed,
            'success_rate': (metrics.actions_completed / 
                           (metrics.actions_completed + metrics.actions_failed)) * 100,
            'avg_response_time': (metrics.total_response_time / 
                                (metrics.actions_completed + metrics.actions_failed)),
            'last_action_time': metrics.last_action_time
        }
        
    def get_overall_performance(self) -> Dict:
        """Get overall performance across all accounts"""
        total_completed = sum(m.actions_completed for m in self.account_metrics.values())
        total_failed = sum(m.actions_failed for m in self.account_metrics.values())
        total_response_time = sum(m.total_response_time for m in self.account_metrics.values())
        
        if total_completed + total_failed == 0:
            return {}
            
        overall_success_rate = (total_completed / (total_completed + total_failed)) * 100
        avg_response_time = total_response_time / (total_completed + total_failed)
        
        # Calculate weighted performance score
        total_performance = 0
        total_weight = 0
        
        for username, metrics in self.account_metrics.items():
            weight = metrics.actions_completed + metrics.actions_failed
            performance = self._calculate_performance_metrics(metrics)
            total_performance += performance * weight
            total_weight += weight
            
        overall_performance = total_performance / total_weight if total_weight > 0 else 0
        
        return {
            'overall_performance': overall_performance,
            'success_rate': overall_success_rate,
            'avg_response_time': avg_response_time,
            'total_actions': total_completed + total_failed,
            'active_accounts': len(self.account_metrics),
            'top_performer': self._get_top_performer()
        }
        
    def _get_top_performer(self) -> Optional[Dict]:
        """Get top performing account"""
        if not self.account_metrics:
            return None
            
        top_account = None
        top_score = -1
        
        for username, metrics in self.account_metrics.items():
            score = self._calculate_performance_metrics(metrics)
            if score > top_score:
                top_score = score
                top_account = username
                
        return {
            'username': top_account,
            'performance_score': top_score
        } if top_account else None
        
    def _load_optimization_rules(self) -> Dict:
        """Load performance optimization rules"""
        return {
            'performance_thresholds': {
                'excellent': 85,
                'good': 70,
                'fair': 60,
                'poor': 50
            },
            'optimization_actions': {
                'poor': 'reduce_activity_increase_delays',
                'fair': 'adjust_timing_patterns',
                'good': 'maintain_current_strategy',
                'excellent': 'increase_activity_carefully'
            }
        }
        
    def get_optimization_recommendation(self, username: str) -> str:
        """Get optimization recommendation for account"""
        if username not in self.account_metrics:
            return "no_data"
            
        performance_score = self._calculate_performance_metrics(self.account_metrics[username])
        
        thresholds = self.optimization_rules['performance_thresholds']
        actions = self.optimization_rules['optimization_actions']
        
        if performance_score >= thresholds['excellent']:
            return actions['excellent']
        elif performance_score >= thresholds['good']:
            return actions['good']
        elif performance_score >= thresholds['fair']:
            return actions['fair']
        else:
            return actions['poor']