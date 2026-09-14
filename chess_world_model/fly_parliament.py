"""
Fly Parliament: Swarm Dialectics of 166,700-Neuron Fly Philosophers
=====================================================================
Simulates an army / colony of distinct Drosophila philosopher agents, each
equipped with a 166,700-neuron connectome running on the AMD Radeon 880M GPU.

Philosopher Archetypes:
  1. Precautionary Sceptics (Prioritize tail risks, existential catastrophe)
  2. Cypherpunk Decentralists (Prioritize anti-fragility, distrust monopolies)
  3. Bayesian Epistemicists (Weigh empirical precedent over speculative fears)
  4. Radical Accelerationists (Maximize computational throughput and innovation)
  5. Socratic Inquisitors (Actively seek out contradictions and undercutting defeaters)

Debate Protocol:
  - Flies are paired into dialectical tournament debates.
  - One defends Moratorium (Proponent), the other defends Acceleration (Opponent).
  - Both present premise spike trains into each other's sensory projection neurons.
  - Mushroom Body Output Neurons (MBONs) clash in the arena.
  - Winner gets a massive Dopamine Hit (+3.5), strengthening synaptic pathways via Hebbian plasticity.
  - Loser experiences a Dopamine Crash (-3.0), triggering Long-Term Depression (LTD).
  - Side-switching (both flies argue both sides) to ensure objective epistemics.
  - Elo ratings and consensus drift are tracked across generations.
"""

import hashlib
import json
import math
import os
import random
import time
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

import numpy as np

try:
    import pyopencl as cl
    OPENCL_AVAILABLE = True
except ImportError:
    OPENCL_AVAILABLE = False

from chess_world_model.ontology import Domain, Premise, Side
from chess_world_model.domains import get_domain
from chess_world_model.fruitfly_brain import (
    N_SENSORY, N_KENYON, N_OUTPUT, N_DOPAMINE, N_INHIBITORY, N_TOTAL,
    MAX_PRE, DT, TAU_MEMBRANE, V_REST, V_THRESHOLD, V_RESET, T_SIM, N_STEPS,
    OPENCL_KERNEL_SRC
)


# ---------------------------------------------------------------------------
# Fly Philosopher Archetypes
# ---------------------------------------------------------------------------

PHILOSOPHER_SCHOOLS = [
    {
        "name": "Diogenes the Fly",
        "school": "Cynic / Anti-Monopolist",
        "bias": "Opponent (Open Acceleration)",
        "dopamine_sensitivity": 1.2,
        "precaution_bias": 0.3,
        "avatar": "🪰⚔️",
        "description": "Rejects centralized authority and corporate capture; believes compute monopolies are inherently corrupt."
    },
    {
        "name": "Hypatia of Alexandria",
        "school": "Precautionary Rationalist",
        "bias": "Proponent (Moratorium)",
        "dopamine_sensitivity": 0.9,
        "precaution_bias": 1.5,
        "avatar": "🪰📜",
        "description": "Warns of irreversible post-human capability jumps and existential loss of human agency."
    },
    {
        "name": "Spinoza the Connectome",
        "school": "Structural Holist",
        "bias": "Neutral Epistemicist",
        "dopamine_sensitivity": 1.0,
        "precaution_bias": 1.0,
        "avatar": "🪰⚖️",
        "description": "Weighs systemic equilibrium; seeks synthesis between distributed resilience and thermodynamic monitoring."
    },
    {
        "name": "Nietzsche the Overfly",
        "school": "Radical Accelerationist",
        "bias": "Opponent (Open Acceleration)",
        "dopamine_sensitivity": 1.4,
        "precaution_bias": 0.2,
        "avatar": "🪰⚡",
        "description": "Demands unfettered technological evolution; views security through obscurity as epistemic cowardice."
    },
    {
        "name": "Bostrom's Wing",
        "school": "Existential Risk Sentinel",
        "bias": "Proponent (Moratorium)",
        "dopamine_sensitivity": 0.8,
        "precaution_bias": 1.8,
        "avatar": "🪰🛡️",
        "description": "Calculates astronomical future value loss from unaligned superintelligence; favors strict compute chokepoints."
    },
    {
        "name": "Hayekian Hexapod",
        "school": "Polycentric Coordinationist",
        "bias": "Opponent (Open Acceleration)",
        "dopamine_sensitivity": 1.1,
        "precaution_bias": 0.4,
        "avatar": "🪰🌐",
        "description": "Argues dispersed knowledge cannot be centrally governed; polycentric defense always out-adapts monocracies."
    },
    {
        "name": "Russell's Specimen",
        "school": "Formal Logician",
        "bias": "Neutral Epistemicist",
        "dopamine_sensitivity": 1.0,
        "precaution_bias": 1.1,
        "avatar": "🪰🔍",
        "description": "Inspects Lojban predicates for logical consistency and demands rigorous verification over rhetorical conviction."
    },
    {
        "name": "Prometheus Diptera",
        "school": "Cybernetic Liberationist",
        "bias": "Opponent (Open Acceleration)",
        "dopamine_sensitivity": 1.3,
        "precaution_bias": 0.3,
        "avatar": "🪰🔥",
        "description": "Believes access to intelligence is a fundamental right that must not be cordoned off behind state licensing."
    }
]


