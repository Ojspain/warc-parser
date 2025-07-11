from setuptools import setup, find_packages

setup(
    name='warc-parser',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'requests>=2.25.1',
        'beautifulsoup4>=4.9.3',
    ],
    entry_points={
        'console_scripts': [
            'collect-urls = warc_parser:main',
        ],
    },
    author='Oliver Spain',
    author_email='oliverjspain@gmail.com',
    description='A script to collect links and form submission URLs from a webpage.',
    long_description='A script that scrapes a given URL for internal links and simulates form submissions to collect resulting URLs.',
    long_description_content_type='text/plain',
    url='https://github.com/Ojspain/warc-parser',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)

