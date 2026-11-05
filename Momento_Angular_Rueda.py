from vpython import *

#  Configuración de la Escena 
scene = canvas(width=900, height=550, background=color.white)
scene.title = "Dinámica Completa: Silla y Rueda (Modos Intercambiables)"
scene.camera.pos = vector(0, 3, 12)

# Controles de cámara con el ratón activados
scene.userspin = True
scene.userzoom = True
scene.userpan = True

# --- Parámetros del sistema ---
M_p = 40.0       # Masa Persona/Silla (kg)
R_p = 0.6        # Radio del cuerpo (m)
H_p = 2.0        # Altura (m)
m_a = 2.0        # Masa de UN brazo (kg)
d_a = 1.2        # Longitud del brazo (m)
m_r = 5.0        # Masa de la Rueda (kg)
R_r = 0.5        # Radio Rueda (m)
omega_rueda_spin = 25.0  # Velocidad interna de la rueda (rad/s)

#  Cálculo Riguroso de Inercias 
I_persona = 0.5 * M_p * R_p**2
I_un_brazo_cm = (1/12) * m_a * d_a**2
distancia_brazo = R_p + (d_a / 2)
I_brazos = 2 * (I_un_brazo_cm + m_a * distancia_brazo**2)

distancia_rueda = R_p + d_a
I_rueda_orbita = 0.5 * m_r * R_r**2 + m_r * distancia_rueda**2

I_sistema_y = I_persona + I_brazos + I_rueda_orbita 
I_rueda_propia = m_r * R_r**2  
L_rueda_total = I_rueda_propia * omega_rueda_spin 

#  Creación de Objetos Visuales 
persona = cylinder(pos=vector(0, -H_p/2, 0), axis=vector(0, H_p, 0), radius=R_p, color=color.blue, opacity=0.5)
nariz = sphere(color=color.yellow, radius=0.1)

brazo_der = cylinder(radius=0.08, color=color.orange)
brazo_izq = cylinder(radius=0.08, color=color.orange)

rueda = ring(radius=R_r, thickness=0.05, color=color.red)
rayo1 = cylinder(radius=0.02, color=color.black)
rayo2 = cylinder(radius=0.02, color=color.black)

flecha_L_rueda = arrow(color=color.green, shaftwidth=0.06)
flecha_L_persona = arrow(color=color.blue, shaftwidth=0.06)
flecha_omega = arrow(color=color.cyan, shaftwidth=0.05)
flecha_torque = arrow(color=color.red, shaftwidth=0.08)
flecha_alfa = arrow(color=color.yellow, shaftwidth=0.06)

#  VARIABLES GLOBALES PARA MODOS 
modo_video = False
theta_inclinacion = 0.0

#  INTERFAZ INTERACTIVA 
scene.append_to_caption(' <b>Controles de cámara:</b> <i>Clic derecho + Arrastrar</i> para rotar.<br><br>')

# Función para alternar modos
def toggle_modo(b):
    global modo_video, theta_inclinacion, phi_persona
    modo_video = not modo_video
    phi_persona = 0.0 # Reiniciar giro visual
    
    if modo_video:
        b.text = "Modo: VIDEO (L_inicial = L_rueda). Reposo a 90°"
        slider_tilt.value = 90
        theta_inclinacion = radians(90)
    else:
        b.text = "Modo: SIMULADOR (L_inicial = 0). Reposo a 0°"
        slider_tilt.value = 0
        theta_inclinacion = radians(0)

boton_modo = button(text="Modo: SIMULADOR (L_inicial = 0). Reposo a 0°", bind=toggle_modo)

scene.append_to_caption('<br><br><b>Arrastra el control deslizante para INCLINAR la rueda:</b>\n')

def ajustar_rueda(s):
    global theta_inclinacion
    theta_inclinacion = radians(s.value)

slider_tilt = slider(bind=ajustar_rueda, min=-90, max=90, value=0, length=400)
scene.append_to_caption(' (-90° a +90°)\n\n')

info_tabla = wtext(text="")

#  Variables de movimiento 
phi_persona = 0.0
phi_rueda = 0.0
theta_anterior = 0.0
dt = 0.01

