from random import seed, randrange, choice
import pydoc

#T2  X6
#Edgar Lopez Herrera
#Miguel Llorente Herrero

AZAR = 75 # Semilla del generador de números aleatorios

# … Otras constantes, funciones y clases …
class Tablero(object):
    def __init__(self, pargamon, num_columnas, num_fichas, fichas):
        """
        Constructor del tablero, añade las columnas especificadas y las fichas de cada jugador.
        :param num_columnas: Entero con el número de columnas a insertar en el tablero.
        :param num_fichas: Entero con el número de fichas a incluir a cada jugador.
        :param fichas: Lista con los caracteres de los jugadores que se incluirán en el tablero
        """
        self.pargamon = pargamon
        self.tablero = []
        self.fichas_sacadas = {i:0 for i in fichas}
        self.crear_tablero_vacio(num_columnas)
        self.añadir_jugadores(fichas, num_fichas)

        
    def __repr__(self):
        """
        Función que retorna la representación en un string, como un jugador humano vería el tablero.
        :return: String que contiene la representación del tablero.
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
        Retorna un número entero perteneciente a la cantidad de fichas de la columna con mayor número de las mismas.
        :return: Entero correspondiente a la cantidad de fichas de la cosilla con más fichas.
        """
        altura = 0
        for columna in self.tablero:
            if columna[1] > altura:
                altura = columna[1]
        return altura


    def añadir_jugadores(self,fichas, numero_fichas):
        """
        Coloca las fichas en el tablero en función de los jugadores especificados y el número de fichas dadas.
        :param fichas: Array de caracteres que serán las representaciones de las fichas de los jugadores.
        :param numero_fichas: Número de fichas que se le asignaran a cada jugador.
        None
        """
        for i in range(0,len(fichas)):
            self.tablero[i][0] = fichas[i]
            self.tablero[i][1] = numero_fichas

            
    def crear_tablero_vacio(self, numero_columnas):
        """
        Crea un tablero con tantas casillas como se le pasen por parametro
        :param numero_columnas: Número de casillas que tendrá el tablero.
        """
        self.tablero = [["",0] for i in range(numero_columnas)]

        
    def obtener_indice_columnas_usables(self, jugador, tablero = None):
        """
        Retorna un array de índices de las casillas del tablero que pertenecen al jugador.
        :param jugador: Carácter de la ficha del jugador a consultar.
        :param tablero: Tablero en el que realizara la comprobación.
        :return int[]: Lista de los índices del tablero que pertenecen al jugador consultado.
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
            del jugador la función devuelve False).
        :param movimiento: Entero que determina la distancia a moverse por el jugador.
        :param jugador: Carácter de la ficha del jugador a comprobar.
        :param tablero: (tablero, optional) Tablero en el que realizara la comprobacion, en el caso de que no
                        se especifique, usara el tablero perteneciente al objeto.
        :return: Booleano que especifica si se puede realizar la jugada consultada o no.
        """
        movimiento_posible = True
        if casilla != -1:
            if tablero is None:
                tablero = self.tablero
            if casilla + movimiento > len(tablero):
                movimiento_posible = False #el intento de movimiento se pasa del maximo del tablero
            if casilla + movimiento < len(tablero):
                if tablero[casilla][0] != jugador: movimiento_posible = False #La casilla pertenece a otro jugador
                if tablero[casilla + movimiento][0] != jugador and tablero[casilla + movimiento][1] > 1: movimiento_posible = False #El otro jugador tiene mas de una ficha en su columna
        return movimiento_posible

      
    def comprobar_movimientos(self, casillas, movimientos, jugador, tablero=None):
        """
        Función que realiza la comprobación de multiples movimientos, se toma el mismo índice de la lista casillas y
            de la lista movimientos para la comprobación de los mismos, a su vez se realiza una copia del tablero
            para no afectar al tablero pasado como parametro.
        :param casillas: Lista de casillas en las que se comprobara si se pueden hacer los movimientos.
        :param movimientos: Lista del resultado de los dados correspondiente al movimiento que se espera realizar
            con las fichas de las casillas.
        :param jugador: Carácter del jugador en el que se van a comprobar los movimientos.
        :param tablero: (Tablero, opcional)Tablero en el que se quiere realizar la comprobación.
        :return: Devuelve un Booleano correspondiente a si se pueden realizar los movimientos a revisar.
        """
        if tablero is None:#Esto se encarga de realizar una pseudo sobrecarga del metodo
            tablero = self.realizar_copia_tablero()
        movimientos_posibles = True
        tablero_virtual = self.realizar_copia_tablero(tablero)

        for i in range(len(movimientos)):
            if movimientos_posibles:
                if self.comprobar_movimiento(casillas[i], movimientos[i], jugador, tablero_virtual):
                    self.realizar_movimiento(casillas[i], movimientos[i], jugador, tablero_virtual)
                else:
                    movimientos_posibles = False
        if not casillas in self.get_jugadas_posibles(movimientos,jugador) and movimientos_posibles == True:
            movimientos_posibles = False
            print("Esta jugada no se puede realizar todo @@@")
        return movimientos_posibles


    def realizar_movimiento(self, casilla, movimiento, jugador, tablero = None, fichas_sacadas = None):
        """
        Función que intenta la realización del movimiento en el tablero especificado como parametro, en caso de no
            especificar uno, utilizara el tablero perteneciente al atributo del objeto.
        :param casilla: Entero que indica el índice de la casilla en la que se espera realizar el movimiento.
        :param movimiento: Entero correspondiente al dado que especifica la distancia que se espera que recorra
            la ficha.
        :param jugador: Carácter del jugador en el que se van a realizar los movimientos.
        :param tablero: (Tablero, opcional)Tablero en el que se quiere realizar el movimiento.
        :return: Devuelve un Booleano correspondiente a si se ha podido realizar el movimiento.
        """
        movimiento_realizado = True
        if casilla != -1:
            if tablero is None:
                tablero = self.tablero
            if fichas_sacadas is None:
                fichas_sacadas = self.fichas_sacadas
            if not self.comprobar_movimiento(casilla, movimiento, jugador, tablero):
                movimiento_realizado = False # si el movimiento no es valido no se hace
            elif casilla + movimiento > len(tablero):#Supuestamente esto lo soluciona, hay que revisarlo
                movimiento_realizado = False
            else:
                if casilla + movimiento == len(tablero):#La ficha ha llegado a la meto
                    fichas_sacadas[jugador] += 1
                elif tablero[casilla + movimiento][0] != jugador and tablero[casilla + movimiento][1] == 1:# verificar una unica ficha enemiga en esa casilla
                    jugador_enemigo = tablero[casilla + movimiento][0]
                    self.cambiar_ficha_comida(casilla + movimiento, jugador_enemigo, tablero)  # cambiar ficha comida
                    tablero[casilla + movimiento][0] = jugador  # colocar ficha jugador que "conquista" la casilla
                    tablero[casilla + movimiento][1] = 1
                else:
                    # si es una casilla vacía o ya tiene fichas del jugador simplemente se apilan
                    tablero[casilla + movimiento][0] = jugador  # asignar nuevo jugador de la columna
                    tablero[casilla + movimiento][1] += 1  # Añadimos una ficha

                tablero[casilla][1] -= 1  # quita ficha casilla de origen

                if tablero[casilla][1] == 0:
                    tablero[casilla][0] = ''  # si no hay fichas limpia casilla
        return movimiento_realizado
      

    def cambiar_ficha_comida(self, posicion_comida, jugador_enemigo, tablero):
        """
        Mueve la ficha capturada a la primera columna válida partiendo del inicio del tablero vacía o con
            fichas del mismo jugador.
        :param posicion_comida: Índice de la casilla donde se ha comido la ficha.
        :param jugador_enemigo: Jugador al que pertenece la ficha capturada.
        :param tablero: Estado actual del tablero.
        """
        #eliminar ficha comida o capturada
        tablero[posicion_comida][0] = ''
        tablero[posicion_comida][1] = 0

        ficha_colocada = False #saber si ya colocamos la ficha
        i = 0
        while i < len(tablero) and not ficha_colocada:
            if tablero[i][0] == jugador_enemigo or tablero[i][0] == '':
                tablero[i][0] = jugador_enemigo  # casilla para el jugador enemigo
                tablero[i][1] += 1  # una ficha más
                ficha_colocada = True
            i += 1

            
    def get_jugadas_posibles(self,dados, jugador):
        """
        Función encargada de preparar y llamar a la función que genera un listado de jugadas posibles.
        :param dados: Lista con los dados con los que se espera comprobar las diferentes jugadas.
        :param jugador: Jugador en el que se van a realizar las comprobaciones.
        :return: Lista con las jugadas posibles en función de los parámetros dados.
        """
        jugadas_posibles:list = self.generador_jugadas(dados, jugador, self.tablero, self.fichas_sacadas)
        if len(jugadas_posibles) > 1: jugadas_posibles.pop(0)
