import random,string,random,time,threading,random,collections

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

class MontanhaRussa():
    def __init__(self,ncarros,npassageiros):
        self.mutex = threading.Lock()
        self.passageiros = npassageiros
        self.totalCarros = ncarros
        self.embarque = threading.Semaphore(0)
        self.carros = 0
        self.threads = []

    def criaCarros(self):
        for i in self.totalCarros:
            c = threading.Thread(target=Carro.run(self.carros))
            self.threads.append(c)

    def criaPassageiro(self):
        global fila
        for i in self.passageiros:
            c = threading.Thread(target=Passageiro(fila).run())
            fila +=1
            self.threads.append(c)




class Passageiro(object):
    def __init__ (self,id):
        self.id = id
        self.chegada = 0
        self.embarque = 0
        self.desembarque = 0

    def board(self):
        global filaVazia
        sentado = False
        global passId
        while not sentado:
            if self.id == passId:
                vaga.acquire()
                print('Passageiro ', self.id,' entrando no carro')
                sentado = True
                if self.id == npassageiros-1:
                    filaVazia = True
                if (self.id)%4 == 0:
                    sentados.release()
                passId+=1

    
    def unboard(self):
        vaza.acquire()
        print('Passageiro ', self.id,'esta saindo do carro')
        # time

    def run(self):
        self.board()
        self.unboard()
        

    

class Carro():
    def __init__ (self,nome):
        self.capacidade = 4
        self.nome = nome
        self.mutex = threading.Lock()
        self.ocupado = threading.Semaphore(0)
        self.ligado = True

    

    def load(self):
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
        print("Carro ",self.nome,"esta em movimento.")
        time.sleep(10)
        self.ocupado.release()

    def unload(self):
        self.ocupado.acquire()
        print("Carro ",self.nome,"chegou terminou o passeio.")
        for i in range(self.capacidade):
                vaza.release()
        
    
    def start (self):
        while not filaVazia:
            self.load(self)
            self.run(self)
            self.unload(self)