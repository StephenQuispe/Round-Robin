import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import random  # Importa el módulo random para generar números aleatorios
import time  # para calcular el tiempo

#parte logica
# Función que implementa el algoritmo de planificación Round Robin

def round_robin(matriz, quantum):
    n = len(matriz)  # Número de procesos
    restante = [proceso[1] for proceso in matriz]  # Lista de tiempos de CPU restantes para cada proceso
    tiempo_total = 0  # Variable para llevar la cuenta del tiempo total de ejecución
    result = []  # Lista para almacenar los resultados del Round Robin
    
    while True:
        bandera = True  # Bandera para controlar si todos los procesos han terminado
        for i in range(n):
            if restante[i] > 0:  # Si el proceso aún tiene tiempo de CPU restante
                bandera = False  # Indica que aún hay procesos pendientes
                tiempo_proceso = min(quantum, restante[i])  # Calcula el tiempo de CPU que se va a asignar
                tiempo_total += tiempo_proceso  # Incrementa el tiempo total de ejecución
                restante[i] -= tiempo_proceso  # Disminuye el tiempo de CPU restante del proceso
                result.append([i, tiempo_total])  # Almacena el índice del proceso y el tiempo total actual

        if bandera:  # Si todos los procesos han terminado, sale del bucle
            break
    return result, tiempo_total  # Devuelve los resultados y el tiempo total de ejecución

# Función para asignar tiempos finales a los procesos
def asigfinal(fin, ini):
    n = len(fin)  # Número de procesos en la lista final
    m = len(ini)  # Número de entradas en la lista inicial
    for i in range(n):
        for j in range(m):
            if i == ini[j][0]:  # Si el índice del proceso coincide
                fin[i][3] = ini[j][1]  # Asigna el tiempo final al proceso

    ini = ini[::-1]  # Invierte la lista inicial
    n = len(fin)
    m = len(ini)
    for i in range(n):
        for j in range(m):
            if i == ini[j][0]:  # Si el índice del proceso coincide
                fin[i][2] = ini[j][1] - 2  # Asigna el tiempo inicial al proceso (ajustado)

    for k in range(n):
        # Calcula los tiempos adicionales para cada proceso
        fin[k][4] = fin[k][3] - fin[k][2]  # Tiempo de respuesta
        fin[k][5] = fin[k][3] - fin[k][1] - fin[k][0]  # Tiempo de espera
        fin[k][6] = fin[k][0] + fin[k][1]  # Suma de tiempo de llegada y tiempo de CPU
        fin[k][7] = round(fin[k][6] / fin[k][4], 2)  # Razón entre la suma de tiempos y el tiempo de respuesta, redondeado a 2 decimales
    return fin

# Función para generar procesos con tiempos de llegada y de CPU aleatorios
def llenar(n, k, ini1, ini2, fin1, fin2):
    for i in range(n):
        tiempo_cero = random.randint(ini1, fin1)  # Genera un tiempo de llegada aleatorio entre 0 y 5
        tiempo_cpu = random.randint(ini2, fin2)  # Genera un tiempo de CPU aleatorio entre 4 y 12
        new = [tiempo_cero, tiempo_cpu, 0, 0, 0, 0, 0, 0]  # Crea una lista con los tiempos y otros campos inicializados a 0
        k.append(new)  # Añade el nuevo proceso a la lista
    return k

# Función para mostrar los resultados
def mostrar(l):
    print("     [t0_tcpu_ti_tf_tr_te_ts_Is]")  # Encabezado de la tabla
    for codigo, e in enumerate(l):
        print(codigo, ':', e)  # Muestra cada proceso con su índice y sus tiempos

