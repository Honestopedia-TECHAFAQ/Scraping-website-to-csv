import requests
from bs4 import BeautifulSoup
import re

def fetch_webpage(url):
    """Fetch the content of the webpage."""
    try:
        response = requests.get(url)
        response.raise_for_status()  
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching the webpage: {e}")
        return None

def parse_html(html_content):
    """Parse the HTML content using BeautifulSoup."""
    return BeautifulSoup(html_content, 'html.parser')

def extract_numbers(soup):
    """Extract all numbers from the parsed HTML."""
    number_pattern = re.compile(r'\b\d{1,3}(?:,\d{3})*(?:\.\d+)?\b')
    text_content = soup.get_text()
    numbers = number_pattern.findall(text_content)
    return [num.replace(',', '') for num in numbers]  

def filter_numbers(numbers, min_value=None, max_value=None):
    """Filter numbers based on a minimum and/or maximum value."""
    filtered_numbers = []
    for number in numbers:
        try:
            value = float(number)
            if (min_value is None or value >= min_value) and (max_value is None or value <= max_value):
                filtered_numbers.append(value)
        except ValueError:
            continue 
    return filtered_numbers

def save_to_file(numbers, filename="numbers.txt"):
    """Save the numbers to a file."""
    with open(filename, 'w') as file:
        for number in numbers:
            file.write(f"{number}\n")
    print(f"Numbers saved to {filename}")

def scrape_numbers(url, min_value=None, max_value=None, save=False):
    """Main function to scrape numbers from a website."""
    html_content = fetch_webpage(url)
    if html_content:
        soup = parse_html(html_content)
        numbers = extract_numbers(soup)
        filtered_numbers = filter_numbers(numbers, min_value, max_value)
        
        if save:
            save_to_file(filtered_numbers)
        
        return filtered_numbers
if __name__ == "__main__":
    url = 'https://example.com'
    min_value = 100  
    max_value = 10000  
    scraped_numbers = scrape_numbers(url, min_value=min_value, max_value=max_value, save=True)
    print("Filtered Numbers:")
    for number in scraped_numbers:
        print(number)
