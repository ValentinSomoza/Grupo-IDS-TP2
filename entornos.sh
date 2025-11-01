#!bin/bash
mkdir WEP-HOSPEDAJES
cd WEP-HOSPEDAJES
mkdir Grupo-IDS-TP2
cd Grupo-IDS-TP2
mkdir Backend
mkdir Frontend
cd Backend
mkdir .venv
mkdir db    
touch app.py
cd ..
cd Frontend
mkdir .venv
mkdir static
mkdir templates
touch app.py
cd ..
cd ..
git clone https://github.com/ValentinSomoza/Grupo-IDS-TP2.git
cd Grupo-IDS-TP2
cd Backend
pipenv install flask
cd ..
cd Frontend
pipenv install flask
cd ..
