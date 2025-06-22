from datetime import datetime, timedelta

from flask import (
    jsonify,
    render_template,
    request,
    redirect,
    url_for,
    session,
)

from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity, get_jwt

from sqlalchemy import or_

from werkzeug.security import generate_password_hash, check_password_hash

from app import app, db, jwt

# --- Importación de modelos de las migraciones de la base de datos --- #

from app.models.models import Usuario, Categoria, Comentario, Entrada

from app.schemas.schema import CategorySchema, PostSchema, CommentSchema, UserSchema


from flask.views import MethodView


def allData():
    data = {
        "posts": Entrada.query.all(),
        "users": Usuario.query.all(),
        "comments": Comentario.query.all(),
        "categories": Categoria.query.all(),
    }
    return data


@app.context_processor
def listCategories():
    categories = Categoria.query.all()
    return dict(categories=categories)


@app.route("/")
def secIndex():
    return render_template(
        "index.html",
    )


@app.route("/inicio")  # Nombre del archivo HTML
def secInicio():  # Nombre de la función que nos va retornar una página HTML
    return render_template(
        "index.html",
    )


@app.route("/signUp")
def secRegister():
    return render_template(
        "signUp.html",
    )


@app.route("/logIn")
def secLogIn():
    return render_template(
        "logIn.html",
    )


@app.route("/btn_register")
def btnRegister():
    return render_template("signUp.html")


@app.route("/logoPostLogIn")
def clickOnLogo():
    data = allData()
    return render_template("inicio.html", data=data)


@app.route("/register_user", methods=["POST"])
def registerUserOnDb():
    usuarioForm = request.form["nameUser"]
    passwordForm = request.form["passwordUser"]
    correoElectronicoForm = request.form["emailUser"]

    passwordHash = generate_password_hash(passwordForm, method="pbkdf2", salt_length=16)

    newUser = Usuario(
        nombreUsuario=usuarioForm, contrasenia=passwordHash, correoElectronico=correoElectronicoForm
    )

    db.session.add(newUser)
    db.session.commit()

    return render_template(
        "index.html",
    )


@app.route("/userLogIn", methods=["POST"])
def logUser():
    usernameLogIn = request.form["nameUserLogin"]
    passwordLogIn = request.form["passwordUserLogin"]

    user = Usuario.query.filter_by(
        nombreUsuario=usernameLogIn
    ).first()  # La función .first() obtiene el primer resultado que cumpla con los criterios especificados.
    # Retorna una lista si encuentra el usuario filtrado por nombre de usuario. En caso de no encontrarlo, devuelve "None".

    if user and check_password_hash(user.contrasenia, passwordLogIn):
        access_token = create_access_token(
            identity=user.nombreUsuario,
            expires_delta=timedelta(seconds=30),
            additional_claims={"userID": user.idUsuario},
        )

        session["userID"] = user.idUsuario

        print(access_token)
        return redirect(url_for("secInicioPostLogin"))

    return render_template("logIn.html")  # render_template recibe archivos HTML como parámetros.


@app.route("/inicioPostLogin")
def secInicioPostLogin():
    data = allData()
    if "userID" in session:
        return render_template("inicio.html", data=data)

    else:
        return redirect(url_for("secLogIn"))


@app.route("/secCreatePost")
def secCreatePost():
    return render_template("createPost.html")


@app.route("/createPost", methods=["POST"])
def createPostOnDb():
    data = allData()
    titlePost = request.form["titlePost"]
    idAuthorPost = session["userID"]
    datePost = datetime.now()
    categoryPost = request.form["categorySelector"]
    commentPost = request.form["commentPost"]

    newPost = Entrada(
        titulo=titlePost,
        autorEntrada=idAuthorPost,
        fechaEntrada=datePost,
        idCategoriaEntrada=categoryPost,
        contenido=commentPost,
    )

    db.session.add(newPost)
    db.session.commit()

    return render_template(
        "createPost.html",
    )


@app.route("/del_post/<int:postId>", methods=["POST"])
def deletePost(postId):
    post = Entrada.query.get(postId)
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for("secInicioPostLogin"))


@app.route("/submitCommentOnDb/<int:postId>", methods=["POST"])
def submitCommentDb(postId):
    data = allData()
    commentPost = request.form["comment"]
    dateComment = datetime.now()
    authorId = session["userID"]
    idCommentPost = postId

    newComment = Comentario(
        textoComentario=commentPost,
        fechaComentario=dateComment,
        autorComentario=authorId,
        idEntradaComentario=idCommentPost,
    )

    db.session.add(newComment)
    db.session.commit()

    return render_template("inicio.html", data=data)


