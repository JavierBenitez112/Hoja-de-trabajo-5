import simpy
import random
import pandas as pd
import matplotlib.pyplot as plt

#Aclaracion, ya que se cambio la modalidad de trabajo de grupos a individual, 
#se reestructuro el codigo desapegandose de la estructura original, por lo que se elimino el uso de clases y se reestructuro el codigo para que sea mas entendible y funcional.

# Parámetros
RANDOM_SEED = 42
NUM_PROCESOS = [25, 50, 100, 150, 200]
INTERVALOS = [10, 5, 1]

def proceso(env, nombre, ram, cpu, CPU_INSTRUCCIONES, intervalo):
    # Estado new
    yield env.timeout(random.expovariate(1.0 / intervalo))
    
    # Estado ready
    memoria_necesaria = random.randint(1, 10)
    yield ram.get(memoria_necesaria)
    
    instrucciones_restantes = random.randint(1, 10)
    tiempo_en_sistema = 0
    while instrucciones_restantes > 0:
        with cpu.request() as req:
            yield req
            
            # Estado running
            yield env.timeout(1)  # Tiempo de ejecución del CPU
            instrucciones_restantes -= CPU_INSTRUCCIONES
            tiempo_en_sistema += 1
            
            if instrucciones_restantes <= 0:
                break

    # Determinar el siguiente estado
    estado_siguiente = "Terminated"
    if random.randint(1, 21) == 1:
        estado_siguiente = "Waiting"
    elif random.randint(1, 21) == 2:
        estado_siguiente = "Ready"
    
    # Guardar resultados
    resultados.append(tiempo_en_sistema)

def ejecutar_simulacion(num_procesos, RAM_CAPACITY, CPU_INSTRUCCIONES, num_cpus, intervalo):
    global resultados
    resultados = []
    env = simpy.Environment()
    random.seed(RANDOM_SEED)
    
    ram = simpy.Container(env, init=RAM_CAPACITY, capacity=RAM_CAPACITY)
    cpu = simpy.Resource(env, capacity=num_cpus)  # Cambiar la capacidad del CPU
    
    for i in range(num_procesos):
        env.process(proceso(env, f"Proceso {i}", ram, cpu, CPU_INSTRUCCIONES, intervalo))
    
    env.run()

def main(RAM_CAPACITY, CPU_INSTRUCCIONES, num_cpus):
    plt.figure(figsize=(10, 6))
    
    for intervalo in INTERVALOS:
        tiempos_promedio = []
        for num_proceso in NUM_PROCESOS:
            ejecutar_simulacion(num_proceso, RAM_CAPACITY, CPU_INSTRUCCIONES, num_cpus, intervalo)
            
            # Calcular promedio de tiempo
            promedio_tiempo = sum(resultados) / num_proceso
            tiempos_promedio.append(promedio_tiempo)
        
        # Crear DataFrame para el gráfico
        df = pd.DataFrame(tiempos_promedio, index=NUM_PROCESOS)

        # Graficar
        plt.plot(df, marker='o', label=f"Intervalo {intervalo}")

    plt.title("Tiempo Promedio en el Sistema vs. Número de Procesos")
    plt.xlabel("Número de Procesos")
    plt.ylabel("Tiempo Promedio en el Sistema")
    plt.xticks(NUM_PROCESOS)
    plt.legend(title="Intervalo")
    plt.grid(True)
    plt.show()

def menu():
    while True:
        print("Simulación de un sistema de procesos")
        print("1. Simulación con 100 de RAM, 3 instrucciones por ciclo y 1 CPU")
        print("2. Salir")
        opcion = int(input("Opción: "))
        
        if opcion == 1:
            RAM_CAPACITY = 100
            CPU_INSTRUCCIONES = 3
            num_cpus = 1
            main(RAM_CAPACITY, CPU_INSTRUCCIONES, num_cpus)
        elif opcion == 2:
            break
        else:
            print("Opción inválida")

menu()
