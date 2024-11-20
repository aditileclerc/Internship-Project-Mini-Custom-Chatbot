
#extract content from all links on a homepage and save to directory


import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def extract_links(homepage_html):
    soup = BeautifulSoup(homepage_html, 'html.parser')
    links = []
    for a_tag in soup.find_all('a', href=True):
        links.append(a_tag['href'])
    return links

def download_html(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        print(f"Failed to download {url}")
        return None

def save_html(content, filename, folder):
    if not os.path.exists(folder):
        os.makedirs(folder)
    file_path = os.path.join(folder, filename)
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)

def download_and_save_linked_pages(base_url, folder):
    homepage_html = download_html(base_url)
    if not homepage_html:
        return

    links = extract_links(homepage_html)
    print(f"Found {len(links)} links on the homepage.")

    for i, link in enumerate(links):
        full_url = urljoin(base_url, link)
        html_content = download_html(full_url)
        if html_content:
            filename = f"page_{i+1}.html"
            save_html(html_content, filename, folder)
            print(f"Saved {full_url} as {filename}")

if __name__ == "__main__":
    homepage_url = "https://gameofthrones.fandom.com/wiki/Wiki_of_Westeros"  # Replace with the actual homepage URL
    output_folder = r"E:\aditi works\purpleslate\udemy\chatbot\GoT"  # Folder to save the HTML files

    download_and_save_linked_pages(homepage_url, output_folder)
