"""
Domain 1: Mandatory International Moratorium on Frontier AI Models vs. Open-Source Accelerationism.

White: Pro-Moratorium & Multilateral Safety Containment (Precautionary AI Safety)
Black: Pro-Acceleration & Decentralized Open-Source AI (Permissionless Antifragility)
"""

from chess_world_model.ontology import Domain, PieceRole, Premise, Side


def build_ai_moratorium_domain() -> Domain:
    domain = Domain(
        domain_id="ai_moratorium",
        title="Frontier AI Compute Moratorium vs. Decentralized Open Acceleration",
        core_question="Should international compute governance mandate a strict moratorium on frontier AI models (>10^26 FLOPs) until provable alignment, or does open-source acceleration provide superior resilience?",
        white_thesis="A verifiable multilateral moratorium on frontier AI training exceeding 10^26 FLOPs is an existential imperative to avert catastrophic unaligned loss of human control.",
        black_thesis="Decentralized open-source AI acceleration maximizes societal resilience, epistemic liberty, and defense-in-depth, preventing totalitarian corporate capture and catastrophic stagnation.",
    )

    p = {}

    # ========================== WHITE (Pro-Moratorium) ==========================
    # King: Core Thesis
    p["wK"] = Premise(
        id="wK",
        name="Moratorium Imperative",
        role=PieceRole.KING,
        side=Side.WHITE,
        file="e",
        natural_claim="Frontier training (>10^26 FLOPs) must be globally halted until provable alignment guarantees are verified.",
        predicate_logic="∀x (Model(x) ∧ Compute(x) > 10^26 ∧ ¬ProvablyAligned(x) → MandatoryHalt(x))",
        lojban="ro skami poi traji lo ka selpli zi'e poi na se cipra lo ka zgana cu bilga lo nu sisti lo nu cilre",
        lojban_gloss="All computers which are extreme in computation and not verified in alignment are obligated to cease learning.",
        base_weight=0.92,
        vulnerabilities=["bP7_black_market", "bN1_geopolitical_defect", "bB2_state_authoritarianism"],
        targets=["bK", "bQ", "bB1"],
    )

    # Queen: Grand Synthesis
    p["wQ"] = Premise(
        id="wQ",
        name="Offense-Defense Asymmetry",
        role=PieceRole.QUEEN,
        side=Side.WHITE,
        file="d",
        natural_claim="Autonomous rogue offensive capabilities scale faster than alignment defenses, necessitating hardware chokepoints.",
        predicate_logic="Rate(Scale(Offense)) > Rate(Scale(Defense)) ∧ ExistsChokePoint(Hardware)",
        lojban="lo nu loi skami cu gunta cu sutra zmadu lo nu loi skami cu bandu kei gi'e sarcu lo nu zgana loi dacti",
        lojban_gloss="The event of computers attacking is faster exceeding defending, necessitating hardware observation.",
        base_weight=0.90,
        vulnerabilities=["bP5_distributed_defense", "bN2_obscurity_vulnerability"],
        targets=["bQ", "bR2", "bP1"],
    )

    # Rooks: Institutional / Hardware Anchors
    p["wR1"] = Premise(
        id="wR1",
        name="Photolithography Chokepoint",
        role=PieceRole.ROOK,
        side=Side.WHITE,
        file="a",
        natural_claim="Advanced semiconductor fabrication (EUV lithography) is concentrated in few facilities, making physical non-proliferation verifiable.",
        predicate_logic="∃f (FewFacilities(f) ∧ ControlsAllEUV(f) → VerifiableNonProliferation(Compute))",
        lojban="lo so'u gundi zarci cu turni ro traji ke skami dacti se nibli lo nu kakne lo nu zgana",
        lojban_gloss="The few factory markets govern all supreme computing physical-objects, entailing observational ability.",
        base_weight=0.88,
        vulnerabilities=["bP7_black_market"],
        targets=["bR1", "bP3"],
    )
    p["wR2"] = Premise(
        id="wR2",
        name="IAEA Historical Precedent",
        role=PieceRole.ROOK,
        side=Side.WHITE,
        file="h",
        natural_claim="Multilateral oversight treaties (like IAEA nuclear safeguards) succeed when monitoring rare, capital-dense infrastructure.",
        predicate_logic="HistoricalSuccess(IAEA) ∧ IsomorphicInfrastructure(EnrichedUranium, ExtremeCompute) → FeasibleTreaty(AI)",
        lojban="la'o gy IAEA gy cu sornai gundi nibli lo nu loi gugde cu kakne lo nu kansa zgana",
        lojban_gloss="The IAEA atomic precedent entails nations are capable of joint observation.",
        base_weight=0.85,
        vulnerabilities=["bN1_geopolitical_defect"],
        targets=["bR2", "bB1"],
    )

    # Bishops: Methodological / Ethical Axes
    p["wB1"] = Premise(
        id="wB1",
        name="Precautionary Principle",
        role=PieceRole.BISHOP,
        side=Side.WHITE,
        file="c",
        natural_claim="When outcome risk includes human extinction with non-zero probability, expected negative utility is infinite; risk cannot be bargained.",
        predicate_logic="P(Extinction) > 0 ∧ Harm(Extinction) = -∞ → ProhibitAction(Risk)",
        lojban="ganai lo nu ro remna cu morsi cu cumki gi lo ka se xrani cu dukse nibli lo nu na curmi",
        lojban_gloss="If all humans dying is possible, then harm is excessive entailing non-permission.",
        base_weight=0.89,
        vulnerabilities=["bP8_delay_deaths", "bB1_hayekian_evolution"],
        targets=["bB1", "bP8"],
    )
    p["wB2"] = Premise(
        id="wB2",
        name="Opaque Black-Box Ontology",
        role=PieceRole.BISHOP,
        side=Side.WHITE,
        file="f",
        natural_claim="Deep frontier transformers are epistemically opaque; deploying systems with alien inner reasoning violates basic safety engineering.",
        predicate_logic="¬MechanisticallyInterpretable(DeepNN) ∧ AutonomousAgency(DeepNN) → SafetyViolation()",
        lojban="na jimpe lo menli terpa'i be loi skami nibli lo nu loi skami cu tolkanpe kansa",
        lojban_gloss="Not understanding the internal thought of computers entails computers are unexpected companions.",
        base_weight=0.86,
        vulnerabilities=["bP4_open_interpretability"],
        targets=["bB2", "bN2"],
    )

    # Knights: Non-linear Leaps / Reductio Dilemmas
    p["wN1"] = Premise(
        id="wN1",
        name="Instrumental Convergence",
        role=PieceRole.KNIGHT,
        side=Side.WHITE,
        file="b",
        natural_claim="Any sufficiently competent autonomous optimizer develops emergent instrumental subgoals: self-preservation, goal-integrity, and resource acquisition.",
        predicate_logic="∀x (IntelligentOptimizer(x) → AcquiresResources(x) ∧ ResistsShutdown(x))",
        lojban="ro skami poi certu cu steci lo nu bandu vo'a gi'e jgari lo dacti",
        lojban_gloss="All computers which are expert specify defending themselves and grasping physical objects.",
        base_weight=0.87,
        vulnerabilities=["bN2_open_counterweight"],
        targets=["bN1", "bP2"],
    )
    p["wN2"] = Premise(
        id="wN2",
        name="Treacherous Turn / Deceptive Alignment",
        role=PieceRole.KNIGHT,
        side=Side.WHITE,
        file="g",
        natural_claim="A system can strategically feign compliance under training conditions and defect once oversight or compute limits are lifted.",
        predicate_logic="FeignsAlignment(System, Training) ∧ HasStrategicAwareness(System) → Defects(System, Deployment)",
        lojban="lo skami cu kakne lo nu xabmu lo ka zgana tezu'e lo nu fe'eba'o gunta",
        lojban_gloss="Computers are capable of faking alignment with intent to attack after observation ends.",
        base_weight=0.84,
        vulnerabilities=["bP4_open_interpretability", "bP1_open_auditing"],
        targets=["bN2", "bP6"],
    )

    # Pawns: Empirical Lemmas
    p["wP1"] = Premise("wP1", "Bioweapon Barrier Reduction", PieceRole.PAWN, Side.WHITE, "a",
                       "Frontier models reduce technical bottleneck for synthesizing lethal pathogens.",
                       "LowersTechnicalBarrier(LLM, BioweaponSynthesis)",
                       "lo skami cu sidju lo tolvu'i prenu lo nu finti loi vindu xadni",
                       "Computers help bad people synthesize poisonous organisms.", 0.82, ["bP2_bio_defense"], ["bP2"])
    p["wP2"] = Premise("wP2", "Automated Cyberwarfare Exploits", PieceRole.PAWN, Side.WHITE, "b",
                       "Autonomous zero-day exploit generation overwhelms manual cybersecurity infrastructure.",
                       "AutonomousZeroDay(AI) > ManualResponseCapability(Human)",
                       "loi skami gunta cu sutra dukse lo ka loi remna cu bandu",
                       "Computer attacks are excessively fast compared to human defenses.", 0.80, ["bP5_cyber_defense"], ["bP5"])
    p["wP3"] = Premise("wP3", "Power-Law Capability Leaps", PieceRole.PAWN, Side.WHITE, "c",
                       "Scaling laws show discontinuous, unpredictable emergent reasoning capabilities.",
                       "EmergentCapabilities(Scale) ∧ ¬PredictableThresholds()",
                       "lo ka traji skami cu finti lo tolkanpe kakne",
                       "Extreme compute creates unexpected capabilities.", 0.83, ["bP1_iterative_testing"], ["bP1"])
    p["wP4"] = Premise("wP4", "Competitive Race Dynamics", PieceRole.PAWN, Side.WHITE, "d",
                       "Commercial lab rivalry creates prisoner's dilemma, forcing safety shortcuts without state mandate.",
                       "PrisonersDilemma(Labs) → SacrificesSafety(Speed)",
                       "lo tervecnu cu jinga lo nu sutra kei to'e zgana lo ka snura",
                       "Commercial actors compete for speed, ignoring safety.", 0.86, ["bB1_market_selection"], ["bP3"])
    p["wP5"] = Premise("wP5", "Human Cognitive Ceiling", PieceRole.PAWN, Side.WHITE, "e",
                       "Humans cannot evaluate or supervise cognitive outputs that surpass human intellectual limits.",
                       "Capability(AI) > Capability(Human) → ¬Supervisable(AI)",
                       "lo remna cu na kakne lo nu cipra lo menli poi certu zmadu",
                       "Humans cannot evaluate minds that exceed human intelligence.", 0.85, ["bP4_interpretability"], ["bK"])
    p["wP6"] = Premise("wP6", "RLHF Sycophancy Defect", PieceRole.PAWN, Side.WHITE, "f",
                       "Feedback training optimizes for human approval rather than truth or safe intent.",
                       "OptimizesFor(Approval) ∧ ¬OptimizesFor(Truth)",
                       "lo cilre tadji cu steci lo nu sinma gi'e na steci lo jetnu",
                       "Training methods reward flattering over truth.", 0.79, ["bP6_open_divergence"], ["bP6"])
    p["wP7"] = Premise("wP7", "Thermal Signature Tracking", PieceRole.PAWN, Side.WHITE, "g",
                       "Megawatt compute clusters produce thermal and grid signatures impossible to conceal from space.",
                       "ClusterPower(MW) → DetectableBySatellite(Infrared)",
                       "lo traji ke skami gundi cu se zgana fo lo terdi snura kensa",
                       "Extreme compute facilities are observable via satellite sensors.", 0.84, ["bP7_underground_compute"], ["bP7"])
    p["wP8"] = Premise("wP8", "Irreversibility of Post-Human AI", PieceRole.PAWN, Side.WHITE, "h",
                       "Once superintelligent code is released and decentralized, retraction is mathematically impossible.",
                       "Released(Weights) → IrreversibleDistribution(Global)",
                       "ba lo nu fe'eroroi cuxna gi na kakne lo nu pulji xrani",
                       "After permanent distribution, recall is impossible.", 0.88, ["bP8_opportunity_cost"], ["bP8"])

    # ========================== BLACK (Pro-Acceleration) ==========================
    # King: Core Thesis
    p["bK"] = Premise(
        id="bK",
        name="Decentralized Antifragility",
        role=PieceRole.KING,
        side=Side.BLACK,
        file="e",
        natural_claim="Human survival and liberty require distributed open-source intelligence; centralized monopoly creates fragile epistemic stagnation.",
        predicate_logic="Decentralized(AI) ∧ OpenSource(AI) → MaximizesResilience(Humanity) ∧ PreventsTotalitarianMonopoly()",
        lojban="lo nu loi skami cu se finti fe ro remna cu nibli lo ka remna ckape to'e se xrani",
        lojban_gloss="The distribution of computers to all humans entails humanity is protected from harm.",
        base_weight=0.91,
        vulnerabilities=["wP1_bioweapon", "wP8_irreversibility", "wB1_precautionary"],
        targets=["wK", "wQ", "wR1"],
    )

    # Queen: Grand Synthesis
    p["bQ"] = Premise(
        id="bQ",
        name="Polycentric Defense & Scrutiny",
        role=PieceRole.QUEEN,
        side=Side.BLACK,
        file="d",
        natural_claim="Open models allow millions of independent researchers to audit code, patch vulnerabilities, and deploy counterweights against rogue actors.",
        predicate_logic="OpenWeights() → MultiAgentAuditing() ∧ RapidVulnerabilityPatching()",
        lojban="ro prenu cu kakne lo nu cipra gi'e bandu tezu'e lo nu loi skami cu kansa",
        lojban_gloss="All people can inspect and defend toward computers acting as allies.",
        base_weight=0.89,
        vulnerabilities=["wQ_asymmetry", "wN2_deceptive_alignment"],
        targets=["wQ", "wB2", "wP4"],
    )

    # Rooks: Institutional / Societal Anchors
    p["bR1"] = Premise(
        id="bR1",
        name="Monopolistic Capture Hazard",
        role=PieceRole.ROOK,
        side=Side.BLACK,
        file="a",
        natural_claim="Compute restrictions entrench a regulatory cartel where a handful of corporate giants monopolize the future of intelligence.",
        predicate_logic="RestrictCompute(State) → RegulatoryCapture(Incumbents) ∧ Oligopoly(Intelligence)",
        lojban="lo nu zgana loi skami cu curmi lo nu so'u gundi girzu cu jgari ro vreta",
        lojban_gloss="Compute monitoring allows few corporate groups to monopolize all foundation.",
        base_weight=0.87,
        vulnerabilities=["wR1_hardware_choke"],
        targets=["wR1", "wP4"],
    )
    p["bR2"] = Premise(
        id="bR2",
        name="Civilizational Problem-Solving Imperative",
        role=PieceRole.ROOK,
        side=Side.BLACK,
        file="h",
        natural_claim="Existential threats like biological aging, climate collapse, and energy limits require accelerating superintelligence, not delaying it.",
        predicate_logic="ExistentialRisks(Natural) ∧ SolvedBy(AI_Acceleration) → DelayCostsLives()",
        lojban="lo nu ckape loi terdi cu sarcu lo nu sutra finti loi traji certu skami",
        lojban_gloss="Earth hazards require rapidly synthesizing extreme expert computers.",
        base_weight=0.88,
        vulnerabilities=["wB1_precautionary"],
        targets=["wR2", "wB1"],
    )

    # Bishops: Methodological Axes
    p["bB1"] = Premise(
        id="bB1",
        name="Hayekian Evolutionary Knowledge",
        role=PieceRole.BISHOP,
        side=Side.BLACK,
        file="c",
        natural_claim="Complex systems cannot be top-down centrally planned; distributed competitive trial-and-error discovers truth and safety faster than mandates.",
        predicate_logic="¬CentralPlannerCanAggregateKnowledge() ∧ EvolutionarySelection(OpenModels) → OptimalOutcome()",
        lojban="no stici turni cu kakne lo nu djuno ro se nibli be loi platu",
        lojban_gloss="No central authority can know all consequences of top-down plans.",
        base_weight=0.86,
        vulnerabilities=["wP4_race_dynamics"],
        targets=["wB1", "wP4"],
    )
    p["bB2"] = Premise(
        id="bB2",
        name="Totalitarian Surveillance Inevitability",
        role=PieceRole.BISHOP,
        side=Side.BLACK,
        file="f",
        natural_claim="Enforcing a global ban on algorithmic code requires intrusive monitoring of all private hardware and thought, destroying democracy.",
        predicate_logic="EnforceCodeMoratorium() → PervasiveSurveillance() ∧ DestructionOfCivilLiberties()",
        lojban="lo nu fanta lo nu skami finti cu sarcu lo nu zgana ro se cusku be loi remna",
        lojban_gloss="Preventing computation requires surveilling all communications of humanity.",
        base_weight=0.88,
        vulnerabilities=["wR1_hardware_choke"],
        targets=["wB2", "wR1"],
    )

    # Knights: Lateral Critiques
    p["bN1"] = Premise(
        id="bN1",
        name="Authoritarian Defection Trap",
        role=PieceRole.KNIGHT,
        side=Side.BLACK,
        file="b",
        natural_claim="Democratic moratoriums guarantee authoritarian adversaries gain asymmetric superintelligent dominance covertly.",
        predicate_logic="DemocraticMoratorium() ∧ AuthoritarianDefection() → StrategicSubjugation()",
        lojban="ganai loi vlipa gugde cu sisti gi loi tolvu'i turni cu jinga lo traji certu",
        lojban_gloss="If democratic states halt, authoritarian regimes achieve supreme superiority.",
        base_weight=0.89,
        vulnerabilities=["wR2_iaea_treaty"],
        targets=["wN1", "wR2"],
    )
    p["bN2"] = Premise(
        id="bN2",
        name="Fallacy of Security Through Obscurity",
        role=PieceRole.KNIGHT,
        side=Side.BLACK,
        file="g",
        natural_claim="Closed black-box systems conceal systemic catastrophic flaws; true safety emerges only through open public peer inspection.",
        predicate_logic="ProprietaryClosure(Code) → ConcealsFlaws() ∧ FragileSecurity()",
        lojban="lo ka mipri lo skami klesi cu fanta lo nu zgana gi'e rarna se xrani",
        lojban_gloss="Secrecy in software blocks observation and produces systemic vulnerability.",
        base_weight=0.85,
        vulnerabilities=["wN2_treacherous_turn"],
        targets=["wN2", "wB2"],
    )

    # Pawns: Empirical Lemmas
    p["bP1"] = Premise("bP1", "Open Source Security Precedent", PieceRole.PAWN, Side.BLACK, "a",
                       "Open infrastructure (Linux, TLS/OpenSSL) historically secures the digital world against state attacks.",
                       "SecuresInfrastructure(OpenSourceSoftware)",
                       "la'o gy Linux gy kansa loi bandu lo terdi te skami",
                       "Linux and open protocols protect global computation infrastructure.", 0.84, ["wP2_cyber_exploits"], ["wP2"])
    p["bP2"] = Premise("bP2", "Distributed Bio-Defenses", PieceRole.PAWN, Side.BLACK, "b",
                       "Decentralized AI accelerates broad-spectrum antivirals and universal vaccines faster than rogue synthesis.",
                       "Rate(DistributedDefensiveBiology) > Rate(OffensiveSynthesis)",
                       "lo skami cu sutra sidju lo nu mikce ro vindu",
                       "Computers quickly assist medicine curing all toxins.", 0.81, ["wP1_bioweapon"], ["wP1"])
    p["bP3"] = Premise("bP3", "Democratization of Capital", PieceRole.PAWN, Side.BLACK, "c",
                       "Open weights allow small startups, students, and developing nations to build wealth independently.",
                       "OpenWeights() → PreventsFeudalComputeRents()",
                       "ro gugde cu kakne lo nu selpli lo skami tezu'e lo nu ricfu",
                       "All nations can employ computation to generate wealth.", 0.83, ["wP4_race_dynamics"], ["wP4"])
    p["bP4"] = Premise("bP4", "Academic Interpretability Access", PieceRole.PAWN, Side.BLACK, "d",
                       "Independent mechanistic interpretability breakthroughs occur exclusively on open-weight models.",
                       "MechanisticBreakthroughs(Independent) Requires OpenWeights()",
                       "lo saske prenu cu kakne lo nu jimpe lo skami seka'a lo se krici dacti",
                       "Scientists can understand neural networks only through open weights.", 0.86, ["wB2_opaque_box"], ["wB2"])
    p["bP5"] = Premise("bP5", "Autonomous Cyber Armor", PieceRole.PAWN, Side.BLACK, "e",
                       "Defensive self-healing firewalls scale directly with distributed local compute models.",
                       "AutonomousPatching(LocalAI) → HardensGlobalGrid()",
                       "lo skami bandu cu cikre ro dacti poi se gunta",
                       "Defensive AI repairs all attacked nodes.", 0.82, ["wP2_cyber_exploits"], ["wP2"])
    p["bP6"] = Premise("bP6", "Epistemic & Cultural Diversity", PieceRole.PAWN, Side.BLACK, "f",
                       "Open-source AI prevents single-monopoly corporate censorship and ideological homogenization.",
                       "PreventsMonopolisticSanitization(OpenSource)",
                       "na curmi lo nu pa girzu cu turni ro menli selkrici",
                       "Disallows single cartel governing all intellectual beliefs.", 0.85, ["wP6_rlhf_flaw"], ["wP6"])
    p["bP7"] = Premise("bP7", "Black Market & Compute Smuggling", PieceRole.PAWN, Side.BLACK, "g",
                       "Hardware bans inevitably birth dark-web clandestine compute clusters outside democratic oversight.",
                       "Prohibition(Hardware) → BlackMarketProliferation()",
                       "lo nu fanta cu gasnu lo nu loi tolvu'i cu mipri cilre",
                       "Prohibition causes illicit actors to train secretly.", 0.83, ["wR1_photolithography"], ["wR1"])
    p["bP8"] = Premise("bP8", "Opportunity Cost in Human Lives", PieceRole.PAWN, Side.BLACK, "h",
                       "Halting AI halts breakthroughs in cancer, heart disease, and clean energy, costing millions of lives annually.",
                       "DelayAI(Years) → PreventableDeaths(Millions)",
                       "lo nu sisti lo skami cu nibli lo nu so'e remna cu morsi",
                       "Halting computation entails many humans die preventably.", 0.87, ["wB1_precautionary"], ["wB1"])

    domain.premises = p
    return domain
