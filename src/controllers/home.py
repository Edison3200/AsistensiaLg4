from flask import render_template, request, redirect, url_for, flash
from src import app
import random
from random import choice
from src.models.sesiones import Sesiones
from src.models.estudiantes import RegistroUsu
from src.models.semestres import Semestres
from datetime import datetime

app.secret_key ='spbYO0JJ0PUFLUikKYbKrpS5w3KUEnab5KcYDdYb'

@app.route('/', methods =['GET', 'POST'])
def index():
    if request.method == 'GET':
       sesiones = Sesiones()
       sesiones = sesiones.Listado()
    return render_template('index.html', sesiones = sesiones)

@app.route('/sesion/crear', methods =['GET', 'POST'])
def sesion_crear():
   if request.method == 'GET':
      semestres = Semestres()
      semestres = semestres.Listado()
      return render_template('crear.html',semestres =semestres)
   if request.method == 'POST':
  
      nombre = request.form.get('nombre')
      descripcion = request.form.get('descripcion')
      semestre = request.form.get('semestres')
      fecha = request.form.get('fecha')
      horai = request.form.get('horai')
      horaf = request.form.get('horaf')
      
      new_ses = Sesiones()
      new_ses =new_ses.insertSesion(nombre,descripcion,semestre,fecha,horai,horaf)
      flash("La sesion ha sido creada con exito","badge bg-success")
      return redirect(url_for('index'))

@app.route('/sesion/estudiantes', methods =['GET', 'POST'])   
def ingresar_sesion():
    if request.method == 'POST':

       id = request.form.get('id') #id sesion
       semestre = request.form.get('semestre') #id semestre
       
       sesion = Sesiones()
       datos = sesion.SesionIni(id)  
       
       aux =[]
       activos = sesion.SesionActiva(id) 
       for i in range(0,len(activos)):
            aux.append(activos[i][0])
       estudiantes = Sesiones()
       estudiantes = estudiantes.ListadoSesion(semestre)
    return render_template('sesion.html', estudiantes = estudiantes, sesion= datos,activos=aux)
    
@app.route('/sesion/estudiantes/guardar', methods =['GET', 'POST'])   
def guardar_sesion():
    if request.method == 'POST':
       id = request.form.get('id') #id sesion
       semestre = request.form.get('semestre')

       estudiantes = Sesiones()
       estudiantes = estudiantes.ListadoSesion(semestre)#Listado de estudiantes de un semestre

       lista_activos = Sesiones()#lista de estudiantes ya activos en base de datos
       lista_activos = lista_activos.SesionActiva(id)

       ssesion = Sesiones()
      
       print("Estudiantes ",estudiantes)
       print("activos en base", lista_activos)

       lista_estudiantes_activos = []
       lista_estudiantes_desac=[]
       for i in range(0,len(estudiantes)):
         valor = request.form.get(str(estudiantes[i][0]))
         
         if valor :
            lista_estudiantes_activos.append(estudiantes[i][0])
         else:
            lista_estudiantes_desac.append(estudiantes[i][0])
       
       print("Lista form activos", lista_estudiantes_activos)
       print("list form desactivos", lista_estudiantes_desac)

       for i in range(0,len(lista_estudiantes_activos)):
          if not lista_estudiantes_activos[i] in lista_activos:
             ssesion.AgregarEstSesion(id,lista_estudiantes_activos[i])

       for i in range(0,len(lista_estudiantes_desac)):
          if not lista_estudiantes_desac[i] in lista_activos:
             ssesion.EliminarEstSesion(id,lista_estudiantes_desac[i])

       return redirect(url_for('index'))
@app.route('/sesion/delete', methods=['GET', 'POST'])  
def delete_sesion():
   if request.method == 'GET':
       return redirect(url_for('index'))

   if request.method == 'POST':
      id = request.form.get('id')
      session = Sesiones()
      session = session.EliminarSesion(id)
      flash("La sesion fue eliminada!..","warning")
      return redirect(url_for('index'))
    
@app.route('/estudiante/crear', methods=['GET', 'POST'])  
def usuario_crear():
   if request.method == 'GET':
      semestres = Semestres()
      semestres = semestres.Listado()
      return render_template('/estudiante/crear.html',semestres =semestres)

   if request.method == 'POST':
      iden = request.form.get('identificacion')
      nombre = request.form.get('nombres')
      apellidos = request.form.get('apellidos')
      celular = request.form.get('celular')
      email = request.form.get('email')
      semestre = request.form.get('semestres')

      new_es = RegistroUsu()
      new_es =new_es.insertarUsu(iden,nombre,apellidos,celular,email,semestre)
      flash("El estudiante ha sido añadido con exito","badge bg-success")
      return redirect(url_for('index'))

@app.route('/estudiantes/listado', methods=['GET', 'POST'])  
def estudiante_listado():
   if request.method == 'GET':
      estudiantes = RegistroUsu()
      estudiantes = estudiantes.Listado()
      return render_template('/estudiante/listar.html',estudiantes =estudiantes)

@app.route('/estudiante/edit', methods=['GET', 'POST'])  
def estudiante_edit():
   if request.method == 'POST':

      id = request.form.get('id')

      estudiante = RegistroUsu()
      estudiante = estudiante.EditarEstu(id)

      semestres = Semestres()
      semestres = semestres.Listado()
   
      return render_template('/estudiante/editar.html',estudiante =estudiante,semestres =semestres)

@app.route('/estudiante/actualizar', methods=['GET', 'POST'])  
def estudiante_actualizar():
   if request.method == 'GET':
         return redirect(url_for('index'))
   if request.method == 'POST':
         id = request.form.get('identificador')
         iden = request.form.get('identificacion')
         nombre = request.form.get('nombres')
         apellidos = request.form.get('apellidos')
         celular = request.form.get('celular')
         email = request.form.get('email')
         semestre = request.form.get('semestres')

         new_es = RegistroUsu()
         new_es =new_es.ActualizarEstu(iden,nombre,apellidos,celular,email,semestre,id)
         flash("El estudiante ha sido editado","badge bg-success")
         return redirect(url_for('index'))

@app.route('/estudiante/delete', methods=['GET', 'POST'])  
def delete_estudiante():
   if request.method == 'GET':
       return redirect(url_for('index'))

   if request.method == 'POST':
      id = request.form.get('id')
      estudiante = RegistroUsu()
      estudiante = estudiante.EliminarEstu(id)
      flash("El estudiante fue eliminado!..","warning")
      return redirect(url_for('index'))

@app.route('/semestre/crear', methods=['GET', 'POST'])  
def semestre_crear():
   if request.method == 'GET':
      return render_template('/semestre/crear.html')
   if request.method == 'POST':
      nombre = request.form.get('nombre')

      new_semes = Semestres()
      new_semes = new_semes.insertSemestre(nombre)
      flash("Se ha creado un semestre de un programa academico","badge bg-success")
      return redirect(url_for('index'))