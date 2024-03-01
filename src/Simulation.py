import simpy as sp
import numpy as np

# Global variables
Times = {"ProcessNumber":[], "time":[]}
class Computer:
    def __init__(self, env, capacityProcesor, CapacityRam, InstructionsPerCycle) -> None:
        self.ram = sp.Container(env, capacity=CapacityRam, init=CapacityRam)
        self.cpu = sp.Resource(env, capacity=capacityProcesor)
        self.InstructionsPerCycle = InstructionsPerCycle

class Process:
    def __init__(self, env, pc) -> None:
        self.env = env
        self.pc = pc
        self.ram_needed = np.random.randint(1, 10)
        self.instruction_counter = np.random.randint(1, 10)

    def run(self):
        ram_req = self.pc.ram.get(self.ram_needed)
        yield ram_req

        def execute_instruction(req):
            for _ in range(3):
                if self.instruction_counter <= 0:
                    break
                else:          
                    yield req
                    yield self.env.timeout(1)
                    if self.instruction_counter > self.pc.InstructionsPerCycle:
                        self.instruction_counter -= self.pc.InstructionsPerCycle
                    else:
                        self.instruction_counter = 0

                self.pc.cpu.release(req)
                
        start_time = self.env.now
        with self.pc.cpu.request() as req:
            # Corre una intruccion por segundo, y un maximo de intrucciones de 3 en el procesador, despues de 3 se mira si se termian de hacer las intrucciones
            # o se interrumpe el proceso
            while (self.instruction_counter > 0):
                yield self.env.process(execute_instruction(req))

                Waiting_Number = np.random.randint(1, 2)

                if Waiting_Number == 1:
                    self.pc.cpu.release(req)
                    yield self.env.timeout(1)
                else:
                    yield self.env.process(execute_instruction(self.pc, req))

        self.pc.cpu.release(req)
        end_time = self.env.now
        self.pc.ram.put(self.ram_needed)
        Times["ProcessNumber"].append(len(Times["ProcessNumber"])+1) 
        Times["time"].append(end_time - start_time)

def CreateProcesses(env, pc, Number_of_processes):
    for _ in range(Number_of_processes):
        Process(env, pc)
        env.process(Process(env, pc).run())


def main(Number_of_processes, Ram_Capacity, CPU_Capacity, InstructionsPerCycle):
    Times["ProcessNumber"] = []
    Times["time"] = []
    env = sp.Environment()
    pc = Computer(env, CPU_Capacity, Ram_Capacity, InstructionsPerCycle)
    CreateProcesses(env, pc, Number_of_processes)
    env.run()
    return Times

