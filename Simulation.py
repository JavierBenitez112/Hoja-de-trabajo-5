import simpy
import random
import pandas as pd
import matplotlib.pyplot as plt

#Aclaracion, ya que se cambio la modalidad de trabajo de grupos a individual, 
#se reestructuro el codigo desapegandose de la estructura original, por lo que se elimino el uso de clases y se reestructuro el codigo para que sea mas entendible y funcional.

# Definición de parámetros estaticos
RANDOM_SEED = 42
NUM_PROCESOS = [25, 50, 100, 150, 200]
INTERVALOS = [10, 5, 1]

# Función para simular el proceso de un proceso
def proceso(env, nombre, ram, cpu, CPU_INSTRUCCIONES, intervalo):
    # Nuevo proceso en espera de tiempo aleatorio
    yield env.timeout(random.expovariate(1.0 / intervalo))
    
    # El proceso está listo, se asigna memoria
    memoria_necesaria = random.randint(1, 10)
    yield ram.get(memoria_necesaria)
    
    # Ejecución de instrucciones hasta terminar
    instrucciones_restantes = random.randint(1, 10)
    tiempo_en_sistema = 0
    while instrucciones_restantes > 0:
        with cpu.request() as req:
            yield req
            
            # Ejecución en el CPU durante un ciclo
            yield env.timeout(1)
            instrucciones_restantes -= CPU_INSTRUCCIONES
            tiempo_en_sistema += 1
            
            if instrucciones_restantes <= 0:
                break
    
    # Determinar el siguiente estado del proceso
    estado_siguiente = "Terminado"
    if random.randint(1, 21) == 1:
        estado_siguiente = "En espera"
    elif random.randint(1, 21) == 2:
        estado_siguiente = "Listo"

    # Registrar el tiempo en el sistema
    resultados.append(tiempo_en_sistema)

# Función para ejecutar la simulación
def ejecutar_simulacion(num_procesos, RAM_CAPACITY, CPU_INSTRUCCIONES, num_cpus, intervalo):
    global resultados
    resultados = []
    env = simpy.Environment()
    random.seed(RANDOM_SEED)
    
    # Inicializar recursos (memoria RAM y CPU)
    ram = simpy.Container(env, init=RAM_CAPACITY, capacity=RAM_CAPACITY)
    cpu = simpy.Resource(env, capacity=num_cpus)
    
    # Crear procesos y agregarlos al entorno
    for i in range(num_procesos):
        env.process(proceso(env, f"Proceso {i}", ram, cpu, CPU_INSTRUCCIONES, intervalo))
    
    # Ejecutar la simulación
    env.run()

# Función principal para la ejecución del programa
def main(RAM_CAPACITY, CPU_INSTRUCCIONES, num_cpus):
    fig, axs = plt.subplots(3, figsize=(10, 18))
    fig.suptitle('Tiempo Promedio en el Sistema vs. Número de Procesos')

    # Iterar sobre diferentes intervalos de tiempo
    for i, intervalo in enumerate(INTERVALOS):
        tiempos_promedio = []
        desviaciones_estandar = []
        
        # Iterar sobre diferentes cantidades de procesos
        for num_proceso in NUM_PROCESOS:
            # Ejecutar la simulación para la configuración dada
            ejecutar_simulacion(num_proceso, RAM_CAPACITY, CPU_INSTRUCCIONES, num_cpus, intervalo)
            
            # Calcular el promedio de tiempo y desviación estándar
            promedio_tiempo = sum(resultados) / num_proceso
            tiempos_promedio.append(promedio_tiempo)
            desviacion_estandar = (sum((x - promedio_tiempo) ** 2 for x in resultados) / num_proceso) ** 0.5
            desviaciones_estandar.append(desviacion_estandar)
            
            # Imprimir resultados individuales
            print(f"Para {num_proceso} procesos con intervalo {intervalo}:")
            print(f"Tiempo promedio en el sistema: {promedio_tiempo}")
            print(f"Desviación estándar: {desviacion_estandar}")
            print("-" * 30)  

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

# Función para mostrar menú y gestionar opciones
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

# Iniciar el menú
menu()