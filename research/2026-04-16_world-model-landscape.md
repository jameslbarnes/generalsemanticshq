# World Model Landscape — April 12-16, 2026

**Date:** April 16, 2026
**Researcher:** Hermes (requested by James Barnes)
**Context:** Three major world model releases this week that are directly relevant to Etherea's real-time, promptable video generation pipeline. All build on the autoregressive diffusion + streaming paradigm (like LongLive) but with significant improvements in memory consistency, real-time speed, and infinite rollout.

---

## 1. Matrix-Game 3.0 (Skywork AI) — Best Overall Match

**Released:** March 27, 2026 (paper April 10)
**Paper:** https://arxiv.org/abs/2604.08995
**Code:** https://github.com/SkyworkAI/Matrix-Game (2,152 stars)
**Weights:** https://huggingface.co/Skywork/Matrix-Game-3.0 (109 likes)
**License:** MIT

### What It Is
A memory-augmented interactive world model for 720p real-time longform video generation. The purest "LongLive successor" — same AR diffusion streaming paradigm but with explicit long-horizon memory and self-correction.

### Key Specs
- **Resolution:** 720p
- **Speed:** Up to 40 FPS real-time (5B base model)
- **Scaling:** 2x14B MoE model for higher quality
- **Memory:** Camera-aware memory retrieval + injection for long-horizon spatiotemporal consistency
- **Self-correction:** Re-injects imperfect generated frames during training so the model learns to fix its own drift on the fly
- **Rollout:** Stable over minute+ sequences without quality collapse

### Architecture
- Prediction residuals modeling (not raw frames)
- Multi-segment autoregressive distillation (DMD-based)
- Model quantization + VAE decoder pruning for real-time inference
- Industrial-scale data engine: Unreal Engine synthetic data + AAA game capture + real-world video augmentation
- Video-Pose-Action-Prompt quadruplet training data

### Interactivity
Fully interactive — conditions on text prompts + actions (mouse/keyboard). New prompts can be fed mid-stream for narrative switches, analogous to LongLive's KV-recache but with stronger long-term coherence.

### Why It Matters for Etherea
This is the closest thing to a drop-in upgrade for the streaming video generation pipeline. Same streaming AR paradigm as LongLive but solves the error-accumulation problem with explicit memory and self-correction. 40 FPS at 720p is production-grade. MIT licensed. If Etherea wanted to swap or supplement its current StreamDiffusion + LLM pipeline, this is the most natural candidate.

---

## 2. LPM 1.0 — MiHoYo (Best for Conversational/Character-Driven)

**Released:** April 9, 2026 (paper v2 updated)
**Paper:** https://arxiv.org/abs/2604.07823
**Team:** MiHoYo AI (Genshin Impact / Honkai: Star Rail studio)
**Parameters:** 17B Diffusion Transformer (Base LPM), distilled to causal streaming generator (Online LPM)

### What It Is
A "Large Performance Model" — focuses on character performance (visual, vocal, temporal behavior) for infinite-length, real-time, identity-consistent video generation. Specifically designed for full-duplex audio-visual conversation.

### Key Specs
- **Length:** Infinite — no practical limit, identity-stable across endless streams
- **Speed:** Real-time inference (Online LPM is a causal streaming distillation)
- **Identity:** Multi-reference identity-aware extraction maintains character consistency forever
- **Audio:** Full-duplex — character simultaneously speaks, listens, reacts, emotes
- **Control:** Text prompts for motion control + audio conditioning

### Architecture
- 17B parameter Diffusion Transformer base
- Multimodal conditioning: character image + identity references + audio + text prompts
- Causal streaming distillation for low-latency online generation
- Human-centric dataset with speaking-listening pairing, performance understanding, identity-aware extraction

### The "Performance Trilemma"
LPM explicitly addresses the tension between:
1. High expressiveness
2. Real-time inference
3. Long-horizon identity stability

Previous models could do two of three. LPM claims all three.

### Use Cases
- Visual engine for conversational AI agents
- Live streaming characters
- Game NPCs
- Interactive drama

### Why It Matters for Etherea
If Etherea moves toward character-driven experiences (imagine a projected character that responds to voice in real time with consistent identity), LPM is the state-of-the-art. The full-duplex audio-visual conversation capability maps directly to Etherea's voice-driven paradigm — except LPM generates consistent character performances while Etherea generates environments. Potential hybrid: LPM for character + Etherea's pipeline for environment.

### LPM-Bench
They also released LPM-Bench, the first benchmark for interactive character performance. Worth tracking for evaluation standards.

---

## 3. HY-World 2.0 (Tencent Hunyuan) — Best for 3D Persistence

**Released:** April 16, 2026 (today!)
**Report:** https://3d-models.hunyuan.tencent.com/world/world2_0/HY_World_2_0.pdf
**Code:** https://github.com/Tencent-Hunyuan/HY-World-2.0 (702 stars)
**Weights:** https://huggingface.co/tencent/HY-World-2.0 (151 likes)
**Demo:** https://3d.hunyuan.tencent.com/sceneTo3D
**Built on:** HY-World 1.5 (WorldPlay) + WorldCompass + WorldMirror

### What It Is
A paradigm shift from video world models to 3D world models. Instead of generating pixel videos that vanish after playback, HY-World 2.0 produces editable, persistent 3D assets (meshes / 3D Gaussian Splats) importable into Unity/Unreal/Blender.

