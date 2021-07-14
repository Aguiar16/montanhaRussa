'''Problema do Bar dos filosofos
Universidade Estadual do Ceara - 2020.1 (2019.2)
Programação Paralela e Concorrente
Prof: Marcial Porto Fernandez
Aluno Erick Santos do Nascimento
'''
import sys
import threading
from threading import Thread, Lock
import time 
import random 

class filosofo (threading.Thread):
    def __init__ (self, filosofo_id, matriz_grafo, numero_de_ciclos):
        self.meu_id = filosofo_id
        self.objetivo = numero_de_ciclos
        self.n_bebidas = 0
        self.tempo_com_sede = 0
        self.tempo_total = 0
        self.estado = 'tranquilo'
        self.minhas_garrafas = self.matriz_grafo_minhas_garrafas(matriz_grafo)
        threading.Thread.__init__ (self)# Atenção essa instrução deve ser chamada para iniciar a thread
    
    def matriz_grafo_minhas_garrafas(self, matriz_grafo):# transforma a matrix_grafo em  uma lista de garrafas [id_garrafa]
        arestas = []
        aux = []
        for i in range( len(matriz_grafo) ):
            for j in range ( len(matriz_grafo[0]) ):
                if (i <= j) and (matriz_grafo [i][j] == 1):
                    aux.append(i)
                    aux.append(j)
                    arestas.append(aux)
                aux = []
        garrafas = []
        aux = []
        for k in range( len(arestas) ):
            if (self.meu_id == arestas[k][0]) or (self.meu_id == arestas[k][1]):
                aux = k
                garrafas.append(aux)
        return garrafas

    def print_info(self):
        print('\n')
        print('Filosofo - {}'.format(self.meu_id))
        print('Garrafas - {}'.format(self.minhas_garrafas))
        print('Vezes bebidas - {}'.format(self.n_bebidas))
        print('Tempo com sede - {}'.format(self.tempo_com_sede))
        print('Tempo total a o final da execução - {}'.format(self.tempo_total))
        print('\n')

    def adquirir_garrafas (self):
        print ("filosofo - {} esta com sede".format(self.meu_id)) 
        pedido = self.gerar_pedido() 
        print('{}° pedido do filosofo {} - {}'.format(self.n_bebidas+1, self.meu_id, pedido))
        global bar_man             
        self.tempo_com_sede = self.tempo_com_sede + bar_man.dar_garrafas(pedido, self.meu_id, self.n_bebidas)

    def beber (self):
        self.estado = 'com_sede'
        aux_time = time.time()
        self.adquirir_garrafas() 
        self.estado = 'bebendo'
        self.n_bebidas = self.n_bebidas + 1
        print ("filosofo - {} bebendo pela {}° vez".format(self.meu_id, self.n_bebidas))        
        time.sleep (1)
        self.estado = 'tranquilo'        
        print ("filosofo - {} terminou de beber pela {}° vez\n".format(self.meu_id, self.n_bebidas))
        self.devolver_garrafas()

    def devolver_garrafas (self):
        global bar_man
        bar_man.receber_garrafas(self.meu_id)
        print ("filosofo - {} terminou devolver as garrafas".format(self.meu_id))

    def viver (self):
        for i in range (self.objetivo):
            self.beber()
            time.sleep (random.randint(0, 2))# de 0 a 2

    def gerar_pedido(self):        
        pedido = []    
        posicoes_do_pedido = []    
        n_garrafas = random.randint( 2, len(self.minhas_garrafas) )        
        while len( posicoes_do_pedido ) < n_garrafas:            
            x = random.randint( 0, len(self.minhas_garrafas)-1 )
            if x in posicoes_do_pedido:
                pass
            else:
                posicoes_do_pedido.append(x)
        posicoes_do_pedido.sort()   
        for i in range(len( posicoes_do_pedido )):
            pedido.append(self.minhas_garrafas[ posicoes_do_pedido[i] ])
        return pedido

    def run (self):
        global terminado
        tempo_inicial = time.time()
        self.viver()
        self.tempo_total = time.time() - tempo_inicial
        self.print_info()
        terminado.append('{:6.0f}      |{:12.0f}             |{:11.5f}     |{:11.5f}   |  {}  '.format(self.meu_id, self.n_bebidas, self.tempo_com_sede, self.tempo_total, self.minhas_garrafas))
        terminado.append('------------|-------------------------|----------------|--------------|-----------')
