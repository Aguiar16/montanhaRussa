import random,string,random,time,threading,random,collections

capacidade = 4
npassageiros = 52
fila = 0
ncarros = 1

embarque = threading.Semaphore(0)
notFull = threading.Semaphore(0)

# Semaforos do carro p/ o passageiro
vaga = threading.Semaphore(0)
vaza = threading.Semaphore(0)

# variavel para os passageiros
passId = 0

sentados = threading.Semaphore(0)
filaVazia = False

class MontanhaRussa:
    def __init__(self,ncarros,npassageiros):
        self.mutex = threading.Lock()
        self.passageiros = npassageiros
        self.totalCarros = ncarros
        self.embarque = threading.Semaphore(0)
        self.carros = 0
    
    def criaCarros(totalCarros):
        for i in totalCarros:
            c = threading.Thread(target=Passageiro)


class Passageiro():
    def __init__ (self,id,chegada,embarque,desembarque):
        self.id = id
        self.chegada = chegada
        self.embarque = embarque
        self.desembarque = desembarque

    def board(self,fila):
        sentado = False
        global passId
        while not sentado:
            if self.id == passId:
                vaga.acquire()
                print('Passageiro ', self.id,' entrando no carro')
                sentado = True
                passId+=1
                if self.id%4 == 0:
                    sentados.release()


    
    def offboard(self):
        vaza.acquire()
        print('Passageiro ', self.id,' saindo do carro')
        # time
        

    

class Carro():
    def __init__ (self,nome):
        self.capacidade = 4
        self.nome = nome
        self.mutex = threading.Lock()
        self.ocupado = threading.Semaphore(0)
        self.ligado = True

    

    def load(self,fila):
        self.ocupado.acquire()
        print("Carro ",self.nome,"pronto para o embarque de passageiros")
        if fila >= 3:
            for i in range(self.capacidade):
                vaga.release()
            time.sleep(1)
            sentados.acquire()
            self.ocupado.release()
    
    def run(self):
        self.ocupado.acquire()
        
    
    def start (self):
        # while self.ligado:
        self.load(self.passageiros)