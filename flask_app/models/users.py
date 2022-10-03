from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash #Importamos flash para mandar mensajes de validación

import re #Importando Expresiones Regulares
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:

    def __init__(self, data):
        #data = {"id": 1, "first_name":"Elena", "last_name":"De Troya", "email":"elena@cd.com", "created_at":"2022-09-26", "updated_at":"2022-09-26"}
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.password = data['password']
    
    @classmethod
    def guardar(cls, formulario):
        #formulario = {"first_name":"Juana", "last_name":"De Arco", "email":"juana@cd.com"}
        query = "INSERT INTO users(first_name, last_name, email, password) VALUES ( %(first_name)s, %(last_name)s, %(email)s, %(password)s )" #->INSERT INTO users(first_name, last_name, email) VALUES('Juana', 'De Arco', 'juana@codingdojo.com')
        result = connectToMySQL('esquema_usuarios_ch').query_db(query, formulario)
        return result
    
    @classmethod
    def muestra_usuarios(cls):
        query = "SELECT * FROM users"
        results = connectToMySQL('esquema_usuarios_ch').query_db(query)
        # [
        #    {"id": "1", "first_name":"Elena", "last_name":"De Troya"..},
        #    {"id": "2", "first_name":"Juana", "last_name":"De Arco"..}
        #]
        users = []
        for u in results: #en u voy a estar guardando mi diccionario
            #u = {"id": "1", "first_name":"Elena", "last_name":"De Troya"..}
            user = cls(u) #user = User(u) -> {"id": "1", "first_name":"Elena", "last_name":"De Troya"..}
            users.append(user)
        
        return users
    
    @classmethod
    def borrar(cls, formulario):
        #formulario = {"id":"1"}
        query = "DELETE FROM users WHERE id = %(id)s"
        result = connectToMySQL('esquema_usuarios_ch').query_db(query, formulario)
        return result
    
    @classmethod
    def mostrar(cls, formulario):
        #formulario = {"id": "1"}
        query = "SELECT * FROM users WHERE id = %(id)s" #Select SIEMPRE regresa una lista
        result = connectToMySQL('esquema_usuarios_ch').query_db(query, formulario)
        #result = [
        #  {"id": "1", "first_name":"Elena", "last_name":"De Troya"..}   
        #]
        diccionario = result[0] #diccionario = {"id": "1", "first_name":"Elena", "last_name":"De Troya"..}
        usuario = cls(diccionario) #usuario = User(diccionario) - Instancia de usuario
        return usuario
    
    @classmethod
    def actualizar(cls, formulario):
        #formulario = {"id":"1", "first_name":"Elena", "last_name":"De Troya", "email":"elena@cd.com"}
        query = "UPDATE users SET first_name=%(first_name)s, last_name=%(last_name)s, email=%(email)s WHERE id=%(id)s"
        result = connectToMySQL('esquema_usuarios_ch').query_db(query, formulario)
        return result
    
    @staticmethod
    def valida_usuario(formulario):
        is_valid = True #Asumimos que todo en el usuario está correcto

        if len(formulario['first_name']) < 3:
            flash('Nombre debe de tener al menos 3 caracteres', 'registro')
            is_valid = False
        
        if len(formulario['last_name']) < 3:
            flash('Apellido debe de tener al menos 3 caracteres', 'registro')
            is_valid = False

        if len(formulario['password']) < 6:
            flash('Contraseña debe tener al menos 6 caracteres', 'registro')
            is_valid = False

        #Verificamos con expresiones regulares que nuestro correo tenga el formato correcto
        if not EMAIL_REGEX.match(formulario['email']):
            flash('Correo Electrónico inválido', 'registro')
            is_valid = False
        
        #Consultar si ya existe ese correo electrónico
        query = "SELECT * FROM users WHERE email = %(email)s"
        results = connectToMySQL('esquema_usuarios_ch').query_db(query, formulario)
        if len(results) >= 1: #Si existe algún registro con ese correo
            flash('E-mail registrado previamente', 'registro')
            is_valid = False

        return is_valid

