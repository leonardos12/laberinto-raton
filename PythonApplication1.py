PUNTOS_MINIMOS = 23
 
# Laberinto original (9 x 9). 'I' = inicio, 'F' = llegada.
LABERINTO = [
    ["F", 1, 1, 3, 0, 1, 1, 1, 4],
    [3, 0, 0, 1, 0, 1, 0, 0, 1],
    [1, 1, 0, 1, 1, 1, 1, 0, 1],
    [0, 1, 0, 1, 0, 0, 1, 0, 1],
    [1, 1, 1, 1, 1, 1, 3, 1, 1],
    [3, 0, 1, 0, 0, 0, 1, 0, 1],
    [1, 1, 1, 1, 3, 1, 1, 1, 1],
    [1, 0, 0, 1, 0, 1, 0, 0, 4],
    ["I", 1, 3, 1, 0, 1, 1, 1, 1],
]
 
# Orden pedido: arriba, derecha, abajo, izquierda  (fila, columna)
MOVIMIENTOS = [(-1, 0), (0, 1), (1, 0), (0, -1)]
 
 
def valor_celda(laberinto, f, c):
    """Devuelve el valor numérico de la celda (I y F equivalen a 1)."""
    v = laberinto[f][c]
    return 1 if v in ("I", "F") else v
 
 
def imprimir_matriz(matriz, titulo):
    """Imprime una matriz con formato alineado."""
    print(f"\n{titulo}")
    print("+" + "---+" * len(matriz[0]))
    for fila in matriz:
        print("|" + "|".join(f"{str(x):^3}" for x in fila) + "|")
        print("+" + "---+" * len(matriz[0]))
 
 
def es_valida(laberinto, visitado, f, c):
    """Dentro de límites, no es pared (0) y no fue visitada en este camino."""
    n = len(laberinto)
    m = len(laberinto[0])
    return (
        0 <= f < n
        and 0 <= c < m
        and valor_celda(laberinto, f, c) != 0
        and not visitado[f][c]
    )
 
 
def resolver(laberinto, f, c, destino, visitado, camino, puntos):
    """
    Backtracking.
    - f, c: celda actual (ya incluida en 'camino' y sumada en 'puntos').
    - Retorna True si encontró un camino a F con puntos >= PUNTOS_MINIMOS.
    """
    # Caso base: llegó a la meta
    if (f, c) == destino:
        return puntos >= PUNTOS_MINIMOS  # si no alcanza, se prueba otra alternativa
 
    for df, dc in MOVIMIENTOS:
        nf, nc = f + df, c + dc
        if es_valida(laberinto, visitado, nf, nc):
            # Elegir
            visitado[nf][nc] = True
            camino.append((nf, nc))
            # Explorar
            if resolver(
                laberinto, nf, nc, destino, visitado, camino,
                puntos + valor_celda(laberinto, nf, nc),
            ):
                return True
            # Deshacer (backtrack)
            camino.pop()
            visitado[nf][nc] = False
 
    return False
 
 
def construir_matriz_solucion(laberinto, camino):
    """Matriz con el recorrido numerado (paso 1, 2, 3...); '.' = no usada, '#' = pared."""
    n, m = len(laberinto), len(laberinto[0])
    sol = [["#" if valor_celda(laberinto, i, j) == 0 else "." for j in range(m)] for i in range(n)]
    for paso, (f, c) in enumerate(camino, start=1):
        sol[f][c] = paso
    return sol
 
 
def construir_matriz_flechas(laberinto, camino):
    """Matriz con flechas que indican hacia dónde avanza el ratón."""
    n, m = len(laberinto), len(laberinto[0])
    flechas = {(-1, 0): "↑", (0, 1): "→", (1, 0): "↓", (0, -1): "←"}
    sol = [["#" if valor_celda(laberinto, i, j) == 0 else "." for j in range(m)] for i in range(n)]
    for k in range(len(camino) - 1):
        (f1, c1), (f2, c2) = camino[k], camino[k + 1]
        sol[f1][c1] = flechas[(f2 - f1, c2 - c1)]
    f, c = camino[-1]
    sol[f][c] = "F"
    return sol
 
 
def main():
    n = len(LABERINTO)
    inicio = (n - 1, 0)   # inferior izquierda
    destino = (0, 0)      # superior izquierda
 
    imprimir_matriz(LABERINTO, "LABERINTO ORIGINAL")
 
    visitado = [[False] * n for _ in range(n)]
    visitado[inicio[0]][inicio[1]] = True
    camino = [inicio]
    puntos_iniciales = valor_celda(LABERINTO, *inicio)
 
    salio = resolver(LABERINTO, inicio[0], inicio[1], destino, visitado, camino, puntos_iniciales)
 
    print("\n" + "=" * 50)
    if salio:
        total = sum(valor_celda(LABERINTO, f, c) for f, c in camino)
        print("¡EL RATÓN LOGRÓ SALIR DEL LABERINTO!")
        print(f"Puntos acumulados: {total} (mínimo requerido: {PUNTOS_MINIMOS})")
        print(f"Pasos del recorrido: {len(camino) - 1}")
        print("=" * 50)
        imprimir_matriz(construir_matriz_solucion(LABERINTO, camino),
                        "MATRIZ SOLUCIÓN (número = orden de paso, # = pared)")
        imprimir_matriz(construir_matriz_flechas(LABERINTO, camino),
                        "MATRIZ SOLUCIÓN CON FLECHAS")
        print("\nCamino (fila, columna):")
        print(" -> ".join(str(p) for p in camino))
    else:
        print("EL RATÓN NO LOGRÓ SALIR DEL LABERINTO")
        print(f"No existe un camino que llegue a F con {PUNTOS_MINIMOS} puntos o más.")
        print("=" * 50)
        sin_salida = [["#" if valor_celda(LABERINTO, i, j) == 0 else "." for j in range(n)] for i in range(n)]
        imprimir_matriz(sin_salida, "MATRIZ (sin camino viable)")
 
 
if __name__ == "__main__":
    main()
 
