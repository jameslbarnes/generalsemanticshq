# Voice Interaction with World Models: UX Patterns & Research Landscape

## Research Report for Etherea — May 2026

---

## Executive Summary

The intersection of voice interaction and world models is an emerging but rapidly converging field. No single established UX paradigm exists yet — which means Etherea has a real opportunity to define one. The research clusters into five pattern families, each with direct relevance to the agent SDK and Nouriel installation.

---

## 1. THE FIVE INTERACTION PATTERNS

### Pattern A: "Narrator as Co-Creator" (Storycaster Model)
**Source:** Storycaster (2025) — CAVE system for room-based AI storytelling (arxiv:2510.22857)

The system transforms a physical room into a responsive narrative environment. A narrator agent guides participants, who co-create stories via voice commands. Each scene generates ambient audio, dialogue, and imagery projected on walls.

**Key UX findings:**
- Narrator and audio were the most impactful elements (not the visuals alone)
- Preserving spatial awareness (no headsets) dramatically increased immersion
- Voice commands evolved stories rather than dictating them — the AI interpreted intent, not literal instructions
- Latency and image resolution were the main pain points

**Etherea relevance:** This is extremely close to what Etherea does. The insight is that the *agent persona* (narrator) matters as much as the visual output. The voice isn't just a control surface — it's a character in the experience.

### Pattern B: "Instruction-Driven World Control" (GameCraft / PAN Model)
**Source:** Hunyuan-GameCraft-2 (arxiv:2511.23429), PAN World Model (arxiv:2511.09057)

Instead of rigid action schemas (keyboard/mouse), users control generated worlds through natural language: "open the door," "trigger an explosion," "draw a torch." The system maps free-form language to causal actions within the generated world.

**Key UX patterns:**
- Natural language replaces discrete input (buttons/keys) for semantic-rich interactions
- The system maintains causal coherence — actions have consequences that persist
- Language acts at different granularities: high-level ("make it stormy") vs specific ("move the red object left")
- Hybrid input works: language for semantics, traditional controls for spatial precision

**Etherea relevance:** This maps directly to the SDK control surface question. Voice handles the semantic layer (mood, style, narrative), while the iPhone app handles spatial/parametric precision (shader params, camera, mixing levels).

### Pattern C: "Adaptive Environment" (Neuro-Adaptive Room)
**Source:** "Designing an adaptive room for captivating collective consciousness" (arxiv:2410.21571)

A room that reads occupants' physiological/behavioral cues (facial expressions, speech analysis) and adjusts visual projections, lighting, and sound to induce desired states (focus, collaboration, creativity).

**Key UX patterns:**
- The environment responds to the *state* of the people, not just their commands
- Speech analysis captures paralinguistic cues (tone, energy, pauses) not just words
- The feedback loop is bidirectional: environment affects people, people affect environment
- Goal is inducing collective states, not individual control

**Etherea relevance:** This is the "ambient" mode of Etherea — where the system listens to conversation tone, energy, and mood rather than explicit commands. The installation doesn't wait to be told what to do; it reads the room.

### Pattern D: "Metaphor-Fluid Voice" (VUI Design Research)
**Source:** "Toward Metaphor-Fluid Conversation Design for VUIs" (2025)

Commercial voice assistants use a single metaphor (helpful assistant). This research shows that different interaction contexts demand different metaphorical relationships:
- **Commands:** User wants an obedient tool (formal, hierarchical)
- **Information seeking:** User wants a knowledgeable peer
- **Social/creative:** User wants a collaborator or muse
- **Error recovery:** User wants patient, calm guidance

A "metaphor-fluid" VUI dynamically shifts persona based on context.

**Etherea relevance:** Critical for the Nouriel installation. When someone says "make it blue," the system should respond as a tool. When someone is having a conversation and the visuals are responding to mood, the system should feel like an ambient presence. These are fundamentally different interaction modes, and the voice UX should shift between them.

### Pattern E: "Multimodal Language-Guided 4D Worlds" (MorphoSim / WorldCanvas)
**Source:** MorphoSim (arxiv:2510.04390), WorldCanvas (arxiv:2512.16924)

These systems combine text instructions with trajectories and reference images to generate controllable 4D environments. Objects can be directed, recolored, removed. Scenes observed from arbitrary viewpoints.

**Key UX patterns:**
- Language provides semantic intent, other modalities provide spatial/visual grounding
- Edits are applied incrementally without full re-generation
- Object-level control coexists with scene-level mood/atmosphere control
- Multi-view consistency maintained across edits

**Etherea relevance:** Maps to the "what can be controlled" question. The SDK should distinguish between scene-level controls (mood, atmosphere, palette — natural for voice) and object-level controls (specific shader parameters, composition — natural for touch/app).

---

## 2. EMERGING UX PARADIGMS

### The Speech-as-UX-Signal Pattern
**Source:** "Beyond Words: Measuring UX through Speech Analysis" (2026)

