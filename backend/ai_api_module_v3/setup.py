# setup.py
"""
AI API Module setup script
"""
from setuptools import setup, find_packages
from pathlib import Path

# Read README
long_description = (Path(__file__).parent / "README.md").read_text(encoding="utf-8")

# Read requirements
requirements = [
    "httpx>=0.24.0",
    "pydantic>=2.0.0", 
    "pyyaml>=6.0",
    "pillow>=9.0.0",
    "asyncio-throttle>=1.0.0",
    "tenacity>=8.0.0",
    "tiktoken>=0.4.0",
]

extras_require = {
    "openai": ["openai>=1.35.0"],
    "anthropic": ["anthropic>=0.31.0"],
    "google": ["google-genai>=0.6.0"],
    "xai": ["xai-sdk>=0.2.0"],
    "all": [
        "openai>=1.35.0",
        "anthropic>=0.31.0", 
        "google-genai>=0.6.0",
        "xai-sdk>=0.2.0"
    ],
    "dev": [
        "pytest>=7.0.0",
        "pytest-asyncio>=0.21.0",
        "pytest-mock>=3.10.0",
        "black>=23.0.0",
        "isort>=5.0.0",
        "mypy>=1.0.0",
        "coverage>=7.0.0"
    ]
}

setup(
    name="ai-api-module",
    version="0.1.0",
    author="AI Team",
    author_email="team@example.com",
    description="Unified interface for multiple AI providers",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/your-org/ai-api-module",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    python_requires=">=3.9",
    install_requires=requirements,
    extras_require=extras_require,
    include_package_data=True,
    package_data={
        "ai_api_module": ["models/*.yaml"]
    },
    entry_points={
        "console_scripts": [
            "ai-api-module=ai_api_module.cli:main",
        ],
    },
)