### The Argument Against Video World Models (Their Framing)
Tencent explicitly positions this against video world models:

| | Video World Models | HY-World 2.0 (3D) |
|--|---|---|
| Output | Pixel videos (non-editable) | Real 3D assets (fully editable) |
| Duration | Limited (~1 min) | Unlimited — assets persist permanently |
| 3D Consistency | Flickering/artifacts | Native 3D consistency |
| Real-Time Rendering | Per-frame inference, high latency | Consumer GPUs render in real time |
| Controllability | Imprecise | Zero-error control, real physics |
| Inference Cost | Accumulates per interaction | One-time generation |
| Engine Compatible | No (video files only) | Yes (Blender/UE/Isaac) |

Their tagline: "Watch a video, then it's gone" vs. "Build a world, keep it forever"

### Two Core Capabilities
1. **World Generation** (text/image to 3D world): Four-stage pipeline:
   - Panorama Generation (HY-Pano 2.0)
   - Trajectory Planning (WorldNav)
   - World Expansion (WorldStereo 2.0)
   - World Composition (WorldMirror 2.0 + 3DGS learning)

2. **World Reconstruction** (multi-view images/video to 3D): WorldMirror 2.0 — single forward pass predicts depth, normals, camera params, point clouds, and 3DGS attributes simultaneously.

### Ecosystem (Full Hunyuan World Stack)
- **HunyuanWorld-1** (Oct 2025): Initial world model, 419 HF likes
- **HunyuanWorld-Voyager** (Oct 2025): Interactive RGBD video + real-time 3D reconstruction, 1,538 GitHub stars
- **HunyuanWorld-Mirror** (Oct 2025): Fast universal 3D reconstruction, 1,083 GitHub stars
- **HY-WorldPlay** / HY-World 1.5 (Mar 2026): Streaming AR video with real-time latency + geometric consistency, 1,436 GitHub stars
- **HY-World 2.0** (Apr 16, 2026): Full 3D world generation + reconstruction

### Open Source Status
- WorldMirror 2.0: Released today (inference code + weights)
- Full World Generation: Coming soon
- Panorama Generation (HY-Pano 2.0): Coming soon
- WorldNav trajectory planning: Coming soon
- WorldStereo 2.0: Coming soon

### Why It Matters for Etherea
The 3D persistence argument is compelling and worth monitoring. If Etherea wanted to generate 3D environments (not just flat projected video), HY-World 2.0's pipeline could produce persistent spaces that render on consumer GPUs without continuous inference cost. However, HY-World 2.0 is more about building static/explorable 3D worlds than real-time streaming video. The earlier HY-WorldPlay (1.5) is actually more directly comparable to Etherea's current pipeline.

The real question: is Etherea's future in streaming video (Matrix-Game 3.0 direction) or persistent 3D worlds (HY-World 2.0 direction)?

---

## Comparison Matrix

| Model | Speed | Resolution | Infinite? | Interactive? | Open Source | Best For |
|-------|-------|-----------|-----------|-------------|-------------|----------|
| Matrix-Game 3.0 | 40 FPS | 720p | Yes (minute+) | Full (text+actions) | Yes (MIT) | Streaming world simulation |
| LPM 1.0 | Real-time | Not specified | Yes (infinite) | Full-duplex audio+visual | Partial | Character performance |
| HY-World 2.0 | One-shot gen | Varies | Persistent 3D | Text/image input | Yes (partial) | 3D world building |
| LongLive (current) | Real-time | 832x480 | Yes | KV-recache prompting | Internal | Etherea's current pipeline |
| Happy Oyster (Alibaba) | Real-time | Unknown | Persistent worlds | Text+actions live | No | Consumer world creation |

---

## Recommendations for Etherea

### Immediate (This Week)
1. **Try Matrix-Game 3.0** — MIT licensed, weights on HuggingFace, closest architecture to LongLive. Could benchmark against current pipeline for quality/speed comparison. The memory module and self-correction could solve drift issues in longer Etherea sessions.

2. **Watch LPM 1.0 demos** — The full-duplex audio-visual capability is exactly what "talking to Etherea and having it respond" would look like for character-driven experiences. Check MiHoYo channels for demos.

### Medium Term
3. **Evaluate HY-World 2.0 for 3D projection** — If Etherea moves toward spatial/3D projection (e.g., volumetric displays, AR glasses), the persistent 3D asset pipeline eliminates per-frame inference cost. WorldMirror 2.0 is already runnable.

4. **Monitor Happy Oyster (Alibaba)** — Product-level competitor in the exact space. Their model architecture is unknown but their product capabilities (directing + wandering modes, real-time streaming via ARTC) represent the target UX.

### Strategic
5. **The field is converging on your thesis** — Four separate major organizations (Skywork, MiHoYo, Tencent, Alibaba) all shipped products/models this week that validate "real-time, interactive, infinite video generation" as a major category. Etherea was early. The moat is physical-space deployment + voice-first interaction + live event expertise.

---

## Also Noted (Not Detailed)
- **INSPATIO-WORLD** — spatial world model, slightly earlier release
- **PixVerse R1 updates** — incremental, less focused on infinite promptable video
- **Seedance 2.0** — video generation advancement (trending on HF daily papers today), but not interactive/world-model focused
