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
        for i in range(self.obtener_altura_tablero()):
            salida += ""
            for j in range(len(self.tablero)):
                if self.tablero[j][0]=="": salida +=" "
                else: salida += self.tablero[j][0]
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

class Pargammon(object):
    def __init__(self, n=18, m=6, d=3, fichas=('\u263a', '\u263b','\u263c')):
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
        """ Intenta realizar la jugada indicada en el string txt_jugada
        :return: None si es válida o un string con un mensaje de error
        """
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