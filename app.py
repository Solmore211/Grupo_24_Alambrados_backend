from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

app = Flask(__name__)

#MySQL Connection
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Sola3187**'
app.config['MYSQL_DB'] = 'servicios_tp'
mysql = MySQL(app)

#vonfiguraciones
app.secret_key = 'mysecretkey' #34'

@app.route("/")
def Index():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM trabajos')
    data = cur.fetchall()
    #print(data)
    return render_template('index.html', services = data) #contacts = data

@app.route("/add_service", methods=['POST'])
def add_service():
    if request.method == 'POST':
        codigo = request.form['codigo']
        servicio = request.form['servicio']
        precio = request.form['precio']
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO trabajos (codigo, servicio, precio) VALUES (%s, %s, %s)', (codigo, servicio, precio)) #contacts
        mysql.connection.commit()
        flash("Servicio agregado exitosamente!!!")
        return redirect(url_for('Index'))

@app.route("/edit/<id>")
def obtener_service(id): #get_contact
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM trabajos WHERE id = %s', (id))
    data = cur.fetchall()
    return render_template('edit-service.html', service = data[0])

@app.route('/update/<id>', methods = ['POST'])
def update_service(id):
    if request.method == 'POST':
        codigo = request.form['codigo']
        servicio = request.form['servicio']
        precio = request.form['precio']
        cur = mysql.connection.cursor()
        cur.execute("""
                    UPDATE trabajos
                    SET codigo = %s,
                        servicio = %s,
                        precio = %s
                    WHERE id = %s
                    """,(codigo, servicio, precio, id))
        mysql.connection.commit()
        flash('Servicio actualizado exitosamente!!!')
        return redirect(url_for('Index'))

@app.route("/delete/<string:id>")
def delete_service(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM trabajos WHERE id = {0}'.format(id))
    mysql.connection.commit()
    flash('Servicio removido exitosamente!!!')
    return redirect(url_for('Index'))
    #return id
    #return 'delete service'

if __name__ == "__main__":
    app.run(port = 4000, debug= True)