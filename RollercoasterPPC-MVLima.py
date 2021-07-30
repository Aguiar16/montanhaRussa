import time,threading,random,statistics

# Begining with the semaphores/mutex for cars and passengers

load = threading.Semaphore(0)
unload = threading.Semaphore(0)
loading = threading.Semaphore(1)
mutex = threading.Lock()

# Passenger's variables

passId = 1
line = 0
passengersSitting = threading.Semaphore(0)
notEmpty = threading.Semaphore(0)
emptyLine = False

# Storing cars and passengers time on arrays, for further statistics

timeCars = []
timePassengers = []

# Starting with the Roller Coaster class, which will be responsible for
# spawning passengers, cars and keep the track of the waiting time for
# passengers.

class RollerCoaster():
    def __init__(self, nCars, nPassengers):
        self.nPassengers = nPassengers # The amount of passengers that were passed from the menu
        self.totalOfCars = nCars # The amount of cars that were passed from the menu
        self.tPassengers = [] # Array containing passengers' threads
        self.tCars = [] # Array containing cars' threads
        self.carsId = 0 # Naming the cars

    def spawnPassengers(self): # Function for creating passengers, each on separate threads
        global line # Variable that creates the line of passengers

        for i in range(self.nPassengers):
            thread = threading.Thread(target=Passenger(i+1, self.nPassengers).start) # Creates a Passenger object on a thread, given an unique id and the total amount of passengers
            self.tPassengers.append(thread) # Adding the just created Thread Passenger to a array of threads

    def spawnCars(self): # Function for creating cars, each on separate threads
        for i in range(self.totalOfCars):
            self.carsId +=1
            thread = threading.Thread(target=Car(self.carsId).start) # Creates an Car object on a thread, given an unique id
            self.tCars.append(thread) # Adding the just created Thread Car to a array of threads

    def run(self):
        self.spawnCars() # Creates the cars
        self.spawnPassengers() # Creates the passengers
        for thread in self.tCars: # Kickstarts all created Car threads
            thread.start()

        for thread in self.tPassengers: # Kickstarts all created Passenger threads BUT...
            zzz = random.choice([1, 2, 3])
            time.sleep(zzz) # ...ONLY after a randon time between 1 an 3 seconds! 
            thread.start()
        
        for thread in self.tCars: # Makes sure these threads...
            thread.join()

        for thread in self.tPassengers: # ...do their routines, when finally...
            thread.join()
        
        print('The roller coaster is closing...\n') # ...the roller coaster operator calls it a day a heads home.

        with open('stats_for_nerds.txt','a') as output: # Here are
            output.write("Taxa de utilizacao dos carros: "+ str(timeCars)+"\n")
            output.write("Tempo medio dos passageiros na fila: "+ str(statistics.mean(timePassengers))+"\n")
            output.write("\nTempo minimo de espera dos passageiros na fila: "+ str(min(timePassengers))+"\n")
            output.write("Tempo maximo de espera dos passageiros na fila: "+ str(max(timePassengers))+"\n")
        
        print('\n################### END ###################\n')

class Passenger():
    def __init__ (self, id, nPassengers):
        self.id = id
        self.nPassengers = nPassengers
        self.tLine = 0
        self.sitting = False

    def board(self):
        global emptyLine
        global passId
        global timePassengers
        global line
        print(f'Passenger {self.id} waiting on line')
        self.tLine = time.time()
        with mutex:
            line +=1

        while not self.sitting:
            if self.id == passId:
                load.acquire()
                timePassengers.append((time.time()-self.tLine))
                print(f'Passenger {self.id} boarding the car')
                self.sitting = True
                with mutex:
                    line -=1
                if self.id == self.nPassengers:
                    emptyLine = True

                if (self.id)%4 == 0:
                    passengersSitting.release()
                passId+=1
    
    def unboard(self):
        unload.acquire()
        print(f'Passenger {self.id} is getting off the car')
        notEmpty.release()

    def start(self):
        self.board()
        self.unboard()
        
class Car:
    def __init__ (self, name):
        self.capacity = 4
        self.name = name
        self.busy = threading.Semaphore(1)
        self.tTotal = time.time()
        self.tRide = 0

    def run(self):
        self.busy.acquire()
        print(f"\nCar {self.name} is moving.\n")
        time.sleep(1)
        self.busy.release()

    def load(self):
        self.busy.acquire()
        print(f"\nCar {self.name} ready for loading passengers\n")
        while not emptyLine:
            if line > 3:
                for i in range(self.capacity):
                    load.release()
                    time.sleep(1)
                passengersSitting.acquire()
                self.busy.release()
                break

    def unload(self):
        self.busy.acquire()
        print(f"\nCar {self.name} finished the ride.\n")
        for i in range(self.capacity):
            unload.release()
            notEmpty.acquire()
            time.sleep(1)
        self.busy.release()
        
    def start(self):
        global timeCars
        global emptyLine
        loading.acquire()
        while not emptyLine:
            self.load()
            loading.release()
            self.beginRun = time.time()
            self.run()
            self.tRide += time.time() - self.beginRun
            self.unload()
            loading.acquire()
        loading.release()
        print(f"\nCar {self.name} is shutting down.\n")
        self.tTotal = time.time() - self.tTotal
        with mutex:
            timeCars.append(self.tRide/self.tTotal)

def main ():
    print('This is a roller coaster simulation using parallel programming \n \n')
    c = input('Please type:\n [1] for [1 car, 52 passengers] \n [2] for [2 cars and 92 passengers] \n [3] for [3 cars and 148 passengers]\n')
    
    if c == '1':
        nCars = 1
        nPassengers = 52
        rollerCoaster = RollerCoaster(nCars, nPassengers)
        rollerCoaster.run()
    
    elif c == '2':
        nCars = 2
        nPassengers = 92
        rollerCoaster = RollerCoaster(nCars, nPassengers)
        rollerCoaster.run()
    
    elif c == '3':
        nCars = 3
        nPassengers = 148
        rollerCoaster = RollerCoaster(nCars, nPassengers)
        rollerCoaster.run()
    else:
        print('\nWrong input! \nPlease type only 1, 2 or 3\n')
        main()

if __name__ == "__main__":
    main()