while True:
    rate(100)
    
    # VELOCIDAD  MANOS 
    w_inclinacion = (theta_inclinacion - theta_anterior) / dt
    theta_anterior = theta_inclinacion
    
    # DINÁMICA (Idéntica en ambos modos) 
    torque_y = - I_rueda_propia * omega_rueda_spin * cos(theta_inclinacion) * w_inclinacion
    alfa_y = torque_y / I_sistema_y
    
    # CINEMÁTICA (Depende del Modo) 
    L_rueda_y = L_rueda_total * sin(theta_inclinacion)
    
    if not modo_video:
        # Ecuación 1
        L_persona_y = -L_rueda_y
        ecuacion_str = "ω = -(I_r·ω_r / I_s) · sin(θ)"
    else:
        # Ecuación 2
        L_persona_y = L_rueda_total * (1 - sin(theta_inclinacion))
        ecuacion_str = "ω = (I_r·ω_r / I_s) · (1 - sin(θ))"
        
    omega_persona = L_persona_y / I_sistema_y
    
    phi_persona += omega_persona * dt
    phi_rueda += omega_rueda_spin * dt
    
    #  GEOMETRÍA VISUAL 
    dir_frente = vector(sin(phi_persona), 0, cos(phi_persona))
    dir_lado = vector(cos(phi_persona), 0, -sin(phi_persona))
    
    nariz.pos = vector(0, H_p/2 - 0.2, 0) + dir_frente * R_p
    
    separacion_hombros = 0.3
    brazo_der.pos = vector(0,0,0) + dir_frente * R_p + dir_lado * separacion_hombros
    brazo_der.axis = dir_frente * d_a
    brazo_izq.pos = vector(0,0,0) + dir_frente * R_p - dir_lado * separacion_hombros
    brazo_izq.axis = dir_frente * d_a
    
    centro_rueda = vector(0,0,0) + dir_frente * (R_p + d_a)
    eje_rueda = cos(theta_inclinacion) * dir_lado + sin(theta_inclinacion) * vector(0,1,0)
    
    rueda.pos = centro_rueda
    rueda.axis = eje_rueda
    
    u = dir_frente
    v = cross(eje_rueda, dir_frente)
    
    rayo1.pos = centro_rueda - R_r * (cos(phi_rueda)*u + sin(phi_rueda)*v)
    rayo1.axis = 2 * R_r * (cos(phi_rueda)*u + sin(phi_rueda)*v)
    rayo2.pos = centro_rueda - R_r * (cos(phi_rueda+pi/2)*u + sin(phi_rueda+pi/2)*v)
    rayo2.axis = 2 * R_r * (cos(phi_rueda+pi/2)*u + sin(phi_rueda+pi/2)*v)
    
    # 5. DIBUJAR VECTORES 
    flecha_L_rueda.pos = centro_rueda
    flecha_L_rueda.axis = eje_rueda * (L_rueda_total / 15) 
    
    altura_cabeza = vector(0, H_p/2, 0)
    flecha_L_persona.pos = altura_cabeza + dir_lado * (R_p + 0.3)
    flecha_L_persona.axis = vector(0, L_persona_y / 15, 0)
    
    flecha_omega.pos = altura_cabeza - dir_lado * (R_p + 0.3)
    flecha_omega.axis = vector(0, omega_persona * 1.5, 0)
    
    flecha_torque.pos = altura_cabeza - dir_frente * (R_p + 0.3)
    flecha_torque.axis = vector(0, torque_y / 50, 0)
    
    flecha_alfa.pos = altura_cabeza - dir_frente * (R_p + 0.5)
    flecha_alfa.axis = vector(0, alfa_y * 1.5, 0)
    
    # HTML
    angulo_grados = degrees(theta_inclinacion)
    
    html_table = f"""
    <table border="1" cellpadding="5" style="border-collapse: collapse; width: 75%; text-align: left; font-family: Arial, sans-serif; margin-top: 10px;">
        <tr style="background-color: #333; color: white;">
            <th colspan="2" style="text-align: center;">Ecuación Activa: {ecuacion_str}</th>
        </tr>
        <tr style="background-color: #e6f7ff;">
            <td style="width: 55%;"><b>Ángulo de Inclinación ($\theta$)</b></td>
            <td style="width: 45%;"><b>{angulo_grados:.1f}°</b></td>
        </tr>
        <tr style="background-color: #e6f7ff;">
            <td><b>Velocidad Angular Persona</b> (Cyan)</td>
            <td><b>{omega_persona:.2f} rad/s</b></td>
        </tr>
        <tr style="background-color: #e6f7ff;">
            <td><b>Aceleración Angular Persona</b> (Amarillo)</td>
            <td><b>{alfa_y:.2f} rad/s²</b></td>
        </tr>
        <tr>
            <td><b>L_y Rueda</b> (Verde)</td>
            <td>{L_rueda_y:.1f} kg·m²/s</td>
        </tr>
        <tr>
            <td><b>L_y Persona</b> (Azul)</td>
            <td>{L_persona_y:.1f} kg·m²/s</td>
        </tr>
        <tr>
            <td><b>Velocidad de Inclinación Manos</b></td>
            <td>{w_inclinacion:.2f} rad/s</td>
        </tr>
        <tr>
            <td><b>Torque de Reacción</b> (Rojo)</td>
            <td>{torque_y:.1f} N·m</td>
        </tr>
    </table>
    """
    info_tabla.text = html_table
