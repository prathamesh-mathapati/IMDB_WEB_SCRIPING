import json,requests
from bs4 import BeautifulSoup

try:
    file=open("topmovies.json",'r')    
    # u=json.load(file)
    file.close()
except:
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
    
finally:
    file=open("topmovies.json",'r')    
    u=json.load(file)
    file.close()




def get_movie_list_details(): # creat a json file in which detail off all movies are store 
    data={}
    c=1
    for i in u['Data']:
        dd={}
        
        print(c)
        so=requests.get(i["Link"])
        soup=BeautifulSoup(so.text,'html.parser')
        
        # # for Title----------------------------------
        title=soup.find("div",class_="TitleBlock__TitleContainer-sc-1nlhx7j-1 jxsVNt")
        title=title.find("h1")
        dd["Name"]=title.text
        
        
        #for run time---------------------------
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
        data[c]=dd
        
        c+=1  
        print()
        print(json.dumps(data,indent=4))
    
    
    file=open("task5.json",'w')
    json.dump(data,file,indent=4)
    file.close()
    return dd
    
get_movie_list_details()