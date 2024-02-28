import simpy as sp
import numpy as np

# Global variables
Ram_capacity = 100


class Computer:
    def __init__(self, env) -> None:
        self.ram = sp.Container(env, capacity=100, init=100)
        self.cpu = sp.Resource(env, capacity=1)


class Process:
    def __init__(self, env, ram, cpu) -> None:
        self.env = env
        self.ram = ram
        self.ram_needed = np.random.randint(1, 10)
        self.cpu = cpu
        self.intruction_counter = np.random.randint(1, 10)

    def run(self):
        ram_req = self.ram.get(self.ram_needed)
        yield ram_req
        print(f"Ram needed: {self.ram_needed}")


        def execute_instruction(cpu ,req):
            for _ in range(3):

                yield req
                yield self.env.timeout(1)
                self.intruction_counter -= 1
                print(f"Instruction counter: {self.intruction_counter}")

                if self.intruction_counter == 0:
                    print("Process finished")
                    break
            print(f"Intructions left: {self.intruction_counter}")
            cpu.release(req)

        with self.cpu.request() as req:
            # Corre una intruccion por segundo, y un maximo de intrucciones de 3 en el procesador, despues de 3 se mira si se termian de hacer las intrucciones
            # o se interrumpe el proceso
            while (self.intruction_counter > 0):
                yield self.env.process(execute_instruction(self.cpu, req))

                Waiting_Number = np.random.randint(1, 2)

                print(f"Waiting number: {Waiting_Number}")
                if Waiting_Number == 1:
                    # Interrupt the process and put it back in the queue
                    print("Process interrupted")
                    self.cpu.release(req)
                    yield self.env.timeout(1)
                else:
                    yield self.env.process(execute_instruction(self.cpu, req))
                    
                

def main():
    env = sp.Environment()
    computer = Computer(env)
    process = Process(env, computer.ram, computer.cpu)
    env.process(process.run())
    env.run(until=100)


main()