##print("Jugadas posibles totales: [", *jugadas_posibles, "]", sep='\n')
        return jugadas_posibles

      
    def generador_jugadas(self, dados, jugador, tablero, fichas_sacadas, jugada = None, jugadas = None):
        """
        Función encargada de generar jugadas individualmente y de manera recursiva para posteriormente asociarlas
            a la lista total de jugadas.
        :param dados: Lista con los dados con los que se espera comprobar las diferentes jugadas.
        :param jugador: Jugador en el que se van a realizar las comprobaciones.
        :param tablero: Tablero en el que se van a realizar las jugadas.
        :param jugada: (Lista, opcional) Jugada actual, se utiliza para almacenar la jugada realizada hasta el momento
            en la recursividad.
        :param jugadas: (Lista, opcional) Listado completo de jugadas, al estar pasado por referencia, la lista es la
            misma para todas las iteraciones de la función, por lo que se utiliza para que desde cualquier punto de
            ejecución, la lista sea igualmente accesible.
        :return: Lista con las jugadas posibles en función de los parámetros dados (Al pasarse por referencia este
            return no es totalmente necesario)
        """
        if jugada is None: jugada = []
        if jugadas is None: jugadas = []
        columnas_usables = [-1] + self.obtener_indice_columnas_usables(jugador, tablero)
        for columna in columnas_usables:#Realiza el movimiento por cada una de las columnas usables
            if self.comprobar_movimiento(columna, dados[0], jugador, tablero):#Comprueba si ese movimiento se puede realizar
                copia_tablero = self.realizar_copia_tablero(tablero)
                copia_fichas_sacadas = fichas_sacadas.copy()
                copia_dados = dados.copy()#Se realiza una copia de los dados antes de realizar el movimiento, para poder borrarlo de la lista
                self.realizar_movimiento(columna, copia_dados[0], jugador, copia_tablero, copia_fichas_sacadas)
                jugada.append(columna)
                copia_dados.pop(0)
                if len(copia_dados) >= 1:
                    self.generador_jugadas(copia_dados, jugador, copia_tablero, copia_fichas_sacadas, jugada, jugadas)
                else:
                    #Aqui se tiene que añadir a la parte final de la jugada el valor de la misma para hacer luego la ordenacion (array.sort(key=lambda L: L[1]), https://www.reddit.com/r/learnpython/comments/loex48/how_to_sort_by_the_second_element_in_a_2d_list/)
                    jugadas.append(jugada.copy())
                jugada.pop()
                copia_tablero = self.realizar_copia_tablero(tablero)
                copia_fichas_sacadas = fichas_sacadas.copy()
            else:
                jugada.append(-1)
                #Hay que añadir un
        return jugadas

      
    def realizar_copia_tablero(self,tablero = None):
        """
        Función encargada de devolver una copia del tablero pasado como parametro, este estará almacenado en
            otro espacio de memoria el cual podrá modificarse sin afectar al original.
        :param tablero: Tablero, el cual se usara como origen para realizar la copia
        :return: Tablero idéntico al pasado como parametro pero localizado en otro espacio de memoria.
        """
        if tablero is None:
            tablero = self.tablero
        return [[j for j in casilla] for casilla in tablero]



