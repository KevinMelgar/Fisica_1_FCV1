from vpython import *

# --- Configuración de la escena ---
scene = canvas(width=1000, height=650, background=color.white)
scene.title = "Simulador Físico: Competición de Inercias (RK4)\nTodos reciben el mismo Torque. Los de menor inercia (I) aceleran más rápido."

# Parámetros físicos base (Masa y dimensiones iguales para comparar)
M = 1.0  # Masa (kg)
R = 1.0  # Radio (m)
L = 4.0  # Longitud de la varilla (m)

tau = 2.0  # Torque constante aplicado a todos (N·m)

# Función auxiliar para crear el eje y la etiqueta
def crear_eje_y_etiqueta(posicion, direccion_eje, texto, inercia, longitud=3.5):
    eje = cylinder(pos=posicion - direccion_eje.hat * (longitud/2), 
                   axis=direccion_eje.hat * longitud, 
                   radius=0.03, color=color.red)
    texto_completo = f"{texto}\nI = {inercia:.3f} kg·m²"
    label(pos=posicion - vector(0, 2.8, 0), text=texto_completo, 
          color=color.black, box=False, height=14, line=False)
    return eje

objetos = []

# ================= FILA 1 =================

# 1. Cilindro sólido o disco (eje simétrico)
I1 = 0.5 * M * R**2
pos1 = vector(-6, 3.5, 0)
eje1_vec = vector(0, 1, 0) 
crear_eje_y_etiqueta(pos1, eje1_vec, "Cilindro simétrico", I1)
cilindro1 = cylinder(pos=pos1 - eje1_vec.hat*0.5, axis=eje1_vec.hat, radius=R, color=color.blue)
objetos.append({'obj': cilindro1, 'eje': eje1_vec, 'centro': pos1, 'I': I1, 'omega': 0})

# 2. Anillo (eje simétrico)
I2 = M * R**2
pos2 = vector(-2, 3.5, 0)
eje2_vec = vector(0, 1, 0) 
crear_eje_y_etiqueta(pos2, eje2_vec, "Anillo simétrico", I2)
anillo1 = ring(pos=pos2, axis=eje2_vec, radius=R, thickness=0.1, color=color.orange)
objetos.append({'obj': anillo1, 'eje': eje2_vec, 'centro': pos2, 'I': I2, 'omega': 0})

# 3. Esfera sólida
I3 = (2/5) * M * R**2
pos3 = vector(2, 3.5, 0)
eje3_vec = vector(0, 1, 0) 
crear_eje_y_etiqueta(pos3, eje3_vec, "Esfera sólida", I3)
esfera1 = sphere(pos=pos3, radius=R, color=color.green)
cylinder(pos=pos3, axis=vector(R,0,0), radius=0.05, color=color.black) # Marca visual
objetos.append({'obj': esfera1, 'eje': eje3_vec, 'centro': pos3, 'I': I3, 'omega': 0})

# 4. Varilla sobre el centro
I4 = (1/12) * M * L**2
pos4 = vector(6, 3.5, 0)
eje4_vec = vector(0, 1, 0) 
crear_eje_y_etiqueta(pos4, eje4_vec, "Varilla (centro)", I4)
varilla1 = cylinder(pos=pos4 - vector(L/2,0,0), axis=vector(L,0,0), radius=0.15, color=color.cyan)
objetos.append({'obj': varilla1, 'eje': eje4_vec, 'centro': pos4, 'I': I4, 'omega': 0})


# ================= FILA 2 =================

# 5. Cilindro sólido (diámetro central)
I5 = (1/4)*M*R**2 + (1/12)*M*L**2
pos5 = vector(-6, -4.5, 0)
eje5_vec = vector(0, 1, 0)
crear_eje_y_etiqueta(pos5, eje5_vec, "Cilindro (diámetro)", I5)
cilindro2 = cylinder(pos=pos5 - vector(0,0,-1), axis=vector(0,0,-2), radius=R, color=color.purple)
objetos.append({'obj': cilindro2, 'eje': eje5_vec, 'centro': pos5, 'I': I5, 'omega': 0})

# 6. Anillo sobre un diámetro
I6 = 0.5 * M * R**2
pos6 = vector(-2, -4.5, 0)
eje6_vec = vector(0, 1, 0) 
crear_eje_y_etiqueta(pos6, eje6_vec, "Anillo (diámetro)", I6)
anillo2 = ring(pos=pos6, axis=vector(0,0,1), radius=R, thickness=0.1, color=color.magenta)
objetos.append({'obj': anillo2, 'eje': eje6_vec, 'centro': pos6, 'I': I6, 'omega': 0})

# 7. Delgada capa esférica (hueca)
I7 = (2/3) * M * R**2
pos7 = vector(2, -4.5, 0)
eje7_vec = vector(0, 1, 0) 
crear_eje_y_etiqueta(pos7, eje7_vec, "Capa esférica", I7)
esfera2 = sphere(pos=pos7, radius=R, color=color.yellow, opacity=0.6)
objetos.append({'obj': esfera2, 'eje': eje7_vec, 'centro': pos7, 'I': I7, 'omega': 0})

# 8. Varilla sobre un extremo
I8 = (1/3) * M * L**2
pos8 = vector(6, -4.5, 0)
eje8_vec = vector(0, 1, 0) 
crear_eje_y_etiqueta(pos8, eje8_vec, "Varilla (extremo)", I8)
varilla2 = cylinder(pos=pos8, axis=vector(L,0,0), radius=0.15, color=color.red)
objetos.append({'obj': varilla2, 'eje': eje8_vec, 'centro': pos8, 'I': I8, 'omega': 0})


# --- Motor Físico (Integración Runge-Kutta 4) ---
dt = 0.01
while True:
    rate(100)
    for item in objetos:
        # En este caso alpha es CONSTANTE, por lo que k1, k2, k3 y k4 son iguales.
        
        def alpha_actual(w):
            # Aquí podrías agregar fricción: return (tau / item['I']) - 0.1*w
            return tau / item['I']
        
        # k1 (Pendiente inicial)
        k1_w = alpha_actual(item['omega'])
        k1_th = item['omega']
        
        # k2 (Pendiente a la mitad)
        k2_w = alpha_actual(item['omega'] + 0.5 * dt * k1_w)
        k2_th = item['omega'] + 0.5 * dt * k1_w
        
        # k3 (Pendiente a la mitad)
        k3_w = alpha_actual(item['omega'] + 0.5 * dt * k2_w)
        k3_th = item['omega'] + 0.5 * dt * k2_w
        
        # k4 (Pendiente al final)
        k4_w = alpha_actual(item['omega'] + dt * k3_w)
        k4_th = item['omega'] + dt * k3_w
        
        # Actualización (Promedio ponderado)
        item['omega'] += (dt / 6.0) * (k1_w + 2*k2_w + 2*k3_w + k4_w)
        d_theta = (dt / 6.0) * (k1_th + 2*k2_th + 2*k3_th + k4_th)
        
        # Rotación del objeto
        item['obj'].rotate(angle=d_theta, axis=item['eje'], origin=item['centro'])