def logica (NProcess,i1,i2,f1,f2,q,ite):
    # Solicita al usuario el número de procesos y el quantum
    #nro, quantum = input("ingrese nro procesos y el quantum separados por un espacio : ").split(' ')
    nro = NProcess  # Convierte el número de procesos a entero
    quantum = q  # Convierte el quantum a entero

    matriz = []  # Lista para almacenar los procesos
    mllena = llenar(nro, matriz,i1,f1,i2,f2)  # Llena la lista con procesos aleatorios
    mllena.sort()  # Ordena la lista de procesos por tiempo de llegada

    x = [0]  # Inicializa la lista x con 0
    y = [0]  # Inicializa la lista y con 0

    # Verifica si el tamaño de mllena es múltiplo de 100
    iteraciones = ite
    multiplo = nro % iteraciones == 0
    incremento = iteraciones

    # Ejecuta el algoritmo de manera incremental
    for i in range(incremento, nro + 1, incremento):
        start_time = time.time()  # Inicia el cronómetro
        result, tiempo_total = round_robin(mllena[:i], quantum)  # Ejecuta el algoritmo con un subconjunto de mllena
        end_time = time.time()  # Detiene el cronómetro
        execution_time = end_time - start_time  # Calcula el tiempo de ejecución
        x.append(i)  # Agrega el intervalo a la lista x
        y.append(round(execution_time, 3))  # Agrega el tiempo de ejecución a la lista y, redondeado a 3 decimales

    # Si el tamaño de mllena no es múltiplo de 5000, ejecuta con todos los procesos
    if not multiplo:
        start_time = time.time()  # Inicia el cronómetro
        result, tiempo_total = round_robin(mllena, quantum)  # Ejecuta el algoritmo con todos los procesos
        end_time = time.time()  # Detiene el cronómetro
        execution_time = end_time - start_time  # Calcula el tiempo de ejecución
        x.append(nro)  # Agrega el tamaño total de mllena a la lista x
        y.append(round(execution_time, 3))  # Agrega el tiempo de ejecución a la lista y, redondeado a 3 decimales

    #print(f"El tiempo de ejecución fue: {execution_time} segundos")
    return x, y

def crear_grafico(x, y, titulo='Gráfico', xlabel='Eje X', ylabel='Eje Y'):
    plt.figure()
    plt.plot(x, y, marker='o')
    plt.title(titulo)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.grid(True)
    plt.show()



# Asigna los tiempos finales a los procesos y muestra los resultados
# mllena = asigfinal(mllena, result)
# mostrar(mllena)

# Crear la ventana principal
root = tk.Tk()
root.title("Round Robin")

x = [0]
y = [0]



# Título centrado
title_label = ttk.Label(root, text="Round Robin", font=("Helvetica", 16))
title_label.grid(row=0, column=0, columnspan=4, pady=10)

# Etiquetas y entradas de texto con variables
labels = [
    "N. Procesos:",
    "Rango Tiempo LLegada Inicio:",
    "Rango Tiempo LLegada Final:",
    "Rango Tiempo CPU Inicio:",
    "Rango Tiempo CPU Final:",
    "Quantum 1:",
    "Quantum 2:",
    "Quantum 3:",
    "Intervalo de Procesos:"
]

variables = [tk.StringVar() for _ in range(9)]
entries = []

for i, (label, var) in enumerate(zip(labels, variables)):
    lbl = ttk.Label(root, text=label, font=12)
    entry = ttk.Entry(root, textvariable=var, font=12)
    if i < 5:
        lbl.grid(row=i+1, column=0, sticky=tk.E, padx=5, pady=5)
        entry.grid(row=i+1, column=1, padx=5, pady=5)
    else:
        lbl.grid(row=(i-5)+1, column=2, sticky=tk.E, padx=5, pady=5)
        entry.grid(row=(i-5)+1, column=3, padx=5, pady=5)
    entries.append(entry)

