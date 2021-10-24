def group_by_decade(l):
    did={}
    ss=set()
    for i in l:
        ss.add(i//10)
        
    for j in ss:
        ll=[]
        for k in l:
            if str(j) in str(k):
                for  a in l[k]:
                    ll.append(a)
                    
                
        did[f'{j}0']=ll
        
    ff=open('group_by_decede.json',"w")
    json.dump(did,ff,indent=4) 
    ff.close()    

group_by_decade(gby)