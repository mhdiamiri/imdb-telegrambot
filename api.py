import json
import requests

BASE_URL = "http://www.omdbapi.com/"

API_KEY = ""

def search_name(name, page):
    url = BASE_URL + "?s={}&page={}&apikey={}".format(name, page, API_KEY)
    resp = requests.get(url)
    if resp.status_code == 200:
        data = json.loads(resp.text)
        if data["Response"] == "True":
            l = []
            movies = data["Search"]
            for movie in movies:
                l.append([movie["Title"], movie["imdbID"]])
            return l
        else:
            return None

def select_item(item):
    url = BASE_URL + "?i={}&apikey={}&plot=full".format(item, API_KEY)
    
    resp = requests.get(url)
    
    if resp.status_code == 200:
        data = json.loads(resp.text)
        if data['Response'] == "True":
            return data
    
    return None

def get_screenshots(item_id):
    links = []
    i = 1
    while True:
        link = f"http://moviesapi.ir/images/{item_id}_screenshot{i}.jpg"
        resp = requests.head(link)
        i += 1
        if resp.status_code != 200:
            break
        links.append(link)
    return links

def generate_message(item):
    if item["Poster"] != 'N/A': 
        poster_name = item["Poster"]
    else: 
        poster_name = None
        
    if item['Type'] == "Movie": 
        title = "Movie Name: "
        
    else: title = "Series Name: "
    
    message = ""
    
    if item["Title"] != 'N/A':       
        message += title + item["Title"]  + "\n\n"
    if item["Plot"] != "N/A":        
        message += "Plot: " + item["Plot"] + "\n\n"
    if item["Year"] != "N/A":        
        message += "Year: " + item["Year"] + "\n\n"
    if item["Rated"] != "N/A":       
        message += "Rated: " + item["Rated"] + "\n\n"
    if item["Runtime"] != "N/A":     
        message += "Runtime: " + item["Runtime"] + "\n\n"
    if item["Genre"] != "N/A":       
        message += "Genre: " + item["Genre"] + "\n\n"
    if item["Actors"] != "N/A":      
        message += "Actors: " + item["Actors"] + "\n\n"
    if item["Language"] != "N/A":    
        message += "Language: " + item["Language"] + "\n\n"
    if item["Country"] != "N/A":     
        message += "Country: " + item["Country"] + "\n\n"
    if item["Awards"] != "N/A":      
        message += "Awards: " + item["Awards"] + "\n\n"
    if item["imdbRating"] != "N/A":  
        message += "IMDB Rating: " + item["imdbRating"]
    
    if message != "": 
        return message, poster_name
    return None