# Función para validar y mostrar los datos
def ejecutar():
    datos = []
    error = False

    # Validar los primeros nueve campos
    for i, var in enumerate(variables):
        valor = var.get()
        if not valor:
            print(f"Error: El campo '{labels[i]}' está vacío.")
            error = True
        elif not valor.isdigit():
            print(f"Error: El campo '{labels[i]}' debe ser un número.")
            error = True
        datos.append(valor) 

    

    #print(datos )
    # Mostrar los datos si no hay errores
   
    if not error:
        x1 = [0]
        y1 = [0]

        x1,y1 = logica(int(datos[0]),int(datos[1]),int(datos[2]),int(datos[3]),int(datos[4]),int(datos[5]),int(datos[8]))

        x2 = [0]
        y2 = [0]

        x2,y2 = logica(int(datos[0]),int(datos[1]),int(datos[2]),int(datos[3]),int(datos[4]),int(datos[6]),int(datos[8]))

        x3 = [0]
        y3 = [0]

        x3,y3 = logica(int(datos[0]),int(datos[1]),int(datos[2]),int(datos[3]),int(datos[4]),int(datos[7]),int(datos[8]))

        fig1 = crear_grafico(x1, y1, titulo='Quantum 1', xlabel='Iteraciones', ylabel='Segundos')
        fig2 = crear_grafico(x2, y2, titulo='Quantum 2', xlabel='Iteraciones', ylabel='Segundos')
        fig3 = crear_grafico(x3, y3, titulo='Quantum 3', xlabel='Iteraciones', ylabel='Segundos')

        canvas1 = FigureCanvasTkAgg(fig1, master=root)
        canvas1.draw()
        canvas1.get_tk_widget().grid(row=6, column=0, padx=5, pady=5)

        canvas2 = FigureCanvasTkAgg(fig2, master=root)
        canvas2.draw()
        canvas2.get_tk_widget().grid(row=6, column=1, padx=5, pady=5)

        canvas3 = FigureCanvasTkAgg(fig3, master=root)
        canvas3.draw()
        canvas3.get_tk_widget().grid(row=6, column=2, padx=5, pady=5)
        #for clave, valor in datos.items():
        #    print(f"{clave} {valor}")

# Botón "Ejecutar"
execute_button = ttk.Button(root, text="Ejecutar", command=ejecutar)
execute_button.grid(row=5, column=3, padx=5, pady=5)

# Crear gráficos usando matplotlib
def crear_grafico(x, y, titulo='Gráfico', xlabel='Eje X', ylabel='Eje Y', fig_size=(4, 4)):
    fig, ax = plt.subplots(figsize=fig_size)
    ax.plot(x, y, marker='o')
    ax.set_title(titulo)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.grid(True)
    return fig



fig1 = crear_grafico(x, y, titulo='Quantum 1', xlabel='Iteraciones', ylabel='Segundos')
fig2 = crear_grafico(x, y, titulo='Quantum 2', xlabel='Iteraciones', ylabel='Segundos')
fig3 = crear_grafico(x, y, titulo='Quantum 3', xlabel='Iteraciones', ylabel='Segundos')

canvas1 = FigureCanvasTkAgg(fig1, master=root)
canvas1.draw()
canvas1.get_tk_widget().grid(row=6, column=0, padx=5, pady=5)

canvas2 = FigureCanvasTkAgg(fig2, master=root)
canvas2.draw()
canvas2.get_tk_widget().grid(row=6, column=1, padx=5, pady=5)

canvas3 = FigureCanvasTkAgg(fig3, master=root)
canvas3.draw()
canvas3.get_tk_widget().grid(row=6, column=2, padx=5, pady=5)

# Textos finales
final_labels = ["TR:", "TE:", "TS:", "IS:"]
final_variables = [tk.StringVar() for _ in range(4)]
final_entries = []

for i, (label, var) in enumerate(zip(final_labels, final_variables)):
    lbl = ttk.Label(root, text=label)
    entry = ttk.Entry(root, textvariable=var)
    lbl.grid(row=7, column=i, sticky=tk.E, padx=5, pady=5)
    entry.grid(row=7, column=i+1, padx=5, pady=5)
    final_entries.append(entry)

# Iniciar el bucle principal de la aplicación
root.mainloop()
