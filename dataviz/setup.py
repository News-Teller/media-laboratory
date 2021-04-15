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
    license='GPLv3',
    url='https://github.com/News-Teller/media-laboratory',
    project_urls={
        "Issue Tracker": "https://github.com/News-Teller/media-laboratory/issues",
        "Source Code": "https://github.com/News-Teller/media-laboratory",
    },
    python_requires=">=2.7, !=3.0.*, !=3.1.*, !=3.2.*",
    packages=find_packages(exclude=["tests*"]),
    zip_safe=False,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Environment :: Web Environment',
        'Framework :: Dash',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Database :: Front-Ends',
        'Topic :: Office/Business :: Financial :: Spreadsheet',
        'Topic :: Scientific/Engineering :: Visualization',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Software Development :: Widget Sets'
    ],
    install_requires=[
        'dash>=1.15.0',
        'dill>=0.3.0',
        'pymongo'
    ],
)
