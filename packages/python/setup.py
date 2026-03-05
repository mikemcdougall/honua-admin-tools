#!/usr/bin/env python3
"""Setup script for honua-admin package."""

from setuptools import setup, find_packages
import os

# Read the README file
here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, '..', '..', 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='honua-admin',
    version='1.0.0a1',
    description='Administrative tools and automation for Honua geospatial services',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Honua Project Contributors',
    author_email='info@honua.dev',
    url='https://github.com/mikemcdougall/honua-admin-tools',
    project_urls={
        'Bug Reports': 'https://github.com/mikemcdougall/honua-admin-tools/issues',
        'Source': 'https://github.com/mikemcdougall/honua-admin-tools',
        'Documentation': 'https://docs.honua.dev/admin-tools',
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Topic :: Scientific/Engineering :: GIS',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    keywords='geospatial gis admin automation devops postgis',
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    python_requires='>=3.9',
    install_requires=[
        'requests>=2.28.0',
        'pydantic>=2.0.0',
        'click>=8.0.0',
        'typing-extensions>=4.0.0',
    ],
    extras_require={
        'geospatial': [
            'geopandas>=0.13.0',
            'shapely>=2.0.0',
            'pyproj>=3.4.0',
        ],
        'dev': [
            'pytest>=7.0.0',
            'pytest-cov>=4.0.0',
            'pytest-asyncio>=0.21.0',
            'black>=23.0.0',
            'isort>=5.12.0',
            'flake8>=6.0.0',
            'mypy>=1.0.0',
            'pre-commit>=3.0.0',
        ],
        'docs': [
            'sphinx>=5.0.0',
            'sphinx-rtd-theme>=1.2.0',
            'sphinx-autodoc-typehints>=1.21.0',
        ],
    },
    entry_points={
        'console_scripts': [
            'honua-admin=honua_admin.cli:main',
        ],
    },
    include_package_data=True,
    zip_safe=False,
)