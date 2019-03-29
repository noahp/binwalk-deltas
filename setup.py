"""
Setup package.
"""
import io
import os
from setuptools import setup

# Get long description from readme
with io.open("README.md", "rt", encoding="utf8") as readmefile:
    readme = readmefile.read()

setup(
    name="binwalk-deltas",
    version="0.1.0",
    description="Parse binwalk output and print deltas",
    author="Noah Pendleton",
    author_email="2538614+noahp@users.noreply.github.com",
    url="https://github.com/noahp/binwalk-deltas",
    project_urls={
        "Code": "https://github.com/noahp/binwalk-deltas",
        "Issue tracker": "https://github.com/noahp/binwalk-deltas/issues",
    },
    long_description=readme,
    long_description_content_type="text/markdown",
    license="MIT",
    py_modules=["binwalk_deltas"],
    install_requires=["humanize"],
    entry_points={
        "console_scripts": [
            "binwalk-deltas=binwalk_deltas:main"
        ]
    },
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.6",
        "Operating System :: OS Independent",
    ]
)
