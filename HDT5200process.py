import simpy
import random
import statistics
import matplotlib.pyplot as plt

RANDSEED = 42
PROCESSNUMBER = 200
INTERVAL = 10
RAMCAP = 100
CPUSPED = 1
process_times = []

random.seed(RANDSEED)

class Process:
    def __init__(self, env, name, ram, cpu, process_times):
        self.env = env
        self.name = name
        self.ram = ram
        self.cpu = cpu
        self.instructions = random.randint(1, 10)
        self.action = env.process(self.run())
        self.process_times = process_times

    def run(self):
        start_time = self.env.now
        yield self.env.timeout(random.expovariate(1.0 / INTERVAL))
        yield self.ram.get(random.randint(1, 10))
        with self.cpu.request() as req:
            yield req
            while self.instructions > 0:
                yield self.env.timeout(1 / CPUSPED)
                self.instructions -= 3
                if self.instructions <= 0:
                    break
        yield self.ram.put(random.randint(1, 10))
        end_time = self.env.now
        self.process_times.append(end_time - start_time)


def setup(env, PROCESSNUMBER, ram, cpu, process_times):
    for num in range(PROCESSNUMBER):
        p = Process(env, f"Proceso {num+1}", ram, cpu, process_times)
        yield env.timeout(0.1)


env = simpy.Environment()
ram = simpy.Container(env, init=RAMCAP, capacity=RAMCAP)
cpu = simpy.Resource(env, capacity=1)

process_times = [0] * PROCESSNUMBER
env.process(setup(env, PROCESSNUMBER, ram, cpu, process_times))
env.run()

process_times = [t for t in process_times if t != 0]

average_time = statistics.mean(process_times)
std_deviation = statistics.stdev(process_times)

plt.plot(range(1, len(process_times)+1), process_times, marker='o')
plt.xlabel("Número de procesos")
plt.ylabel("Tiempo del proceso")
plt.title("Tiempo promedio para cada proceso")
plt.show()

print(f"El tiempo promedio que el proceso está en la computadora es: {average_time:.2f}")
print(f"La desviación estándar es: {std_deviation:.2f}")
