from flask import Flask, render_template, request, redirect, url_for
import requests
import os

app = Flask(__name__)

# Directorio donde se guardarán las imágenes
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Lista para almacenar noticias (cada noticia es un diccionario con 'titulo', 'texto' e 'imagen')
noticias = []

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# Listas para almacenar libros y pedidos
libros = []
pedidos = []

# Contraseña 
contrasena = "yyyyyyyyy"
contrasena2 = "xxxxxxxxxx"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/Noticias", methods=['GET', 'POST'])
def Noticias():
    if request.method == 'POST':
        # Obtener los datos del formulario
        titulo = request.form['titulo']
        copete = request.form['copete']  
        texto = request.form['texto']


        # Verificar si se proporcionó un archivo de imagen
        if 'imagen' in request.files:
            imagen = request.files['imagen']

            # Guardar la imagen en el sistema de archivos fuera del directorio estático
            if imagen and allowed_file(imagen.filename):
                filename = os.path.join(app.config['UPLOAD_FOLDER'], imagen.filename)
                imagen.save(filename)

                # Agregar la noticia a la lista con la ruta de la imagen en lugar de la imagen
                noticias.append({'titulo': titulo, 'copete': copete,'texto': texto, 'imagen': filename}) # Modifica esta línea

        return redirect(url_for('Noticias'))

    # Si es una solicitud GET, renderizar el formulario
    return render_template("Noticias.html", noticias=noticias)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Verificar si se proporcionó la contraseña correcta
        if request.form.get('contrasena') == contrasena:
            # Contraseña correcta, redirigir a la página de carga de noticias
            return redirect(url_for('cargar_noticias'))

    # Si es una solicitud GET o una contraseña incorrecta, mostrar el formulario
    return render_template("login.html", error=None)

@app.route("/cargar_noticias", methods=['GET', 'POST'])
def cargar_noticias():
    if request.method == 'POST':
        # Obtener los datos del formulario
        titulo = request.form['titulo']
        copete = request.form['copete']
        texto = request.form['texto']
        imagen = request.files['imagen']

        # Guardar la noticia en la lista
        noticias.append({'titulo': titulo,'copete': copete,'texto': texto,'imagen': imagen.filename})

        return redirect(url_for('Noticias'))
    elif request.method == 'GET':
        # Manejar la solicitud GET renderizando una plantilla
        return render_template("cargar_noticias.html")  # Reemplaza con el nombre correcto de tu plantilla

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route("/tienda_de_inventos", methods=['GET', 'POST'])
def tienda_de_inventos():
    if request.method == 'POST':
        # Obtener los datos del formulario
        orden = request.form['orden']
        titulo = request.form['titulo']
        precio = request.form['precio']
        comprar = request.form['comprar']

        # Verificar si se proporcionó un archivo de imagen
        if 'imagen' in request.files:
            imagen = request.files['imagen']

            # Guardar la imagen en el sistema de archivos fuera del directorio estático
            if imagen and allowed_file(imagen.filename):
                filename = os.path.join(app.config['UPLOAD_FOLDER'], imagen.filename)
                imagen.save(filename)

                # Agregar el libro a la lista con la ruta de la imagen en lugar de la imagen
                libros.append({'orden': orden, 'titulo': titulo, 'precio': precio, 'comprar': comprar, 'imagen': filename})

        return redirect(url_for('tienda_de_inventos'))
    
    # Si es una solicitud GET, renderizar el formulario
    return render_template("tienda_de_inventos.html", libros=libros)

@app.route("/password", methods=['GET', 'POST'])
def password ():
    if request.method == 'POST':
        # Verificar si se proporcionó la contraseña correcta
        if request.form.get('contrasena2') == contrasena2:
            # Contraseña correcta, redirigir a la página de carga de libros
            return redirect(url_for('cargar_libro'))

    # Si es una solicitud GET o una contraseña incorrecta, mostrar el formulario
    return render_template("password.html", error=None)

@app.route("/cargar_libro", methods=['GET', 'POST'])
def cargar_libro():
    if request.method == 'POST':
        # Obtener los datos del formulario
        orden = request.form['orden']
        titulo = request.form['titulo']
        precio = request.form['precio']
        imagen = request.files['imagen']
        comprar = request.form['comprar']

        # Guardar el libro en la lista
        libros.append({'orden': orden, 'titulo': titulo, 'precio': precio, 'comprar': comprar, 'imagen': imagen.filename})

        return redirect(url_for('tienda_de_inventos'))
    elif request.method == 'GET':
        # Manejar la solicitud GET renderizando una plantilla
        return render_template("cargar_invento.html")  # Reemplaza con el nombre correcto de tu plantilla

if __name__ == '__main__':
    app.run(debug=True)