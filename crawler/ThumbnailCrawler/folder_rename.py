import os
 
def changeName(path, cName):
    i = 1
    for filename in os.listdir(path):
        os.rename(path+filename, path+str(cName)+str(i)+'.jpg')
        i += 1
 
cnt = 0
for id in os.listdir('KCeleb_raw'):
    os.rename('KCeleb_raw/'+id, 'KCeleb_raw/'+str(cnt))
    cnt+=1