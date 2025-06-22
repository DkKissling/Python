## Blog en Flask Dockerizado ##

*Bienvenidos a nuestro Blog de Flask*

En este repositorio de GitHub les presentamos a *InstaPosts*. Un Vlog interactivo, el cuál dispone de las siguientes características y funcionalidades:

1. *Frontend*: Desarrollado en HTML y CSS. Lo que permite correrlo en el navegador predeterminado de cada usuario.
2. *Backend*: Desarrollado con Python (Flask). 
3. Autenticación de usuario (registro y logeo).
4. Encriptado de contraseñas mediante la función SHA256.
5. Creación de Posteos, comentarios, borrado de publicaciones y obtención de categorías disponibles.

En paralelo, también cuenta con una API, mediante el uso de la clase MethodView y endpoints, para poder realizar funcionalidades CRUD (create, read, update and delete). Como también el Logeo típico de una aplicación. 

### Requisitos Previos ###

- Docker
- Docker Compose
- Python
- Git
- Pip (Administrador de paquetes de Python)

**Pasos a seguir para poder correr este proyecto en tu computadora**:

1. **Cloná el repositorio en tu máquina local**

`git clone git@github.com:juantobares4/docker_vlog.git` (usando SSH) |`git clone https://github.com/juantobares4/docker_vlog.git` (usando HTTPS)

2. **Entrá a la carpeta clonada**:

`cd docker_vlog`

3. **Creá el archivo .env**

Es necesario seguir el modelo del archivo *.env.example* por lo que vas a tener que copiarlo y modificarle el nombre a ".env"

4. **Configurá las variables de entorno**

Modificá las siguientes variables:

- `MYSQL_PASSWORD=contraseña`
- `MYSQL_DATABASE=nombre_base_datos`
- `MYSQL_USER=usuario`
- `MYSQL_CONTAINER_NAME=nombre_contenedor`

- `SECRET_KEY = secret-key-ejemplo`

5. **Configurá la base de datos**:

Entrá a la carpeta `/init` y luego en el archivo `create_schema.sql`. Y modificá las siguiente lineas (**sin comillas**):

`CREATE DATABASE "nombre_data_base";`

`USE "nombre_data_base";`

**Es importante que en el nombre de la base de datos uses el mismo que colocaste anteriormente en la variable *MYSQL_DATABASE* del archivo .env**

6. **Modificá el archivo Dockerfile**

En las lineas:

`COPY . /docker_vlog`
`WORKDIR /docker_vlog`

Modificá según el directorio que vas a copiar y en el cuál vas a trabajar.

7. **Construí la imágen de Docker**:

Corré el comando `sudo docker compose build` para contruir la imágen que posteriormente usará el contendor para poder correr **(Si no te funciona ese comando, probá con agregarle un guión medio de la siguiente forma: `sudo docker-compose build`)**

8. **Corré el contenedor**:

A partir de la imágen construida anteriormente, corré el comando `sudo docker compose up`.

9. **Accede a la página**:

Después de unos segundos (y un largo suceso de mensajes), debería correr el contenedor correctamente. Por lo que en una de las últimas líneas debería aparecerte un mensaje como este `Listening at: http://0.0.0.0:5005`. Apretando en esa dirección deberías poder acceder a la interfaz principal (manteniendo el `CTRL + click`).

**¡Y con esto, ya estaría todo listo para poder empezar a vlogear!**

### Contribuciones ###

- Los usuarios que realizaron este código fueron juantobares4, Dkkisslingtt y emanuel079.

**¡Esperamos que disfrutes utilizando esta aplicación para crear tu vlog y gestionar tu contenido de video de manera eficiente!**

