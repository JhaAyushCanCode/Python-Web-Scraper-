import requests
from bs4 import BeautifulSoup
from googlesearch import search
import pandas as pd

def fetch_search_results(query, num_results=10):
    """Fetch the top URLs from a Google search."""
    return list(search(query, num=num_results, stop=num_results))

def scrape_website(url, parameters):
    """Scrape the given website URL and extract relevant data based on user-defined parameters."""
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    data = {'URL': url}
    
    for param in parameters:
        param_lower = param.lower()
        extracted_value = 'N/A'

        if soup.find(string=lambda text: text and param_lower in text.lower()):
            extracted_value = soup.find(string=lambda text: text and param_lower in text.lower()).parent.text.strip()
        elif soup.find('meta', attrs={'name': param_lower}):
            extracted_value = soup.find('meta', attrs={'name': param_lower})['content']

        data[param] = extracted_value
    
    return data

def save_to_excel(data, filename):
    """Save the scraped data to an Excel file."""
    df = pd.DataFrame(data)
    df.to_excel(filename, index=False)

def main():
    search_query = input("Enter your search query (e.g., 'rent house 2bhk in delhi'): ")
    num_parameters = int(input("Enter the number of parameters you want to extract: "))
    parameters = [input(f"Enter parameter {i+1}: ") for i in range(num_parameters)]
    
    num_results = 10  # You can change this if needed

    # Fetch top URLs
    urls = fetch_search_results(search_query, num_results)
    
    # Scrape each URL and collect data
    scraped_data = []
    for url in urls:
        try:
            data = scrape_website(url, parameters)
            scraped_data.append(data)
        except Exception as e:
            print(f"Failed to scrape {url}: {e}")

    # Save data to an Excel file
    output_file = 'rental_data.xlsx'
    save_to_excel(scraped_data, output_file)
    print(f"Data saved to {output_file}")

if __name__ == "__main__":
    main()