People's voices carry rich signals beyond words — affect, effort, frustration, engagement. A system that analyzes paralinguistic cues can detect interaction breakdowns and adapt in real-time.

**For Etherea:** The system could detect when someone is frustrated ("this isn't working") vs. delighted vs. bored — not from the words but from vocal quality — and adjust its behavior. This turns voice from a command channel into a continuous feedback signal.

### The Dual-Architecture Pattern (X-Streamer)
**Source:** X-Streamer (arxiv:2509.21574) — unified audiovisual world modeling

A "Thinker-Actor" architecture: the Thinker perceives and reasons over streaming inputs, while the Actor translates hidden states into synchronized multimodal streams.

**For Etherea:** This maps to the existing architecture — LLM reasoning about speech/context (Thinker) driving the visual generation pipeline (Actor). The insight is that the reasoning layer and generation layer need different temporal rhythms. The Thinker can update continuously; the Actor should smooth those updates into coherent visual transitions.

### The Hybrid Input Pattern (Gesture + Voice for CAD)
**Source:** "Combining Gesture and Voice Control for Mid-Air Manipulation" (arxiv:2011.09138)

Voice commands compensate for deficiencies in gesture recognition. The two modalities are complementary: gestures for spatial manipulation, voice for semantic operations (naming, grouping, mode switching).

**For Etherea:** iPhone touch = gesture channel (precise parametric control). Voice = semantic channel (mood, narrative, style). Neither replaces the other. The SDK should make this split explicit.

---

## 3. DESIGN IMPLICATIONS FOR THE ETHEREA SDK

### Voice Interaction Tiers (from research synthesis)

**Tier 1 — Ambient Listening (no explicit command)**
- System reads room energy, conversation tone, speech patterns
- Visual environment drifts and responds organically
- No wake word, no explicit interaction required
- Pattern C (Adaptive Environment) + Speech-as-UX-Signal

**Tier 2 — Conversational Steering (soft direction)**
- "I'm thinking about the ocean" → system shifts palette, movement, mood
- Not a command — a suggestion, a collaboration
- Pattern A (Narrator as Co-Creator) + Pattern D (Metaphor-Fluid, social mode)

**Tier 3 — Direct Command (explicit control)**
- "Make it red" / "Switch to the geometric shader" / "Slow everything down"
- System responds immediately and deterministically
- Pattern B (Instruction-Driven) + Pattern D (Metaphor-Fluid, command mode)

**Tier 4 — Parametric Control (app/touch surface)**
- Fine-grained shader params, composition, streaming settings
- Not voice — this is the iPhone app domain
- Pattern E (Object-Level vs Scene-Level)

### SDK Surface Suggestion

The agent SDK could expose these as distinct modes or channels:
- `ambient.listen()` — continuous speech analysis, no response expected
- `steer(intent)` — soft directional input, system interprets
- `command(action, params)` — deterministic execution
- `params.set(key, value)` — direct parametric control (app-facing)

---

## 4. KEY REFERENCES

| Paper | Year | Why It Matters |
|-------|------|----------------|
| Storycaster (arxiv:2510.22857) | 2025 | Closest existing system to Etherea — room-based, voice-driven, generative |
| Hunyuan-GameCraft-2 (arxiv:2511.23429) | 2025 | NL-driven world control replacing rigid input schemas |
| PAN World Model (arxiv:2511.09057) | 2025 | General, interactable, long-horizon world simulation via language |
| MorphoSim (arxiv:2510.04390) | 2025 | Language-guided 4D world with object-level editing |
| WorldCanvas (arxiv:2512.16924) | 2025 | Multi-modal promptable world events (text + trajectory + reference) |
| X-Streamer (arxiv:2509.21574) | 2025 | Unified audiovisual world modeling with Thinker-Actor architecture |
| Metaphor-Fluid VUI Design (2025) | 2025 | Dynamic persona shifting based on interaction context |
| Beyond Words: Speech as UX (2026) | 2026 | Paralinguistic cues as continuous UX signal |
| Adaptive Room (arxiv:2410.21571) | 2024 | Environment responds to collective physiological state |
| Gesture + Voice CAD (arxiv:2011.09138) | 2020 | Hybrid modality — voice for semantics, gesture for spatial |

---

## 5. THE GAP ETHEREA FILLS

None of these systems combine:
1. Real-time generative visuals (StreamDiffusion/LongLive)
2. Continuous voice interaction (not turn-based)
3. Ambient + command hybrid modes
4. Physical installation context (projection, not headset)
5. iPhone companion as parametric control surface

Etherea is uniquely positioned at this intersection. The closest analog is Storycaster, but it's turn-based (generate scene, wait, voice input, generate next scene). Etherea's continuous generation + continuous voice listening is a fundamentally different interaction paradigm — closer to a living environment than a conversational agent.

The agent SDK, by defining these interaction tiers explicitly, would be the first formal API for this class of system.
