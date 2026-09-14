"""
Run Fruit Fly Connectome Evaluation on AI Moratorium Domain
Uses 166,700 neurons accelerated on AMD Radeon 880M GPU via OpenCL.
"""
import json, time, os

from chess_world_model.fruitfly_brain import FruitFlyBrain
from chess_world_model.domains import get_domain

domain = get_domain("ai_moratorium")
print("Initializing 166,700-neuron Fruit Fly Connectome for:", domain.title)

t0 = time.time()
brain = FruitFlyBrain(domain, seed=1337)
summary = brain.evaluate_full_domain(n_rounds=100, verbose=True)
elapsed = time.time() - t0

os.makedirs("experiments/results", exist_ok=True)
out_path = "experiments/results/fruitfly_ai_moratorium.json"

with open(out_path, "w", encoding="utf-8") as f:
    json.dump(summary, f, indent=2)

print(f"\nCompleted in {elapsed:.1f}s")
print(f"Results successfully saved to: {out_path}")