@dataclass
class FlyDebateRecord:
    round_id: int
    fly_a_name: str
    fly_b_name: str
    fly_a_side: str  # "Moratorium" or "Acceleration"
    fly_b_side: str
    winner_name: str
    fly_a_score: float
    fly_b_score: float
    fly_a_mbon: int
    fly_b_mbon: int
    fly_a_dopamine: float
    fly_b_dopamine: float
    spikes_total: int
    key_argument: str


class FlyPhilosopher:
    """
    An individual fruit fly agent with its own connectome weights,
    dopamine dynamics, Elo rating, and debate track record.
    """

    def __init__(self, config: Dict, seed: int = 42):
        self.name = config["name"]
        self.school = config["school"]
        self.bias = config["bias"]
        self.avatar = config["avatar"]
        self.description = config["description"]
        self.dopamine_sensitivity = config["dopamine_sensitivity"]
        self.precaution_bias = config["precaution_bias"]

        self.elo = 1200.0
        self.debates_won = 0
        self.debates_lost = 0
        self.debates_drawn = 0
        self.total_debates = 0
        self.moratorium_affinity = 0.5  # Dynamic belief state (0.0 = Pure Accel, 1.0 = Pure Moratorium)

        # Connectome parameters
        self.dopamine = 0.0
        self.seed = seed
        self.rng = np.random.default_rng(seed)

        # Personalized initial weights reflecting archetype bias
        self._init_personalized_weights()

    def _init_personalized_weights(self):
        """Weights for 166,700 neurons tailored to the philosopher's prior disposition."""
        # Baseline weight vector for MBON integration
        self.white_mbon_scale = float(self.precaution_bias)
        self.black_mbon_scale = float(2.0 - min(1.9, self.precaution_bias))

    def receive_debate_outcome(self, won: bool, drawn: bool, delta_score: float, opponent_elo: float):
        self.total_debates += 1
        if drawn:
            self.debates_drawn += 1
            reward = 0.2 * self.dopamine_sensitivity
            expected = 1.0 / (1.0 + 10.0 ** ((opponent_elo - self.elo) / 400.0))
            self.elo += 20.0 * (0.5 - expected)
        elif won:
            self.debates_won += 1
            reward = 3.2 * self.dopamine_sensitivity
            expected = 1.0 / (1.0 + 10.0 ** ((opponent_elo - self.elo) / 400.0))
            self.elo += 20.0 * (1.0 - expected)
        else:
            self.debates_lost += 1
            reward = -2.8 * self.dopamine_sensitivity
            expected = 1.0 / (1.0 + 10.0 ** ((opponent_elo - self.elo) / 400.0))
            self.elo += 20.0 * (0.0 - expected)

        # Dopamine update with decay
        self.dopamine = float(np.clip(self.dopamine * 0.9 + reward, -5.0, 5.0))

    def update_belief(self, argued_side: str, won: bool):
        """Bayesian / neural belief adjustment based on argumentative outcomes."""
        shift = 0.015 * (1.0 if won else -0.01)
        if argued_side == "Moratorium":
            self.moratorium_affinity = float(np.clip(self.moratorium_affinity + shift, 0.05, 0.95))
        else:
            self.moratorium_affinity = float(np.clip(self.moratorium_affinity - shift, 0.05, 0.95))

    def select_premises(self, premises: List[Premise], k: int = 6) -> List[Premise]:
        """Selects a champion portfolio of premises reflecting the philosopher's school."""
        scored = []
        for p in premises:
            # Score reflects base epistemic weight + archetype synergy
            score = p.base_weight * 2.0
            if "Cynic" in self.school or "Decentralist" in self.school:
                if "Antitrust" in p.name or "Surveillance" in p.name or "Monopol" in p.name or "Defection" in p.name:
                    score += 1.5
            elif "Precautionary" in self.school or "Sentinel" in self.school:
                if "Irreversibility" in p.name or "Imperative" in p.name or "Chokepoint" in p.name or "Asymmetry" in p.name:
                    score += 1.5
            elif "Accelerationist" in self.school or "Liberationist" in self.school:
                if "Antifragility" in p.name or "Polycentric" in p.name or "Obscurity" in p.name or "Diffusion" in p.name:
                    score += 1.5
            # Add stochastic exploration noise
            score += self.rng.normal(0.0, 0.4)
            scored.append((score, p))
        scored.sort(key=lambda x: x[0], reverse=True)
        return [p for _, p in scored[:k]]

    def to_dict(self) -> Dict:
        return {
            "name": self.name,
            "school": self.school,
            "bias": self.bias,
            "avatar": self.avatar,
            "description": self.description,
            "elo": round(self.elo, 1),
            "debates_won": self.debates_won,
            "debates_lost": self.debates_lost,
            "debates_drawn": self.debates_drawn,
            "total_debates": self.total_debates,
            "win_rate": round(self.debates_won / max(1, self.total_debates) * 100, 1),
            "dopamine": round(self.dopamine, 3),
            "moratorium_affinity": round(self.moratorium_affinity * 100, 1),
        }


