import requests
from bs4 import BeautifulSoup
import sys
from urllib.parse import urlparse, urljoin
import argparse
import logging
import time

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

# Parses command-line arguments to get the base URL.
def get_base_url():
    parser = argparse.ArgumentParser(description="Scrape links and form submissions from a given URL.")
    parser.add_argument("url", help="Base URL to scrape")
    parser.add_argument("--rate-limit", type=float, default=1.0,
                        help="Time in seconds to wait between requests (default: 1.0)")
    args = parser.parse_args()
    return args.url, args.rate_limit


# Fetches the content of a given URL and parses it with BeautifulSoup.
# Handles potential request errors.
def fetch_and_parse(url, rate_limit_sleep):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx or 5xx)
        return BeautifulSoup(response.text, 'html.parser')
    except requests.exceptions.RequestException as e:
        logging.error(f"Error accessing URL {url}: {e}")
        sys.exit(1)
    finally:
        time.sleep(rate_limit_sleep)


# Finds and processes all <a> tags on the page, adding valid URLs to collected_urls.
def collect_links(soup, base_url, base_domain, collected_urls, rate_limit_sleep):
    for a_tag in soup.find_all('a'):
        href = a_tag.get('href')

        if href:
            absolute_url = urljoin(base_url, href)
            parsed_absolute_url = urlparse(absolute_url)

            if parsed_absolute_url.netloc == base_domain and not parsed_absolute_url.fragment:
                collected_urls.add(absolute_url)
                logging.info(f"Collected (Link): {absolute_url}")


# Finds and processes all forms on the page, simulating submissions
# and collecting resulting URLs. Includes rate limiting.
def process_forms(soup, initial_page_url, base_domain, collected_urls, rate_limit_sleep):
    for form_tag in soup.find_all('form'):
        form_action = form_tag.get('action')
        form_method = form_tag.get('method', 'get').lower()
        full_form_action_url = urljoin(initial_page_url, form_action or initial_page_url)

        for select_tag in form_tag.find_all('select'):
            select_name = select_tag.get('name')

            if select_name:
                for option_tag in select_tag.find_all('option'):
                    option_value = option_tag.get('value')

                    if option_value is not None:
                        form_submission_data = {select_name: option_value}

                        try:
                            if form_method == 'post':
                                form_response = requests.post(full_form_action_url, data=form_submission_data)
                            else:  # Default to GET
                                form_response = requests.get(full_form_action_url, params=form_submission_data)

                            form_response.raise_for_status()

                            resulting_url = form_response.url
                            parsed_resulting_url = urlparse(resulting_url)

                            if parsed_resulting_url.netloc == base_domain and not parsed_resulting_url.fragment:
                                collected_urls.add(resulting_url)
                                logging.info(f"Collected (Form): {resulting_url}")
                            else:
                                logging.info(f"Skipped (Form, different domain or fragment): {resulting_url}")

                        except requests.exceptions.RequestException as e:
                            logging.error(f"Error submitting form for URL '{full_form_action_url}' with data '{form_submission_data}': {e}")
                        
                        # Apply rate limiting
                        time.sleep(rate_limit_sleep)

# Writes all unique collected URLs to a specified file.
def write_urls_to_file(collected_urls, output_filename='urls.txt'):
    with open(output_filename, 'w') as f:
        for url_to_write in sorted(list(collected_urls)):
            f.write(url_to_write + '\n')
    logging.info(f"\nAll unique URLs written to {output_filename}")
    logging.info(f"Total unique URLs collected: {len(collected_urls)}")

def main():
    base_url, rate_limit_sleep = get_base_url()

    parsed_base_url = urlparse(base_url)
    base_domain = parsed_base_url.netloc

    collected_urls = set()
    collected_urls.add(base_url)

    soup = fetch_and_parse(base_url, rate_limit_sleep)

    collect_links(soup, base_url, base_domain, collected_urls, rate_limit_sleep)
    process_forms(soup, base_url, base_domain, collected_urls, rate_limit_sleep)
    write_urls_to_file(collected_urls)

if __name__ == "__main__":
    main()
