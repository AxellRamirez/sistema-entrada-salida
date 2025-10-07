from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL
import MySQLdb.cursors

app = Flask(__name__)

# Configuración de la base de datos
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Estudiante'
app.config['MYSQL_DB'] = 'registro_entrada_salida'

mysql = MySQL(app)

# Diccionario para traducir días al español
DAYS_TRANSLATION = {
    'Monday': 'Lunes',
    'Tuesday': 'Martes',
    'Wednesday': 'Miércoles',
    'Thursday': 'Jueves',
    'Friday': 'Viernes',
    'Saturday': 'Sábado',
    'Sunday': 'Domingo'
}

def translate_day(day):
    return DAYS_TRANSLATION.get(day, day)

# Ruta para la página principal
@app.route('/')
def index():
    return render_template('index.html')

# Ruta para la página de horarios
@app.route('/horarios')
def horarios():
    return render_template('horarios.html')

# Ruta para la página Cómo Funciona
@app.route('/como_funciona')
def como_funciona():
    return render_template('como_funciona.html')

# Rutas para las secciones específicas
@app.route('/11-2')
def seccion_11_2():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT h.id, h.clase_id, h.dia, h.hora_inicio, h.hora_fin, c.nombre "
                   "FROM Horarios h "
                   "JOIN Clases c ON h.clase_id = c.id "
                   "WHERE h.seccion = '11-2' "
                   "ORDER BY FIELD(h.dia, 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'), h.hora_inicio")
    data = cursor.fetchall()
    for item in data:
        item['dia'] = translate_day(item['dia'])
    return render_template('11-2.html', data=data, dias=DAYS_TRANSLATION)

@app.route('/9-3')
def seccion_9_3():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT h.id, h.clase_id, h.dia, h.hora_inicio, h.hora_fin, c.nombre "
                   "FROM Horarios h "
                   "JOIN Clases c ON h.clase_id = c.id "
                   "WHERE h.seccion = '9-3' "
                   "ORDER BY FIELD(h.dia, 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'), h.hora_inicio")
    data = cursor.fetchall()
    for item in data:
        item['dia'] = translate_day(item['dia'])
    return render_template('9-3.html', data=data, dias=DAYS_TRANSLATION)

# Ruta para agregar horarios
@app.route('/add', methods=['POST'])
def add():
    seccion = request.form['seccion']
    clase_id = request.form['clase_id']
    dia = request.form['dia']
    hora_inicio = request.form['hora_inicio']
    hora_fin = request.form['hora_fin']
    cursor = mysql.connection.cursor()
    cursor.execute('INSERT INTO Horarios (clase_id, seccion, dia, hora_inicio, hora_fin) VALUES (%s, %s, %s, %s, %s)', (clase_id, seccion, dia, hora_inicio, hora_fin))
    mysql.connection.commit()
    return redirect(url_for(f'seccion_{seccion.replace("-", "_")}'))

# Ruta para eliminar horarios
@app.route('/delete/<int:id>', methods=['GET'])
def delete(id):
    cursor = mysql.connection.cursor()
    cursor.execute('DELETE FROM Horarios WHERE id = %s', (id,))
    mysql.connection.commit()
    return redirect(url_for('index'))

# Ruta para modificar horarios
@app.route('/edit/<int:id>', methods=['POST', 'GET'])
def edit(id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    if request.method == 'POST':
        seccion = request.form['seccion']
        clase_id = request.form['clase_id']
        dia = request.form['dia']
        hora_inicio = request.form['hora_inicio']
        hora_fin = request.form['hora_fin']
        cursor.execute('UPDATE Horarios SET clase_id = %s, seccion = %s, dia = %s, hora_inicio = %s, hora_fin = %s WHERE id = %s', (clase_id, seccion, dia, hora_inicio, hora_fin, id))
        mysql.connection.commit()
        return redirect(url_for(f'seccion_{seccion.replace("-", "_")}'))
    else:
        cursor.execute('SELECT * FROM Horarios WHERE id = %s', (id,))
        data = cursor.fetchone()
        return render_template('edit.html', data=data)

if __name__ == "__main__":
    app.run(debug=True)
