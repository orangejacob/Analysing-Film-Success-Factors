
import numpy as np
import pandas as pd
import warnings
import json
import csv
import requests


def get_movie_list(api_key):
    
    # Get Top 10000 ->  Movie in terms of revenue - Movie Details + Casting Detail through TMDB API
    # Each page -> 20 Movie
    for page_no in range(1, 2):
        page_url = "https://api.themoviedb.org/3/discover/movie?api_key={key}&language=en-US&sort_by=revenue.desc&include_adult=false&include_video=false&page={page}".format(page = page_no, key = api_key)
        page_result = requests.get(page_url)
        if(page_result.status_code == 200):
            page_result = json.loads(page_result.content)['results']
            movie_list = []
            for movie in page_result:
                # Extract Casting Information for the movie
                movie_url = "https://api.themoviedb.org/3/movie/{mov_id}?api_key={key}".format(mov_id = movie['id'], key = api_key)
                credit_url = "https://api.themoviedb.org/3/movie/{mov_id}/credits?api_key={key}&language=en-US".format(mov_id = movie['id'], key = api_key)
                movie_json = requests.get(movie_url)
                credit_json = requests.get(credit_url)
                if(credit_json.status_code == 200 and movie_json.status_code == 200):
                    movie_detail = json.loads(movie_json.content)                    
                    casting = []
                    credit_detail = json.loads(credit_json.content)
                    
                    # Get Top 10 Casting from the movie.
                    cast_size = 9 if len(credit_detail['cast']) > 9 else len(credit_detail['cast'])
                    for i in credit_detail['cast'][:cast_size]:
                        casting.append(i['name'])
                    movie_detail['cast'] = casting
                    
                    #Get Director
                    movie_detail['director'] = next((crew['name'] for crew in credit_detail['crew'] 
                    if crew['job'] == 'Director'),None)
                    
                    movie_list.append(movie_detail)
                    
            df = pd.DataFrame.from_dict(movie_list)
            df.to_csv('movie_data_new.csv', mode = 'a', header = False)
            
    
    return "Success"


# Map day_of_week
def return_month(x):

    if x == 1.0:
        return "Jan"
    
    if x == 2.0:
        return "Feb"
            
    if x == 3.0:
        return "Mar"
    
    if x == 4.0:
        return "Apr"
        
    if x == 5.0:
        return "May"
        
    if x == 6.0:
        return "Jun"
    
    if x == 7.0:
        return "Jul"
    
    if x == 8.0:
        return "Aug"
            
    if x == 9.0:
        return "Sep"
    
    if x == 10.0:
        return "Oct"
        
    if x == 11.0:
        return "Nov"
        
    if x == 12.0:
        return "Dec"
    
    return ''


def return_day(x):
#    print(x)
    if x == 0.0:
        return "Mon"

    if x == 1.0:
        return "Tue"
    
    if x == 2.0:
        return "Wed"
            
    if x == 3.0:
        return "Thu"
    
    if x == 4.0:
        return "Fri"
        
    if x == 5.0:
        return "Sat"
        
    if x == 6.0:
        return "Sun"
        
    return ''
