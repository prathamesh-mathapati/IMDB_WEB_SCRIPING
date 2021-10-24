def group_by_year(mov):    #task 2
    di={}
    s=set()
    for i in mov:
        s.add(int(i['Year']))
    
    for j in s:
        l=[]
        for k in mov:
            if str(j)==k["Year"]:
                l.append(k)
        di[j]=l

    ff=open('group_by_year.json',"w")
    json.dump(di,ff,indent=4) 
    ff.close()
    return di
        
group_by_year(movie)