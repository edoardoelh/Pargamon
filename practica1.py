from random import seed, randrange, choice
import pydoc

AZAR = 75 # Semilla del generador de números aleatorios

# … Otras constantes, funciones y clases …
class Tablero(object):
    def __init__(self, num_columnas, num_fichas, fichas):
        """
        Constructror del tablero, añade las columnas especificadas y las fichas de cada jugador.
        :param num_columnas: Entero con el numero de columnas a insertar en el tablero.
        :param num_fichas: Entero con el numero de fichas a incluir a cada jugador.
        :param fichas: Lista con los caracteres de los jugadores que se incluiran en el tablero
        """
        self.tablero = []
        self.crear_tablero_vacio(num_columnas)
        self.añadir_jugadores(fichas, num_fichas)

    def __repr__(self):
        """
        Funcion que retorna la representacion en un string, como un jugador humnano veria el tablero.
        :return:
        """
        salida = ""
        altura_tablero = self.obtener_altura_tablero()
        for i in range(altura_tablero):
            salida += ""
            for j in range(len(self.tablero)):
                if self.tablero[j][0] == "": salida += " "
                else:
                    if self.tablero[j][1] >= altura_tablero - i: salida += self.tablero[j][0]
                    else: salida += " "
                if not j-1 == len(self.tablero): salida += "|"
            salida += "\n"
        for i in range(len(self.tablero)):
            salida += chr(65+i) + " "

        return salida

    def obtener_altura_tablero(self):
        """
        Retorna un numero entero perteneciente a la cantidad de fichas de la columna con mayor numero de los mismas.
        :return: Entero correspondiente a la cantidad de fichas de la cosilla con mas fichas.
        """
        altura = 0
        for columna in self.tablero:
            if columna[1] > altura:
                altura = columna[1]
        return altura


    def añadir_jugadores(self,fichas, numero_fichas):
        """
        Coloca las fichas en el tablero en funcion de los jugadores especificados y el numero de fichas dadas.
        :param fichas: Array de caracteres que seran las representaciones de las fichas de los jugadores.
        :param numero_fichas: Numero de fichas que se le asignaran a cada jugador.
        None
        """
        for i in range(0,len(fichas)):
            self.tablero[i][0] = fichas[i]
            self.tablero[i][1] = numero_fichas

    def crear_tablero_vacio(self, numero_columnas):
        """
        Crea un tablero con tantas casillas como se le pasen por parametro
        :param numero_columnas: Numero de casillas que tendra el tablero.
        """
        self.tablero = [["",0] for i in range(numero_columnas)]

    def obtener_indice_columnas_usables(self, jugador, tablero = None):
        """
        Retorna un array de indices de las casillas del tablero que pertenecen al jugador.
        :param jugador: Caracter de la ficha del jugador a consultar.
        :param tablero: Tablero en el que realizara la comprobacion.
        :return int[]: Lista de los indices del tablero que pertenecen al jugador consultado.
        """
        if tablero is None:
            tablero = self.tablero
        columnas_usables = []
        for indice in range(len(tablero)):
            if tablero[indice][0] == jugador:
                columnas_usables.append(indice)
        return columnas_usables

    def comprobar_movimiento(self, casilla, movimiento, jugador, tablero = None):
        """
        Retorna un valor booleano correspondiente a si se puede realizar el moviminto solicitado.
        :param casilla: Casilla que contiene la ficha del jugador a mover (De no tratarse de una ficha
            del jugador la funcion devuelve False).
        :param movimiento: Entero que determina la distancia a moverse por el jugador.
        :param jugador: Caracter de la ficha del jugador a comprobar.
        :param tablero: (tablero, optional) Tablero en el que realizara la comprobacion, en el caso de que no
                        se especifique, usara el tablero perteneciente al objeto.
        :return: Boleano que especifica si se puede realizar la jugada consultada o no.
        """

        movimiento_posible = True
        if casilla != -1:
            if tablero is None:
                tablero = self.tablero
            if casilla + movimiento > len(tablero)+1:
                movimiento_posible = False #el intento de movimiento se pasa del maximo del tablero
            if casilla + movimiento < len(tablero):
                if tablero[casilla][0] != jugador: movimiento_posible = False #La casilla pertenece a otro jugador
                if tablero[casilla + movimiento][0] != jugador and tablero[casilla + movimiento][1] > 1: movimiento_posible = False #El otro jugador tiene mas de una ficha en su columna
        return movimiento_posible

    def comprobar_movimientos(self, casillas, movimientos, jugador, tablero=None):
        """
        Funcion que realiza la comprobacion de multiples movimientos, se toma el mismo indice de la lista casillas y
            de la lista movimientos para la comprobacion de los mismos, a su vez se realiza una copia del tablero
            para no afectar al tablero pasado como parametro.
        :param casillas: Lista de casillas en las que se comprobara si se pueden hacer los movimientos.
        :param movimientos: Lista del resultado de los dados correspondiente al movimiento que se espera realizar
            con las fichas de las casillas.
        :param jugador: Caracter del jugador en el que se van a comprobar los movimientos.
        :param tablero: (Tablero, opcional)Tablero en el que se quiere realizar la comprobacion.
        :return: Devuelve un Booleano correspondiente a si se pueden realizar los movimientos a comprobar.
        """
        if tablero is None:#Esto se encarga de realizar una pseudo sobrecarga del metodo
            tablero = self.realizar_copia_tablero()
        movimientos_posibles = True
        tablero_virtual = self.realizar_copia_tablero(tablero)
        for i in range(len(movimientos)):
            if movimientos_posibles:
                #print(self.comprobar_movimiento(casillas[i], movimientos[i], jugador, tablero_virtual))  #BORRAR POSTERIORMENTE
                if self.comprobar_movimiento(casillas[i], movimientos[i], jugador, tablero_virtual):
                    self.realizar_movimiento(casillas[i], movimientos[i], jugador, tablero_virtual)
                else:
                    movimientos_posibles = False
        #print(tablero_virtual) #BORRAR POSTERIORMENTE
        return movimientos_posibles


    def realizar_movimiento(self, casilla, movimiento, jugador, tablero = None):
        """
        Funcion que intenta la realizacion del movimiento en el tablero especificado como parametro, en caso de no
            especificar uno, utilizara el tablero perteneciente al atributo del objeto.
        :param casilla: Entero que indica el indice de la casilla en la que se espera realizar el movimiento.
        :param movimiento: Entero correspondiente al dado que especifica la distancia que se espera que recorra
            la ficha.
        :param jugador: Caracter del jugador en el que se van a realizar los movimientos.
        :param tablero: (Tablero, opcional)Tablero en el que se quiere realizar el movimiento.
        :return: Devuelve un Booleano correspondiente a si se ha podido realizar el movimiento.
        """
        movimiento_realizado = True
        if casilla != -1:
            if tablero is None:
                tablero = self.tablero
            if not self.comprobar_movimiento(casilla, movimiento, jugador, tablero):
                movimiento_realizado = False
            else:
                if tablero[casilla + movimiento][0] != jugador and tablero[casilla + movimiento][1] == 1:
                    tablero[casilla + movimiento][0] = jugador
