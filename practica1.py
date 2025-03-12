from random import seed, randrange, choice

AZAR = 75 # Semilla del generador de números aleatorios

# … Otras constantes, funciones y clases …
class Tablero(object):
    def __init__(self, num_columnas, num_fichas, fichas):
        self.tablero = []
        self.crear_tablero_vacio(num_columnas)
        self.añadir_jugadores(fichas, num_fichas)
        print("edie cabron")


    def añadir_jugadores(self,fichas, numero_fichas):
        for i in range(0,len(fichas)):
            self.tablero[i][0] = fichas[i]
            self.tablero[i][1] = numero_fichas





    def crear_tablero_vacio(self, numero_columnas):
        self.tablero = [["",0] for i in range(numero_columnas)]

class Pargammon(object):
    def __init__(self, n=18, m=6, d=3, fichas=('\u263a', '\u263b')):
        self.N = n # Número de columnas
        self.M = m # Número inicial de fichas
        self.D = d # Número de dados
        self.J = len(fichas) # Numero de jugadores
        self.FICHAS = fichas # Caracteres de las fichas de cada jugador
        self.tablero = Tablero(self.N, self.M, self.FICHAS)


    def __repr__(self) -> str:
        """
        :return: Un string que indica el tablero y estado de la partida
        """
        # …

    def cambiar_turno(self) -> bool:
        """ Cambia de turno. Devuelve True si es fin de partida, False si no """
        # …
        # La tirada de dados se debe realizar con esta línea:
        self.dados = [randrange(6) + 1 for _ in range(self.D)]
        # …

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
    # …

if __name__=="__main__":
   main()