from typing import Text
import requests
import json
from bs4 import BeautifulSoup
url='https://www.imdb.com/india/top-rated-indian-movies/'
res=requests.get(url) 
soup = BeautifulSoup(res.text,"html.parser")


def scrape_top_list():    #task 1
    aa=soup.find("div",class_="lister")
    rr=aa.find("tbody",class_="lister-list")
    tr=rr.find_all("tr")
    allmovies={}
    # global movielist
    movielist=[]
    for i in tr:
        ddd=["Movie","Year","Position","Rating","Link"]
        detail=i.find("td",class_="titleColumn").text.strip().split("\n") #list of movie,year position
        detail.insert(1,(detail.pop(1)).strip())
        
        detail.insert(2,(detail.pop(2)).strip(')('))
        
        detail.insert(2,(detail.pop(0)).strip("."))
        
        detail.append(i.find("strong").string) # imbd rating
        
        detail.append('https://www.imdb.com'+str(i.find("td",class_="titleColumn").a['href'])) #for adding  link
        data=dict(zip(ddd,detail))
        
        movielist.append(data)
        

    allmovies.update({'Data':movielist})
    file=open("topmovies.json","w")
    json.dump(allmovies,file,indent=4)
    file.close()
    return movielist

movie=scrape_top_list()