from vpython import *

#  Configuración de la Escena 
scene = canvas(width=900, height=550, background=color.white)
scene.title = "Conservación del Momento Angular (Efecto Bailarina)"
scene.camera.pos = vector(0, 3, 15)

# Controles de cámara con el ratón activados
scene.userspin = True
scene.userzoom = True
scene.userpan = True

#  Parámetros del sistema 
M_c = 20.0     # Masa cilindro (kg)
R_c = 1.0      # Radio cilindro (m)
H_c = 6.0      # Altura cilindro (m)
m_v = 3.0      # Masa brazos (kg)
m_e = 5.0      # Masa puños (kg)
R_e = 1.2      # Radio puños (m)

d_inicial = 4.0 # Longitud inicial de los brazos (m)
omega_inicial = 1.5 # Velocidad inicial (rad/s)

#  Creación de Objetos Visuales 
eje_rotacion = vector(0, 1, 0)
objetos_rotantes = []

# Base / Suelo (Estático)
plataforma = cylinder(pos=vector(0, -H_c/2 - 0.5, 0), axis=vector(0, 0.5, 0), radius=R_c*3, color=color.gray(0.8))

# Cuerpo central
cilindro = cylinder(pos=vector(0, -H_c/2, 0), axis=vector(0, H_c, 0), radius=R_c, color=color.blue, opacity=0.75)
objetos_rotantes.append(cilindro)

# Eje de rotación (Línea central)
cylinder(pos=vector(0, -H_c/2 - 1, 0), axis=vector(0, H_c + 2.5, 0), radius=0.05, color=color.black)

# Brazo y puño DERECHO
brazo_der = cylinder(pos=vector(R_c, 0, 0), axis=vector(d_inicial, 0, 0), radius=0.2, color=color.orange)
esfera_der = sphere(pos=vector(R_c + d_inicial + R_e, 0, 0), radius=R_e, color=color.red, shininess=0.8)
objetos_rotantes.extend([brazo_der, esfera_der])

# Brazo y puño IZQUIERDO
brazo_izq = cylinder(pos=vector(-R_c, 0, 0), axis=vector(-d_inicial, 0, 0), radius=0.2, color=color.orange)
esfera_izq = sphere(pos=vector(-(R_c + d_inicial + R_e), 0, 0), radius=R_e, color=color.red, shininess=0.8)
objetos_rotantes.extend([brazo_izq, esfera_izq])

#  VECTORES (Flechas físicas) 
# Flecha para el Momento Angular (L) - Constante
flecha_L = arrow(pos=vector(0, H_c/2 + 0.2, 0), color=color.green, shaftwidth=0.15)
# Flecha para la Velocidad Angular (omega) - Variable
flecha_omega = arrow(pos=vector(R_c + 0.5, H_c/2 + 0.2, 0), color=color.cyan, shaftwidth=0.1)

#  CÁLCULO INICIAL DEL MOMENTO ANGULAR (L) 
I_cil = 0.5 * M_c * R_c**2
I_esf_cm = (2/5) * m_e * R_e**2

def calcular_inercia_total(d):
    I_brazo_cm = (1/12) * m_v * d**2
    I_brazo = I_brazo_cm + m_v * (R_c + d/2)**2
    I_esfera = I_esf_cm + m_e * (R_c + d + R_e)**2
    return I_cil + 2*I_brazo + 2*I_esfera

I_inicial = calcular_inercia_total(d_inicial)
L_constante = I_inicial * omega_inicial 

#  INTERFAZ INTERACTIVA (HTML y Slider) 
scene.append_to_caption('<b>Controles de cámara:</b> <i>Clic derecho + Arrastrar</i> para rotar | <i>Rueda del ratón</i> para Zoom.<br><br>')
scene.append_to_caption('<b>Arrastra para estirar o recoger los brazos:</b>\n')

def ajustar_brazos(s):
    pass

slider_d = slider(bind=ajustar_brazos, min=0.1, max=4.0, value=d_inicial, length=400)
scene.append_to_caption('\n\n')

# Objeto dinámico para la tabla HTML
info_tabla = wtext(text="")

# Bucle de Animación 
dt = 0.01
while True:
    rate(100)
    
    # Acá lo importante física
    d_actual = slider_d.value
    I_actual = calcular_inercia_total(d_actual)
    omega_actual = L_constante / I_actual
    
    # Actualizar visualmente la longitud de los brazos
    dir_der = brazo_der.axis.hat
    brazo_der.pos = dir_der * R_c
    brazo_der.axis = dir_der * d_actual
    esfera_der.pos = dir_der * (R_c + d_actual + R_e)
    
    dir_izq = brazo_izq.axis.hat
    brazo_izq.pos = dir_izq * R_c
    brazo_izq.axis = dir_izq * d_actual
    esfera_izq.pos = dir_izq * (R_c + d_actual + R_e)
    
    # Rotar objetos
    for obj in objetos_rotantes:
        obj.rotate(angle=omega_actual * dt, axis=eje_rotacion, origin=vector(0,0,0))
        
    #  Vectores
    flecha_L.axis = vector(0, L_constante / 100, 0) # Escala visual fija
    flecha_omega.axis = vector(0, omega_actual * 1.5, 0) # Cambia de tamaño según la velocidad
        
    # Tabla HTML 
    html_table = f"""
    <table border="1" cellpadding="6" style="border-collapse: collapse; width: 60%; text-align: left; font-family: Arial, sans-serif;">
        <tr style="background-color: #f2f2f2;">
            <th colspan="2" style="text-align: center;">Datos del Sistema (Conservación de L)</th>
        </tr>
        <tr>
            <td style="width: 50%;"><b>Postura de brazos (d)</b></td>
            <td style="width: 50%;">{d_actual:.2f} m</td>
        </tr>
        <tr>
            <td><b>Inercia Actual (I)</b></td>
            <td>{I_actual:.1f} kg·m²</td>
        </tr>
        <tr>
            <td><b>Velocidad Angular (Cyan)</b></td>
            <td>{omega_actual:.2f} rad/s</td>
        </tr>
        <tr style="background-color: #e6ffe6;">
            <td><b>Momento Angular (Verde)</b></td>
            <td><b>{L_constante:.1f} kg·m²/s (CONSTANTE)</b></td>
        </tr>
    </table>
    """
    info_tabla.text = html_table
