import threading
import time
import collections
from random import randint
import sys

CARRO_SIZE = 4
PASSAGEIROS = 17
LAPS = PASSAGEIROS/CARRO_SIZE

class MontanhaRussa(object):

    def __init__(self,size):
        self.mutex = threading.Lock() 
        self.notFull = threading.Semaphore(0) 
        self.notEmpty = threading.Semaphore(0) 
        self.notReady = threading.Semaphore(0)
        self.numpax = 0
        self.total = 0
        self.rides = True

        msg = 'we have '
        msg = msg + str(PASSAGEIROS)
        msg = msg + ' passengers'
        print(msg)

    def stop(self):
        self.notReady.acquire()
        self.rides = False
        time.sleep(1)
        print('\nThe car ends\n')
        for i in range(PASSAGEIROS % CARRO_SIZE):
            self.notFull.release()
            self.notEmpty.release()

    def load(self):
        self.notReady.acquire()
        print('\nCar loading...\n')
        for i in range(CARRO_SIZE):
            self.notFull.release()

    def unload(self):
        self.notReady.acquire()
        print('Car unloading...\n')
        for i in range(CARRO_SIZE):
            self.notEmpty.release()

    def ride(self):
        self.notReady.acquire()
        print('\nCar running ... \n')
        time.sleep(1)
        self.notReady.release()

    def board(self, name):
        self.notFull.acquire()
        if self.rides:
            print(name,'boarding')
            with self.mutex:
                self.numpax = self.numpax + 1
                if (self.numpax == CARRO_SIZE):
                    self.notReady.release()
        else:
            msg = name + ': I will be back'
            print(msg)

    def quit(self, name):
        if (self.rides):
            self.notEmpty.acquire()
            print(name, "unboarding")
            with self.mutex:
                self.numpax = self.numpax - 1
                if (self.numpax == 0):
                    self.notReady.release()

    def greet(self, name):
        with self.mutex:
            print("Hello my name is ", name)
            self.total = self.total + 1
            if (self.total == PASSAGEIROS):
                self.notReady.release()

    def goodbye(self, name):
        msg = name + ": Bye"
        print(msg)

def Carro(carro):
    for i in range(int(LAPS)):
        carro.load()
        carro.ride()
        carro.unload()
    carro.stop()

def Passageiro(carro):
    num = randint(1,500)
    name = str(num)
    carro.greet(name)
    carro.board(name)
    carro.quit(name)
    carro.goodbye(name)

def main():
    threads = []

    carro = MontanhaRussa(CARRO_SIZE)
    for i in range(PASSAGEIROS):
        c = threading.Thread(target=Passageiro, args=(carro, ))
        threads.append(c)

    p = threading.Thread(target=Carro, args=(carro, ))
    threads.append(p)

    for t in threads:
        t.start()

    for t in threads:
        t.join()

    print("End")

if __name__ == "__main__":
    main()