# --- Rutas para Schemas --- #


class LoginApi(MethodView):
    def post(self):
        dataLogin = request.get_json()
        usernameJson = dataLogin.get("username")
        passwordJson = dataLogin.get("password")

        user = Usuario.query.filter_by(nombreUsuario=usernameJson).first()

        if user and check_password_hash(user.contrasenia, passwordJson):
            accessToken = create_access_token(
                identity=user.idUsuario,
                expires_delta=timedelta(seconds=120),
                additional_claims={"userID": user.idUsuario},
            )

            session["userID"] = user.idUsuario

            return {"Datos correctos": "Usuario logeado", "Token de acceso": accessToken}, 202

        else:
            return jsonify(Mensaje=f"Los datos de logeo son incorrectos. Intente de nuevo."), 400


app.add_url_rule("/loginApi", view_func=LoginApi.as_view("login"))

# --- MethodView para Usuarios --- #


class UserApi(MethodView):
    # --- Get trae usuarios por ID o sin ID --- #
    def get(self, userId=None):
        if userId is None:
            users = Usuario.query.all()

            if len(users) == 0:
                return jsonify(Mensaje=f"La lista de usuarios está vacía."), 404

            schemaUsers = UserSchema().dump(users, many=True)

            if len(users) > 0:
                newSchemaUsers = []
                for user in schemaUsers:
                    newSchemaUser = {
                        "Nombre": user["nombreUsuario"],
                        "Correo Electrónico": user["correoElectronico"],
                        "Contraseña": user["contrasenia"],
                        "Posteos": user["posteosUsuario"],
                    }

                    newSchemaUsers.append(newSchemaUser)

                return jsonify(newSchemaUsers), 200

        # --- Si userId tiene un valor ejecuta el siguiente if. --- #
        if userId is not None:
            user = Usuario.query.get(userId)

            # --- Si el ID existe en la DB, entra en el primer if. --- #
            if user is not None:
                schemaUser = UserSchema().dump(user)
                return jsonify(Mensaje=f"Usuario con ID {userId}: {schemaUser}"), 200

            # --- Si el ID no está en la DB, entra en el else. --- #
            else:
                return jsonify(Mensaje=f"El usuario con ID {userId} no existe."), 404

    # --- Post crea un nuevo usuario --- #
    def post(self):
        data = request.get_json()
        username = data.get("username")
        email = data.get("email")
        password = data.get("password")

        dataUser = Usuario.query.filter(
            or_(Usuario.nombreUsuario == username, Usuario.correoElectronico == email)
        ).first()  # Si cumple una condición o la otra, retorna una lista con los datos del usuario filtrado.
        # Si no cumple con ninguna condición retorna 'None' por lo que accede a crear el nuevo usuario.

        if dataUser is None:
            passwordHash = generate_password_hash(password, method="pbkdf2", salt_length=16)

            newUser = Usuario(
                nombreUsuario=username,
                correoElectronico=email,
                contrasenia=passwordHash,
            )

            dataNewUser = {
                "Username": newUser.nombreUsuario,
                "Email": newUser.correoElectronico,
                "Password": newUser.contrasenia,
            }

            db.session.add(newUser)
            db.session.commit()

            return (
                jsonify(Mensaje=f"Se creó con éxito el usuario: {dataNewUser}"),
                201,
            )  # Código de error (En este caso: La entidad ha sido creada correctamente.)

        return (
            jsonify(
                Mensaje=f"El usuario {username} con el correo electrónico {email} ya existe. Introduce los datos nuevamente."
            ),
            404,
        )  # Código de error (En este caso: El recurso solicitado no se encontró.)

    # --- Put modifica datos de usuarios por ID --- #
    def put(self, userId=None):
        if userId is not None:
            user = Usuario.query.get(userId)

            if user is not None:
                oldData = user.nombreUsuario
                dataUser = request.get_json()  # Trae los datos del JSON.
                newData = dataUser.get("username")  # Trae la clave llamada "username" del JSON.

                filterDataUser = Usuario.query.filter(
                    Usuario.nombreUsuario == newData
                ).first()  # Filtro para no poner un nombre de usuario repetido.

                if filterDataUser is None:
                    user.nombreUsuario = newData  # Reemplaza el nombre de usuario antiguo de la clase "Usuario" por el nuevo nombre.
                    db.session.commit()

                    return jsonify(Mensaje=f"Dato anterior: {oldData} | Nuevo dato: {newData}"), 200

                return (
                    jsonify(
                        Mensaje=f"El usuario {newData} ya existe. Introduce un nombre de usuario distinto."
                    ),
                    400,
                )

            if user is None:
                return jsonify(Mensaje=f"El usuario con ID {userId} no existe."), 404

        if userId is None:
            return (
                jsonify(
                    Mensaje=f"Error: El ID {userId} no es válido. Proporciona un ID para continuar."
                ),
                400,
            )

    # --- Delete borra usuarios por ID --- #
    def delete(self, userId):
        user = Usuario.query.get(userId)

        if user is not None:
            db.session.delete(user)
            db.session.commit()
            return (
                jsonify(
                    Mensaje=f"El usuario {user.nombreUsuario} con ID {userId} fue borrado con éxito."
                ),
                200,
            )  # Código de error (En este caso: la solicitud se empleó con éxito y procede a mostrar el contenido solicitado en la respuesta.)

        if user is None:
            return jsonify(Mensaje=f"El usuario con ID {userId} no se encontró."), 404


