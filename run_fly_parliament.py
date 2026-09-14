"""
Run Fly Parliament: Swarm of 166,700-Neuron Drosophila Philosophers
Runs continuous pairwise debates on the AMD Radeon 880M GPU.
"""

import argparse
import time
import sys

from chess_world_model.domains import get_domain
from chess_world_model.fly_parliament import FlyParliamentAgora


def main():
    parser = argparse.ArgumentParser(description="Fly Parliament GPU Swarm Debate Runner")
    parser.add_argument("--domain", default="ai_moratorium", help="Domain ID (default: ai_moratorium)")
    parser.add_argument("--matches", type=int, default=12, help="Matches per tournament cycle")
    parser.add_argument("--cycles", type=int, default=10, help="Number of cycles (ignored if --continuous)")
    parser.add_argument("--continuous", action="store_true", help="Run indefinitely in the background")
    args = parser.parse_args()

    domain = get_domain(args.domain)
    agora = FlyParliamentAgora(domain)

    cycle_count = 0
    print(f"Starting Fly Parliament for '{domain.title}'")
    print(f"Mode: {'CONTINUOUS DAEMON' if args.continuous else f'{args.cycles} cycles'}\n")

    try:
        while True:
            cycle_count += 1
            print(f">>> Fly Parliament Cycle #{cycle_count} <<<", flush=True)
            agora.run_tournament_cycle(matches=args.matches, verbose=True)

            if not args.continuous and cycle_count >= args.cycles:
                break

            time.sleep(1.0)
    except KeyboardInterrupt:
        print("\nStopping Fly Parliament. State saved.")


if __name__ == "__main__":
    main()
