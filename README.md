# WARC Parser

A Python script to collect internal links and simulate form submissions from a given webpage, saving the collected URLs to a file named after the site.

# Installation

To install this script and its dependencies, clone the repository and use pip:
```
git clone https://github.com/Ojspain/warc-parser.git
cd warc-parser
python3 -m venv venv
source venv/bin/activate
pip install .
```
This will install the necessary Python packages and make the collect-urls command available in your terminal in the directory you installed it.

# Usage

Run the script from your terminal, providing the base URL you want to scrape:
```
collect-urls https://www.example.edu
```
You can also specify a custom rate limit (delay between requests) in seconds:
```
collect-urls https://www.example.edu --rate-limit 2.0
```
The collected URLs will be saved in a file named like {sitename}-urls.txt (e.g., www-example-edu-urls.txt) in the directory where you ran the command.