# URL para poder acceder a la clase por medio de ThunderClient/Postman o navegador.
app.add_url_rule("/user", view_func=UserApi.as_view("user"))
app.add_url_rule("/user/<userId>", view_func=UserApi.as_view("userById"))

# --- MethodView para posteos --- #


class PostApi(MethodView):
    # --- Get trae posteos por ID o sin ID --- #
    def get(self, postId=None):
        if postId is None:
            posts = Entrada.query.all()

            if len(posts) == 0:
                return jsonify(Mensaje=f"La lista de posteos está vacía."), 404

            if len(posts) > 0:
                schemaPosts = PostSchema().dump(posts, many=True)

                newSchemaPosts = []
                for post in schemaPosts:
                    newSchemaPost = {
                        "Título": post["titulo"],
                        "Autor": post["autorEntrada"],
                        "Contenido": post["contenido"],
                        "Fecha": post["fechaEntrada"],
                        "Categoría": post["idCategoriaEntrada"],
                        "Comentarios": post["comentarios"],
                    }

                    newSchemaPosts.append(newSchemaPost)

                return jsonify(newSchemaPosts), 200

        # --- Si postId tiene un valor ejecuta el siguiente if. --- #
        if postId is not None:
            post = Entrada.query.get(postId)

            # --- Si el ID existe en la DB, entra en el primer if. --- #
            if post is not None:
                schemaPost = PostSchema().dump(post)
                return jsonify(schemaPost), 200

            # --- Si el ID no está en la DB, entra en el else. --- #
            else:
                return jsonify(Mensaje=f"El posteo con ID {postId} no existe."), 404

    # --- Post crea un nuevo posteo en la DB. --- #
    def post(self):
        dataPost = request.get_json()
        title = dataPost.get("title")
        idAuthor = session["userID"]
        datePost = datetime.now()
        content = dataPost.get("content")
        idCategory = dataPost.get("idCategoria")

        newPost = Entrada(
            titulo=title,
            autorEntrada=idAuthor,
            fechaEntrada=datePost,
            idCategoriaEntrada=idCategory,
            contenido=content,
        )

        dataNewPost = {
            "Título del posteo": newPost.titulo,
            "Autor": newPost.autorEntrada,
            "Fecha de publicación": newPost.fechaEntrada,
            "Contenido": newPost.contenido,
            "Categoría": newPost.idCategoriaEntrada,
        }

        db.session.add(newPost)
        db.session.commit()

        return (
            jsonify(Mensaje=f"Se creó con éxito la publicación: {dataNewPost}"),
            201,
        )  # Código de error (En este caso: La entidad ha sido creada correctamente.)

    # --- Put modifica posteos por ID en la DB. --- #
    def put(self, postId=None):
        if postId is not None:
            post = Entrada.query.get(postId)

            if post is not None:
                oldData = (
                    post.contenido
                )  # Trae la anterior información ya que está antes del commit a la DB.
                dataPost = request.get_json()  # Trae los datos del JSON.
                newContent = dataPost.get("content")  # Trae la clave llamada "contenido" del JSON.

                post.contenido = newContent  # Reemplaza el contenido antiguo de la clase "Entrada" por el nuevo contenido.
                db.session.commit()

                newDataPost = (
                    post.contenido
                )  # Trae la nueva información ya que está después del commit a la DB.

                return (
                    jsonify(
                        Mensaje=f"Anterior contenido: {oldData} | Nuevo contenido: {newDataPost}"
                    ),
                    200,
                )

            if post is None:
                return jsonify(Mensaje=f"El posteo con ID {postId} no existe."), 404

        if postId is None:
            return (
                jsonify(Mensaje=f"¡Tenés que especificar el ID del posteo que querés modificar!"),
                400,
            )

    # --- Delete borra posteos por ID en la DB. --- #
    def delete(self, postId):
        post = Entrada.query.get(postId)

        if post is not None:
            db.session.delete(post)
            db.session.commit()
            return (
                jsonify(
                    Mensaje=f"El posteo que se titula '{post.titulo}' con ID {post.idEntrada} fue borrado con éxito."
                ),
                200,
            )

        if post is None:
            return jsonify(Mensaje=f"El posteo que intentabas borrar no existe."), 404


