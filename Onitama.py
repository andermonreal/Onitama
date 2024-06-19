import sys
import copy

########## CLASE CARTA ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
class Carta:
    def __init__(self, owner, card_id, dx_1, dy_1, dx_2, dy_2, dx_3, dy_3, dx_4, dy_4):
        self.owner = owner
        self.card_id = card_id
        self.dx_1 = dx_1
        self.dx_2 = dx_2
        self.dx_3 = dx_3
        self.dx_4 = dx_4
        self.dy_1 = dy_1
        self.dy_2 = dy_2
        self.dy_3 = dy_3
        self.dy_4 = dy_4


########## CLASE MOVIMIENTO ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
class Movimiento:
    def __init__ (self, card_id, movimiento):
        self.card_id = card_id
        self.movimiento = movimiento


########## CLASE NODO ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
class Nodo:
    def __init__ (self, tablero, turno, posiblesMovimientos, cartas):
        self.tablero = tablero
        self.turno = turno # 0 para Azules, 1 para Rojos
        self.posiblesMovimientos = posiblesMovimientos # Son los hijos del estado en el que estas es decir, cada posible movimiento que puedes hacer para cada estado con sus respectivas comprobaciones de si se puede hacer y demás
        self.cartas = cartas

    ### METODOS DE LA CLASE NODO <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

    # Devuelve verdadero si es el jugador W
    def es_jugador_0 (self, i, j):
        return (self.tablero[i][j] == 'W' or self.tablero[i][j] == 'w')


    # Devuelve verdadero si es el jugador B
    def es_jugador_1 (self, i, j):
        return (self.tablero[i][j] == 'B' or self.tablero[i][j] == 'b')


    # Devuelve verdadero si es el maestro W
    def es_maestro_W (self, i, j):
        return (self.tablero[i][j] == 'W')


    # Devuelve verdadero si es el maestro B
    def es_maestro_B (self, i, j):
        return (self.tablero[i][j] == 'B')


    # Cambia de turno
    def cambio_de_turno (self):
        return (1 - self.turno)


    # Devuelve verdadero si alguno de los maestros se encuentra en el templo oponente
    def maestro_en_templo_oponente (self):
        return (self.es_maestro_W(0, 2) or self.es_maestro_B(4, 2))


     # Devuelve verdadero si se ha terminado el juego
    def final_juego (self):
        return (not(self.maestros_en_juego()) or self.maestro_en_templo_oponente())


    # Nos sirve para saber si podemos hacer un movimiento o no
    def no_se_sale_del_tablero (self, i, j):
        return  ((0 <= i <= 4) and (0 <= j <= 4))


    # Devuelve verdadero si es posible hacer el movimiento para dicha pieza
    def es_movimiento_posible (self, i, j):
        if (self.turno == 0):
            return (self.no_se_sale_del_tablero (i, j) and (not(self.es_jugador_0(i, j))))
        else:
            return (self.no_se_sale_del_tablero (i, j) and (not(self.es_jugador_1(i, j))))

    # Funcion para almacenar la posicion de las piezas en un turno
    def posiciones_piezas (self):
        piezas = []
        if (self.turno == 0):
            for i in range (5):
                for j in range (5):
                    if (self.tablero[i][j] != '.'):
                        if (self.es_jugador_0(i, j)):
                            piezas.append((i, j))

        else:
            for i in range (5):
                for j in range (5):
                    if (self.tablero[i][j] != '.'):
                        if (self.es_jugador_1(i, j)):
                            piezas.append((i, j))
        return piezas


    # A la hora de cambiar la carta central, surge el problema de que dicha carta tiene que ser dada la vuelta, de esta siguiente forma cumplimos este requisito
    def modificar_carta_central (self, carta):
        carta.dx_1 = carta.dx_1 * (-1)
        carta.dx_2 = carta.dx_2 * (-1)
        carta.dx_3 = carta.dx_3 * (-1)
        carta.dx_4 = carta.dx_4 * (-1)
        carta.dy_1 = carta.dy_1 * (-1)
        carta.dy_2 = carta.dy_2 * (-1)
        carta.dy_3 = carta.dy_3 * (-1)
        carta.dy_4 = carta.dy_4 * (-1)


    # Cambia la carta del medio por la que se va a usar
    def cambiar_cartas (self, card_id):
        for carta in self.cartas: # Primer bucle para buscar la carta del centro
            if carta.owner == -1:
                carta.owner = self.turno
        for carta in self.cartas: # Segundo bucle para buscar la carta usada y, la modifico
            if carta.card_id == card_id:
                carta.owner = -1
                self.modificar_carta_central(carta)


    # Devuelve verdadero si se encuentran ambos maestros | ACABADA
    def maestros_en_juego (self):
        maestro_B = False
        maestro_M = False
        for i in range(5):
            for j in range (5):
                if (self.es_maestro_B(i, j)): # Si encuentro al maestro B
                    maestro_B = True
                    if (maestro_M):
                        return True
                elif (self.es_maestro_W(i, j)): # Si encuentro al maestro M
                    maestro_M = True
                    if (maestro_B):
                        return True

        return False # Salgo del bucle sin haber encontrado a los dos maestros


    # Devuelve una lista con los posibles movimientos de cada pieza
    def calcular_posibles_movimientos(self):
        #los posibles movimientos
        self.posiblesMovimientos = []
        for carta in self.cartas:
            if carta.owner == self.turno:
                for x, y in self.posiciones_piezas():
                    for dy, dx in [(carta.dx_1, carta.dy_1), (carta.dx_2, carta.dy_2), (carta.dx_3, carta.dy_3), (carta.dx_4, carta.dy_4)]: # Bucle para cada posible movimiento de cada carta
                        if (dx, dy) != (0,0):
                            if self.turno == 0:
                                x_destino, y_destino = x-dx, y+dy
                            else:
                                x_destino, y_destino = x+dx, y+dy
                            if self.no_se_sale_del_tablero(x_destino, y_destino) and self.es_movimiento_posible(x_destino, y_destino):
                                self.posiblesMovimientos.append(Movimiento(carta.card_id,(str(x) + str(y) + str(x_destino) + str(y_destino))))



    # Realiza el movimiento correspondiente a la pieza y a la carta y devuelve el nuevo estado generado
    def mover_pieza(self, mover):
        nuevo_estado = copy.deepcopy(self) # Copio el estado actual al nuevo
        (i_actual, j_actual, i_destino, j_destino) = mover.movimiento
        nuevo_estado.turno = self.cambio_de_turno() # Cambio de turno
        nuevo_estado.tablero[int(i_destino)][int(j_destino)] = self.tablero[int(i_actual)][int(j_actual)] # Copio el contenido de la casilla actual a la casilla de destino
        nuevo_estado.cambiar_cartas(mover.card_id) # Cambio la carta del medio por la que acabo de usar
        nuevo_estado.calcular_posibles_movimientos() # Calculo los posibles movimientos para el nuevo estado actual
        return nuevo_estado


    # Devuelve la posición del rey contrario, necesario para futuras funciones
    def coordenadas_rey_rival (self):
        if self.turno == 0:
            for i in range(5):
                for j in range(5):
                    if (self.tablero[i][j] == 'B'):
                        return (i, j)

        else:
            for i in range(5):
                for j in range(5):
                    if (self.tablero[i][j] == 'W'):
                        return (i, j)
        return (i, j)


    def coordenadas_de_mi_rey (self):
        if self.turno == 0:
            for i in range(5):
                for j in range(5):
                    if (self.tablero[i][j] == 'W'):
                        return (i, j)

        else:
            for i in range(5):
                for j in range(5):
                    if (self.tablero[i][j] == 'B'):
                        return (i, j)
        return (i, j)


    def contar_piezas (self):
        aliadas = 0
        rivales = 0
        if self.turno == 0:
            for i in range (5):
                for j in range (5):
                    if (self.es_jugador_1 (i, j)):
                        rivales=+1
                    elif (self.es_jugador_0 (i, j)):
                        aliadas=+1

        else:
            for i in range (5):
                for j in range (5):
                    if (self.es_jugador_0 (i, j)):
                        rivales=+1
                    elif (self.es_jugador_1 (i, j)):
                        aliadas=+1

        return (aliadas, rivales)

    # Nuestra heuristica sera la distancia de manhatan a la casilla del rey rival
    def heuristica (self):

        miMejorHeuristica = 0.001
        suMejorHeuristica = 10
        (rRey_i, rRey_j) = self.coordenadas_rey_rival() # Coordenadas de su rey
        (mRey_i, mRey_j) = self.coordenadas_de_mi_rey() # Coordenadas de tu rey
        (piezasAliadas, piezasRivales) = self.contar_piezas() # Numero de piezas rivales y aliadas


        if (self.turno == 0): # SI SOY LAS W

            for i in range(5):
                for j in range(5):
                    if (self.es_jugador_1 (i, j)): # Para el otro jugador
                        suHeurisitica = abs(i-mRey_i) + abs(j-mRey_j) + 0.000000001
                        #print("[-] Su eurisitica: ", suHeurisitica, "\n",  file=sys.stderr, flush=True)

                    # Si la resta de su heuristica con mi mejor heuristica es mas pequeña que su mejor heuristica ...
                        if (1/miMejorHeuristica - 1/suHeurisitica) < suMejorHeuristica:
                            suMejorHeuristica = (1/miMejorHeuristica - 1/suHeurisitica) + (piezasRivales - piezasAliadas)

                    if (self.es_jugador_0 (i, j)): # Para mi
                        miHeuristica = abs(i-rRey_i) + abs(j-rRey_j) + 0.000000001
                        #print("[+] Mi eurisitica: ", miHeuristica, "\n",  file=sys.stderr, flush=True)

                    # Si la resta de mi heuristica con su mejor heuristica es mayor que mi mejor heuristica  ...
                        if (1/miHeuristica - 1/suMejorHeuristica) > miMejorHeuristica:
                            miMejorHeuristica = (1/miHeuristica - 1/suMejorHeuristica) + (piezasAliadas - piezasRivales)


                    #print("Mi mejor Heurisitica: ",  miMejorHeuristica,  "\nSu mejor Heuristica: ", suMejorHeuristica, "\n", file=sys.stderr, flush=True)


        else: # SI SOY LAS B
            for i in range(5):
                for j in range(5):

                    if (self.es_jugador_0 (i, j)): # Para el otro jugador
                        suHeurisitica = abs(i-mRey_i) + abs(j-mRey_j) + 0.000000001

                    # Si la resta de su heuristica con mi mejor heuristica es mas pequeña que su mejor heuristica ...
                        if (1/miMejorHeuristica - 1/suHeurisitica) < suMejorHeuristica:
                            suMejorHeuristica = (1/miMejorHeuristica - 1/suHeurisitica) + (piezasRivales - piezasAliadas)

                    if (self.es_jugador_1 (i, j)): # Para mi
                        miHeuristica = abs(i-rRey_i) + abs(j-rRey_j) + 0.000000001

                    # Si la resta de mi heuristica con su mejor heuristica es mayor que mi mejor heuristica  ...
                        if (1/miHeuristica - 1/suMejorHeuristica) > miMejorHeuristica:
                            miMejorHeuristica = (1/miHeuristica - 1/suMejorHeuristica) + (piezasAliadas - piezasRivales)


        #print("[j] Resultado de la funcion: ", miMejorHeuristica, "\n\n",  file=sys.stderr, flush=True)
        return miMejorHeuristica
        #return piezasAliadas - piezasRivales






