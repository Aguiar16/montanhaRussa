import threading
import time
import collections
from random import randint
import sys

VAGON_SIZE = 4
USERS = 17
LAPS = USERS/VAGON_SIZE

class roller(object):
# desde esta clase controlamos la concurrencia de todas las operaciones que realizan los pasajeros y el vagon. Para ello utilizamos tres semaforos y un mutex.
    def __init__(self,size):
        self.mutex = threading.Lock() # contador pasajeros vagon
        self.notFull = threading.Semaphore(0) # controla vagon lleno
        self.notEmpty = threading.Semaphore(0) #controla vagon vacio
        self.notReady = threading.Semaphore(0)
        self.numpax = 0
        self.total = 0
        self.viajes = True

        msg = 'we have '
        msg = msg + str(USERS)
        msg = msg + ' passengers'
        print(msg)
    def start(self):
        self.notReady.acquire()
        print('\nThe car works ....\n')
        self.notReady.release()
    def stop(self):
        self.notReady.acquire()
        self.viajes = False
        time.sleep(1)
        print('\nThe car ends\n')
        for i in range(USERS % VAGON_SIZE):
            self.notFull.release()
            self.notEmpty.release()
    def cargar(self):
        self.notReady.acquire()
        print('\nCar loading...\n')
        for i in range(VAGON_SIZE):
            self.notFull.release()
    def descargar(self):
        self.notReady.acquire()
        print('Car unloading...\n')
        for i in range(VAGON_SIZE):
            self.notEmpty.release()
    def rodar(self):
        self.notReady.acquire()
        print('\nCar running ... \n')
        time.sleep(4)
        self.notReady.release()
    def subir(self, name):
        self.notFull.acquire()
        if self.viajes:
            print(name,'boarding')
            with self.mutex:
                self.numpax = self.numpax + 1
                if (self.numpax == VAGON_SIZE):
                    self.notReady.release()
        else:
            msg = name + ': I will be back'
            print(msg)
    def bajar(self, name):
        if (self.viajes):
            self.notEmpty.acquire()
            print(name, "unboarding")
            with self.mutex:
                self.numpax = self.numpax - 1
                if (self.numpax == 0):
                    self.notReady.release()

    def saluda(self, name):
        with self.mutex:
            print("Hello my name is ", name)
            self.total = self.total + 1
            if (self.total == USERS):
                self.notReady.release()

    def despide(self, name):
        msg = name + ": Bye"
        print(msg)

def mivagon(vagon):
    vagon.start()
    for i in range(int(LAPS)):
        vagon.cargar()
        vagon.rodar()
        vagon.descargar()
        vagon.stop()

def pasajeros(vagon):
    num = randint(1, 456)
    name = str(num)
    vagon.saluda(name)
    vagon.subir(name)
    vagon.bajar(name)
    vagon.despide(name)

def main():
    threads = []

    vagon = roller(VAGON_SIZE)
    for i in range(USERS):
        c = threading.Thread(target=pasajeros, args=(vagon, ))
        threads.append(c)

    p = threading.Thread(target=mivagon, args=(vagon, ))
    threads.append(p)

    for t in threads:
        t.start()

    for t in threads:
        t.join()

    print("End")

if __name__ == "__main__":
    main()