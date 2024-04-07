from pathlib import Path
from robo_sim.sim import Sim

sim = Sim(Path("examples", "test.yaml"), algorithm="Dijkstra")
sim.run()