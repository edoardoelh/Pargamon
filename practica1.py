from random import seed, randrange, choice

AZAR = 75 # Semilla del generador de números aleatorios

# … Otras constantes, funciones y clases …
class Tablero(object):
    def __init__(self, num_columnas, num_fichas, fichas):
        self.tablero = []
        self.crear_tablero_vacio(num_columnas)
        self.añadir_jugadores(fichas, num_fichas)

    def __repr__(self):
        salida = ""
        altura_tablero = self.obtener_altura_tablero()
        for i in range(altura_tablero):
            salida += ""
            for j in range(len(self.tablero)):
                if self.tablero[j][0]=="": salida +=" "
                else:
                    if self.tablero[j][1] >= altura_tablero - i: salida += self.tablero[j][0]
                    else: salida +=" "
                if not j-1==len(self.tablero): salida += "|"
            salida += "\n"
        for i in range(len(self.tablero)):
            salida += chr(65+i) + " "

        return salida

    def obtener_altura_tablero(self):
        altura = 0
        for columna in self.tablero:
            if columna[1] > altura:
                altura = columna[1]
        return altura


    def añadir_jugadores(self,fichas, numero_fichas):
        for i in range(0,len(fichas)):
            self.tablero[i][0] = fichas[i]
            self.tablero[i][1] = numero_fichas

    def crear_tablero_vacio(self, numero_columnas):
        self.tablero = [["",0] for i in range(numero_columnas)]

    def obtener_indice_columnas_usables(self, jugador):
        columnas_usables = []
        for indice in range(len(self.tablero)):
            if self.tablero[indice][0] == jugador:
                columnas_usables.append(indice)
        return columnas_usables

    def comprobar_movimiento(self, casilla, movimiento, jugador, tablero = None):
        if tablero is None:
            tablero = self.tablero
        movimiento_posible = True
        if casilla + movimiento > len(tablero)+1:
            movimiento_posible = False #el intento de movimiento se pasa del maximo del tablero
        if casilla + movimiento < len(tablero):
            if(tablero[casilla][0] != jugador): movimiento_posible = False #La casilla pertenece a otro jugador
            if tablero[casilla + movimiento][0]!=jugador and tablero[casilla + movimiento][1]>1: movimiento_posible = False #El otro jugador tiene mas de una ficha en su columna
        return movimiento_posible

    def comprobar_movimientos(self, casillas, movimientos, jugador, tablero= None):
        if tablero is None:
            tablero = self.tablero
        print("Llega aqui")
        movimientos_posibles = True
        tablero_virtual = tablero
        for i in range(len(movimientos)):
            if movimientos_posibles:
                print(self.comprobar_movimiento(casillas[i], movimientos[i], jugador, tablero_virtual))
                if self.comprobar_movimiento(casillas[i], movimientos[i], jugador, tablero_virtual):
                    self.realizar_movimiento(casillas[i], movimientos[i], jugador, tablero_virtual)
                else:
                    movimientos_posibles = False
        print(tablero_virtual)
        return movimientos_posibles


    def realizar_movimiento(self, casilla, movimiento, jugador, tablero = None):
        if tablero is None:
            tablero = self.tablero
        movimiento_realizado = True
        if self.comprobar_movimiento(casilla, movimiento, jugador, tablero):
            movimiento_realizado = False
        else:
            if tablero[casilla + movimiento][0]!=jugador and tablero[casilla + movimiento][1]==1:
                tablero[casilla + movimiento][0] = jugador
#FALTA: llamada a la funcion que hace que la casilla comida se mueva a donde le corresponda
            else:
                tablero[casilla + movimiento][0] = jugador
                tablero[casilla + movimiento][1] += 1
        return movimiento_realizado

    def get_jugadas_posibles(self,dados, jugador):
        tablero_virtual = self.tablero.copy()
        jugadas_posibles:list = self.generador_jugadas(dados, jugador, self.tablero)
        print("Jugadas posibles totales: [", *jugadas_posibles, "]", sep='\n')
        return jugadas_posibles

    def generador_jugadas(self, dados, jugador, tablero, jugada = None):
        if jugada is None: jugada = []
        jugadas = []
        for columna in self.obtener_indice_columnas_usables(jugador):#Realiza el movimiento por cada una de las columnas usables
            if self.comprobar_movimiento(columna, dados[0], jugador, tablero):#Comprueba si ese movimiento se puede realizar
                copia_tablero = tablero.copy()
                copia_dados = dados.copy()
                self.realizar_movimiento(columna, copia_dados[0], jugador, copia_tablero)
                copia_dados.pop()
                jugada.append(columna)
                if len(copia_dados)>1:
                    self.generador_jugadas(copia_dados, jugador, copia_tablero, jugada.append(columna))
                else:
                    jugadas.append(jugada)
            else:
                jugada.append(-1)
        return jugadas    
            


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
        simbolos_dados= ["⚀","⚁","⚂", "⚃", "⚄","⚅"] #https://es.piliapp.com/symbol/dice/
        resultado = ""
        for cara_dado in self.dados:
            resultado += simbolos_dados[cara_dado - 1] + " "
        return resultado

    def cambiar_turno(self) -> bool:
        """ Cambia de turno. Devuelve True si es fin de partida, False si no """
        # …
        self.turno+= 1 #cambio turno
        # La tirada de dados se debe realizar con esta línea:
        self.dados = [randrange(6) + 1 for _ in range(self.D)] #estas dos lineas de los dados podriamos hacerlo en una funcion pequeñas, como veas
        self.historial_dados += [self.dados[:]]
        print(self)
        #Aqui se tiene que añadir una concicion que compruebe si se ha terminado la partida, en ese caso retorna un False

        return True #Devuelve un True cuando puede cambiar el turno, dejara de poder cambiar el turno al haberse terminado la partida

    def obtener_jugador_actual(self):
        return self.FICHAS[self.turno%len(self.FICHAS)]

    def jugar(self, txt_jugada: str) -> None | str:
        jugador_actual=self.obtener_jugador_actual()
#Aqui se tiene que añadir una funcion que compruebe que el texto introducido es valido y que la cantidad de caracteres no supera las de los dados
        movimientos:list = [ord(c.lower()) - ord('a') for c in txt_jugada]
        jugadas_posibles = self.tablero.get_jugadas_posibles(self.dados, jugador_actual)
        if self.tablero.comprobar_movimientos(movimientos, self.dados, jugador_actual):
            for i in range(len(movimientos)):
                self.tablero.realizar_movimiento(movimientos[i], self.dados[i], jugador_actual)
        # …

def main():
    seed(AZAR)
    print("*** PARGAMMON ***")
    params = map(int, input("Numero de columnas, fichas y dados = ").split())
    juego = Pargammon(*params)
    while juego.cambiar_turno():
        juego.jugar(input("Jugada: "))



if __name__=="__main__":
   main()
