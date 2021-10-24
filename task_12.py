import json,requests
from bs4 import BeautifulSoup


def print_movies(a):  #print all  movies  from topmovies,json
    a=a["Data"]
    for i in a:
        print(i["Position"],i['Movie'])
    mov=int(input('enter the movie no. :  ')) #enter movie to get link
    return a[mov-1]["Link"]    #get link

def scrape_top_list():       #all movies come and topmovies.json file create

    url='https://www.imdb.com/india/top-rated-indian-movies/'
    res=requests.get(url) 
    soup = BeautifulSoup(res.text,"html.parser")

    aa=soup.find("div",class_="lister")
    rr=aa.find("tbody",class_="lister-list")
    tr=rr.find_all("tr")
    allmovies={}
    global movielist
    movielist=[]
    for i in tr:
        ddd=["Movie","Year","Position","Rating","Link"]
        detail=i.find("td",class_="titleColumn").text.strip().split("\n") #list of movie,year position
        detail.insert(1,(detail.pop(1)).strip())
        
        detail.insert(2,int((detail.pop(2)).strip(')(')))
        
        detail.insert(2,(detail.pop(0)).strip("."))
        
        detail.append(float(i.find("strong").string) )# imbd rating
        
        detail.append('https://www.imdb.com'+str(i.find("td",class_="titleColumn").a['href'])) #for adding  link
        data=dict(zip(ddd,detail))
        
        movielist.append(data)
    
    allmovies["Data"]=movielist
    
    f=open("topmovies.json","w") #JSON file created
    json.dump(allmovies,f,indent=4)
    f.close()


try:
    file=open("topmovies.json",'r')    
    file.close()
except:
    scrape_top_list()

finally:
    file=open("topmovies.json",'r')    
    u=json.load(file)
    file.close()
    lin=print_movies(u)
    
    
    
    

    
res=requests.get(lin)
soup=BeautifulSoup(res.text,"html.parser")
l=soup.find("a",{"aria-label":"See full cast and crew"})["href"] # link of cast
# print(l)
id=l.split('/')[2]      #cast id 
# print(id)

try:
    f=open(f'{id}.json','r')
    print(f.read())
    f.close()
except:
    
    url1=f"https://www.imdb.com{l}"
    er=requests.get(url1)

    soup1=BeautifulSoup(er.text,"html.parser")
    liss=soup1.find('table',class_="cast_list")
    adl=liss.find_all('tr',class_="odd")
    evl=liss.find_all('tr',class_="even")
    com=adl+evl
    allcastlist=[]
    for i in com:
        cast={}
        # print(i.find_all('a'))
        ida=i.find_all("a")[1]["href"].split("/")[2]
        name=i.find_all('a')[1].text.strip()
        cast['imbd_id']=ida
        cast['name']=name
        allcastlist.append(cast)
        

    file=open(f'{id}.json','w')
    json.dump(allcastlist,file,indent=4)
    file.close()
    
    print(json.dumps(allcastlist,indent=4))