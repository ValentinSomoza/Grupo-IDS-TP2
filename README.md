# Sitio Web de Hopedajes

El proyecto consiste en la creación de una plataforma web que sirva para ver reseñas y solicitar reservas en un hotel. 

- La plataforma contará con una galería con fotos de las distintas habitaciones, un apartado de reseñas y opiniones. un apartado de contacto por temas de consultas.

- Una interfaz para hacer reservas indicando fechas y cantidad de personas.

- Ademas se contará con funcionalidades que permiten enviar toda la información por algún medio mail-whatsapp al usuario con los datos de la reserva (checkIN, checkOUT, importe a pagar, cant pax, y toda información extra de la reserva).

## Integrantes del grupo

- [Valentín Gabriel Somoza 109188](https://github.com/ValentinSomoza)
- [Juan Ignacio Sleiman Bonavia 114442](https://github.com/Juano1973)
- [Ronny Mamani Torrez 114779](https://github.com/MTRony)
- [Alvaro Ricardo Avalos Aguilar 114565](https://github.com/Alvaro17-max)

## Guia para el Proyecto Hospedaje (FLASK)

Para disponer del sitio web es necesario seguir con los siguientes pasos:

### 1. Crear la estructura de directorios y archivos

Se puede crear de forma manual o automática:

- **(Automática)** descargar y ejecutar el script [entornos.sh](/entornos.sh):

```bash
bash entornos.sh
```

- **(Manual)**


    - Para la descargar del contenido ubícate en el directorio, abre la **Terminal** y ejecuta el siguiente comando:

        ```bash
        git clone https://github.com/ValentinSomoza/Grupo-IDS-TP2.git 
        ```

    - Crear los siguientes directorios *.evenv* en la estrutura para el entorno virtual:

        - `/Grupo-IDS-TP2`

            - `/Backend`

                - [X] `/.evenv`
                - `/db`
                - `app.py`

            - `/Frontend`

                - [X] `/.evenv`
                - `/static`
                - `/templates`
                - `app.py`

    - Instalar flask en el entorno virtual (Backend y Frontend):

         ```bash
        pipenv install flask
        ```

### 2. Activación del entorno virtual

Esta acción se debe realizar tanto para el Backend y Fronted (**en diferentes terminales**)

```bash
pipenv shell
```

### 3. Instalación de dependecias

- **(Automática)** instalar todas las [dependencias](/dependencias.txt):

    ```bash
    pip install -r requerimientos.txt
    ```

- **(Manual)**

    - Backend
    
        ```bash
        apt sudo install Flask
        pip install Flask-Mail
        pip install python-dotenv
        ```

    - Frontend
        
        ```bash
        apt sudo install Flask
        pip install Flask-Mail
        pip install python-dotenv
        ```

### 4. Iniciar el servidor

Se dispone de dos opciones para utilizar (Backend y Frontend se inican de forma individual):

```bash
python3 app.py
```

```bash
export FLASK_APP=app.py
export FLASK_DEBUG=1
flask run
```

## Desactivar entorno virtual

```bash
deactivate
```