########## ALGORITMO MINIMAX ########## ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def algoritmo_miniMax (nodo, profundidad, jugadorMAX):
    if (profundidad == 0 or nodo.final_juego()):
        return None, nodo.heuristica()

    mejorMovimiento = None
    if (jugadorMAX):
        valor = float('-inf')
        for movimiento in nodo.posiblesMovimientos:
            #print("     Posible movimiento: ", movimiento, file=sys.stderr, flush=True)
            nuevoNodo = nodo.mover_pieza(movimiento)
            #print(nuevoNodo.tablero, file=sys.stderr, flush=True)
            #print("\n", file=sys.stderr, flush=True)

            _, valorNodoNuevo = algoritmo_miniMax(nuevoNodo, profundidad, False)
            if (valorNodoNuevo > valor):
                valor = valorNodoNuevo
                mejorMovimiento = movimiento
                #print((mejorMovimiento.card_id,movimiento.movimiento), file=sys.stderr, flush=True)

        return (mejorMovimiento, valor)

    else:
        valor = float('inf')
        for movimiento in nodo.posiblesMovimientos:
            nuevoNodo = nodo.mover_pieza (movimiento)
            #print(nuevoNodo.tablero, file=sys.stderr, flush=True)
            #print("\n", file=sys.stderr, flush=True)

            _, valorNodoNuevo = algoritmo_miniMax (nuevoNodo, profundidad-1, True)
            if (valorNodoNuevo < valor):
                valor = valorNodoNuevo
                mejorMovimiento = movimiento

        return (mejorMovimiento, valor)