#-------------------------------------------------------------------------------
class controle_bar(object):
    def __init__ (self, matriz_grafo):
        global ordem_de_sessao
        self.mutex = threading.Condition()
        self.controle_garrafa = []
        self.prateleira = []
        arestas = []
        aux = []
        for i in range( len(matriz_grafo) ):
            for j in range ( len(matriz_grafo[0]) ):
                if i <= j and (matriz_grafo [i][j] == 1):
                    aux.append(i)
                    aux.append(j)
                    arestas.append(aux)
                aux = []
        aux = []
        for k in range( len(arestas) ):
            aux = ficha_garrafa(k, arestas[k], -1)
            self.controle_garrafa.append(aux)
            self.prateleira.append(k)

    def print_info(self, id_filosofo):
        print(self.prateleira)
        print(' Garrafa | Propietario | Filosofos |   Interesse    | Filosofo que chamou')
        for i in  range( len(self.controle_garrafa) ):
            self.controle_garrafa[i].print_info(id_filosofo)
    
    def marcar_garrafas(self, lista_pedido, id_filosofo):#marca na ficha da garrafa e remove ela na prateleira
        for i in range( len( lista_pedido ) ):
            self.controle_garrafa[lista_pedido[i]].propietario = id_filosofo
        for i in range( len(lista_pedido) ):
            self.prateleira.remove( lista_pedido[i] )
        return True

    def desmarcar_garrafas(self, id_filosofo):#desmarca na ficha da garrafa e adiciona ela na prateleira
        for i in range( len( self.controle_garrafa ) ):
            if self.controle_garrafa[i].propietario == id_filosofo:
                self.controle_garrafa[i].propietario = -1               
                self.prateleira.append(  self.controle_garrafa[i].garrafa_id )
        return True 

    def mostrar_interesse_bar (self, lista_pedido, id_filosofo, numero_de_sessao):    
        for i in range( len( lista_pedido ) ):
            self.controle_garrafa [lista_pedido[i]].mostrar_interesse(id_filosofo, numero_de_sessao)   

    def retirar_interesse_bar (self, id_filosofo):
        for i in range( len( self.controle_garrafa ) ):
            if self.controle_garrafa[i].propietario == id_filosofo:
                self.controle_garrafa [i].retirar_interesse(id_filosofo)

    def dar_garrafas(self, lista_pedido, id_filosofo, numero_de_sessao):       
        aux_time = time.time()        
        ok = False        
        self.mostrar_interesse_bar (lista_pedido, id_filosofo, numero_de_sessao)        
        while not ok:

            self.mutex.acquire()

            if self.garrafas_disponiveis(id_filosofo, lista_pedido, numero_de_sessao):    
                ok = True
                tempo = time.time() - aux_time
                ordem_de_sessao.append([id_filosofo, numero_de_sessao])
                self.marcar_garrafas(lista_pedido, id_filosofo)
            else:
                self.mutex.wait()

            self.mutex.release()
        return tempo

    def receber_garrafas(self, id_filosofo):
        self.mutex.acquire()
        self.retirar_interesse_bar(id_filosofo)
        self.desmarcar_garrafas(id_filosofo)#cuidado todas as ações que precisam de propietario devem ser executadas antes pois vai pra -1        
        self.mutex.notifyAll()       
        self.mutex.release()

    def garrafas_disponiveis(self, id_filosofo, lista_pedido, numero_de_sessao):# True se filosofo pode pegar suas garrafas
        for i in range( len( lista_pedido ) ):
            if not self.controle_garrafa[ lista_pedido[i] ].filosofo_pode_usar( id_filosofo , numero_de_sessao):
                return False
        return True
