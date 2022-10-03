#Importamos Flask y lo que utilizamos de flask
from flask import Flask, render_template, request, redirect, session

#Importamos la app
from flask_app import app

#Importamos los modelos que usaremos
from flask_app.models.users import User

@app.route('/')
def index():
    users = User.muestra_usuarios()
    return render_template('index.html', usuarios=users)

@app.route('/new')
def new():
    return render_template('new.html')

@app.route('/create', methods=['POST'])
def create():
    #Recibimos el formulario a través de una variable llamada request.form
    #request.form = {"first_name":"Juana", "last_name":"De Arco", "email":"juana@cd.com"}

    if not User.valida_usuario(request.form):
        return redirect('/new')
    else:
        User.guardar(request.form)
        return redirect('/')

@app.route('/delete/<int:id>')
def delete(id):
    formulario = {"id": id} #diccionario que le ponemos como nombre de variable formulario
    User.borrar(formulario)
    return redirect('/')

@app.route('/edit/<int:id>')
def edit(id):
    formulario = {"id": id}
    user = User.mostrar(formulario) #Instancia de usuario
    return render_template('edit.html', usuario = user)

@app.route('/update', methods=['POST'])
def update():
    #request.form = diccionario con el formulario de edit.html
    User.actualizar(request.form)
    return redirect('/')