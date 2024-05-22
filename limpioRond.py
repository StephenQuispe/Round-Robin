import random
import decimal
def round_robin(matriz, quantum):
    n = len(matriz)
    restante = [proceso[1] for proceso in matriz]
    tiempo_total = 0
    result = []
    
    while True:
        bandera = True
        for i in range(n):
            if restante[i] > 0:
                bandera = False
                tiempo_proceso = min(quantum, restante[i])
                tiempo_total += tiempo_proceso
                restante[i] -= tiempo_proceso
                result.append([i, tiempo_total])

        if bandera:
            break

    return result, tiempo_total

def asigfinal(fin, ini):
  n = len(fin)
  m = len(ini)
  for i in range (n):
    for j in range (m):
      if(i==ini[j][0]):
        fin[i][3]= ini[j][1]
  ini = ini[::-1]
  n = len(fin)
  m = len(ini)
  for i in range (n):
    for j in range (m):
      if(i==ini[j][0]):
        fin[i][2]= ini[j][1]-2
  r = len(fin)
  for k in range (n):
    #decimal.getcontext().prec = 3
    fin[k][4]=fin[k][3]-fin[k][2]
    fin[k][5]=fin[k][3]-fin[k][1]-fin[k][0]
    fin[k][6]=fin[k][0]+fin[k][1]
    fin[k][7]= round(fin[k][6]/fin[k][4],2)
  return fin

def llenar(n,k):
    for i in range (n):
        tiempo_cero =random.randint(0,5)
        tiempo_cpu =random.randint(4,12)
        new=[tiempo_cero,tiempo_cpu,0,0,0,0,0,0]
        k.append(new)
    return k

def mostrar(l):
    print("     [t0_tcpu_ti_tf_tr_te_ts_Is]")
    for codigo,e in enumerate(l):
        print(codigo,':', e)

nro, quantum = input("ingrese nro procesos y el quantum separados por un espacio : ").split(' ')
nro=int(nro)
quantum = int(quantum)
matriz = []
mllena=llenar(nro,matriz)
mllena.sort()
result, tiempo_total = round_robin(mllena, quantum)
print("Resultado de la lógica Round Robin: ", result)
print("Tiempo total de ejecución: ", tiempo_total)
mllena = asigfinal(mllena, result)
mostrar(mllena)
input()
#revers = ini[::-1]