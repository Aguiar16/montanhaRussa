import random,string,random,time,threading,random,collections

capacidade = 4
npassageiros = 52
ncarros = 1

embarque = threading.Semaphore(0)
notFull = threading.Semaphore(0)
notEmpty = threading.Semaphore(0)
filaVazia = False

class MontanhaRussa:
    def __init__(self,ncarros,npassageiros):
        self.mutex = threading.Lock()
        self.passageiros = npassageiros
        self.totalCarros = ncarros
        self.carros = 0
        self.embarque = threading.Semaphore(0)
    
    def criaCarros(totalCarros):
        for i in totalCarros:
            c = threading.Thread(target=Passageiro)


class Passageiro():
    def __init__ (self,id,chegada,embarque,desembarque):
        self.id = id
        self.chegada = chegada
        self.embarque = embarque
        self.desembarque = desembarque
    
    

    

class Carro():
    def __init__ (self,capacidade):
        self.capacidade = capacidade
        self.mutex = threading.Lock()
        self.ocupado = threading.Semaphore(0)
        self.passageiros = 0
        self.ligado = True

    def board(self, passageiros):
        notFull.acquire()
        if self.ligado:
            with self.mutex:
                self.passageiros +=1
                if self.passageiros == self.capacidade:
                    self.
        else:
            
    def load():
    
    def start (self):
            # self.ocupado.acquire()
            self.load(self.passageiros)