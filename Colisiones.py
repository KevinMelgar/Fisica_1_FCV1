import numpy as np

# [INVESTIGA]: ¿Por qué el coeficiente de restitución (e) determina el tipo de choque? ¿Qué significa e=1.0?
e = 1.0

# Bola 1
m1 = 0.50
# [PISTA]: A diferencia de las masas puntuales, en videojuegos/simulaciones los radios son vitales. ¿Por qué?
r1 = 0.15  
p1 = np.array([-1.00, -0.50]) 
v1 = np.array([1.00, 0.30])   

# Bola 2
m2 = 1.50
r2 = 0.25  
p2 = np.array([0.90, 0.50])   
v2 = np.array([-0.50, -0.50]) 



# 1. PREDICCIÓN DEL TIEMPO DE IMPACTO
# [INVESTIGA]: Aquí evaluamos la distancia relativa. 
# Si D(t) = P2(t) - P1(t), ¿cómo se relaciona la cinemática básica (P = P0 + v*t) con dp y dv?
dp = p2 - p1 
dv = v2 - v1 
suma_radios = r1 + r2

# [PISTA MATEMÁTICA]: Esta es una ecuación cuadrática (at^2 + bt + c = 0). 
# Nace de igualar la magnitud de la distancia al cuadrado con la suma de los radios al cuadrado.
# Investiga: ¿Qué representa el producto punto (np.dot) de un vector por sí mismo?
a = np.dot(dv, dv)
b = 2 * np.dot(dp, dv)
c = np.dot(dp, dp) - suma_radios**2

# [PREGUNTA GUÍA]: Si el discriminante es negativo, t no tiene solución real. 
# Físicamente, ¿qué nos dice esto sobre las trayectorias de las bolas en el espacio 2D?
discriminante = b**2 - 4 * a * c

t_impacto = -1 

if discriminante >= 0 and a != 0:
    # [PISTA]: Fórmula general. ¿Por qué obtenemos dos tiempos (t1 y t2)? ¿Qué representan geométricamente?
    t1 = (-b - np.sqrt(discriminante)) / (2 * a)
    t2 = (-b + np.sqrt(discriminante)) / (2 * a)
    
    # [PREGUNTA GUÍA]: ¿Por qué nos interesa estrictamente el primer tiempo que sea mayor a cero?
    if t1 > 0:
        t_impacto = t1
    elif t2 > 0:
        t_impacto = t2
    print(f'Tiempo: {t_impacto}')



# 2. RESOLUCIÓN DE LA COLISIÓN (REDUCCIÓN DE 2D A 1D)
if t_impacto > 0:
    print(f"¡COLISIÓN DETECTADA! Ocurrirá en t = {t_impacto:.4f} segundos.\n")
    
    # [PREGUNTA GUÍA]: ¿Por qué es un error fatal usar las posiciones p1 y p2 (t=0) para calcular la geometría del rebote?
    p1_impacto = p1 + v1 * t_impacto
    p2_impacto = p2 + v2 * t_impacto
    
    # [INVESTIGA]: Creación de un "Sistema de Coordenadas Local".
    dx = p2_impacto[0] - p1_impacto[0]
    dy = p2_impacto[1] - p1_impacto[1]
    distancia = np.sqrt(dx**2 + dy**2)
    
    # [PISTA]: Estos son los Vectores Unitarios. ¿Por qué su magnitud debe ser exactamente 1?
    un_x = dx / distancia
    un_y = dy / distancia
    
    # [INVESTIGA]: Observa cómo se define el eje tangencial respecto al normal. 
    # ¿Qué transformación matemática (giro) ocurre al cruzar las coordenadas X e Y y cambiar un signo?
    ut_x = -un_y
    ut_y = un_x
    
    # [PREGUNTA GUÍA]: Proyección Escalar. Al multiplicar las velocidades X e Y de la pantalla por los unitarios,
    # ¿qué le estamos haciendo a la perspectiva del problema? (Pista: Piensa en rotar el mundo).
    v1n = (v1[0] * un_x) + (v1[1] * un_y)
    v1t = (v1[0] * ut_x) + (v1[1] * ut_y)
    
    v2n = (v2[0] * un_x) + (v2[1] * un_y)
    v2t = (v2[0] * ut_x) + (v2[1] * ut_y)
    
    # [INVESTIGA]: ¡La magia 1D! Reconoce estas fórmulas. ¿De dónde provienen? 
    # ¿Por qué solo se aplican a la velocidad normal ('n') y no tocamos la velocidad tangencial ('t')?
    suma_masas = m1 + m2
    v1nf = ((m1 - e * m2) / suma_masas) * v1n + (((1 + e) * m2) / suma_masas) * v2n
    v2nf = (((1 + e) * m1) / suma_masas) * v1n + ((m2 - e * m1) / suma_masas) * v2n
    
    # [PISTA]: Reconstrucción. Ahora ''des-rotamos'' el mundo combinando la nueva velocidad de impacto (normal) 
    # con la velocidad de deslizamiento (tangencial) para devolverle al juego coordenadas X e Y estándar.
    v1fx = (v1nf * un_x) + (v1t * ut_x)
    v1fy = (v1nf * un_y) + (v1t * ut_y)
    
    v2fx = (v2nf * un_x) + (v2t * ut_x)
    v2fy = (v2nf * un_y) + (v2t * ut_y)
    
    print("--- RESULTADOS DE VELOCIDAD ---")
    print(f"Bola 1 Velocidad Final: vx = {v1fx:.4f}, vy = {v1fy:.4f}")
    print(f"Bola 2 Velocidad Final: vx = {v2fx:.4f}, vy = {v2fy:.4f}")
    
    
    # 3. CÁLCULO DE DIRECCIONES (ÁNGULOS)
    # [PREGUNTA GUÍA]: ¿Por qué en programación física se usa arctan2(y,x) en lugar de la tangente inversa tradicional arctan(y/x)?
    angulo_bola1 = np.degrees(np.arctan2(v1fy, v1fx))
    angulo_bola2 = np.degrees(np.arctan2(v2fy, v2fx))
    
    print("\n--- DIRECCIONES FINALES ---")
    print(f"Ángulo de salida Bola 1: {angulo_bola1:.2f}°")
    print(f"Ángulo de salida Bola 2: {angulo_bola2:.2f}°")
    
else:
    print("Las trayectorias de las bolas nunca se cruzan. No hay colisión.")
