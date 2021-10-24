import json
f=open('task5.json','r')
a=json.load(f)
f.close()

genre={}
for i in a.values():
    for j in i['genre']:
        if j in  genre:
            genre[j]=genre[j]+1
        else:
            genre[j]=1
print(json.dumps(genre,indent=8))
sd=open("genre.json",'w')
json.dump(genre,sd,indent=8)
sd.close()