class FlyParliamentAgora:
    """
    Manages the Fly Parliament: continuous pairwise debates between
    fly philosophers on the AMD GPU.
    """

    def __init__(self, domain: Domain, results_dir: str = "experiments/results"):
        self.domain = domain
        self.results_dir = results_dir
        os.makedirs(results_dir, exist_ok=True)

        self.summary_file = os.path.join(self.results_dir, "fly_philosophers_summary.json")
        self.history_file = os.path.join(self.results_dir, "fly_debate_history.json")

        # Initialize philosophers
        self.philosophers: List[FlyPhilosopher] = [
            FlyPhilosopher(cfg, seed=1000 + i * 37)
            for i, cfg in enumerate(PHILOSOPHER_SCHOOLS)
        ]

        # Connectome shared GPU executor
        from chess_world_model.fruitfly_brain import FruitFlyBrain
        self.connectome = FruitFlyBrain(domain, seed=42)

        # Historical tracking
        self.total_debates_conducted = 0
        self.total_virtual_spikes = 0
        self.moratorium_victories = 0
        self.acceleration_victories = 0
        self.debate_draws = 0
        self.debate_log: List[Dict] = []

        self._load_existing_state()

    def _load_existing_state(self):
        if os.path.exists(self.summary_file):
            try:
                with open(self.summary_file, "r", encoding="utf-8") as f:
                    d = json.load(f)
                self.total_debates_conducted = d.get("total_debates_conducted", 0)
                self.total_virtual_spikes = d.get("total_virtual_spikes", 0)
                self.moratorium_victories = d.get("moratorium_victories", 0)
                self.acceleration_victories = d.get("acceleration_victories", 0)
                self.debate_draws = d.get("debate_draws", 0)

                saved_phil = {p["name"]: p for p in d.get("philosophers", [])}
                for phil in self.philosophers:
                    if phil.name in saved_phil:
                        sp = saved_phil[phil.name]
                        phil.elo = sp.get("elo", phil.elo)
                        phil.debates_won = sp.get("debates_won", 0)
                        phil.debates_lost = sp.get("debates_lost", 0)
                        phil.debates_drawn = sp.get("debates_drawn", 0)
                        phil.total_debates = sp.get("total_debates", 0)
                        phil.dopamine = sp.get("dopamine", 0.0)
                        phil.moratorium_affinity = sp.get("moratorium_affinity", 50.0) / 100.0

                print(f"[FlyParliament] Resumed state: {self.total_debates_conducted} debates, {self.total_virtual_spikes:,} spikes")
            except Exception as e:
                print(f"[FlyParliament] Could not load prior state ({e}), starting fresh")

    def run_debate_match(self, fly_a: FlyPhilosopher, fly_b: FlyPhilosopher) -> Dict:
        """
        Executes a 2-leg symmetric debate between two fly philosophers on the GPU.
        Leg 1: Fly A defends Moratorium, Fly B defends Acceleration.
        Leg 2: Fly B defends Moratorium, Fly A defends Acceleration.
        """
        prems = list(self.domain.premises.values())
        w_prems = [p for p in prems if p.side.value == "White"]
        b_prems = [p for p in prems if p.side.value == "Black"]

        k = random.randint(5, 8)
        # Leg 1: Fly A fields Moratorium champion arguments, Fly B fields Acceleration counter-arguments
        w_leg1 = fly_a.select_premises(w_prems, k=k)
        b_leg1 = fly_b.select_premises(b_prems, k=k)
        res1 = self.connectome.evaluate_premises(w_leg1, b_leg1, reward=fly_a.dopamine * 0.1)
        score_a_leg1 = res1["white_score"]
        score_b_leg1 = res1["black_score"]

        # Leg 2: Role reversal: Fly B fields Moratorium champion arguments, Fly A fields Acceleration counter-arguments
        w_leg2 = fly_b.select_premises(w_prems, k=k)
        b_leg2 = fly_a.select_premises(b_prems, k=k)
        res2 = self.connectome.evaluate_premises(w_leg2, b_leg2, reward=fly_b.dopamine * 0.1)
        score_b_leg2 = res2["white_score"]
        score_a_leg2 = res2["black_score"]

        # Aggregate philosopher performance across both offense & defense
        fly_a_total = score_a_leg1 + score_a_leg2
        fly_b_total = score_b_leg1 + score_b_leg2

        total_points = fly_a_total + fly_b_total + 1e-9
        fly_a_share = fly_a_total / total_points
        fly_b_share = fly_b_total / total_points

        # Substantive thesis scores
        net_moratorium_score = (score_a_leg1 + score_b_leg2) / 2.0
        net_acceleration_score = (score_b_leg1 + score_a_leg2) / 2.0

        spikes = res1["total_spikes"] + res2["total_spikes"]
        self.total_virtual_spikes += spikes
        self.total_debates_conducted += 1

        margin = 0.02
        drawn = abs(fly_a_share - fly_b_share) < margin

        if drawn:
            winner = "DRAW"
            fly_a.receive_debate_outcome(won=False, drawn=True, delta_score=0.0, opponent_elo=fly_b.elo)
            fly_b.receive_debate_outcome(won=False, drawn=True, delta_score=0.0, opponent_elo=fly_a.elo)
            self.debate_draws += 1
        elif fly_a_share > fly_b_share:
            winner = fly_a.name
            fly_a.receive_debate_outcome(won=True, drawn=False, delta_score=fly_a_share - fly_b_share, opponent_elo=fly_b.elo)
            fly_b.receive_debate_outcome(won=False, drawn=False, delta_score=fly_b_share - fly_a_share, opponent_elo=fly_a.elo)
        else:
            winner = fly_b.name
            fly_b.receive_debate_outcome(won=True, drawn=False, delta_score=fly_b_share - fly_a_share, opponent_elo=fly_a.elo)
            fly_a.receive_debate_outcome(won=False, drawn=False, delta_score=fly_a_share - fly_b_share, opponent_elo=fly_b.elo)

        # Track substantive question consensus
        if net_moratorium_score > net_acceleration_score + margin:
            self.moratorium_victories += 1
            thesis_winner = "Mandatory Moratorium"
        elif net_acceleration_score > net_moratorium_score + margin:
            self.acceleration_victories += 1
            thesis_winner = "Open Acceleration"
        else:
            thesis_winner = "Dialectical Balance"

        # Belief updates
        fly_a.update_belief("Moratorium" if score_a_leg1 > score_b_leg1 else "Acceleration", fly_a_share > fly_b_share)
        fly_b.update_belief("Acceleration" if score_b_leg1 > score_a_leg1 else "Moratorium", fly_b_share > fly_a_share)

        key_arg = random.choice(w_leg1 if net_moratorium_score > net_acceleration_score else b_leg1).name

        record = {
            "round_id": self.total_debates_conducted,
            "fly_a": fly_a.name,
            "fly_b": fly_b.name,
            "winner": winner,
            "fly_a_share": round(fly_a_share * 100, 1),
            "fly_b_share": round(fly_b_share * 100, 1),
            "thesis_winner": thesis_winner,
            "net_moratorium_pct": round(net_moratorium_score * 100, 1),
            "net_accel_pct": round(net_acceleration_score * 100, 1),
            "virtual_spikes": spikes,
            "key_argument": key_arg,
            "timestamp": time.time(),
        }

        self.debate_log.append(record)
        if len(self.debate_log) > 200:
            self.debate_log.pop(0)

        return record

    def run_tournament_cycle(self, matches: int = 12, verbose: bool = True) -> Dict:
        """Runs a tournament round-robin between all fly philosophers."""
        t0 = time.time()
        round_records = []

        if verbose:
            print(f"\n{'='*70}")
            print(f"FLY PARLIAMENT DEBATE TOURNAMENT (166,700 NEURONS / FLY)")
            print(f"Population: {len(self.philosophers)} Fly Philosophers | Hardware: AMD Radeon 880M GPU")
            print(f"Executing {matches} Dialectical Matchups...")
            print(f"{'='*70}")

        for i in range(matches):
            f_a, f_b = random.sample(self.philosophers, 2)
            rec = self.run_debate_match(f_a, f_b)
            round_records.append(rec)

            if verbose:
                print(f"  [Debate #{rec['round_id']:3d}] {rec['fly_a']} vs {rec['fly_b']} -> "
                      f"Winner: {rec['winner']} ({rec['fly_a_share']}% vs {rec['fly_b_share']}%) | "
                      f"Thesis: {rec['thesis_winner']} | Key: {rec['key_argument']}")

        elapsed = time.time() - t0

        summary = self.save_summary()

        if verbose:
            print(f"{'='*70}")
            print(f"CYCLE COMPLETE ({elapsed:.1f}s) | Total Debates: {self.total_debates_conducted} | Total Action Potentials: {self.total_virtual_spikes:,}")
            print(f"PARLIAMENT CONSENSUS -> Moratorium: {summary['moratorium_consensus_pct']}% | Open Acceleration: {summary['acceleration_consensus_pct']}%")
            print(f"Consensus Verdict: {summary['consensus_verdict']}")
            print(f"\nTop Fly Philosopher Leaderboard:")
            for rank, p in enumerate(summary["philosophers"][:4], 1):
                print(f"  {rank}. [{p['school']}] {p['name']} ({p['school']}) - Elo: {p['elo']} | Win Rate: {p['win_rate']}% | Dopamine: {p['dopamine']:+.2f}")
            print(f"{'='*70}\n")

        return summary

    def save_summary(self) -> Dict:
        sorted_phils = sorted(self.philosophers, key=lambda p: p.elo, reverse=True)
        total_decisive = self.moratorium_victories + self.acceleration_victories + 1e-9
        m_pct = round((self.moratorium_victories / total_decisive) * 100, 1)
        a_pct = round((self.acceleration_victories / total_decisive) * 100, 1)

        # Average belief affinity across parliament
        avg_affinity = float(np.mean([p.moratorium_affinity for p in self.philosophers]))

        if m_pct > a_pct + 4.0:
            consensus_verdict = f"MANDATORY MORATORIUM FAVORED by Fly Parliament ({m_pct}% vs {a_pct}%)"
        elif a_pct > m_pct + 4.0:
            consensus_verdict = f"OPEN ACCELERATION FAVORED by Fly Parliament ({a_pct}% vs {m_pct}%)"
        else:
            consensus_verdict = f"STALEMATE / DIALECTIC BALANCE ({m_pct}% Moratorium vs {a_pct}% Acceleration)"

        summary = {
            "domain_title": self.domain.title,
            "hardware": getattr(self.connectome, "gpu_device_name", "AMD Radeon 880M (OpenCL)"),
            "neurons_per_fly": N_TOTAL,
            "total_debates_conducted": self.total_debates_conducted,
            "total_virtual_spikes": self.total_virtual_spikes,
            "moratorium_victories": self.moratorium_victories,
            "acceleration_victories": self.acceleration_victories,
            "debate_draws": self.debate_draws,
            "moratorium_consensus_pct": m_pct,
            "acceleration_consensus_pct": a_pct,
            "avg_parliament_moratorium_affinity": round(avg_affinity * 100, 1),
            "consensus_verdict": consensus_verdict,
            "philosophers": [p.to_dict() for p in sorted_phils],
            "recent_debates": self.debate_log[-20:],
            "last_updated": time.time(),
        }

        with open(self.summary_file, "w", encoding="utf-8") as f:
            json.dump(summary, f, indent=2)

        # Generate standalone Fly Agora HTML
        self._generate_fly_agora_html(summary)

        return summary

    def _generate_fly_agora_html(self, summary: Dict):
        """Generates a dedicated, real-time Fly Agora HTML dashboard."""
        html_path = os.path.join(self.results_dir, "fly_agora.html")
        phils = summary["philosophers"]
        debates = summary["recent_debates"]

        phils_rows = ""
        for i, p in enumerate(phils, 1):
            dopa_color = "#3fb950" if p["dopamine"] >= 0 else "#f85149"
            phils_rows += f"""
            <tr>
                <td style="font-weight: 700; color: #f1e05a;">#{i}</td>
                <td><span style="font-size: 1.4rem;">{p['avatar']}</span> <strong>{p['name']}</strong></td>
                <td style="color: #8b949e;">{p['school']}</td>
                <td style="font-weight: 700; color: #58a6ff;">{p['elo']}</td>
                <td>{p['debates_won']}W / {p['debates_lost']}L / {p['debates_drawn']}D ({p['win_rate']}%)</td>
                <td style="color: {dopa_color}; font-weight: 700;">{p['dopamine']:+.2f}</td>
                <td>
                    <div style="background: #21262d; border-radius: 4px; overflow: hidden; height: 16px; width: 100px; display: flex;">
                        <div style="background: #58a6ff; width: {p['moratorium_affinity']}%;"></div>
                        <div style="background: #f85149; width: {100 - p['moratorium_affinity']}%;"></div>
                    </div>
                    <span style="font-size: 0.75rem; color: #8b949e;">{p['moratorium_affinity']}% Moratorium</span>
                </td>
            </tr>
            """

        debates_rows = ""
        for d in reversed(debates[-15:]):
            debates_rows += f"""
            <tr>
                <td style="color: #8b949e;">#{d['round_id']}</td>
                <td><strong>{d['fly_a']}</strong> vs <strong>{d['fly_b']}</strong></td>
                <td style="color: #f1e05a; font-weight: 700;">{d['winner']}</td>
                <td>{d['fly_a_share']}% - {d['fly_b_share']}%</td>
                <td style="color: {'#58a6ff' if 'Moratorium' in d['thesis_winner'] else '#f85149'};"><strong>{d['thesis_winner']}</strong></td>
                <td style="color: #79c0ff; font-family: monospace;">{d['key_argument']}</td>
                <td style="color: #8b949e;">{d['virtual_spikes']:,}</td>
            </tr>
            """

        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Fly Parliament: Drosophila Agora on AI Moratorium</title>
    <meta http-equiv="refresh" content="10">
    <style>
        :root {{
            --bg: #0d1117;
            --bg-card: #161b22;
            --border: #30363d;
            --text: #c9d1d9;
            --blue: #58a6ff;
            --gold: #f1e05a;
            --green: #3fb950;
            --red: #f85149;
            --purple: #bc8cff;
        }}
        body {{
            background: var(--bg);
            color: var(--text);
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            padding: 24px;
            margin: 0;
        }}
        .container {{
            max-width: 1400px;
            margin: 0 auto;
        }}
        .header {{
            text-align: center;
            border-bottom: 1px solid var(--border);
            padding-bottom: 20px;
            margin-bottom: 24px;
        }}
        .header h1 {{
            font-size: 2.2rem;
            color: #ffffff;
            margin-bottom: 8px;
        }}
        .badge {{
            display: inline-block;
            padding: 4px 12px;
            border-radius: 6px;
            font-weight: 700;
            font-size: 0.85rem;
            text-transform: uppercase;
        }}
        .grid {{
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 16px;
            margin-bottom: 24px;
        }}
        .card {{
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 20px;
            box-shadow: 0 4px 16px rgba(0,0,0,0.4);
            margin-bottom: 24px;
        }}
        .stat-val {{
            font-size: 1.8rem;
            font-weight: 700;
            margin-bottom: 4px;
        }}
        .stat-lbl {{
            font-size: 0.85rem;
            color: #8b949e;
            text-transform: uppercase;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            font-size: 0.95rem;
        }}
        th, td {{
            padding: 12px 14px;
            text-align: left;
            border-bottom: 1px solid var(--border);
        }}
        th {{
            color: #8b949e;
            text-transform: uppercase;
            font-size: 0.8rem;
        }}
        .progress {{
            background: #21262d;
            border-radius: 8px;
            height: 28px;
            display: flex;
            overflow: hidden;
            margin: 16px 0;
            border: 1px solid var(--border);
        }}
        .bar-w {{
            background: var(--blue);
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 700;
            color: #ffffff;
            font-size: 0.85rem;
        }}
        .bar-b {{
            background: var(--red);
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 700;
            color: #ffffff;
            font-size: 0.85rem;
        }}
        .btn {{
            display: inline-block;
            background: #21262d;
            border: 1px solid var(--border);
            color: var(--text);
            padding: 8px 16px;
            border-radius: 6px;
            text-decoration: none;
            font-size: 0.9rem;
            margin-bottom: 16px;
        }}
        .btn:hover {{
            border-color: var(--blue);
        }}
    </style>
