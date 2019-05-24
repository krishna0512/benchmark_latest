import requests
import os
import json
import time

os.chdir('images')
for i in range(1,20):
    username = 'admin'
    userapikey = 'u1234'
    get_url = 'http://preon.iiit.ac.in:8100/api/dataset_image/'+str(i)+'/?username='+username+'&api_key='+userapikey
    r = requests.get(get_url)
    imageloc = 'http://127.0.0.1:8100'+r.json()['image']
    os.system('wget -q '+imageloc)
    print('Downloaded the Image from server')


    # this is to simulate the process of the calculating result.
    time.sleep(1)



    url = 'http://preon.iiit.ac.in:8100/api/submission/?username='+username+'&api_key='+userapikey
    data = {
        'title':'sample',
        'description':'sample submission for demo',
        'authors':'krishna',
        'result':'50,4,2,56,4,52,5,4\n5,54,2,54,52,\n5,2,65,15,4,64,64\n6,468,46,46846\n8,468,46,4,3,8\n40,64,06,406,406,4\n06,406,46,84,646,4',
        'did':1
    }
    headers = {'Content-type':'application/json'}
    r = requests.post(url,json.dumps(data), headers=headers)
    print('Submission saved successfully')
r = requests.get('http://preon.iiit.ac.in:8100/benchmark/confirm/')
print('saved and confirmed the submission in benchmark portal')
os.system('rm *')
os.chdir('..')
