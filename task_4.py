import json,requests
from bs4 import BeautifulSoup
file=open("topmovies.json",'r')    
u=json.load(file)
c=1
data={}
Data=u['Data']

def print_movies(a):
    for i in a:
        print(i["Position"],i['Movie'])
    mov=int(input('enter the movie no. :  '))
    return a[mov-1]["Link"]
aw=print_movies(Data)
print(aw)



def scrape_movie_deatils(sds):
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
    
      
    print()
    print(json.dumps(dd,indent=4))

scrape_movie_deatils(aw)