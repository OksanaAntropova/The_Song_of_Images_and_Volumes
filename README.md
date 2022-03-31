# The_Song_of_Images_and_Volumes
A homework for Quantori Data Engineering School 2022 on SQLAlchemy + Docker + Logging
It contains a tiny demo database of the gorgeous universe of "A Song of Ice and Fire" by George R.R. Martin.

Tested on Linux Mint 20 Cinnamon
### current state
Semi-working:
- for me it was impossible to create dev- and prod-containers both on one system without deleting the other one first. Each one works perfectly though.
### todo
- survive the coming winter a.k.a. "the test" =)
### development:
To deploy - from the root folder:
```Linux Kernel Module
docker-compose up -d --build
```
### production:
To deploy - from the root folder:
```Linux Kernel Module
docker-compose -f docker-compose.prod.yml up -d --build
```
### Work with the project:
Go inside my_python container's shell:
```Linux Kernel Module
docker exec -it my_python bash
```
Now you can work with the project:
#### To erase all the data and seed the db with test data:
```Linux Kernel Module
python admin.py
```
#### To add a new hero to the database:
```Linux Kernel Module
python user.py add_hero
```
#### To add a new motto to the database:
```Linux Kernel Module
python user.py add_motto
```
#### To add a new story to the database:
```Linux Kernel Module
python user.py add_story
```
#### To delete a hero from the database:
```Linux Kernel Module
python user.py delete_hero
```
#### To add a new combat to the database:
```Linux Kernel Module
python user.py add_combat
```
#### To print out the content of the database:
```Linux Kernel Module
python user.py print_db
```
### Switching off containers:
To switch all the containers off:
```Linux Kernel Module
docker stop $(docker ps -q)
```
