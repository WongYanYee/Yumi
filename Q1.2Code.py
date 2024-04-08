#imports modules
import requests
from bs4 import BeautifulSoup
import re

#searches specific pattern within the url
def extract_movie_id(url):
    match = re.search(r'gr(\d+)/', url)
    if match:
        group_id = match.group(1)
        return "gr" + group_id
    else:
        return None
        
#scrapes the introduction part of movies
def scrape_movie_intro(movie_url):
    if not movie_url.startswith('https://www.boxofficemojo.com/'):
        movie_url = 'https://www.boxofficemojo.com/' + movie_url
    response = requests.get(movie_url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        intro_section = soup.find('div', class_='a-section mojo-heading-summary') #searches 'div' element with the class 'a-section mojo-heading-summary'.
        if intro_section:
            intro_paragraph = intro_section.find('p', class_='a-size-medium')
            if intro_paragraph:
                return intro_paragraph.text.strip() #removes leading or trailing whitespace from the text.
        return None
    else:
        print(f"{movie_url}") 
        return None

#retrieves and extracts movie information from Box Office Mojo website for year 2023.
if __name__ == "__main__":
    url = f"https://www.boxofficemojo.com/year/world/2023/"
    response = requests.get(url) #sends a GET request to the specified url https://www.boxofficemojo.com/year/world/2023/.
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        tables = soup.find_all('table', class_='mojo-body-table') 
         if tables:
            movie_info = [] #stores the extracted information from the tables
            for table in tables:
                rows = table.find_all('tr')
                for row in rows:
                    columns = row.find_all('td')
                    if columns:
                        movie_name = columns[1].text.strip().replace("\t", ",")
                        movie_url = columns[1].find('a')['href']
                        movie_id = extract_movie_id(movie_url)
                        movie_intro = scrape_movie_intro(movie_url)
                        if movie_intro:
                            movie_info.append((movie_name, movie_id, movie_intro)) #collects the extracted information and stores them in the list 
                            
#writes the extracted movie information into a text file.
            with open("TopMoviesIntro.txt", "w", encoding="utf-8") as file:
                for movie in movie_info:
                    file.write(f"{movie[0]},{movie[1]},{movie[2]}\n") 
            print("TopMoviesIntro.txt") #prints 'TopMoviesIntro.txt', this file is successfully created.
