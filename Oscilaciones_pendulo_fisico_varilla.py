Web VPython 3.2

# --- Configuración de la Escena 3D ---
scene.width = 600
scene.height = 300
scene.background = color.white
scene.title = "Péndulo Físico (Varilla)"
color_azul = vector(0, 85/255, 164/255)

pivote = cylinder(pos=vector(0, 2, -0.2), axis=vector(0, 0, 0.4), radius=0.1, color=color.red)
varilla = cylinder(pos=pivote.pos, axis=vector(0, -3, 0), radius=0.15, color=color_azul)

# --- Gráficas ---
grafica_cinematica = graph(title="Cinemática Angular", xtitle="Tiempo (s)", ytitle="Amplitud", width=600, height=250, background=color.white)
curva_theta = gcurve(color=color_azul, label="Pos. Angular (rad)")
curva_omega = gcurve(color=color.orange, label="Vel. Angular (rad/s)")
curva_alpha = gcurve(color=color.red, label="Acel. Angular (rad/s^2)")

grafica_energia = graph(title="Energías", xtitle="Tiempo (s)", ytitle="Energía (J)", width=600, height=250, background=color.white)
curva_k = gcurve(color=color.green, label="Cinética Rotacional")
curva_u = gcurve(color=color.purple, label="Potencial")
curva_e = gcurve(color=color.black, label="Mecánica Total")

# --- Parámetros Físicos ---
A = 0.4       
phi = 0       
g = 9.81      
m = 2.0       
L = 3.0       
d = L / 2.0   
I = (1.0 / 3.0) * m * L**2
omega_osc = sqrt((m * g * d) / I)

t = 0
dt = 0.01

# --- Bucle de Simulación ---
while t < 10:
    rate(100)
    
    # Ecuaciones Cinemáticas
    theta_t = A * sin(omega_osc * t + phi)
    vel_ang_t = A * omega_osc * cos(omega_osc * t + phi)
    acel_ang_t = -A * omega_osc**2 * sin(omega_osc * t + phi)
    
    # Ecuaciones de Energía
    h_cm = d * (1 - cos(theta_t))
    K = 0.5 * I * (vel_ang_t**2)
    U = m * g * h_cm
    E = K + U
    
    # Actualización 3D
    varilla.axis = vector(L * sin(theta_t), -L * cos(theta_t), 0)
    
    # Trazado de Gráficas
    curva_theta.plot(t, theta_t)
    curva_omega.plot(t, vel_ang_t)
    curva_alpha.plot(t, acel_ang_t)
    curva_k.plot(t, K)
    curva_u.plot(t, U)
    curva_e.plot(t, E)
    
    t = t + dt
