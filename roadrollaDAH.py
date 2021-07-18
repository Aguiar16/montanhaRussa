import random,random,time,threading,random,statistics

npassageiros = 0
ncarros = 0

# Semaforos/mutex do carro/passageiro
vaga = threading.Semaphore(0)
vaza = threading.Semaphore(0)
mutex = threading.Lock() 
embarque = threading.Semaphore(0)
notFull = threading.Semaphore(0)
# variavel para os carros
temposC = []
# variavel para os passageiros
passId = 1
fila = 1
sentados = threading.Semaphore(0)
filaVazia = False
temposP = []

class MontanhaRussa():

    def __init__(self,ncarros,npassageiros):
        self.mutex = threading.Lock()
        self.passageiros = npassageiros
        self.totalCarros = ncarros
        self.embarque = threading.Semaphore(0)
        self.carrosId = 1
        self.threadsC = []
        self.threadsP = []

    def criaCarros(self):
        for i in self.totalCarros:
            c = threading.Thread(target=Carro(self.carrosId).start())
            self.carrosId +=1
            self.threadsC.append(c)

    def criaPassageiro(self):
        global fila
        for i in self.passageiros:
            c = threading.Thread(target=Passageiro(fila).start())
            fila +=1
            self.threadsP.append(c)

    def run(self):
        self.criaCarros()
        self.criaPassageiro()

        for t in self.threadsC:
            t.start()

        for t in self.threadsP:
            t.start()
            zzz = random.choice([1,2,3])
            time.sleep(zzz)
        
        for t in self.threadsC:
            t.join()

        for t in self.threadsP:
            t.join()
        
        with open('statistics.txt','a') as output:
            output.write("media de tempo na fila dos passageiros: ",statistics.mean(temposP))
            output.write("maximo de tempo na fila dos passageiros: ",max(temposP))
            output.write("minimo de tempo na fila dos passageiros: ",min(temposP))
            output.write("taxa de utilização dos carros: ",temposC)


class Passageiro():
    def __init__ (self,id):
        self.id = id
        self.nasceu = time.time()

    def board(self):
        global filaVazia
        sentado = False
        global passId
        global tempos
        global fila
        while not sentado:
            if self.id == passId:
                vaga.acquire()
                temposP.append((time.time()-self.nasceu))
                print('Passageiro ', self.id,' entrando no carro')
                sentado = True
                if fila == 1:
                    filaVazia = True
                elif fila != 1:
                    fila -=1

                if (self.id)%4 == 0:
                    sentados.release()
                passId+=1

    
    def unboard(self):
        vaza.acquire()
        print('Passageiro ', self.id,'esta saindo do carro')

    def start(self):
        self.board()
        self.unboard()
        

class Carro():
    def __init__ (self,nome):
        self.capacidade = 4
        self.nome = nome
        self.ocupado = threading.Semaphore(0)
        self.ligado = True
        self.tTotal = time.time()

    def load(self):
        self.ocupado.acquire()
        embarque.acquire()
        print("Carro ",self.nome," pronto para o embarque de passageiros")
        if fila >= 3:
            for i in range(self.capacidade):
                vaga.release()
            time.sleep(1)
            sentados.acquire()
            embarque.release()
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
        global temposC
        global filaVazia
        while not filaVazia:
            self.load(self)
            self.inicioCorrida = time.time()
            self.run(self)
            self.tCorrida += time.time() - self.inicioCorrida
            self.unload(self)
        self.tTotal = time.time - self.tTotal
        with mutex:
            temposC.append(self.tCorrida/self.tTotal)

def main ():
    global ncarros
    global npassageiros
    c = input('1 - 1 carro, 52 passageiros, 2- 2 carros e 92 passageiros, 3- 3 carros e 148 passageiros\n')
    if c == 1:
        ncarros = 1
        npassageiros = 52
        c = MontanhaRussa().run()
    elif c == 2:
        ncarros = 2
        npassageiros = 92
        c = MontanhaRussa().run()
    elif c == 3:
        ncarros = 3
        npassageiros = 148
        c = MontanhaRussa().run()

if __name__ == "__main__":
    main()