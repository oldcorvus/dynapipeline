"""
Setup configuration for the dynapipeline package.
"""

from setuptools import find_packages, setup

setup(
    name="dynapipeline",
    version="0.1.0",
    description="A flexible, event-driven pipeline framework for data processing",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Moel",
    author_email="mohana.rj13@example.com",
    url="https://github.com/oldcorvus/dynapipeline",
    packages=find_packages(exclude=["tests", "examples", "docs"]),
    include_package_data=True,
    install_requires=[
        "pydantic>=1.8.2",
        "PyYAML>=5.3.1",
        "toml>=0.10.2",
        "pika>=1.2.0",
        "asyncio>=3.4.3",
    ],
    extras_require={
        "dev": ["pytest", "tox", "flake8"],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
)
