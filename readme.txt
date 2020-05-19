# Music System Application - Part 1

A microservice architecture based music system application.
Application uses 4 different microservices namely Users, Descriptions, Tracks, Playlists 
hosted as four separate applications connected to a single database.
Provides users with functionality to create music playlists. 

## Built With

1. [Python](https://www.python.org/)
2. [Flask API](https://www.flaskapi.org/)
3. [SQLite3](https://www.sqlite.org/index.html)

## Pre-requsites:

1. Editor (Visual Studio Code / Atom / other)
2. Python
3. Tuffix VM (Linux distribution such as Ubuntu or Fedora)
4. SQLite3

## Command Details  

###### Run project and activate all microsrvices:
    foreman start

###### Test all micro services:
    python3 app.py test
