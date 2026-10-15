Web VPython 3.2

# --- Configuración de la Escena 3D ---
scene.width = 800
scene.height = 500
scene.background = color.white
scene.title = "Oscilador No Lineal en Diferentes Fluidos"
scene.center = vector(0, 0, 0)
scene.forward = vector(0, 0, -1)

# ==========================================================
# SELECCIÓN DE FLUIDO (Descomenta solo uno de los bloques)
# ==========================================================

# --- OPCIÓN 1: AIRE (Poca resistencia) ---
#fluido_nombre = "Aire"
#b = 0.1          # Coeficiente de fricción viscosa (kg/s)
#fluido_color = color.white
#fluido_opacidad = 0.0  # Invisible, pero el aire está ahí

# --- OPCIÓN 2: AGUA (Resistencia media) ---
# fluido_nombre = "Agua"
# b = 0.8
# fluido_color = color.cyan
# fluido_opacidad = 0.3  # Semitransparente para ver los resortes

# --- OPCIÓN 3: ACEITE (Alta resistencia) ---
fluido_nombre = "Aceite"
b = 5.0
fluido_color = color.orange
fluido_opacidad = 0.5  # Más opaco para simular densidad

# ==========================================================

# --- Parámetros Físicos ---
L = 1.20       # Distancia vertical al anclaje (m)
k = 40.0       # Constante del resorte (N/m)
m = 1.0        # Masa (kg)
x = 0.500      # Posición inicial (m)
v = 0.0        # Velocidad inicial (m/s)
dt = 0.01      # Paso de tiempo

# --- Función de Aceleración (Fricción Viscosa) ---
def calcular_aceleracion(pos_x, vel_x):
    # 1. Fuerza de los resortes (No lineal)
    distancia = sqrt(pos_x**2 + L**2)
    fuerza_resortes = -2 * k * pos_x * (1 - L / distancia)
    
    # 2. Fuerza de fricción viscosa (Resistencia del fluido)
    fuerza_friccion = -b * vel_x
    
    # 3. Fuerza Neta
    fuerza_neta = fuerza_resortes + fuerza_friccion
    
    return fuerza_neta / m

# --- Objetos Visuales ---
# El contenedor del fluido (una caja grande alrededor del sistema)
contenedor_fluido = box(pos=vector(0, 0, 0), size=vector(6, 4, 2), 
                        color=fluido_color, opacity=fluido_opacidad)

riel = box(pos=vector(0, 0, 0), size=vector(6, 0.05, 0.2), color=color.gray(0.8))
anclaje_sup = sphere(pos=vector(0, L, 0), radius=0.08, color=color.black)
anclaje_inf = sphere(pos=vector(0, -L, 0), radius=0.08, color=color.black)
masa = sphere(pos=vector(x, 0, 0), radius=0.15, color=vector(0, 85/255, 164/255), make_trail=True)

resorte_sup = helix(pos=anclaje_sup.pos, axis=masa.pos - anclaje_sup.pos, radius=0.1, coils=15, thickness=0.03, color=color.gray(0.6))
resorte_inf = helix(pos=anclaje_inf.pos, axis=masa.pos - anclaje_inf.pos, radius=0.1, coils=15, thickness=0.03, color=color.gray(0.6))

# --- Etiquetas ---
etiqueta_fluido = label(pos=vector(0, 2.5, 0), text=f"Fluido: {fluido_nombre}\nb = {b} kg/s", height=15, color=color.black, box=False)
etiqueta_info = label(pos=vector(0, -2.5, 0), text="", height=15, color=color.black, box=False)

# --- Gráficas ---
g_energia = graph(title=f"Energías en {fluido_nombre}", xtitle="Tiempo (s)", ytitle="Energía (J)", width=500, height=250, background=color.white)
curva_K = gcurve(color=color.green, label="Cinética (K)")
curva_U = gcurve(color=color.purple, label="Potencial (U)")
curva_E = gcurve(color=color.black, label="Mecánica Total (E)")

g_potencial = graph(title="Energía Potencial U(x)", xtitle="Posición x (m)", ytitle="U (J)", width=500, height=250, background=color.white)
curva_Ux = gcurve(color=color.purple, label="U(x)")
punto_actual = gdots(color=color.red, radius=4, label="Estado actual")

# --- Bucle de Simulación ---
t = 0
while t < 15:
    rate(200)
    
    # ==========================================
    # INTEGRACIÓN RUNGE-KUTTA 4 (RK4)
    # ==========================================
    # k1
    k1_x = v
    k1_v = calcular_aceleracion(x, v)
    
    # k2
    k2_x = v + 0.5 * dt * k1_v
    k2_v = calcular_aceleracion(x + 0.5 * dt * k1_x, v + 0.5 * dt * k1_v)
    
    # k3
    k3_x = v + 0.5 * dt * k2_v
    k3_v = calcular_aceleracion(x + 0.5 * dt * k2_x, v + 0.5 * dt * k2_v)
    
    # k4
    k4_x = v + dt * k3_v
    k4_v = calcular_aceleracion(x + dt * k3_x, v + dt * k3_v)
    
    # Actualización
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
    
    etiqueta_info.text = f"t = {t:.2f} s\nx = {x:.4f} m\nv = {v:.4f} m/s\nE_mec = {E:.4f} J"
    
    t = t + dt
