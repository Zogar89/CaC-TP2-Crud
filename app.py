from time import strftime
from flask import Flask, render_template_string
from flask import render_template, request, redirect
from flaskext.mysql import MySQL
from datetime import datetime
import os

app=Flask(__name__)

mysql=MySQL()
app.config['MYSQL_DATABASE_HOST']='localhost'
app.config['MYSQL_DATABASE_USER']='root'
app.config['MYSQL_DATABASE_PASSWORD']=''
app.config['MYSQL_DATABASE_DB']='tp2sistema'
mysql.init_app(app)

CARPETA=os.path.join('uploads')
app.config['CARPETA']=CARPETA

@app.route('/')
def index():

    sql="SELECT * FROM `empleados`;"
    conn=mysql.connect()
    cursor=conn.cursor()
    cursor.execute(sql)
    empleados=cursor.fetchall()
    conn.commit()

    return render_template('empleados/index.html', empleados=empleados) 

@app.route('/create')
def create():
    return render_template('empleados/create.html')

@app.route('/destroy/<int:id>')
def destroy(id):
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM empleados WHERE id=%s",(id))
    conn.commit()
    
@app.route('/edit/<int:id>')
def edit(id):
    conn=mysql.connect()
    cursor=conn.cursor()
    cursor.execute("SELECT * FROM empleados WHERE id=%s",(id))
    empleados=cursor.fetchall()
    conn.commit()
    return render_template('empleados/edit.html', empleados=empleados)

@app.route('/update', methods=['POST'])
def update():

    nombre=request.form['txtNombre']
    correo=request.form['txtCorreo']
    foto=request.files['txtFoto']
    id=request.form['txtID']

    sql="UPDATE `empleados` SET `nombre`=%s, `correo`=%s WHERE id=%s;"
    datos=(nombre,correo,id)

    now=datetime.now()
    tiempo=now.strftime("%Y%H%S")

    if foto.filename != '':
        nuevoNombreFoto = tiempo + foto.filename
        foto.save("uploads/"+nuevoNombreFoto)

        cursor.execute("SELECT foto FROM `empleados` WHERE id=%s",(id))
        fila = cursor.fetchall()
        os.remove(os.path.join(app.config['CARPETA'], fila[0][0]))

        cursor.execute("UPDATE `empleados` SET foto=%s WHERE id=%s")

    else:
        nuevoNombreFoto = 'SinFoto.jpg'

    cursor.execute(sql,datos)
    conn.commit()

    return redirect('/')

@app.route('/store', methods=['POST'])
def storage():
    nombre=request.form['txtNombre']
    correo=request.form['txtCorreo']
    foto=request.files['txtFoto']
    now=datetime.now()
    tiempo=now.strftime("%Y%H%S")

    if foto.filename != '':
        nuevoNombreFoto = tiempo + foto.filename
        foto.save("uploads/"+nuevoNombreFoto)
    else:
        nuevoNombreFoto = 'SinFoto.jpg'

    sql="INSERT INTO `empleados` (`id`, `nombre`, `correo`, `foto`) VALUES (NULL, '{}', '{}', '{}')".format(nombre, correo, nuevoNombreFoto)
    conn=mysql.connect()
    cursor=conn.cursor()
    cursor.execute(sql)
    conn.commit()
    return render_template('empleados/index.html')

if __name__ == '__main__':
    #DEBUG is SET to TRUE. CHANGE FOR PROD
    app.run(debug=True)