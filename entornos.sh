#!bin/bash
mkdir WEP-HOSPEDAJES
cd WEP-HOSPEDAJES
mkdir GRUPO-IDS-TP2
cd GRUPO-IDS-TP2
mkdir BACKEND
mkdir FRONTEND
cd BACKEND
mkdir .venv
mkdir db    
touch app.py
cd ..
cd FRONTEND
mkdir .venv
mkdir static
mkdir templates
touch app.py
cd ..
cd ..
git clone https://github.com/ValentinSomoza/Grupo-IDS-TP2.git
cd Grupo-IDS-TP2
cd BACKEND
pipenv install flask
cd ..
cd FRONTEND
pipenv install flask
cd ..
