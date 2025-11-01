#!bin/bash

git clone https://github.com/ValentinSomoza/Grupo-IDS-TP2.git

cd Grupo-IDS-TP2
mkdir Backend
mkdir Frontend

cd Backend
mkdir .venv
mkdir db    
pipenv install flask
cd ..

cd Frontend
mkdir .venv
mkdir static
mkdir templates
pipenv install flask
cd ..

cd ..
echo ""
echo "Entornos creados correctamente"