app.add_url_rule("/post", view_func=PostApi.as_view("post"))
app.add_url_rule("/post/<postId>", view_func=PostApi.as_view("postById"))

# --- MethodView para comentarios --- #


class CommentApi(MethodView):
    def get(self, id=None):
        if id is None:
            comments = Comentario.query.all()

            if len(comments) == 0:
                return jsonify(Mensaje=f"La lista de comentarios está vacía."), 404

            if len(comments) > 0:
                schemaComments = CommentSchema().dump(comments, many=True)

                newSchemaComments = []
                for comment in schemaComments:
                    newSchemaComment = {
                        "Texto": comment["textoComentario"],
                        "Fecha de publicación": comment["fechaComentario"],
                        "Autor": comment["autorComentario"],
                        "Publicación": comment["idEntradaComentario"],
                    }

                    newSchemaComments.append(newSchemaComment)

                return jsonify(newSchemaComments), 200

        if id is not None:
            comment = Comentario.query.get(id)

            if comment is not None:
                schemaComment = CommentSchema().dump(comment)
                return jsonify(schemaComment), 200

            if comment is None:
                return jsonify(Mensaje=f"El comentario con ID {id} no existe.")

    def post(
        self, id=None
    ):  # El usuario pasa como parámetro el ID del posteo al cuál quiere comentar.
        if id is not None:
            post = Entrada.query.get(id)

            if post is None:
                return jsonify(Mensaje=f"El posteo que estás intentando comentar no existe."), 404

            else:
                commentData = request.get_json()
                commentDate = datetime.now()
                author = session["userID"]
                newCommentOnPost = commentData.get("comment")
                commentPostId = id  # Le asigno la clave foránea al comentario (es decir, el ID de la publicación a la cuál pertenece).

                newComment = Comentario(
                    textoComentario=newCommentOnPost,
                    fechaComentario=commentDate,
                    autorComentario=author,
                    idEntradaComentario=commentPostId,
                )

                db.session.add(newComment)
                db.session.commit()

                return (
                    jsonify(
                        Mensaje=f"El comentario '{newCommentOnPost}' se realizó con éxito a la publicación {commentPostId}"
                    ),
                    201,
                )

        if id is None:
            return jsonify(Mensaje=f"¡Tenés que especificar que publicación querés comentar!"), 400

    def put(self, id=None):
        if id is not None:
            comment = Comentario.query.get(id)

            if comment is not None:
                oldData = (
                    comment.textoComentario
                )  # Trae la información antigua ya que está antes del commit a la DB (La almaceno en una variable para utilizarla más adelante.)
                dataComment = request.get_json()  # Trae los datos del JSON.
                newContent = dataComment.get(
                    "content"
                )  # Trae la clave llamada "contenido" del JSON.

                comment.textoComentario = newContent  # Reemplazo el contenido antiguo del objeto "comment" de la clase "Comentario", por el nuevo contenido.
                db.session.commit()  # Envía los cambios a la DB.

                newDataComment = (
                    comment.textoComentario
                )  # Trae la nueva información del comentario ya que se comitearon los cambios anteriormente.

                return (
                    jsonify(
                        Mensaje=f"Anterior contenido: {oldData} | Nuevo contenido: {newDataComment}"
                    ),
                    200,
                )

            if comment is None:
                return jsonify(Mensaje=f"El comentario con ID {id} no existe."), 404

        if id is None:
            return jsonify(Mensaje=f"¡Debés especificar el comentario que querés modificar!"), 400

    def delete(self, id=None):
        comment = Comentario.query.get(id)

        if id is not None:
            if comment is not None:
                db.session.delete(comment)
                db.session.commit()
                return (
                    jsonify(
                        Mensaje=f"El comentario '{comment.textoComentario}' con ID {comment.idComentario} fue borrado con éxito."
                    ),
                    200,
                )

            if comment is None:
                return jsonify(Mensaje=f"El comentario que intentabas borrar no existe."), 404

        if id is None:
            return (
                jsonify(
                    Mensaje=f"¡El ID del comentario debe ser especificado para poder ser borrado!"
                ),
                400,
            )