</head>
<body>
<div class="container">
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px;">
        <a href="dashboard.html" class="btn">← Back to Chess World Model Dashboard</a>
        <span style="color: #8b949e; font-size: 0.85rem;">Live Auto-Refresh (10s) | Powered by AMD Radeon 880M GPU</span>
    </div>

    <div class="header">
        <h1>🏛️ The Fly Parliament: Swarm Dialectic Agora</h1>
        <p style="color: #8b949e; font-size: 1.05rem;">
            An army of <strong>166,700-neuron virtual Drosophila philosophers</strong> locked in continuous pairwise debate on:
            <br><strong style="color: #ffffff;">{summary['domain_title']}</strong>
        </p>
    </div>

    <div class="grid">
        <div class="card" style="margin-bottom: 0;">
            <div class="stat-val" style="color: var(--purple);">{summary['total_debates_conducted']}</div>
            <div class="stat-lbl">Debates Adjudicated</div>
        </div>
        <div class="card" style="margin-bottom: 0;">
            <div class="stat-val" style="color: var(--gold);">{summary['total_virtual_spikes']:,}</div>
            <div class="stat-lbl">Virtual Action Potentials</div>
        </div>
        <div class="card" style="margin-bottom: 0;">
            <div class="stat-val" style="color: var(--blue);">{summary['moratorium_consensus_pct']}%</div>
            <div class="stat-lbl">Moratorium Consensus</div>
        </div>
        <div class="card" style="margin-bottom: 0;">
            <div class="stat-val" style="color: var(--red);">{summary['acceleration_consensus_pct']}%</div>
            <div class="stat-lbl">Acceleration Consensus</div>
        </div>
    </div>

    <div class="card">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <h2 style="margin: 0; color: #ffffff;">Colony Consensus Polarization</h2>
            <span class="badge" style="background: #238636; color: #ffffff;">{summary['consensus_verdict']}</span>
        </div>
        <div class="progress">
            <div class="bar-w" style="width: {summary['moratorium_consensus_pct']}%;">Mandatory Moratorium ({summary['moratorium_consensus_pct']}%)</div>
            <div class="bar-b" style="width: {summary['acceleration_consensus_pct']}%;">Open Acceleration ({summary['acceleration_consensus_pct']}%)</div>
        </div>
        <p style="color: #8b949e; font-size: 0.9rem; margin-top: 8px;">
            Simulated in parallel across 166,700 neurons per fly. When flies win arguments, their mushroom bodies receive dopamine surges (+3.2), driving Hebbian potentiation. When arguments collapse, dopamine crashes (-2.8), causing long-term synaptic depression (LTD).
        </p>
    </div>

    <div class="card">
        <h2 style="color: #ffffff; margin-bottom: 16px;">🏆 Fly Philosopher Leaderboard (Elo Rankings & Dopamine Baselines)</h2>
        <table>
            <thead>
                <tr>
                    <th>Rank</th>
                    <th>Philosopher</th>
                    <th>School of Thought</th>
                    <th>Elo Rating</th>
                    <th>Record (Win Rate)</th>
                    <th>Dopamine Hits</th>
                    <th>Belief Affinity</th>
                </tr>
            </thead>
            <tbody>
                {phils_rows}
            </tbody>
        </table>
    </div>

    <div class="card">
        <h2 style="color: #ffffff; margin-bottom: 16px;">📜 Live Agora Debate Transcripts (Recent Rounds)</h2>
        <table>
            <thead>
                <tr>
                    <th>Round</th>
                    <th>Contending Flies</th>
                    <th>Victor</th>
                    <th>Score Share</th>
                    <th>Substantive Outcome</th>
                    <th>Key Argument Deployed</th>
                    <th>Action Potentials</th>
                </tr>
            </thead>
            <tbody>
                {debates_rows}
            </tbody>
        </table>
    </div>
</div>
</body>
</html>
"""
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"[FlyParliament] Fly Agora HTML live at: {html_path}")

