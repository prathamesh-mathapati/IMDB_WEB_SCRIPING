import json,requests
from bs4 import BeautifulSoup



def print_movies(a,asd): #print list  of movie
    return a["Data"][asd]["Link"]

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
       
def cast(llls): # all cast details with imbd id
    
    res=requests.get(llls)
    soup=BeautifulSoup(res.text,"html.parser")
    l=soup.find("a",{"aria-label":"See full cast and crew"})["href"] # link of cast
    # print(l)
    global id
    id=l.split('/')[2]      #cast id 
    # print(id)


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
        


    return allcastlist,id

def scrape_movie_deatils(sds):  #scraping the details of given one movie
    dd={}
    so=requests.get(sds)
    soup=BeautifulSoup(so.text,'html.parser')
    
    # # for Title----------------------------------
    title=soup.find("div",class_="TitleBlock__TitleContainer-sc-1nlhx7j-1 jxsVNt")
    title=title.find("h1")
    dd["Name"]=title.text
    
    # print(title.text)
    
    # #for run time---------------------------
    tt=soup.find("ul",class_="ipc-inline-list ipc-inline-list--show-dividers TitleBlockMetaData__MetaDataList-sc-12ein40-0 dxizHm baseAlt")
    t=1
    for k in tt:
        if t==len(tt):
            ti=k.text
            total=int(ti[0])*60
            if len(ti)==2:
                # print(total,'min')
                pass
            else:
                total=total+int(ti[3:-3])
                # print(total,"min")
            break
        t+=1  
    dd["RunTime"]=total
    
    # # for list of dicrector--------------------------
    d=soup.find("li",class_="ipc-metadata-list__item")  
    d=d.find_all("li",class_="ipc-inline-list__item")
    ld=[]
    for i in d:
        sas=i.text
        ld.append(sas)
        # print(sas) 
    dd["Director"]=(ld)

    #for Bio data-----------
    bio=soup.find('div',class_="Hero__ContentContainer-kvkd64-10 eaUohq")
    bio=bio.find('span',class_="GenresAndPlot__TextContainerBreakpointXS_TO_M-cum89p-0 dcFkRD").get_text()
    # print(bio)
    dd['Bio']=bio
    
    #for genres----------------------------------
    gg=soup.find("div",class_="Storyline__StorylineWrapper-sc-1b58ttw-0 iywpty")
    gg=gg.find_all("a",class_="ipc-metadata-list-item__list-content-item ipc-metadata-list-item__list-content-item--link")
    
    # gg=gg.find_all("li",class_="ipc-inline-list__item")
    gl=[]
    for i in gg:
        ae=i.text
        if ae=="Add content advisory":
            continue
        else:
            # print(ae)
            gl.append(ae)
    dd["genre"]=(gl)
    
    #for country----------------------------
    both=soup.find('li',{"data-testid":"title-details-origin"}).a.get_text()
    # print(both)
    dd["country"]=both
    
    #for language-------------
    ll=[]
    oth=soup.find('li',{"data-testid":"title-details-languages"})
    oth=oth.find_all("li",class_="ipc-inline-list__item")
    for i in oth:
        # print(i.text)
        ll.append(i.text)
    dd["Language"]=(ll)
    
    # for poster-------------
    pp=soup.find("div",class_="AnswersCTA__AnswersCtaSection-sc-1ebj0gg-1 fajPuA").img["srcset"]
    asd=pp[:-5]
    # print(asd)
    dd["poster_image_url"]=asd
    
    # for cast
    dd["cast"],id=cast(sds)
    
    return dd
    
def alcast():       #create a file of all movies and all cast in movie 
    main=[]
    for i in range(10):
        try:
            file=open("topmovies.json",'r')    
            file.close()
        except:
            scrape_top_list()

        finally:
            file=open("topmovies.json",'r')    
            u=json.load(file)
            file.close()
            lin=print_movies(u,i)
        
            ca=scrape_movie_deatils(lin)
            main.append(ca)
    jj=open('castall.json',"w")   
    json.dump(main,jj,indent=4)
    jj.close()      
     
try:
    f=open('castall.json',"r")
    ay=json.load(f)
    f.close()
    
except:
    alcast()
    f=open('castall.json',"r")
    ay=json.load(f)
    f.close()

 
s=set()

for i  in ay:
    for j in i["cast"]:
        s.add(j["imbd_id"])
all={}
for j in s :
    for  l in ay:
        for j in l['cast']:
            if j["imbd_id"] in all:
                all[j['imbd_id']]=[]
          
j["name"]j["name"]
        
