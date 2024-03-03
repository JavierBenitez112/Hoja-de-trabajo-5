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
    fig, axs = plt.subplots(3, figsize=(10, 18))
    fig.suptitle('Tiempo Promedio en el Sistema vs. Número de Procesos')

    for i, intervalo in enumerate(INTERVALOS):
        tiempos_promedio = []
        desviaciones_estandar = []
        for num_proceso in NUM_PROCESOS:
            ejecutar_simulacion(num_proceso, RAM_CAPACITY, CPU_INSTRUCCIONES, num_cpus, intervalo)
            
            # Calcular promedio de tiempo
            promedio_tiempo = sum(resultados) / num_proceso
            tiempos_promedio.append(promedio_tiempo)
            
            # Calcular desviación estándar
            desviacion_estandar = (sum((x - promedio_tiempo) ** 2 for x in resultados) / num_proceso) ** 0.5
            desviaciones_estandar.append(desviacion_estandar)
            
            print(f"Para {num_proceso} procesos con intervalo {intervalo}:")
            print(f"Tiempo promedio en el sistema: {promedio_tiempo}")
            print(f"Desviación estándar: {desviacion_estandar}")
            print("-" * 30)  # Separador entre los resultados de cada configuración de la simulación

        # Crear DataFrame para el gráfico
        df = pd.DataFrame({'Tiempo Promedio': tiempos_promedio, 'Desviación Estándar': desviaciones_estandar}, index=NUM_PROCESOS)

        # Gráfico
        axs[i].plot(df.index, df['Tiempo Promedio'], marker='o', label=f"Intervalo {intervalo}")
        axs[i].fill_between(df.index, df['Tiempo Promedio'] - df['Desviación Estándar'], df['Tiempo Promedio'] + df['Desviación Estándar'], alpha=0.2)
        axs[i].set_xlabel("Número de Procesos")
        axs[i].set_ylabel("Tiempo Promedio en el Sistema")
        axs[i].legend()
        axs[i].grid(True)

    plt.tight_layout()
    plt.show()

def menu():
    while True:
        print("-"*30)
        print("Simulación de un sistema de procesos")
        print("1. Simulación con 100 de RAM, 3 instrucciones por ciclo y 1 CPU")
        print("2. Simulación con 200 de RAM, 3 instrucciones por ciclo y 1 CPU")
        print("3. Simulación con 100 de RAM, 6 instrucciones por ciclo y 1 CPU")
        print("4. Simulación con 100 de RAM, 3 instrucciones por ciclo y 2 CPU")
        print("5. Salir")
        opcion = int(input("Opción: "))
        
        if opcion == 1:
            RAM_CAPACITY = 100
            CPU_INSTRUCCIONES = 3
            num_cpus = 1
            main(RAM_CAPACITY, CPU_INSTRUCCIONES, num_cpus)
        elif opcion == 2:
            RAM_CAPACITY = 200
            CPU_INSTRUCCIONES = 3
            num_cpus = 1
            main(RAM_CAPACITY, CPU_INSTRUCCIONES, num_cpus)
        elif opcion == 3:
            RAM_CAPACITY = 100
            CPU_INSTRUCCIONES = 6
            num_cpus = 1
            main(RAM_CAPACITY, CPU_INSTRUCCIONES, num_cpus)
        elif opcion == 4:
            RAM_CAPACITY = 100
            CPU_INSTRUCCIONES = 3
            num_cpus = 2
            main(RAM_CAPACITY, CPU_INSTRUCCIONES, num_cpus)
        elif opcion == 5:
            break
        else:
            print("Opción inválida")

menu()