########## ALGORITMO ALFA-BETA ########## ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def algoritmo_alfa_beta(nodo, profundidad, alfa, beta, jugadorMAX, idjugador):
    if (profundidad == 0 or nodo.final_juego()):
        return None, nodo.heuristica()

    mejorMovimiento = None
    if jugadorMAX == True:
        valor = float('-inf')
        #nodo.calcular_posibles_movimientos()
        #print([m.movimiento for m in nodo.posiblesMovimientos])
        for movimiento in nodo.posiblesMovimientos:
            #print("MAX --------", movimiento.movimiento, file=sys.stderr, flush=True)
            nuevoNodo = nodo.mover_pieza(movimiento)
            #print(nuevoNodo.tablero, file=sys.stderr, flush=True)
            if idjugador == 0:
                id_new = 1
            else:
                id_new = 0
            _, valorNodoNuevo = algoritmo_alfa_beta(nuevoNodo, profundidad, alfa, beta, False, id_new)
            if (valorNodoNuevo > valor):
                valor = valorNodoNuevo
                mejorMovimiento = movimiento
                alfa = valor
            if alfa >= beta :
                break
        return (mejorMovimiento, valor)

    else:
        valor = float('inf')
        #nodo.calcular_posibles_movimientos()
        #print([m.movimiento for m in nodo.posiblesMovimientos])
        for movimiento in nodo.posiblesMovimientos:
            #print("MIN --------", movimiento.movimiento, file=sys.stderr, flush=True)
            nuevoNodo = nodo.mover_pieza(movimiento)
            #print(nuevoNodo.tablero, file=sys.stderr, flush=True)
            if idjugador == 0:
                id_new = 1
            else:
                id_new = 0
            _, valorNodoNuevo = algoritmo_alfa_beta(nuevoNodo, profundidad-1, alfa, beta, True, id_new)
            if (valorNodoNuevo < valor):
                valor = valorNodoNuevo
                mejorMovimiento = movimiento
                beta = valor
            if alfa >= beta :
                break
        return (mejorMovimiento, valor)

