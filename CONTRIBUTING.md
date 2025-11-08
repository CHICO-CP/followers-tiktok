# 🤝 Contributing Guide

Thank you for your interest in contributing to the followers-tiktok! This document provides guidelines and instructions for contributors.

## 🎯 Project Overview

The followers-tiktok is an advanced, modular research platform designed for:
- Digital interaction pattern analysis  
- AI-powered content generation research
- Ethical automation in academic contexts

## 📋 Table of Contents

- [Code of Conduct](#-code-of-conduct)
- [Getting Started](#-getting-started)
- [Development Setup](#-development-setup)
- [Project Structure](#-project-structure)
- [Contribution Workflow](#-contribution-workflow)
- [Code Standards](#-code-standards)
- [Testing](#-testing)
- [Documentation](#-documentation)
- [Pull Request Process](#-pull-request-process)

## 🙏 Code of Conduct

### Our Pledge
We are committed to maintaining a welcoming and respectful environment for all contributors. By participating in this project, you agree to:

- Use welcoming and inclusive language
- Be respectful of differing viewpoints and experiences
- Gracefully accept constructive criticism
- Focus on what is best for the community
- Show empathy towards other community members

### Our Standards
Examples of behavior that contributes to a positive environment:

- Demonstrating empathy and kindness toward other people
- Being respectful of differing opinions, viewpoints, and experiences
- Giving and gracefully accepting constructive feedback
- Accepting responsibility and apologizing to those affected by our mistakes
- Focusing on what is best not just for us as individuals, but for the overall community

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher
- Git
- Basic understanding of async programming in Python
- Familiarity with web automation concepts

### First Time Contributors
1. Look for issues labeled `good first issue` or `help wanted`
2. Comment on the issue to express your interest
3. Wait for maintainer assignment before starting work
4. Follow the development setup below

## 💻 Development Setup

### 1. Fork & Clone
```bash
# Fork the repository on GitHub
# Clone your fork locally
git clone https://github.com/CHICO-CP /followers-tiktok.git
cd followers-tiktok
```

2. Environment Setup

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/macOS
# venv\Scripts\activate  # Windows

# Install development dependencies
pip install -r requirements-dev.txt
```

3. Pre-commit Setup

```bash
# Install pre-commit hooks
pre-commit install

# Run pre-commit on all files
pre-commit run --all-files
```

# 🏗 Project Structure

```
followers-tiktok/
├── core/                 # Core automation functionality
│   ├── browser_manager.py    # Browser automation & stealth
│   ├── session_manager.py    # Account session handling
│   ├── action_executor.py    # Platform interactions
│   └── safety_monitor.py     # Risk detection & management
├── ai/                   # AI-powered intelligence
│   ├── content_generator.py  # Context-aware content creation
│   └── behavior_simulator.py # Human behavior emulation
├── analytics/            # Data analysis & reporting
│   ├── database.py           # Data persistence
│   └── performance_tracker.py # Metrics & optimization
├── security/             # Security & protection
│   ├── encryption.py         # Data encryption
│   └── proxy_rotator.py      # Proxy management
├── config/               # Configuration files
├── tests/                # Test suites
├── docs/                 # Documentation
└── scripts/              # Utility scripts
```

# 🔄 Contribution Workflow

1. Branch Naming

Use descriptive branch names following the pattern:

```bash
git checkout -b feature/description
git checkout -b fix/issue-description  
git checkout -b docs/topic-update
git checkout -b test/component-name
```

2. Commit Messages

Follow conventional commit format:

Types:

· feat: New feature

· fix: Bug fix

· docs: Documentation

· style: Formatting changes

· refactor: Code restructuring

· test: Adding tests

· chore: Maintenance tasks

Examples:

```
feat(ai): add sentiment analysis for comment generation
fix(browser): resolve fingerprint detection issues
docs(readme): update installation instructions
```

🎨 Code Standards

Python Standards

· Follow PEP 8 style guide

· Use type hints for all function signatures

· Maximum line length: 88 characters (Black formatter)

· Use descriptive variable and function names

Documentation Standards

· Google-style docstrings for all functions and classes

· Include examples in docstrings where applicable

· Keep README.md updated with new features

· Document all configuration options

Example Code Structure

```python
class ExampleComponent:
    """Brief description of the component.
    
    Detailed explanation of the component's purpose and functionality.
    
    Args:
        config: Configuration dictionary for the component
        logger: Logger instance for logging activities
        
    Attributes:
        enabled: Whether the component is active
        settings: Current configuration settings
    """
    
    def __init__(self, config: Dict, logger: logging.Logger):
        self.config = config
        self.logger = logger
        self.enabled = config.get('enabled', True)
        
    async def perform_action(self, data: Any) -> bool:
        """Perform a specific action with the given data.
        
        Args:
            data: Input data for the action
            
        Returns:
            bool: Success status of the action
            
        Raises:
            ValueError: If data is invalid
            RuntimeError: If action cannot be completed
        """
        if not self._validate_data(data):
            raise ValueError("Invalid data provided")
            
        try:
            result = await self._execute_action(data)
            self.logger.info(f"Action completed: {result}")
            return True
        except Exception as e:
            self.logger.error(f"Action failed: {e}")
            return False
```

🧪 Testing

Test Structure

· Place tests in tests/ directory

· Use test_ prefix for test files and functions

· Mock external dependencies

· Include both unit and integration tests

Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=tiktok_bot

# Run specific test module
pytest tests/test_browser_manager.py -v

# Run tests with specific marker
pytest -m "integration" --verbose
```

Writing Tests

```python
import pytest
from unittest.mock import AsyncMock, patch


class TestBrowserManager:
    """Test suite for BrowserManager functionality."""
    
    @pytest.mark.asyncio
    async def test_browser_creation(self):
        """Test successful browser instance creation."""
        manager = BrowserManager()
        browser = await manager.create_browser()
        
        assert browser is not None
        assert isinstance(browser, Browser)
        
    @pytest.mark.asyncio
    async def test_proxy_integration(self):
        """Test browser creation with proxy configuration."""
        with patch('security.proxy_rotator.ProxyRotator.get_proxy') as mock_proxy:
            mock_proxy.return_value = "http://proxy.example.com:8080"
            
            manager = BrowserManager()
            browser = await manager.create_browser()
            
            mock_proxy.assert_called_once()
```

# 📚 Documentation

Inline Documentation

· Document all public functions and classes

· Include type hints in all function signatures

· Provide examples for complex functionality

· Document exceptions that may be raised

External Documentation

· Update README.md for user-facing changes

· Add to docs/ directory for detailed explanations

· Include configuration examples

· Document security considerations

# 🔀 Pull Request Process

1. Pre-Submission Checklist

· Code follows project standards

· Tests pass locally

· Documentation updated

· Branch is up to date with main

· Commit messages follow conventions

2. PR Description Template

```markdown
## Description
Brief description of the changes

## Related Issues
Fixes #issue_number

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing Performed
- [ ] Unit tests added/updated
- [ ] Integration tests performed
- [ ] Manual testing completed

## Screenshots/Logs
If applicable, add screenshots or log outputs
```

3. Review Process

· Maintainers will review within 48 hours

· Address review comments promptly

· Request re-review when changes are made

· Squash commits before merging

# 🐛 Reporting Issues

Bug Reports

When reporting bugs, include:

· Detailed description of the issue

· Steps to reproduce

· Expected vs actual behavior

· Environment information

· Error logs or screenshots

Feature Requests

For new features, describe:

· Use case and motivation

· Proposed implementation approach

· Potential alternatives considered

· Impact on existing functionality

# 🏆 Recognition

All contributors will be:

· Listed in the CONTRIBUTORS.md file

· Credited in release notes

· Recognized for significant contributions

· Eligible for maintainer roles with consistent contributions

---

Thank you for contributing to ethical AI research and digital behavior analysis!

Last Updated: November 2025
