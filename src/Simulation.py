import simpy as sp
import numpy as np

# Global variables
Ram_capacity = 100

# TODO: Cambiar los comentarios a unos mas utiles, descriptivos y no generados automaticamente
class Computer:
    def __init__(self, env) -> None:
        self.ram = sp.Container(env, capacity=100, init=100)
        self.cpu = sp.Resource(env, capacity=1)
    
def Process(env, ram, cpu):
    # If ram is not enough, wait until it is enough
    if ram.level == 0:
        pass  # Placeholder for the indented block
    else:
        # Use the ram
        ram_used = np.random.randint(1, 10)
        print(f"Ram Usada: {ram_used}")
        intruction_counter = np.random.randint(1, 10)
        print(f"Cantidad de instrucciones: {intruction_counter}")
        ram.get(ram_used)
        with cpu.request() as req:
            for _ in range(intruction_counter): # 
                yield req
                if intruction_counter < 3:
                    yield env.timeout(intruction_counter)
                    break
                else:
                    yield env.timeout(3)
                    intruction_counter -= 3
                
            #Release the cpu
            cpu.release(req)

        # Release the ram
        ram.put(ram_used)
        # After releasing the CPU
        random_number = np.random.randint(1, 21)
        if random_number == 1:
            # Go to Waiting state
            yield env.timeout(0)  # Placeholder for the indented block
        elif random_number == 2:
            # Go to Ready state
            yield env.timeout(0)  # Placeholder for the indented block
        else:
            # Go to Terminated state
            return
        
def main():
    env = sp.Environment()
    computer = Computer(env)
    env.process(Process(env, computer.ram, computer.cpu))
    env.run(until=100)

if __name__ == "__main__":
    main()