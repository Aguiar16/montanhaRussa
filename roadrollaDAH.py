import random,random,time,threading,random,statistics

npassageiros = 0
ncarros = 0

# Semaforos/mutex do carro/passageiro
vaga = threading.Semaphore(0)
vaza = threading.Semaphore(0)
mutex = threading.Lock() 
embarque = threading.Semaphore(1)

# variavel para os carros
temposC = []
# variavel para os passageiros
passId = 1
fila = 0
sentados = threading.Semaphore(0)
vazaro = threading.Semaphore(0)
filaVazia = False
temposP = []

class MontanhaRussa:

    def __init__(self,ncarros,npassageiros):
        self.passageiros = npassageiros
        self.totalCarros = ncarros
        self.carrosId = 1
        self.threadsC = []
        self.threadsP = []

    def criaCarros(self):
        for i in range(self.totalCarros):
            c = threading.Thread(target=Carro(self.carrosId).start)
            self.carrosId +=1
            self.threadsC.append(c)

    def criaPassageiro(self):
        global fila
        for i in range(self.passageiros):
            c = threading.Thread(target=Passageiro(i+1).start)
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
        
        print('A montanha russa esta fechando ...\n')

        with open('statistics.txt','a') as output:
            output.write("\nmedia de tempo na fila dos passageiros: "+ str(statistics.mean(temposP))+"\n")
            output.write("maximo de tempo na fila dos passageiros: "+ str(max(temposP))+"\n")
            output.write("minimo de tempo na fila dos passageiros: "+ str(min(temposP))+"\n")
            output.write("taxa de utilização dos carros: "+ str(temposC)+"\n")
        
        print('Adeus\n')

class Passageiro:
    def __init__ (self,id):
        self.id = id
        self.tfila = 0
        self.sentado = False

    def board(self):
        global filaVazia
        global passId
        global temposP
        global fila
        print(f'Passageiro {self.id} esperando na fila')
        self.tfila = time.time()
        with mutex:
            fila +=1

        while not self.sentado:
            if self.id == passId:
                vaga.acquire()
                temposP.append((time.time()-self.tfila))
                print(f'Passageiro {self.id} entrando no carro')
                self.sentado = True
                with mutex:
                    fila -=1
                if self.id == npassageiros:
                    filaVazia = True

                if (self.id)%4 == 0:
                    sentados.release()
                passId+=1
    
    def unboard(self):
        vaza.acquire()
        print(f'Passageiro {self.id} esta saindo do carro')
        vazaro.release()

    def start(self):
        self.board()
        self.unboard()
        
class Carro:
    def __init__ (self,nome):
        self.capacidade = 4
        self.nome = nome
        self.ocupado = threading.Semaphore(1)
        self.tTotal = time.time()
        self.tCorrida = 0

    def load(self):
        self.ocupado.acquire()
        print(f"\nCarro {self.nome} pronto para o embarque de passageiros\n")
        while not filaVazia:
            if fila > 3:
                for i in range(self.capacidade):
                    vaga.release()
                    time.sleep(1)
                sentados.acquire()
                self.ocupado.release()
                break
    
    def run(self):
        self.ocupado.acquire()
        print(f"\nCarro {self.nome} esta em movimento.\n")
        time.sleep(10)
        self.ocupado.release()

    def unload(self):
        self.ocupado.acquire()
        print(f"\nCarro {self.nome} terminou o passeio.\n")
        for i in range(self.capacidade):
            vaza.release()
            vazaro.acquire()
            time.sleep(1)
        self.ocupado.release()
        
    def start (self):
        
        global temposC
        global filaVazia
        embarque.acquire()
        while not filaVazia:
            self.load()
            embarque.release()
            self.inicioCorrida = time.time()
            self.run()
            self.tCorrida += time.time() - self.inicioCorrida
            self.unload()
            embarque.acquire()
        embarque.release()
        print(f"\nCarro {self.nome} esta sendo desligado.\n")
        self.tTotal = time.time() - self.tTotal
        with mutex:
            temposC.append(self.tCorrida/self.tTotal)

def main ():
    global ncarros
    global npassageiros
    c = input('1 - 1 carro, 52 passageiros, 2- 2 carros e 92 passageiros, 3- 3 carros e 148 passageiros\n')
    if c == '1':
        ncarros = 1
        npassageiros = 52
        d = MontanhaRussa(ncarros,npassageiros)
        d.run()
    elif c == '2':
        ncarros = 2
        npassageiros = 92
        d = MontanhaRussa(ncarros,npassageiros)
        d.run()
    elif c == '3':
        ncarros = 3
        npassageiros = 148
        d = MontanhaRussa(ncarros,npassageiros)
        d.run()

if __name__ == "__main__":
    main()