#FALTA: llamada a la funcion que hace que la casilla comida se mueva a donde le corresponda
                else:
                    tablero[casilla + movimiento][0] = jugador
                    tablero[casilla + movimiento][1] += 1
                    tablero[casilla][1] -= 1
                    if tablero[casilla][1] == 0: tablero[casilla][0] = ''
        return movimiento_realizado

    def get_jugadas_posibles(self,dados, jugador):
        """
        Funcion encargada de preparar y llamar a la funcion que genera un listado de jugadas posibles.
        :param dados: Lista con los dados con los que se espera comprobar las diferentes jugadas.
        :param jugador: Jugador en el que se van a realizar las comprobaciones.
        :return: Lista con las jugadas posibles en funcion de los parametros dados.
        """
        #tablero_virtual = self.tablero.copy()
        jugadas_posibles:list = self.generador_jugadas(dados, jugador, self.tablero)
        print("Jugadas posibles totales: [", *jugadas_posibles, "]", sep='\n')
        return jugadas_posibles

    def generador_jugadas(self, dados, jugador, tablero, jugada = None, jugadas = None):
        """
        Funcion encargada de generar jugadas individualmente y de manera recursivo para posteriormente asociarlas
            a la lista total de jugadas.
        :param dados: Lista con los dados con los que se espera comprobar las diferentes jugadas.
        :param jugador: Jugador en el que se van a realizar las comprobaciones.
        :param tablero: Tablero en el que se van a realizar las jugadas.
        :param jugada: (Lista, opcional) Jugada actual, se utiliza para almacenar la jugada realizada hasta el momento
            en la recursividad.
        :param jugadas: (Lista, opcional) Listado completo de jugadas, al estar pasado por referencia, la lista es la
            misma para todas las iteraciones de la funcion, por lo que se utiliza para que desde cualquier punto de
            ejecucion, la lista sea igualmente accesible.
        :return: Lista con las jugadas posibles en funcion de los parametros dados (Al pasarse por referencia este
            return no es del todo necesario)
        """
        if jugada is None: jugada = []
        if jugadas is None: jugadas = []
        columnas_usables = self.obtener_indice_columnas_usables(jugador, tablero)
        for columna in columnas_usables:#Realiza el movimiento por cada una de las columnas usables
            if self.comprobar_movimiento(columna, dados[0], jugador, tablero):#Comprueba si ese movimiento se puede realizar
                copia_tablero = self.realizar_copia_tablero(tablero)
                copia_dados = dados.copy()#Se realiza una copia de los dados antes de realizar el movimiento, para poder borrarlo de la lista
                self.realizar_movimiento(columna, copia_dados[0], jugador, copia_tablero)
                jugada.append(columna)
                copia_dados.pop(0)
                if len(copia_dados) >= 1:
                    self.generador_jugadas(copia_dados, jugador, copia_tablero, jugada, jugadas)
                else:
                    #Aqui se tiene que añadir a la parte final de la jugada el valor de la misma para hacer luego la ordenacion (array.sort(key=lambda L: L[1]), https://www.reddit.com/r/learnpython/comments/loex48/how_to_sort_by_the_second_element_in_a_2d_list/)
                    jugadas.append(jugada.copy())
                jugada.pop()
                copia_tablero = self.realizar_copia_tablero(tablero)
            else:
                jugada.append(-1)
        return jugadas

    def realizar_copia_tablero(self,tablero = None):
        if tablero == None:
            tablero = self.tablero
        return [[j for j in casilla] for casilla in tablero]
            