class Pargammon(object):
    def __init__(self, n=18, m=6, d=3, fichas=('\u263a', '\u263b')):
        """
        Inicializador de la partida Pargamon, recibe una seria de parámetros para establecer las condiciones iniciales
            de la partida.
        :param n: Entero correspondiente al número de columnas que tendrá el tablero.
        :param m: Entero correspondiente al número de fichas que tendrá cada jugador al comienzo de la partida.
        :param d: Entero correspondiente al número de dados con los que se jugaran.
        :param fichas: Lista que contiene los caracteres de los jugadores de la partida.
        """
        self.N = n # Número de columnas
        self.M = m # Número inicial de fichas
        self.D = d # Número de dados
        self.J = len(fichas) # Numero de jugadores
        self.FICHAS = fichas # Caracteres de las fichas de cada jugador
        self.tablero = Tablero(self, self.N, self.M, self.FICHAS)
        self.turno = -1 # Para el wey que le toca tirar
        self.dados = [] #Para guardar la última tirada de dados y esta luego ponerla en un array con todas las tiradas de la partida
        self.historial_dados = []
        self.tipos_jugadores = []


    def __repr__(self) -> str:
        """
        Función que retorna la representación en un string, como un jugador humano vería el turno actual de la partida.
        :return: String que contiene la representación del turno actual de la partida.
        """
        salida = f"JUGADA #{self.turno + 1}\n"
        salida += str(self.tablero) + "\n"
        salida += f"Turno de {self.obtener_jugador_actual()}: {self.imagen_dado()}"
        return salida

    ######
    ######
    ######
    ######
    ######
    ######

    def calcular_puntuacion_jugador(self, jugador, tablero=None, fichas_sacadas=None):
        """
        calcula puntuacion jugada por fichas y posiciones
        :param jugador: caracter indentifica jugador
        :param tablero: Estado actual del tablero
        :param fichas_sacadas: diccionario con las fichas sacadas
        :return: Puntuación numerica
        """

        if tablero is None:
            tablero = self.tablero.tablero  #copia tablero
        if fichas_sacadas is None:
            fichas_sacadas = self.tablero.fichas_sacadas  #copia fichas sacadas

        N = len(tablero)  #numero total de columnas
        M = self.M  #numero inicial de fichas por jugador
        copia_fichas_sacadas = fichas_sacadas.get(jugador, 0)  #fichas sacadas por este jugador


        puntos = 3 * (N + 1) * copia_fichas_sacadas #puntos base(3) por fichas sacadas

        #calcula puntos por fichas en el tablero
        for c in range(N):
            if tablero[c][0] == jugador:  #si columna es del jugador
                I_c = c + 1  #indice 1-based (A=1, B=2,...)
                N_c = tablero[c][1]  #cantidad de fichas en esta columna
                A_c = 2 if N_c > 1 else 1  #factor de apilamiento (2 o mas fichas = hay apilamiento)

                puntos += A_c * I_c * N_c #suma de los puntos

        return puntos  #puntuacion total

    def calcular_valor_jugada(self, jugada, jugador_actual):
        """
        Evalua una jugada calculando su valor estrategico, porque??? no basta con saber cuanto ganas tu,
        sino cuánto pierde el rival esto evita que la máquina elija jugadas que:
                te dan puntos, pero dan mas al rival
                no bloquean al rival cuando está por ganar
        :param jugada: lista de movimientos a evaluar
        :param jugador_actual: jugador que realiza la jugada
        :return: valor numeico de la jugada (mayor = mejor)
        """
        # Prepara copias para simular la jugada sin afectar el estado real
        tablero_simulado = self.tablero.realizar_copia_tablero()  #copia tablero
        fichas_sacadas_simulado = self.tablero.fichas_sacadas.copy()  #copia fichas tablero sacadas

        #simulacion cada movimiento
        for i in range(len(jugada)):
            if jugada[i] != -1:  #no es un movimiento nulo @
                # Aplica el movimiento en la simulación
                self.tablero.realizar_movimiento(
                    jugada[i],  #indice columns
                    self.dados[i],  #valor dado de esa columna
                    jugador_actual,  #jugador activo
                    tablero_simulado,  #copia tablero
                    fichas_sacadas_simulado  #copia fichas tablero sacadas
                )

        #calculo puntuación jugadores
        puntuaciones = {}
        for jugador in self.FICHAS:
            puntuaciones[jugador] = self.calcular_puntuacion_jugador(
                jugador,
                tablero_simulado,
                fichas_sacadas_simulado
            )

        #formula pag 8 sum(2*puntos_jugador - suma_puntos_rivales)
        p_j = puntuaciones[jugador_actual]  #puntos del jugador actual


        sum_p_k = 0  #suma puntos de todos los oponentes

        for jugador in puntuaciones:    #jugador y puntos

            if jugador != jugador_actual:   #si jugador actual
                sum_p_k += puntuaciones[jugador]  #sumar sus puntos

        return 2 * p_j - sum_p_k  #valor final jugada

    def obtener_jugadas_ordenadas(self, jugador):
        """
        Genera y ordena todas las jugadas posibles por su valor
        :param jugador: jugador actual
        :return: lista de jugadas ordenadas de mejor a peor (mayor a menor puntuacion)
        """

        jugadas_posibles = self.tablero.get_jugadas_posibles(self.dados, jugador)


        jugadas_con_valor = []  #guadar jugada y valor
        for jugada in jugadas_posibles:
            valor = self.calcular_valor_jugada(jugada, jugador)
            jugadas_con_valor.append((jugada, valor))  #una tupla de jugada y valor

        #ordenar mayor a menor
        for i in range(len(jugadas_con_valor)):
            for j in range(i + 1, len(jugadas_con_valor)):
                if jugadas_con_valor[i][1] < jugadas_con_valor[j][1]:
                    #intercambia las jugadas si están en el orden incorrectoº
                    jugadas_con_valor[i], jugadas_con_valor[j] = jugadas_con_valor[j], jugadas_con_valor[i]

        jugadas_ordenadas = jugadas_con_valor

        #extrae las jugadas sin los valores y las devuelve
        return [jugada for jugada, valor in jugadas_ordenadas]

    def jugada_maquina_lista(self):
        """
        Selecciona automáticamente la mejor jugada para la máquina 'lista'
        :return: String con la jugada en formato texto (ej. "AB@C")
        """
        jugador_actual = self.obtener_jugador_actual()

        #jugadas ordenadas por puntuaje
        jugadas_ordenadas = self.obtener_jugadas_ordenadas(jugador_actual)

        jugada_texto = "@" * self.D  #valor por defecto si no hay jugadas posibles con esos dados, movimiento nulo

        if len(jugadas_ordenadas) > 0:
            mejor_jugada = jugadas_ordenadas[0]
            jugada_texto = []
            for movimiento in mejor_jugada:
                if movimiento == -1:
                    jugada_texto.append('@')
                else:
                    jugada_texto.append(chr(65 + movimiento))
            jugada_texto = ''.join(jugada_texto)

        return jugada_texto

    def jugada_maquina_tonta(self):
        """
        Selecciona una jugada válida aleatoria para la máquina 'tonta'
        Devuelve la jugada en formato texto (ej. "AB@") o movimiento nulo si no hay jugadas válidas
        """
        jugador_actual = self.obtener_jugador_actual()
        jugadas_posibles = self.tablero.get_jugadas_posibles(self.dados, jugador_actual)

        jugada_texto = "@" * self.D  #valor por defecto si no hay jugadas posibles con esos dados, movimiento nulo

        if len(jugadas_posibles) > 0:  #al menos 1 jugada
            jugada_elegida = choice(jugadas_posibles)
            jugada_texto = "".join(
                "@" if mov == -1 else chr(65 + mov)
                for mov in jugada_elegida
            )
        #else se mantiene el valor por defecto, jugada sin movimiento @*numdados

        return jugada_texto

    ######
    ######
    ######
    ######
    ######
    ######

    def get_numero_jugador(self, jugador):
        return self.FICHAS.index(jugador) + 1


    def imagen_dado (self):
        """
        Función que retorna la representación de la tirada de dados.
        :return: String que contiene la representación de los dados de la tirada actual.
        """
        # devuelve el la cara de dado que haya salido
        simbolos_dados = ["⚀","⚁","⚂", "⚃", "⚄","⚅"] #https://es.piliapp.com/symbol/dice/
        resultado = ""
        for cara_dado in self.dados:
            resultado += simbolos_dados[cara_dado - 1] + " "
        return resultado

      
    def cambiar_turno(self) -> bool:
        """
         Cambia de turno. Devuelve True si es fin de partida, False si no
        :return: Booleano correspondiente a la verificación de si se ha terminado la partida.
        """
        # …
        self.turno += 1 #cambio turno
        # La tirada de dados se debe realizar con esta línea:
        self.dados = [randrange(6) + 1 for _ in range(self.D)] #estas dos lineas de los dados podriamos hacerlo en una funcion pequeñas, como veas
        self.historial_dados += [self.dados[:]]
        print(self)
        #Aqui se tiene que añadir una concicion que compruebe si se ha terminado la partida, en ese caso retorna un False

        return True #Devuelve un True cuando puede cambiar el turno, dejara de poder cambiar el turno al haberse terminado la partida

      
    def obtener_jugador_actual(self):
        """
        Función que retorna el carácter del jugador al que le toca jugar el turno.
        :return: Char del jugador actual.
        """
        return self.FICHAS[self.turno%len(self.FICHAS)]

        # |||||
        # |||||
        # |||||
        # |||||
        # |||||

    def configurar_jugadores(self):
        """
        Configura el tipo de cada jugador (Humano/Máquina Tonta/Máquina Lista)
        :return: lista de tipos de jugador (['H', 'T'], ['L', 'H'], etc.)
        """
        tipos_validos = {'H', 'T', 'L'}
        tipos_jugadores = []

        for ficha in self.FICHAS:
            tipo = self.pedir_tipo_jugadores(ficha, tipos_validos)
            tipos_jugadores.append(tipo)

        return tipos_jugadores

    def pedir_tipo_jugadores(self, ficha, tipos_validos):
        """
        Pide y valida el tipo de jugador
        :param ficha: simbolo del jugador
        :param tipos_validos:
        :return: tipo de jugador(H/T/L)
        """
        tipo = ""
        while tipo not in tipos_validos:
            entrada = input(f"Jugador {ficha} es [H]umano, Máquina [T]onta o Máquina [L]ista: ").upper()
            if entrada in tipos_validos:
                tipo = entrada
            else:
                print("Error: Ingrese H, T o L")
        return tipo

    def obtener_jugada_automatica(self, tipo_jugador):
        """
        Obtiene jugada automatica según el tipo de jugador
        :param tipo_jugador: H/T/L
        :return: jugada en formato texto o cadena vacia si no es maquina
        """
        jugada = ""
        if tipo_jugador == 'T':
            jugada = self.jugada_maquina_tonta()
        elif tipo_jugador == 'L':
            jugada = self.jugada_maquina_lista()

        return jugada

    # |||||
    # |||||
    # |||||
    # |||||
    # |||||


    def jugar(self, txt_jugada: str) -> None | str:
        """
        Función encargada de realizar la jugada del turno correspondiente al jugador actual.
            Comprueba si se puede realizar la jugada o no e intenta volver a pedir al usuario tantas
            veces como sea necesario que el jugador inserte una jugada válida
        :param txt_jugada: String correspondiente a la jugada que quiere realizar el jugador.
        :return: Booleano correspondiente a si se ha podido realizar o no la jugada.
        """
        jugada_realizada = False
        jugador_actual=self.obtener_jugador_actual()
        jugador_idx = self.FICHAS.index(jugador_actual)
        tipo_jugador = self.tipos_jugadores[jugador_idx]
