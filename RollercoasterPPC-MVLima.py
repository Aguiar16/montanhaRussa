import random, statistics, time, threading

# This is a function for storing stats when the program finishes its execution

def writeTheTimes(timeCars, timePassengers):
    with open('stats_for_nerds.txt','a') as output: # Here are the time stats for analisys
        output.write("######################################################################\n")
        output.write("Total utilization time of the car(s): " + str(timeCars) + "\n")
        output.write("Average passenger's passenger waiting time: "+ str(statistics.mean(timePassengers)) + "\n")
        output.write("\nMinimum passenger's waiting time on the line: "+ str(min(timePassengers)) + "\n")
        output.write("Maximum passenger's waiting time on the line: "+ str(max(timePassengers)) + "\n")
        output.write("######################################################################\n")

# Begining with the semaphores/mutex for cars and passengers

load = threading.Semaphore(0)
unload = threading.Semaphore(0)
loading = threading.Semaphore(1)
mutex = threading.Lock()

# Passenger's variables

passengerId = 1 # Start the naming of the passengers
line = 0 # The line starts empty, of course
passengersSitting = threading.Semaphore(0) # Semaphore to indicate if the passengers are sitting on the car
notEmpty = threading.Semaphore(0) # Semaphore for checking if the car is occupied
emptyLine = False # Flag that defines if the line of passengers is empty

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
            self.tPassengers.append(thread) # Adding the just created Thread Passenger to an array of threads

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
        
        print('* The roller coaster is closing *\n') # ...the roller coaster operator calls it a day a heads home.

        writeTheTimes(timeCars, timePassengers) # Calls the function for writing the times
        
        print('\n################### END ###################\n')

# Here we have the class Passenger, which contains actions that the passenger does,
# such as board and unboard:
class Passenger():
    def __init__ (self, id, nPassengers):
        self.id = id # Receives the id of this instance
        self.nPassengers = nPassengers # Receives the total amount of passengers
        self.tLine = 0 # Begins the counting of in line time of this passenger
        self.sitting = False # Flag for indicate if the passenger is on the car

    def board(self): # All aboard!
        global emptyLine
        global passengerId
        global timePassengers
        global line
        print(f'- Passenger {self.id} waiting on line') # When a passenger "arrives" on the line, this message is printed
        self.tLine = time.time() # Then we got a timestamp for that paticular moment
        with mutex:
            line +=1

        while not self.sitting:
            if self.id == passengerId:
                load.acquire() # Tries to sit on the car
                timePassengers.append((time.time() - self.tLine)) # When the passenger finally sits down, the time is accounted
                print(f'-> Passenger {self.id} boarding the car ->')
                self.sitting = True
                with mutex:
                    line -= 1
                if self.id == self.nPassengers: # If the id of the passenger is equivalent to the total amount of passengers...
                    emptyLine = True # ...then the line is empty.

                if (self.id) % 4 == 0: # Checks if the passenger is the last of a block of 4 to sit down
                    passengersSitting.release()
                passengerId += 1
    
    def unboard(self): # Gets off the car
        unload.acquire() 
        print(f'<- Passenger {self.id} is getting off the car <-')
        notEmpty.release() # Declares that the car is now ready for receiving new passengers

    def start(self):
        self.board()
        self.unboard()

# Now the Car class, that can ride, load and unload Passengers:
class Car:
    def __init__ (self, name):
        self.capacity = 4 # Defines the number of passengers for each car
        self.name = name # Name of the car
        self.busy = threading.Semaphore(1) # Semaphore to determine if the car is busy
        self.timeTotal = time.time() # Time stamp for the car start existing
        self.timeRide = 0 # Starts to track the amount of time for the ride

    def load(self): # Loads itself with a bunch of kids
        self.busy.acquire() # Sets the semaphore for the car to be busy
        print(f"\n***** Car {self.name} ready for loading passengers. *****\n")
        while not emptyLine: # Loads the passengers if there are passengers waiting in line
            if line > 3:
                for i in range(self.capacity):
                    load.release()
                    time.sleep(1) # 1 second for each passenger to load
                passengersSitting.acquire()
                self.busy.release()
                break

    def unload(self): # Gets rid of the now sicken children
        self.busy.acquire() # Sets the semaphore for the car to be busy
        print(f"\n***** Car {self.name} finished the ride. *****\n")
        for i in range(self.capacity): # Unloads all the passengers, one by one
            unload.release()
            notEmpty.acquire()
            time.sleep(1) # It takes 1 second to do this
        self.busy.release() # The car is free again

    def run(self): # The method to actually ride
        self.busy.acquire() # Sets the semaphore for the car to be busy
        print(f"\n***** Car {self.name} is moving. *****\n") # The car rides...
        time.sleep(10) # ...for preciselly 10 seconds and...
        self.busy.release() # ...ends the ride.
        
    def start(self): # Does his thing
        global timeCars # Time tracker for the cars
        global emptyLine # Marks the existence of a waiting line

        loading.acquire()
        while not emptyLine: # The car rides until there are either no passengers or less than 4. 
            self.load() # Have I mentioned before that I have vertigo? 
            loading.release()
            self.beginRun = time.time() # Time of the begining of the ride
            self.run() # Weeeeee
            self.timeRide += time.time() - self.beginRun # Stores the time of the ride
            self.unload() # Please do not throw up on the platform
            loading.acquire()
        loading.release()
        print(f"\n****** Car {self.name} is parking. *****\n") # Bye
        self.timeTotal = time.time() - self.timeTotal # Total time spent
        with mutex:
            timeCars.append(self.timeRide/self.timeTotal) # Calculates the time of the ride

def main ():
    print('##################################################################\n')
    print('# This is a roller coaster simulation using parallel programming #\n')
    print('##################################################################\n\n')
    c = input('Please type:\n\n[1] for [1 car, 52 passengers] \n[2] for [2 cars and 92 passengers] \n[3] for [3 cars and 148 passengers]\n\n')
    
    if c == '1': # The first case
        nCars = 1
        nPassengers = 52
        rollerCoaster = RollerCoaster(nCars, nPassengers) # Creates a RollerCoaster object with the given number of cars and passengers
        rollerCoaster.run()
    
    elif c == '2': # Second case...
        nCars = 2
        nPassengers = 92
        rollerCoaster = RollerCoaster(nCars, nPassengers) # Creates a RollerCoaster object with the given number of cars and passengers
        rollerCoaster.run()
    
    elif c == '3': # You already know the rest, don't you?
        nCars = 3
        nPassengers = 148
        rollerCoaster = RollerCoaster(nCars, nPassengers) # Creates a RollerCoaster object with the given number of cars and passengers
        rollerCoaster.run()

    else: # Please stop trying to break my code, will ya?
        print('\n###### Wrong input! ######\nPlease type only 1, 2 or 3\n\n')
        main()

if __name__ == "__main__":
    main()