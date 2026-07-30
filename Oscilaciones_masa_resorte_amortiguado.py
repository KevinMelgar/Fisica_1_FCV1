Web VPython 3.2

# --- Configuración de la Escena 3D ---
scene.width = 600
scene.height = 400
scene.background = color.white
scene.title = "Sistema Masa-Resorte Amortiguado"

# Color azul de la plantilla
color_azul = vector(0, 85/255, 164/255)

# --- Parámetros Físicos ---
A = 1.0       
phi = 0       
k = 20.0      
m = 2.0       
b = 0.8       # Constante de amortiguamiento (kg/s)

gamma = b / (2 * m)
omega_d = sqrt((k / m) - gamma**2)

y_equilibrio = -1.5
x_inicial = A * sin(phi) 

# --- Objetos Visuales ---
techo = box(pos=vector(0, 2, 0), size=vector(4, 0.2, 2), color=color.gray(0.5))

# 1. Masa
masa = box(pos=vector(0, y_equilibrio + x_inicial, 0), size=vector(0.8, 0.8, 0.8), color=color_azul)

# 2. Resorte Superior
punto_conexion_sup = vector(0, masa.pos.y + 0.4, 0)
resorte = helix(pos=techo.pos, axis=punto_conexion_sup - techo.pos, radius=0.3, coils=10, thickness=0.05, color=color.gray(0.7))

# 3. Amortiguador Viscoso (Dashpot) Inferior
# Contenedor de fluido (transparente para ver el pistón)
contenedor = box(pos=vector(0, -4.0, 0), size=vector(1.5, 2.5, 1.5), color=vector(0.2, 0.7, 0.8), opacity=0.3)
# Varilla conectada debajo de la masa
punto_conexion_inf = vector(0, masa.pos.y - 0.4, 0)
varilla = cylinder(pos=punto_conexion_inf, axis=vector(0, -1.5, 0), radius=0.08, color=color.gray(0.4))
# Disco del pistón sumergido en el fluido
disco = cylinder(pos=varilla.pos + varilla.axis, axis=vector(0, -0.1, 0), radius=0.6, color=color.gray(0.2))

# --- Gráficas ---
grafica_cinematica = graph(title="Cinemática (Subamortiguada)", xtitle="Tiempo (s)", ytitle="Amplitud", width=600, height=250, background=color.white)
curva_x = gcurve(color=color_azul, label="Posición (m)")
curva_v = gcurve(color=color.orange, label="Velocidad (m/s)")
curva_a = gcurve(color=color.red, label="Aceleración (m/s^2)")

grafica_energia = graph(title="Energías", xtitle="Tiempo (s)", ytitle="Energía (J)", width=600, height=250, background=color.white)
curva_k = gcurve(color=color.green, label="Cinética")
curva_u = gcurve(color=color.purple, label="Potencial")
curva_e = gcurve(color=color.black, label="Mecánica Total")

t = 0
dt = 0.01

# --- Bucle de Simulación ---
while t < 20:
    rate(100)
    
    decaimiento = exp(-gamma * t)
    
    # Ecuaciones Cinemáticas
    x_t = A * decaimiento * sin(omega_d * t + phi)
    v_t = A * decaimiento * (omega_d * cos(omega_d * t + phi) - gamma * sin(omega_d * t + phi))
    a_t = A * decaimiento * ((gamma**2 - omega_d**2) * sin(omega_d * t + phi) - 2 * gamma * omega_d * cos(omega_d * t + phi))
    
    # Ecuaciones de Energía
    K = 0.5 * m * (v_t**2)
    U = 0.5 * k * (x_t**2)
    E = K + U
    
    # --- Actualización 3D ---
    # Mover la masa
    masa.pos = vector(0, y_equilibrio + x_t, 0)
    
    # Estirar/comprimir el resorte
    punto_conexion_sup = vector(0, masa.pos.y + 0.4, 0)
    resorte.axis = punto_conexion_sup - techo.pos
    
    # Mover el amortiguador (varilla y disco)
    punto_conexion_inf = vector(0, masa.pos.y - 0.4, 0)
    varilla.pos = punto_conexion_inf
    disco.pos = varilla.pos + varilla.axis
    
    # --- Trazado de Gráficas ---
    curva_x.plot(t, x_t)
    curva_v.plot(t, v_t)
    curva_a.plot(t, a_t)
    curva_k.plot(t, K)
    curva_u.plot(t, U)
    curva_e.plot(t, E)
    
    t = t + dt
