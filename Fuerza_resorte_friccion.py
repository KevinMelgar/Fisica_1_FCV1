Web VPython 3.2

# --- Configuración de la Escena 3D ---
scene.width = 800
scene.height = 500
scene.background = color.white
scene.title = "Fricción Seca: Efecto del Material"
scene.center = vector(0, 0, 0)
scene.forward = vector(0, 0, -1)

# ==========================================================
# SELECCIÓN DE MATERIAL (Descomenta solo uno de los bloques)
# ==========================================================

# --- OPCIÓN 1: HIELO (Poca fricción) ---
material = "Hielo"
mu = 0.05
color_riel = color.cyan

# --- OPCIÓN 2: MADERA (Fricción media) ---
#material = "Madera"
#mu = 0.3
#color_riel = color.orange

# --- OPCIÓN 3: GOMA (Mucha fricción) ---
#material = "Goma"
#mu = 0.8
#color_riel = color.gray(0.2)

# ==========================================================

# --- Parámetros Físicos ---
L = 1.20       # Distancia vertical al anclaje (m)
k = 40.0       # Constante del resorte (N/m)
m = 1.0        # Masa (kg)
g = 9.8        # Gravedad (m/s^2) - Necesaria para la Fuerza Normal
x = 0.500      # Posición inicial (m)
v = 0.0        # Velocidad inicial (m/s)
dt = 0.01      # Paso de tiempo

# Variables para la gráfica de energía
E_inicial = 0.0
trabajo_friccion = 0.0

# --- Función de Aceleración (CON FRICCIÓN SECA) ---
def calcular_aceleracion(pos_x, vel_x):
    # 1. Fuerza de los resortes (No lineal)
    distancia = sqrt(pos_x**2 + L**2)
    fuerza_resortes = -2 * k * pos_x * (1 - L / distancia)
    
    # 2. Fuerza de fricción seca
    # La Fuerza Normal es N = m * g (asumiendo riel horizontal)
    N = m * g
    umbral = 0.001 # Para evitar división por cero y manejar el "sticking"
    
    if abs(vel_x) > umbral:
        # Fricción cinética (se está moviendo)
        # Se opone a la velocidad: F = -mu * N * signo(v)
        fuerza_friccion = -mu * N * (vel_x / abs(vel_x))
    else:
        # Fricción estática (evaluar si la masa se queda pegada)
        if abs(fuerza_resortes) > mu * N:
            # La fuerza del resorte supera la fricción estática, se mueve
            fuerza_friccion = -mu * N * (fuerza_resortes / abs(fuerza_resortes))
        else:
            # La fricción estática cancela exactamente la fuerza del resorte
            # La masa se queda quieta
            fuerza_friccion = -fuerza_resortes
            
    # 3. Fuerza Neta
    fuerza_neta = fuerza_resortes + fuerza_friccion
    
    return fuerza_neta / m, fuerza_friccion

# --- Objetos Visuales ---
riel = box(pos=vector(0, 0, 0), size=vector(6, 0.05, 0.2), color=color_riel)
anclaje_sup = sphere(pos=vector(0, L, 0), radius=0.08, color=color.black)
anclaje_inf = sphere(pos=vector(0, -L, 0), radius=0.08, color=color.black)
masa = sphere(pos=vector(x, 0, 0), radius=0.15, color=vector(0, 85/255, 164/255), make_trail=True)

resorte_sup = helix(pos=anclaje_sup.pos, axis=masa.pos - anclaje_sup.pos, radius=0.1, coils=15, thickness=0.03, color=color.gray(0.6))
resorte_inf = helix(pos=anclaje_inf.pos, axis=masa.pos - anclaje_inf.pos, radius=0.1, coils=15, thickness=0.03, color=color.gray(0.6))

# --- Etiquetas ---
etiqueta_material = label(pos=vector(0, 1.5, 0), text=f"Material: {material}\nμ = {mu}", height=15, color=color.black, box=False)
etiqueta_info = label(pos=vector(0, -1.8, 0), text="", height=15, color=color.black, box=False)

# --- Gráficas ---
g_energia = graph(title="Balance de Energía (Fricción Seca)", xtitle="Tiempo (s)", ytitle="Energía (J)", width=500, height=250, background=color.white)
curva_K = gcurve(color=color.green, label="Cinética (K)")
curva_U = gcurve(color=color.purple, label="Potencial (U)")
curva_E = gcurve(color=color.black, label="Mecánica Total (E)")
curva_Calor = gcurve(color=color.red, label="Energía Disipada (Calor)")

# --- Bucle de Simulación ---
t = 0
while t < 15:
    rate(200)
    
    # ==========================================
    # INTEGRACIÓN RUNGE-KUTTA 4 (RK4)
    # ==========================================
    # k1
    k1_x = v
    k1_v, _ = calcular_aceleracion(x, v)
    
    # k2
    k2_x = v + 0.5 * dt * k1_v
    k2_v, _ = calcular_aceleracion(x + 0.5 * dt * k1_x, v + 0.5 * dt * k1_v)
    
    # k3
    k3_x = v + 0.5 * dt * k2_v
    k3_v, _ = calcular_aceleracion(x + 0.5 * dt * k2_x, v + 0.5 * dt * k2_v)
    
    # k4
    k4_x = v + dt * k3_v
    k4_v, _ = calcular_aceleracion(x + dt * k3_x, v + dt * k3_v)
    
    # Guardar posición anterior para calcular el trabajo
    x_anterior = x
    
    # Actualización de posición y velocidad
    x = x + (dt / 6.0) * (k1_x + 2*k2_x + 2*k3_x + k4_x)
    v = v + (dt / 6.0) * (k1_v + 2*k2_v + 2*k3_v + k4_v)
    
    # ==========================================
    
    # Calcular trabajo de la fricción (W = F * dx)
    _, fuerza_friccion_actual = calcular_aceleracion(x, v)
    dx = x - x_anterior
    trabajo_friccion += fuerza_friccion_actual * dx
    
    # Actualizar la posición visual
    masa.pos = vector(x, 0, 0)
    resorte_sup.axis = masa.pos - anclaje_sup.pos
    resorte_inf.axis = masa.pos - anclaje_inf.pos
    
    # Calcular Energías
    distancia_hipotenusa = sqrt(x**2 + L**2)
    U = k * x**2 + 2 * k * L * (L - distancia_hipotenusa)
    K = 0.5 * m * v**2
    E = K + U
    
    # La energía disipada es el trabajo negativo de la fricción
    # (lo ponemos positivo para la gráfica)
    Energia_Disipada = -trabajo_friccion
    
    if t == 0:
        E_inicial = E
        
    # Graficar
    curva_K.plot(t, K)
    curva_U.plot(t, U)
    curva_E.plot(t, E)
    curva_Calor.plot(t, Energia_Disipada)
    
    etiqueta_info.text = f"t = {t:.2f} s\nx = {x:.4f} m\nv = {v:.4f} m/s\nE_mec = {E:.4f} J"
    
    t = t + dt