app.add_url_rule("/comment", view_func=CommentApi.as_view("comment"))
app.add_url_rule("/comment/<id>", view_func=CommentApi.as_view("commentById"))
# /<id> deber llamarse igual que en los
# parámetros de las funciones.

# --- MethodView para categorías --- #


class CategoryApi(MethodView):
    def get(self, categoryId=None):
        if categoryId is None:
            categories = Categoria.query.all()

            if len(categories) == 0:
                return jsonify(Mensaje=f"¡El listado de categorías está vacío (por ahora)!"), 404

            if len(categories) > 0:
                schemaCategories = CategorySchema().dump(categories, many=True)

                newSchemaCategories = []
                for category in schemaCategories:
                    newSchemaCategory = {
                        "ID de la categoría": category["idCategoria"],
                        "Nombre de la categoría": category["etiquetaCategoria"],
                    }

                    newSchemaCategories.append(newSchemaCategory)

                return jsonify(newSchemaCategories), 200

        if categoryId is not None:
            category = Categoria.query.get(categoryId)

            if category is not None:
                schemaCategory = CategorySchema().dump(category)
                return jsonify(schemaCategory), 200

            if category is None:
                return jsonify(Mensaje=f"La categoría con ID {categoryId} no existe."), 404

    def post(self):
        dataNewCategory = request.get_json()
        nameCategory = dataNewCategory.get("name")

        filterDataCategory = Categoria.query.filter(
            Categoria.etiquetaCategoria == nameCategory
        ).first()

        if filterDataCategory is None:
            newCategory = Categoria(etiquetaCategoria=nameCategory)

            db.session.add(newCategory)
            db.session.commit()

            return (
                jsonify(Mensaje=f"Se creó con éxito la categoría: {nameCategory}"),
                201,
            )  # Código de error (En este caso: La entidad ha sido creada correctamente.)

        return jsonify(Mensaje=f"La categoría '{nameCategory}' ya existe."), 400

    def put(self, categoryId=None):
        if categoryId is not None:
            category = Categoria.query.get(categoryId)

            if category is not None:
                oldData = (
                    category.etiquetaCategoria
                )  # Trae la información antigua ya que está antes del commit a la DB (La almaceno en una variable para utilizarla más adelante.)
                dataNewCategory = request.get_json()  # Trae los datos del JSON.
                newName = dataNewCategory.get("name")  # Trae la clave llamada "contenido" del JSON.

                filterDataCategory = Categoria.query.filter(
                    Categoria.etiquetaCategoria == newName
                ).first()  # Filtro para no poner un nombre de categoría repetido.

                if filterDataCategory is None:
                    category.etiquetaCategoria = newName
                    db.session.commit()

                    return jsonify(Mensaje=f"Dato anterior: {oldData} | Nuevo dato: {newName}"), 200

                # Si filterDataCategory is not None quiere decir que la categoría existe.
                return (
                    jsonify(
                        Mensaje=f"La categoría '{newName}' ya existe. Introduce una categoría distinta."
                    ),
                    400,
                )

            if category is None:
                return jsonify(Mensaje=f"La categoría con ID {categoryId} no existe."), 404

        if categoryId is None:
            return jsonify(Mensaje=f"¡Debés especificar la categoría que querés modificar!"), 400

    def delete(self, categoryId=None):
        if categoryId is not None:
            category = Categoria.query.get(categoryId)

            if category is not None:
                db.session.delete(category)
                db.session.commit()
                return (
                    jsonify(
                        Mensaje=f"La categoría que se titula '{category.etiquetaCategoria}' con ID {category.idCategoria} fue borrada con éxito."
                    ),
                    200,
                )

            if category is None:
                return jsonify(Mensaje=f"La categoría que intentabas borrar no existe"), 404

        if categoryId is None:
            return (
                jsonify(
                    Mensaje=f"ID de categoría no válido. Debes especificarlo para poder borrar la categoría deseada."
                ),
                400,
            )

app.add_url_rule("/category", view_func=CategoryApi.as_view("category"))
app.add_url_rule("/category/<categoryId>", view_func=CategoryApi.as_view("categoryById"))