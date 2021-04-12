import io
from setuptools import find_packages, setup

setup(
    name='dataviz',
    version='2.0.0',
    description='Data visualisation tool to share your visual analysis on the Web',
    long_description=io.open("../README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author='Marco Romanelli',
    author_email="marco.romanelli@epfl.ch",
    license='MIT',
    url='https://github.com/News-Teller/media-laboratory',
    project_urls={
        "Issue Tracker": "https://github.com/News-Teller/media-laboratory/issues",
        "Source Code": "https://github.com/News-Teller/media-laboratory",
    },
    python_requires=">=2.7, !=3.0.*, !=3.1.*, !=3.2.*",
    packages=find_packages(exclude=["tests*"]),
    zip_safe=False
)