#-------------------------------------------------------------------------------
class ficha_garrafa(object):
    def __init__ (self, id_garrafa, usuarios, propietario):
        self.garrafa_id =  id_garrafa
        self.usuarios = usuarios        
        self.interesse = [ False , False ]        
        self.propietario = propietario        
        self.numero_de_sessao_g = [1, 1]

    def mostrar_interesse(self, id_filosofo, numero_de_sessao):
        if self.usuarios[0] == id_filosofo:
            self.interesse[0] = True            
            self.numero_de_sessao_g[0] = numero_de_sessao            
            return True            
        elif self.usuarios[1] == id_filosofo:       
            self.interesse[1] = True        
            self.numero_de_sessao_g[1] = numero_de_sessao        
            return True       
        else:
            print('----------ERRO, ESSE FILOSOFO NÃO FOI IDENTIFICADO (marcar)----------')

    def retirar_interesse(self, id_filosofo):        
        if self.usuarios[0] == id_filosofo:
            self.interesse[0] = False           
            return True        
        if self.usuarios[1] == id_filosofo:
            self.interesse[1] = False           
            return True
        print('----------ERRO, ESSE FILOSOFO NÃO FOI IDENTIFICADO  (desmarcar)----------')

    def print_info(self, id_filosofo):
                print('{:5.0f}    |{:8.0f}     |  {}   | {} |{:8.0f}'.format(self.garrafa_id, self.propietario, self.usuarios, self.interesse, id_filosofo))
    
    def filosofo_pode_usar(self, id_filosofo, numero_de_sessao):        
        sou_o_propietario = self.propietario == id_filosofo        
        esta_livre = self.propietario == -1        
        if self.usuarios[0] == id_filosofo:
            o_outro_tem_interesse = self.interesse[1]
        elif self.usuarios[1] == id_filosofo:
            o_outro_tem_interesse = self.interesse[0]
        else:
            print('----------ERRO, ESSE FILOSOFO NÃO FOI IDENTIFICADO (pode usar)----------')        
        if self.usuarios[0] == id_filosofo:            
            meu_numero_de_sessão_menor = self.numero_de_sessao_g[0] <= self.numero_de_sessao_g[1]        
        elif self.usuarios[1] == id_filosofo:            
            meu_numero_de_sessão_menor = self.numero_de_sessao_g[1] <= self.numero_de_sessao_g[0]        
        else:
            print('----------ERRO, ESSE FILOSOFO NÃO FOI IDENTIFICADO (pode usar)----------')        
        if (not o_outro_tem_interesse) and esta_livre :
            return True        
        if (meu_numero_de_sessão_menor) and (esta_livre or sou_o_propietario):
            return True
        return False
#-------------------------------------------------------------------------------
def ler_matriz(local_de_arquivo):
    matriz = []
    aux = []
    arq = open(local_de_arquivo, 'r')
    for linha in arq:
        linha = linha.strip()
        linha = linha.split(", ")        
        for i in range(len(linha)):
            aux.append( int( linha[i] ) )   
        matriz.append(aux)
        aux = []
    return matriz
#-------------------------------------------------------------------------------"Trecho Principal"
caminho = sys.argv[1]
matriz_grafo = ler_matriz(caminho)

if len(matriz_grafo) < 9:
    numero_de_ciclos = 6
else:
    numero_de_ciclos = 3

terminado = []
terminado.append('\n\nFilosofo id | numero de vezes bebidas | tempo com sede |  tempo total |  garrafas ')
terminado.append('------------|-------------------------|----------------|--------------|-----------')

threads = []
numero_de_filosofos = len(matriz_grafo)
ordem_de_sessao = []

bar_man = controle_bar(matriz_grafo)

for i in range (numero_de_filosofos):
    novo_filosofo = filosofo (i, matriz_grafo, numero_de_ciclos)
    threads.append (novo_filosofo)
    novo_filosofo.start ()
for t in threads:
    t.join ()
print('\n\n')
for i in range( len( terminado ) ):#tabela
    print(terminado[i])
print('\n')
print('id, vez')
for i in range( len(ordem_de_sessao) ):
    print(ordem_de_sessao[i])
