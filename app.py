from flask import Flask, render_template, request, redirect, flash, session
import mysql.connector

app = Flask(__name__)
app.secret_key = 'mensajes'

# Conexión a la base de datos
def get_db_connection():
    return mysql.connector.connect(
        host = 'localhost',
        user = 'root',
        password = '1234',
        database = 'inscripciones'
    )

# Rutas
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        correo = request.form['correo'].strip()
        contrasena = request.form['contrasena'].strip()
        
        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            
            # Buscar alumno por correo y contraseña
            cursor.execute(
                "SELECT * FROM alumno WHERE correo_alm = %s AND contrasena = %s",
                (correo, contrasena)
            )
            alumno = cursor.fetchone()
            
            if alumno:
                session['alumno_id'] = alumno['id_alm']
                return redirect('/horarios')
            else:
                cursor.execute("SELECT * FROM alumno WHERE correo_alm = %s", (correo,))
                if cursor.fetchone():
                    flash('Contraseña incorrecta', 'danger')
                else:
                    flash('Correo no registrado', 'danger')
                return render_template('login.html', correo=correo)
                
        except Exception as e:
            flash(f'Error al conectar con la base de datos: {str(e)}', 'danger')
            return redirect('/')
        finally:
            cursor.close()
            conn.close()
    
    return render_template('login.html')

@app.route('/horarios')
def horarios():
    if 'alumno_id' not in session:
        return redirect('/')
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Obtener datos básicos del alumno
        cursor.execute(
            "SELECT nombre_alm FROM alumno WHERE id_alm = %s", 
            (session['alumno_id'],)
        )
        alumno = cursor.fetchone()
        
        # Obtener materias inscritas con detalles
        cursor.execute("""
            SELECT 
                a.nombre_asg,
                p.nombre_prof AS profesor,
                s.nombre_sln AS salon,
                d.dia,
                h.hrs_inicio,
                h.hrs_fin
            FROM inscripcion i
            JOIN horario h ON i.id_hrs = h.id_hrs
            JOIN asignatura a ON h.id_asg = a.id_asg
            JOIN profesor p ON h.id_prof = p.id_prof
            JOIN salon s ON h.id_sln = s.id_sln
            JOIN dia_sem d ON h.id_dia_sem = d.id_dia_sem
            WHERE i.id_alm = %s
            ORDER BY d.id_dia_sem, h.hrs_inicio
        """, (session['alumno_id'],))
        
        materias = cursor.fetchall()
        
        return render_template(
            'horarios.html',
            alumno_nombre=alumno['nombre_alm'],
            materias=materias
        )
        
    except Exception as e:
        flash(f'Error al cargar horarios: {str(e)}', 'danger')
        return redirect('/')
    finally:
        cursor.close()
        conn.close()

@app.route('/horarios-disponibles')
def horarios_disponibles():
    if 'alumno_id' not in session:
        return redirect('/')
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # 1. Obtener semestre del alumno
        cursor.execute(
            "SELECT semestre_alm FROM alumno WHERE id_alm = %s",
            (session['alumno_id'],)
        )
        semestre = cursor.fetchone()['semestre_alm']
        
        # 2. Obtener horarios disponibles para su semestre
        cursor.execute("""
            SELECT 
                h.id_hrs,
                a.nombre_asg,
                p.nombre_prof AS profesor,
                s.nombre_sln AS salon,
                d.dia,
                h.hrs_inicio,
                h.hrs_fin,
                (SELECT COUNT(*) FROM inscripcion WHERE id_hrs = h.id_hrs) AS inscritos,
                s.cupo
            FROM horario h
            JOIN asignatura a ON h.id_asg = a.id_asg
            JOIN profesor p ON h.id_prof = p.id_prof
            JOIN salon s ON h.id_sln = s.id_sln
            JOIN dia_sem d ON h.id_dia_sem = d.id_dia_sem
            WHERE a.semestre_asg = %s
            ORDER BY d.id_dia_sem, h.hrs_inicio
        """, (semestre,))
        
        horarios = cursor.fetchall()
        
        # 3. Obtener materias ya inscritas para evitar doble inscripción
        cursor.execute("""
            SELECT id_hrs FROM inscripcion 
            WHERE id_alm = %s
        """, (session['alumno_id'],))
        
        inscripciones = [x['id_hrs'] for x in cursor.fetchall()]
        
        return render_template(
            'horarios_disponibles.html',
            horarios=horarios,
            inscripciones=inscripciones
        )
        
    except Exception as e:
        flash(f'Error al cargar horarios: {str(e)}', 'danger')
        return redirect('/horarios')
    finally:
        cursor.close()
        conn.close()

