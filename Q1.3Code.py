#imports necessary modules
import os
import requests
from bs4 import BeautifulSoup
import re

#extracts a movie's unique identifier from its url using general expression.
def extract_movie_id(url):
    match = re.search(r'gr(\d+)/', url)
    if match:
        group_id = match.group(1)
        return "gr" + group_id
    else:
        return None

#downloads and saves a movie's poster image from its url, and each movie identifier is its file name
def scrape_movie_image(movie_url, movie_id):
    if not movie_url.startswith('https://www.boxofficemojo.com/'):
        movie_url = 'https://www.boxofficemojo.com/' + movie_url
    response = requests.get(movie_url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        section_tags = soup.find_all('div', class_='a-section a-spacing-none mojo-posters')
        for section_tag in section_tags:
            img_tag = section_tag.find('img', alt=True)
            if img_tag and 'src' in img_tag.attrs:
                image_url = img_tag['src']
                response = requests.get(image_url)
                if response.status_code == 200:
                    with open(os.path.join("Images", f"{movie_id}.jpg"), 'wb') as file:
                        file.write(response.content)
                        print(f"{movie_id}.jpg")
                else:
                    print(f"{image_url}")
                return
    print(f"{movie_url}")

#scrapes and saves top50 movie posters 
if __name__ == "__main__":
    if not os.path.exists("Images"):
        os.makedirs("Images")
    url = f"https://www.boxofficemojo.com/year/world/2023/"
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        tables = soup.find_all('table', class_='mojo-body-table')
        if tables:
            count = 0
            for table in tables:
                rows = table.find_all('tr')
                for row in rows:
                    columns = row.find_all('td')
                    if columns:
                        count += 1
                        if count > 50:
                            break
                        movie_url = columns[1].find('a')['href']
                        movie_id = extract_movie_id(movie_url)
                        scrape_movie_image(movie_url, movie_id)
                      else:
            print() 
 
