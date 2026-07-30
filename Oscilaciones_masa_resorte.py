Web VPython 3.2

# --- Configuración de la Escena 3D ---
scene.width = 600
scene.height = 300
scene.background = color.white
scene.title = "Sistema Masa-Resorte"
color_azul = vector(0, 85/255, 164/255)

techo = box(pos=vector(0, 2, 0), size=vector(4, 0.2, 2), color=color.gray(0.5))
masa = box(pos=vector(0, 0, 0), size=vector(0.8, 0.8, 0.8), color=color_azul)
resorte = helix(pos=techo.pos, axis=masa.pos - techo.pos, radius=0.3, coils=10, thickness=0.05, color=color.gray(0.7))

# --- Gráficas ---
grafica_cinematica = graph(title="Cinemática", xtitle="Tiempo (s)", ytitle="Amplitud", width=600, height=250, background=color.white)
curva_x = gcurve(color=color_azul, label="Posición (m)")
curva_v = gcurve(color=color.orange, label="Velocidad (m/s)")
curva_a = gcurve(color=color.red, label="Aceleración (m/s^2)")

grafica_energia = graph(title="Energías", xtitle="Tiempo (s)", ytitle="Energía (J)", width=600, height=250, background=color.white)
curva_k = gcurve(color=color.green, label="Cinética")
curva_u = gcurve(color=color.purple, label="Potencial")
curva_e = gcurve(color=color.black, label="Mecánica Total")

# --- Parámetros Físicos ---
A = 1.0       
phi = 0       
k = 20.0      
m = 2.0       
omega = sqrt(k / m)

t = 0
dt = 0.01

# --- Bucle de Simulación ---
while t < 10:
    rate(100)
    
    # Ecuaciones Cinemáticas
    x_t = A * sin(omega * t + phi)
    v_t = A * omega * cos(omega * t + phi)
    a_t = -A * omega**2 * sin(omega * t + phi)
    
    # Ecuaciones de Energía
    K = 0.5 * m * (v_t**2)
    U = 0.5 * k * (x_t**2)
    E = K + U
    
    # Actualización 3D
    masa.pos.y = -1.5 + x_t 
    resorte.axis = masa.pos - techo.pos
    
    # Trazado de Gráficas
    curva_x.plot(t, x_t)
    curva_v.plot(t, v_t)
    curva_a.plot(t, a_t)
    curva_k.plot(t, K)
    curva_u.plot(t, U)
    curva_e.plot(t, E)
    
    t = t + dt
