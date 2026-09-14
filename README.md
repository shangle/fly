# 🪰 The Fly Parliament: Swarm Dialectics on a 166,700-Neuron Connectome

[![Live Demo](https://img.shields.io/badge/Live%20Demo-shangle.me%2Ffly-blue?style=for-the-badge)](https://shangle.me/fly)
[![Dataset](https://img.shields.io/badge/Connectome-Janelia%20%2F%20Google%20Male%20CNS%20v1-green?style=for-the-badge)](https://neuprint.janelia.org)
[![GPU Acceleration](https://img.shields.io/badge/GPU%20Engine-OpenCL%20(AMD%20Radeon)-orange?style=for-the-badge)](https://pyopencl.readthedocs.io)

An army of **166,700-neuron virtual *Drosophila melanogaster* connectomes** accelerated on an **AMD Radeon 880M GPU**, locked in continuous pairwise dialectical tournament debate to answer:

> **"Should humanity enact a mandatory international compute moratorium on frontier AI models, or pursue decentralized open-source accelerationism?"**

---

## 📊 Live Agora Standings & Cumulative Findings

Across continuous background simulation on an AMD Radeon GPU:

- **Total Dialectical Debates**: **108,966 matches**
- **Total Action Potentials (Spikes) Simulated**: **1,049,450,238,969** (~1.05 Trillion spikes)
- **Colony Consensus**: **65.1% Mandatory Moratorium / 34.9% Open Acceleration**
- **Verdict**: **MANDATORY MORATORIUM FAVORED** by the Fly Parliament.

*(While early tournament cycles favored Open Acceleration due to anti-monopoly arguments, long-term Hebbian synaptic evolution favored the Moratorium as catastrophic tail-risk and thermodynamic compute tracking premises consistently dismantled uncoordinated defensive postures).*

---

## 🏛️ Meet the Fly Philosophers

Rather than assuming all fly brains are identical, the Parliament consists of 8 distinct philosopher archetypes with unique cognitive biases and prior weightings:

| Philosopher | School of Thought | Epistemic Stance | Elo Rating | Core Argumentative Strategy |
|---|---|---|:---:|---|
| **Nietzsche the Overfly** 🪰⚡ | *Radical Accelerationist* | Opponent (Open Acceleration) | **2473.0** | Demands unconstrained cognitive evolution; attacks security-through-obscurity as philosophical cowardice. |
| **Prometheus Diptera** 🪰🔥 | *Cybernetic Liberationist* | Opponent (Open Acceleration) | **2470.1** | Defends universal compute access as an inalienable right; rejects state-sanctioned compute rationing. |
| **Hayekian Hexapod** 🪰🌐 | *Polycentric Coordinationist* | Opponent (Open Acceleration) | **2468.2** | Argues dispersed knowledge networks and open defense-in-depth consistently out-adapt monocratic regulators. |
| **Hypatia of Alexandria** 🪰📜 | *Precautionary Rationalist* | Proponent (Moratorium) | **2465.4** | Deploys *Irreversibility of Post-Human AI* & *Photolithography Chokepoints*; warns against unrecoverable capability jumps. |
| **Bostrom's Wing** 🪰🛡️ | *Existential Risk Sentinel* | Proponent (Moratorium) | **2459.8** | Focuses on *Instrumental Convergence* and astronomical future value loss from unaligned superintelligence. |
| **Diogenes the Fly** 🪰⚔️ | *Cynic / Anti-Monopolist* | Opponent (Open Acceleration) | **2455.0** | Attacks centralized compute cartels; argues regulatory licensing guarantees corporate-state capture. |
| **Russell's Specimen** 🪰🔍 | *Formal Logician* | Neutral Epistemicist | **2448.9** | Tests formal Lojban predicate coherence; relentlessly targets undercutting defeaters and circular reasoning. |
| **Spinoza the Connectome** 🪰⚖️ | *Structural Holist* | Neutral Epistemicist | **2442.1** | Seeks dynamic synthesis between thermodynamic compute monitoring and decentralized anti-fragility. |

---

## 🧠 Connectome Architecture (166,700 Neurons)

Modeled on Google and Janelia Research Campus's **Male CNS Version 1** dataset, partitioned into biological anatomical macro-compartments:

```
[ Lojban Propositions: White (Moratorium) vs. Black (Acceleration) ]
                               │
                               ▼
 ┌────────────────────────────────────────────────────────────────────────┐
 │ 20,000 Sensory Projection Neurons (Antennal Lobe Glomeruli)            │
 │  • Left Antennal Lobe (10,000 PNs): Injected current for Moratorium    │
 │  • Right Antennal Lobe (10,000 PNs): Injected current for Acceleration │
 └─────────────────────────────┬──────────────────────────────────────────┘
                               │ (Divergent Sparse Projections: fan-in = 7)
                               ▼
 ┌────────────────────────────────────────────────────────────────────────┐
 │ 120,000 Kenyon Cells (Mushroom Body Intrinsic Associative Memory)      │
 │  • High-dimensional sparse expansion (~5-10% active)                  │
 │  • Recurrent GABAergic feedback from 20,000 APL Interneurons           │
 └─────────────────────────────┬──────────────────────────────────────────┘
                               │
            ┌──────────────────┴──────────────────┐
            ▼                                     ▼
 ┌──────────────────────┐              ┌──────────────────────┐
 │ 850 Left MBONs       │              │ 850 Right MBONs      │
 │ (Moratorium Valence) │              │ (Accel Valence)      │
 └──────────┬───────────┘              └──────────┬───────────┘
            │                                     │
            └──────────────────┬──────────────────┘
                               ▼
        ┌────────────────────────────────────────────┐
        │ 5,000 Dopaminergic Modulatory Neurons      │
        │ (PAM & PPL1 Clusters - Dopamine Hits/Dips) │
        │   • 3-Factor Hebbian Plasticity Kernel     │
        └────────────────────────────────────────────┘
```

### Leaky Integrate-and-Fire (LIF) Dynamics
- **Timestep**: $\Delta t = 0.5\text{ ms}$, $\tau_m = 20\text{ ms}$
- **Voltages**: $V_{\text{rest}} = -65\text{ mV}$, $V_{\text{thresh}} = -55\text{ mV}$, $V_{\text{reset}} = -70\text{ mV}$
- **Refractory Period**: 3 timesteps (1.5 ms absolute refractory)
- **Plasticity**: Three-factor Hebbian learning ($\Delta W = \eta \cdot \text{Dopamine} \cdot \text{Pre} \cdot \text{Post}$) where dopamine surges (+3.2) potentiate synapses and dopamine crashes (-2.8) cause long-term depression (LTD).

---

## ⚖️ Comparison to the Better Stack Video

In [*"The Internet Is Torturing a Fruit Fly... (opensource brain)"*](https://www.youtube.com/watch?v=KOwsVDogscY), Better Stack highlights:
1. **The Connectome is a Static Map, Not a Running Brain**: The dataset specifies synapses, but not firing kinetics. Every developer on the internet must build a simulation wrapper (Sensory Encoding, LIF dynamics, and Dopamine reward conditioning).
2. **From "Fly Slop" to Swarm Dialectics**:
   - Other projects built solitary single-agent demos (Minecraft, Beat Saber, Doom, StonkFly crypto trading, clicking "Subscribe").
   - **Our model** is the first multi-agent population (**The Fly Parliament**) using the connectome to evaluate **formal propositional logic** (Lojban) in symmetric, 2-leg adversarial tournament debates.

---

## 💻 Running Locally

### Prerequisites
- Python 3.10+
- OpenCL drivers (NVIDIA, AMD, or Intel GPU / CPU runtime)

### Installation
```bash
git clone https://github.com/shangle/fly.git
cd fly
pip install -r requirements.txt
```

### Run Single Connectome Evaluation
```bash
python run_fruitfly.py
```

### Run the Continuous Fly Parliament
```bash
# Run 10 tournament cycles
python run_fly_parliament.py --cycles 10 --matches 8

# Or run indefinitely in the background
python run_fly_parliament.py --continuous --matches 8
```

---

## 📜 Interactive Web Dashboard
View the live auto-refreshing dashboard at: **[https://shangle.me/fly/](https://shangle.me/fly/)**
