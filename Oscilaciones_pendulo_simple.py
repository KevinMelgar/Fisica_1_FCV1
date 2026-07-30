Web VPython 3.2

# --- Configuración de la Escena 3D ---
scene.width = 600
scene.height = 300
scene.background = color.white
scene.title = "Péndulo Simple"
color_azul = vector(0, 85/255, 164/255)

techo = box(pos=vector(0, 2, 0), size=vector(4, 0.2, 2), color=color.gray(0.5))
masa = sphere(pos=vector(0, -1, 0), radius=0.4, color=color_azul)
cuerda = cylinder(pos=techo.pos, axis=masa.pos - techo.pos, radius=0.05, color=color.gray(0.7))

# --- Gráficas ---
grafica_cinematica = graph(title="Cinemática Angular", xtitle="Tiempo (s)", ytitle="Amplitud", width=600, height=250, background=color.white)
curva_theta = gcurve(color=color_azul, label="Pos. Angular (rad)")
curva_omega = gcurve(color=color.orange, label="Vel. Angular (rad/s)")
curva_alpha = gcurve(color=color.red, label="Acel. Angular (rad/s^2)")

grafica_energia = graph(title="Energías", xtitle="Tiempo (s)", ytitle="Energía (J)", width=600, height=250, background=color.white)
curva_k = gcurve(color=color.green, label="Cinética")
curva_u = gcurve(color=color.purple, label="Potencial")
curva_e = gcurve(color=color.black, label="Mecánica Total")

# --- Parámetros Físicos ---
A = 0.3       
phi = 0       
g = 9.81      
L = 3.0       
m_pendulo = 2.0 
omega_osc = sqrt(g / L)

t = 0
dt = 0.01

# --- Bucle de Simulación ---
while t < 10:
    rate(100)
    
    # Ecuaciones Cinemáticas (Angulares)
    theta_t = A * sin(omega_osc * t + phi)
    vel_ang_t = A * omega_osc * cos(omega_osc * t + phi)
    acel_ang_t = -A * omega_osc**2 * sin(omega_osc * t + phi)
    
    # Ecuaciones de Energía (usando geometría exacta)
    v_tangencial = L * vel_ang_t
    h = L * (1 - cos(theta_t))
    K = 0.5 * m_pendulo * (v_tangencial**2)
    U = m_pendulo * g * h
    E = K + U
    
    # Actualización 3D
    masa.pos = techo.pos + vector(L * sin(theta_t), -L * cos(theta_t), 0)
    cuerda.axis = masa.pos - techo.pos
    
    # Trazado de Gráficas
    curva_theta.plot(t, theta_t)
    curva_omega.plot(t, vel_ang_t)
    curva_alpha.plot(t, acel_ang_t)
    curva_k.plot(t, K)
    curva_u.plot(t, U)
    curva_e.plot(t, E)
    
    t = t + dt