@app.route('/inscribir/<int:id_horario>')
def inscribir_materia(id_horario):
    if 'alumno_id' not in session:
        return redirect('/')
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Verificar cupo disponible
        cursor.execute("""
            SELECT COUNT(*) as inscritos, s.cupo
            FROM inscripcion i
            JOIN horario h ON i.id_hrs = h.id_hrs
            JOIN salon s ON h.id_sln = s.id_sln
            WHERE h.id_hrs = %s
        """, (id_horario,))
        
        resultado = cursor.fetchone()
        if resultado['inscritos'] >= resultado['cupo']:
            flash('Esta clase ya no tiene cupo disponible', 'warning')
            return redirect('/horarios-disponibles')
        
        # Realizar inscripción
        cursor.execute(
            "INSERT INTO inscripcion (id_alm, id_hrs) VALUES (%s, %s)",
            (session['alumno_id'], id_horario)
        )
        conn.commit()
        flash('Inscripción exitosa', 'success')
        
    except mysql.connector.Error as err:
        conn.rollback()
        flash(f'Error al inscribir: {err.msg}', 'danger')
    finally:
        cursor.close()
        conn.close()
    
    return redirect('/horarios')

@app.route('/baja/<int:id_inscripcion>', methods=['POST'])
def dar_baja(id_inscripcion):
    if 'alumno_id' not in session:
        return redirect('/')
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Verificar que la inscripción pertenece al alumno
        cursor.execute(
            "SELECT i.id_insc, a.nombre_asg FROM inscripcion i " +
            "JOIN horario h ON i.id_hrs = h.id_hrs " +
            "JOIN asignatura a ON h.id_asg = a.id_asg " +
            "WHERE i.id_insc = %s AND i.id_alm = %s",
            (id_inscripcion, session['alumno_id'])
        )
        inscripcion = cursor.fetchone()
        
        if not inscripcion:
            flash('No tienes permiso para esta acción o la inscripción no existe', 'danger')
            return redirect('/horarios')
        
        # Eliminar la inscripción
        cursor.execute(
            "DELETE FROM inscripcion WHERE id_insc = %s",
            (id_inscripcion,)
        )
        conn.commit()
        flash('Has sido dado de baja correctamente', 'success')
        
    except Exception as e:
        conn.rollback()
        flash(f'Error al dar de baja: {str(e)}', 'danger')
    finally:
        cursor.close()
        conn.close()
    
    return redirect('/horarios')

# Agrega esta ruta después de las demás rutas
@app.route('/cambiar-contrasena', methods=['GET', 'POST'])
def cambiar_contrasena():
    if 'alumno_id' not in session:
        return redirect('/')
    
    if request.method == 'POST':
        contrasena_actual = request.form['contrasena_actual'].strip()
        nueva_contrasena = request.form['nueva_contrasena'].strip()
        confirmacion = request.form['confirmacion'].strip()
        
        # Validaciones
        if not all([contrasena_actual, nueva_contrasena, confirmacion]):
            flash('Todos los campos son obligatorios', 'danger')
            return redirect('/cambiar-contrasena')
        
        if nueva_contrasena != confirmacion:
            flash('Las contraseñas nuevas no coinciden', 'danger')
            return redirect('/cambiar-contrasena')
        
        if len(nueva_contrasena) < 6 or len(nueva_contrasena) > 15:
            flash('La contraseña debe tener entre 6 y 15 caracteres', 'danger')
            return redirect('/cambiar-contrasena')
        
        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            
            # Verificar contraseña actual
            cursor.execute(
                "SELECT contrasena FROM alumno WHERE id_alm = %s",
                (session['alumno_id'],)
            )
            alumno = cursor.fetchone()
            
            if not alumno or alumno['contrasena'] != contrasena_actual:
                flash('La contraseña actual es incorrecta', 'danger')
                return redirect('/cambiar-contrasena')
            
            # Actualizar contraseña
            cursor.execute(
                "UPDATE alumno SET contrasena = %s WHERE id_alm = %s",
                (nueva_contrasena, session['alumno_id'])
            )
            conn.commit()
            
            flash('Contraseña cambiada exitosamente', 'success')
            return redirect('/')
            
        except Exception as e:
            conn.rollback()
            flash(f'Error al cambiar contraseña: {str(e)}', 'danger')
            return redirect('/cambiar-contrasena')
        finally:
            cursor.close()
            conn.close()
    
    return render_template('cambiar_contrasena.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)