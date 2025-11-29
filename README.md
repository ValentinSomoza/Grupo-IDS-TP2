# Sitio Web de Hopedajes

El proyecto consta de una pagina web y una aplicacion para el celular hecha con Kivy UI. La pagina web se conforma de un fronted y un backend.
Se utilizo el framework flask para front y back, un template con bootstrap, base de datos sql y autenticacion con Google.

Para correr la pagina web se puede hacer de 2 formas:

- Utilizar Docker
- Utilizar flask

Con Docker:
```bash
docker compose up --build
```
Con Flask:
```bash
cd Directorio
pipenv shell
flask run
```
Donde directorio es Frontend/ o Backend/.
Se recomienda primero inciar el servicio de sql, luego iniciar el Backend/ y por ultimo iniciar el /Frontend.
Para iniciar el servicio de sql en Linux se debe hacer:
```bash
sudo systemctl start mariadb
```
Para ejecutar la App Kivy se debe:
```bash
pipenv shell
python app.py
```
Para detener el servicio de mysql:
```bash
sudo systemctl stop mariadb
```
Para detener la ejecucion del Docker:
```bash
docker compose down
```
Todo se ejecutara en modo DEBUG de forma default.

Para poder correr el programa se debe completar 2 archivos .env que utilizan la libreria de python-dotenv
El primero debe estar dentro del Frontend:
```bash
CLIENT_ID="Credencial brindada por la api de Google, se lo tramita aqui: https://console.cloud.google.com/apis/credentials"
BACKEND_URL="URL elegido, por default es http://127.0.0.1:5000 o http://localhost:5000"
APP_SECRET_KEY="random"
CLIENT_SECRET="Credencial brindada por la api de Google, se lo tramita aqui: https://console.cloud.google.com/apis/credentials"
FRONTEND_URL="URL elegido arbitrariamente"
```
y el .env del Backend:
```bash
DB_HOST="por default es: localhost"
DB_USER="Usuario de mysql"
DB_PASS="contrasenia de mysql"
DB_NAME=HotelBruno
MAIL_USERNAME="Credencial de servicio de gmail se la tramita aqui: https://myaccount.google.com/security"
MAIL_PASSWORD="Credencial de gmail"
MAIL_DEFAULT_SENDER="Credencial de gmail"
CLIENT_ID="Credencial brindada por la api de Google, se lo tramita aqui: https://console.cloud.google.com/apis/credentials"
```
## Integrantes del grupo

- [Valentín Gabriel Somoza 109188](https://github.com/ValentinSomoza)
- [Juan Ignacio Sleiman Bonavia 114442](https://github.com/Juano1973)
- [Ronny Mamani Torrez 114779](https://github.com/MTRony)
- [Alvaro Ricardo Avalos Aguilar 114565](https://github.com/Alvaro17-max)