class Pargammon(object):
    def __init__(self, n=18, m=6, d=3, fichas=('\u263a', '\u263b')):
        self.N = n # Número de columnas
        self.M = m # Número inicial de fichas
        self.D = d # Número de dados
        self.J = len(fichas) # Numero de jugadores
        self.FICHAS = fichas # Caracteres de las fichas de cada jugador
        self.tablero = Tablero(self.N, self.M, self.FICHAS)
        self.turno = -1 # Para el wey que le toca tirar
        self.dados = [] #Para guardar la ultima tirada de dados y esta luego ponerla en un array con todas las tiradas de la partida
        self.historial_dados = []


    def __repr__(self) -> str:
        salida = f"JUGADA #{self.turno + 1}\n"
        salida += str(self.tablero) + "\n"
        salida += f"Turno de {self.obtener_jugador_actual()}: {self.imagen_dado()}"
        return salida

    def imagen_dado (self):
        # devuelve el la cara de dado que haya salido
        simbolos_dados = ["⚀","⚁","⚂", "⚃", "⚄","⚅"] #https://es.piliapp.com/symbol/dice/
        resultado = ""
        for cara_dado in self.dados:
            resultado += simbolos_dados[cara_dado - 1] + " "
        return resultado

    def cambiar_turno(self) -> bool:
        """ Cambia de turno. Devuelve True si es fin de partida, False si no """
        # …
        self.turno += 1 #cambio turno
        # La tirada de dados se debe realizar con esta línea:
        self.dados = [randrange(6) + 1 for _ in range(self.D)] #estas dos lineas de los dados podriamos hacerlo en una funcion pequeñas, como veas
        self.historial_dados += [self.dados[:]]
        print(self)
        #Aqui se tiene que añadir una concicion que compruebe si se ha terminado la partida, en ese caso retorna un False

        return True #Devuelve un True cuando puede cambiar el turno, dejara de poder cambiar el turno al haberse terminado la partida

    def obtener_jugador_actual(self):
        return self.FICHAS[self.turno%len(self.FICHAS)]

    def jugar(self, txt_jugada: str) -> None | str:
        jugada_realizada = False
        jugador_actual=self.obtener_jugador_actual()
#Aqui se tiene que añadir una funcion que compruebe que el texto introducido es valido y que la cantidad de caracteres no supera las de los dados

        #Esta funcion esta dando problemas, por ahora me centrare en hacer que funcione la realizacion de jugadas
        jugadas_posibles = self.tablero.get_jugadas_posibles(self.dados, jugador_actual)
        print(jugadas_posibles)

        while not jugada_realizada:
            movimientos: list = [ord(c.lower()) - ord('a') for c in txt_jugada]
            if self.tablero.comprobar_movimientos(movimientos, self.dados, jugador_actual):
                for i in range(len(movimientos)):
                    jugada_realizada = self.tablero.realizar_movimiento(movimientos[i], self.dados[i], jugador_actual)
            else:
                txt_jugada = input("Jugada: ")
        # …

def main():
    seed(AZAR)
    pydoc.writedoc('practica1')
    print("*** PARGAMMON ***")
    params = map(int, input("Numero de columnas, fichas y dados = ").split())
    juego = Pargammon(*params)
    while juego.cambiar_turno():
        juego.jugar(input("Jugada: "))



if __name__=="__main__":
   main()
