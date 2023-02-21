import flask
import flask_login
import sqlite3
import json
import os
import sys

def getDocker(serverType):
    with open('dockerlink.json') as json_data:
        d = json.load(json_data)
        container = d[serverType]
    # run docker pull in dockerFolder 
    os.chdir("dockerFolder")
    os.system('docker pull ' + container)
    os.chdir('..')
    return container

if __name__ == '__main__':
    container = getDocker("papermc")
    os.system('docker run -d -p 25565:25565 ' + container)