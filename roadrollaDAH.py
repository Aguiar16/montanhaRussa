import random,random,time,threading,random,statistics

nPassengers = 0
nCars = 0

# Semaforos/mutex do Car/Passenger
vaga = threading.Semaphore(0)
vaza = threading.Semaphore(0)
mutex = threading.Lock() 
embarque = threading.Semaphore(1)

# Storing Cars and Passengers time
timeCars = []
timePassengers = []
# variavel para os passengers
passId = 1
fila = 0
sentados = threading.Semaphore(0)
vazaro = threading.Semaphore(0)
filaVazia = False

class RollerCoaster:

    def __init__(self, nCars, nPassengers):
        self.passengers = nPassengers
        self.totalOfCars = nCars
        self.carsId = 1
        self.threadsC = []
        self.threadsP = []

    def spawnCars(self):
        for i in range(self.totalOfCars):
            c = threading.Thread(target=Car(self.carsId).start)
            self.carsId +=1
            self.threadsC.append(c)

    def spawnPassenger(self):
        global fila
        for i in range(self.passengers):
            c = threading.Thread(target=Passenger(i+1).start)
            self.threadsP.append(c)

    def run(self):
        self.spawnCars()
        self.spawnPassenger()
        for t in self.threadsC:
            t.start()

        for t in self.threadsP:
            t.start()
            zzz = random.choice([1, 2, 3])
            time.sleep(zzz)
        
        for t in self.threadsC:
            t.join()

        for t in self.threadsP:
            t.join()
        
        print('The roller coaster is closing up...\n')

        with open('statistics.txt','a') as output:
            output.write("\nTempo médio dos passageiros na fila: "+ str(statistics.mean(timePassengers))+"\n")
            output.write("Tempo máximo de espera dos passageiros na fila: "+ str(max(timePassengers))+"\n")
            output.write("Tempo mínimo de espera dos passageiros na fila: "+ str(min(timePassengers))+"\n")
            output.write("Taxa de utilização dos carros: "+ str(timeCars)+"\n")
        
        print('Farewell\n')

class Passenger:
    def __init__ (self,id):
        self.id = id
        self.tfila = 0
        self.sentado = False

    def board(self):
        global filaVazia
        global passId
        global timePassengers
        global fila
        print(f'Passenger {self.id} esperando na fila')
        self.tfila = time.time()
        with mutex:
            fila +=1

        while not self.sentado:
            if self.id == passId:
                vaga.acquire()
                timePassengers.append((time.time()-self.tfila))
                print(f'Passenger {self.id} entrando no Car')
                self.sentado = True
                with mutex:
                    fila -=1
                if self.id == nPassengers:
                    filaVazia = True

                if (self.id)%4 == 0:
                    sentados.release()
                passId+=1
    
    def unboard(self):
        vaza.acquire()
        print(f'Passenger {self.id} esta saindo do Car')
        vazaro.release()

    def start(self):
        self.board()
        self.unboard()
        
class Car:
    def __init__ (self,nome):
        self.capacidade = 4
        self.nome = nome
        self.ocupado = threading.Semaphore(1)
        self.tTotal = time.time()
        self.tCorrida = 0

    def load(self):
        self.ocupado.acquire()
        print(f"\nCar {self.nome} pronto para o embarque de passengers\n")
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
        print(f"\nCar {self.nome} esta em movimento.\n")
        time.sleep(10)
        self.ocupado.release()

    def unload(self):
        self.ocupado.acquire()
        print(f"\nCar {self.nome} terminou o passeio.\n")
        for i in range(self.capacidade):
            vaza.release()
            vazaro.acquire()
            time.sleep(1)
        self.ocupado.release()
        
    def start (self):
        
        global timeCars
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
        print(f"\nCar {self.nome} esta sendo desligado.\n")
        self.tTotal = time.time() - self.tTotal
        with mutex:
            timeCars.append(self.tCorrida/self.tTotal)

def main ():
    global nCars
    global nPassengers
    print('This is a roller coaster simulation using parallel programming \n \n')
    c = input('Please type:\n [1] for [1 car, 52 passengers] \n [2] for [2 cars and 92 passengers] \n [3] for [3 cars and 148 passengers]\n')
    
    if c == '1':
        nCars = 1
        nPassengers = 52
        rollerCoaster = RollerCoaster(nCars,nPassengers)
        rollerCoaster.run()
    
    elif c == '2':
        nCars = 2
        nPassengers = 92
        rollerCoaster = RollerCoaster(nCars,nPassengers)
        rollerCoaster.run()
    
    elif c == '3':
        nCars = 3
        nPassengers = 148
        rollerCoaster = RollerCoaster(nCars,nPassengers)
        rollerCoaster.run()
    else:
        print('\nWrong input! \nPlease type only 1, 2 or 3\n')
        main()

if __name__ == "__main__":
    main()