########## FUNCIONES AUXILIARES ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def convertir_letras_a_numeros (cadena):
    nums = ['5', '4', '3', '2', '1']
    letras = ['A', 'B', 'C', 'D', 'E']
    col1 = letras.index(cadena[0])
    fil1 = nums.index(cadena[1])
    col2 = letras.index(cadena[2])
    fil2 = nums.index(cadena[3])
    return str(fil1) + str(col1) + str(fil2) + str(col2)


def convertir_numeros_a_letras (cadena):
    nums = ['5', '4', '3', '2', '1']
    letras = ['A', 'B', 'C', 'D', 'E']
    col1 = letras[int(cadena[1])]
    fil1 = nums[int(cadena[0])]
    col2 = letras[int(cadena[3])]
    fil2 = nums[int(cadena[2])]
    return str(col1) + str(fil1) + str(col2) + str(fil2)


########## PROGRAMA PRINCIPAL (MAIN) ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#print("[+] Inicio de la IA de onitama \n", file=sys.stderr, flush=True) # Para printear la informacion por pantalla

player_id = int(input()) # Solicita al usuario su ID, para saber que jugador eres
#print("player_id", player_id, file=sys.stderr, flush=True)

# game loop
while True:
    posibles_movimientos_letras = []
    posibles_movimientos_numeros = []
    cartas = []
    profundidad = 1
    casillas_auxiliares = [['.', '.', '.', '.', '.'], ['.', '.', '.', '.', '.'], ['.', '.', '.', '.', '.'], ['.', '.', '.', '.', '.'], ['.', '.', '.', '.', '.']] # Me da error de otras maneras



    for i in range(5):
        board = input() # se lee 5 veces la entrada de la consola para obtener el estado actual del tablero del juego.
        #print("board", board, file=sys.stderr, flush=True)
        #print(board, file=sys.stderr, flush=True) # Para printear la informacion por pantalla
        for j in range(5):
            casillas_auxiliares[i][j] = board[j]

    #print("Estado inicial del tablero: \n", file=sys.stderr, flush=True) # Para printear la informacion por pantalla
    #print(tablero, file=sys.stderr, flush=True)
    #print("\n", file=sys.stderr, flush=True)

    for i in range(5):
        owner, card_id, dx_1, dy_1, dx_2, dy_2, dx_3, dy_3, dx_4, dy_4 = [int(j) for j in input().split()] # Los valores leídos se asignan a varias variables, como el propietario de la carta, el ID de la carta y las coordenadas de movimiento de la carta.
        #print("carta ",i, "-> ", owner, card_id, dx_1, dy_1, dx_2, dy_2, dx_3, dy_3, dx_4, dy_4, player_id, file=sys.stderr, flush=True)
        nueva_carta = Carta(owner, card_id, dx_1, dy_1, dx_2, dy_2, dx_3, dy_3, dx_4, dy_4)
        cartas.append(nueva_carta)

    numeroPosiblesMovimientosInicio = int(input()) #numero de los posibles movimientos al inicio de la partida
    #print("Numero de posibles movimientos al inicio: ", numeroPosiblesMovimientosInicio, file=sys.stderr, flush=True)

    for i in range(numeroPosiblesMovimientosInicio):
        posibleMovimientoInicial = input().split() # Nos da cada iteracion. el card_id y el move
        #print("posibleMovimientoInicial: ", posibleMovimientoInicial, file=sys.stderr, flush=True)
        card_id = int(posibleMovimientoInicial[0])
        movimiento = posibleMovimientoInicial[1]
        posibles_movimientos_letras.append(Movimiento(card_id, movimiento)) # Meto en una lista, los posibles movimientos, con su carta y el movimiento
        posibles_movimientos_numeros.append(Movimiento(card_id, convertir_letras_a_numeros (movimiento)))



    nodo_inicial = Nodo(casillas_auxiliares, player_id, posibles_movimientos_numeros, cartas)
    # print([(movimiento.card_id, movimiento.movimiento) for movimiento in posibles_movimientos_numeros], file=sys.stderr, flush=True)
    #print("\nENTRO AL ALGORITMO --------", file=sys.stderr, flush=True)
    #[movimiento, valor] = algoritmo_miniMax(nodo_inicial, profundidad, True)
    [movimiento, valor] = algoritmo_alfa_beta(nodo_inicial, profundidad, float('-inf'), float('inf'), True, player_id)
    movimiento.movimiento = convertir_numeros_a_letras(movimiento.movimiento)
    #print("SALGO DEL ALGORITMO --------", file=sys.stderr, flush=True)

    print(movimiento.card_id,movimiento.movimiento, "Mi turno")