#Aqui se tiene que añadir una funcion que compruebe que el texto introducido es válido y que la cantidad de caracteres no supera las de los dados
        if tipo_jugador in ('T', 'L') and txt_jugada is None:
            txt_jugada = self.obtener_jugada_automatica()
            print(f"Jugada automática: {txt_jugada}")
        #jugadas_posibles = self.tablero.get_jugadas_posibles(self.dados, jugador_actual)
        #print(jugadas_posibles)

        while not jugada_realizada:
            movimientos: list = [-1 if ord(c.lower()) - ord('a') == -33 else ord(c.lower()) - ord('a') for c in txt_jugada]

            if self.tablero.comprobar_movimientos(movimientos, self.dados, jugador_actual):
                for i in range(len(movimientos)):
                    jugada_realizada = self.tablero.realizar_movimiento(movimientos[i], self.dados[i], jugador_actual)
            else:
                txt_jugada = input("Jugada: ")
        # …

        
def main():
    """
    Función principal encargada de ejecutar el pargamon y mantener la partida activa hasta que se termine.
    :return: None
    """
    seed(AZAR)
    pydoc.writedoc('practica1')
    print("*** PARGAMMON ***")
    params = map(int, input("Numero de columnas, fichas y dados = ").split())
    juego = Pargammon(*params)
    while juego.cambiar_turno():
        resultado = None
        while resultado is not None:
            jugador_actual = juego.obtener_jugador_actual()
            jugador_idx = juego.FICHAS.index(jugador_actual)

            if juego.tipos_jugadores[jugador_idx] == 'H':
                resultado = juego.jugar(input("Jugada: "))
            else:
                resultado = juego.jugar()  # Sin parámetro para jugada automática

            if resultado is not None:
                print(resultado)


if __name__=="__main__":
   main()
