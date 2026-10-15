Web VPython 3.2

# --- Configuración de la Escena 3D ---
scene.width = 800
scene.height = 400
scene.background = color.white
scene.title = "Oscilador No Lineal - Runge-Kutta 4"
scene.center = vector(0, 0, 0)
scene.forward = vector(0, 0, -1)

# --- Parámetros Físicos ---
L = 1.20       # Distancia vertical al anclaje (m)
k = 40.0       # Constante del resorte (N/m)
m = 1.0        # Masa (kg)
x = 0.500      # Posición inicial (m)
v = 0.0        # Velocidad inicial (m/s)
dt = 0.01      # Paso de tiempo (¡Con RK4 puedes usar un dt más grande!)

# --- Función de Aceleración ---
def calcular_aceleracion(pos_x):
    # Ecuación no lineal: F = -2kx(1 - L / sqrt(x^2 + L^2))
    distancia = sqrt(pos_x**2 + L**2)
    fuerza = -2 * k * pos_x * (1 - L / distancia)
    return fuerza / m

# --- Objetos Visuales ---
riel = box(pos=vector(0, 0, 0), size=vector(6, 0.05, 0.2), color=color.gray(0.8))
anclaje_sup = sphere(pos=vector(0, L, 0), radius=0.08, color=color.black)
anclaje_inf = sphere(pos=vector(0, -L, 0), radius=0.08, color=color.black)
masa = sphere(pos=vector(x, 0, 0), radius=0.15, color=vector(0, 85/255, 164/255), make_trail=True)

resorte_sup = helix(pos=anclaje_sup.pos, axis=masa.pos - anclaje_sup.pos, radius=0.1, coils=15, thickness=0.03, color=color.gray(0.6))
resorte_inf = helix(pos=anclaje_inf.pos, axis=masa.pos - anclaje_inf.pos, radius=0.1, coils=15, thickness=0.03, color=color.gray(0.6))

# --- Gráficas ---
g_energia = graph(title="Energías vs Tiempo (RK4)", xtitle="Tiempo (s)", ytitle="Energía (J)", width=400, height=250, background=color.white)
curva_K = gcurve(color=color.green, label="Cinética (K)")
curva_U = gcurve(color=color.purple, label="Potencial (U)")
curva_E = gcurve(color=color.black, label="Mecánica Total (E)")

g_potencial = graph(title="Energía Potencial U(x)", xtitle="Posición x (m)", ytitle="U (J)", width=400, height=250, background=color.white)
curva_Ux = gcurve(color=color.purple, label="U(x)")
punto_actual = gdots(color=color.red, radius=4, label="Estado actual")

etiqueta_info = label(pos=vector(0, -2, 0), text="", height=15, color=color.black, box=False)

# --- Bucle de Simulación ---
t = 0
while t < 10:
    rate(200)
    
    # ==========================================
    # INTEGRACIÓN RUNGE-KUTTA 4 (RK4)
    # ==========================================
    
    # k1 (Pendiente al inicio del intervalo)
    k1_x = v
    k1_v = calcular_aceleracion(x)
    
    # k2 (Pendiente a la mitad, usando k1)
    k2_x = v + 0.5 * dt * k1_v
    k2_v = calcular_aceleracion(x + 0.5 * dt * k1_x)
    
    # k3 (Pendiente a la mitad, usando k2)
    k3_x = v + 0.5 * dt * k2_v
    k3_v = calcular_aceleracion(x + 0.5 * dt * k2_x)
    
    # k4 (Pendiente al final del intervalo, usando k3)
    k4_x = v + dt * k3_v
    k4_v = calcular_aceleracion(x + dt * k3_x)
    
    # Actualización de posición y velocidad (Promedio ponderado)
    x = x + (dt / 6.0) * (k1_x + 2*k2_x + 2*k3_x + k4_x)
    v = v + (dt / 6.0) * (k1_v + 2*k2_v + 2*k3_v + k4_v)
    
    # ==========================================
    
    # Actualizar la posición visual
    masa.pos = vector(x, 0, 0)
    resorte_sup.axis = masa.pos - anclaje_sup.pos
    resorte_inf.axis = masa.pos - anclaje_inf.pos
    
    # Calcular Energías
    distancia_hipotenusa = sqrt(x**2 + L**2)
    U = k * x**2 + 2 * k * L * (L - distancia_hipotenusa)
    K = 0.5 * m * v**2
    E = K + U
    
    # Graficar
    curva_K.plot(t, K)
    curva_U.plot(t, U)
    curva_E.plot(t, E)
    punto_actual.plot(x, U)
    
    etiqueta_info.text = f"t = {t:.2f} s\nx = {x:.4f} m\nv = {v:.4f} m/s\nE_total = {E:.4f} J"
    
    t = t + dt
