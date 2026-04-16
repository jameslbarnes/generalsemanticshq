# Happy Oyster AI — Research Report

**Date:** April 16, 2026  
**Researcher:** Hermes (requested by James Barnes)  
**URL:** https://happyoyster.ai  
**Domain:** happyoysterai.com (for sale on Spaceship — not the active product)

---

## What It Is

Happy Oyster is a consumer-facing web app that provides **real-time safety assessments for raw oyster consumption** across Europe. Its tagline: *"Should I eat you today? — Real-time safety for today's oysters."*

The app was built using **Lovable** (formerly GPT Engineer), a no-code/low-code AI app builder. It runs on Supabase for backend/auth and uses the Open-Meteo weather archive API for environmental data.

**Lovable Project:** https://lovable.dev/projects/83c55300-e510-4c8f-b22d-04a741233596

---

## How It Works

### Data Sources
- **Open-Meteo Archive API** — Historical and near-real-time precipitation and temperature data, fetched per-region based on oyster origin coordinates
- **ipapi.co** — Geolocation to detect user's country and auto-select EU shipping zone

### Risk Assessment Model

The app evaluates three risk dimensions:

**1. Rainfall Risk (Norovirus/runoff contamination)**
- Analyzes precipitation in the 5 days before harvest
- `>25mm` single-day spike → DANGER (high runoff risk)
- `>=15mm` single-day spike → CAUTION
- `>50mm` cumulative over window → CAUTION (ground saturation)
- Warns about viral contamination (Norovirus) from land runoff

**2. Temperature Risk (Vibrio bacteria)**
- `>25°C` water temp → DANGER (breeding ground for bacteria)
- `>=20°C` → CAUTION
- `<20°C` → SAFE

**3. Spawning Season (Texture/Quality)**
- May through August (months 4-7) = spawning season
- Diploid oysters become soft, milky, or mushy during this period
- Only affects diploid varieties (not triploid)

**Overall Risk** = worst of rainfall + temperature risk. If both are DANGER, it's flagged as CRITICAL.

### Oyster Brands Tracked
Eight European premium brands with precise harvest coordinates:
- **Belon (Flats)** — Riec-sur-Bélon, France (diploid)
- **Fine de Claire** — Marennes, France (diploid)
- **Gillardeau** — Marennes, France (diploid)
- **Muirgen** — Cancale, France
- **Ostra Regal** — Bannow Bay, Ireland
- **Pousse en Claire** — Marennes, France (diploid)
- **Sentinelles** — Bannow Bay, Ireland
- **Tsarskaya** — Cancale, France

### EU Shipping Zones
The app calculates estimated harvest-to-table delay based on zone:
- Zone 1 (France, Ireland, UK, Netherlands, Belgium): 2 days
- Zone 2 (Germany, Italy, Spain, Switzerland, Austria, Denmark): 4 days
- Zone 3 (Sweden, Norway, Finland, Poland, etc.): 6 days

### Forward-Looking Features
- **Next Batch Risk** — Projects risk for upcoming harvest based on weather forecast
- **"Safer Next Week"** — Advises waiting if conditions are expected to improve
- **Physical Safety Tips** — Includes visual/tactile inspection guide (plump, glossy, retracts on touch)

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Framework | React (with React Query / TanStack) |
| UI | Tailwind CSS + Radix UI (shadcn/ui components) |
| Backend | Supabase (auth, real-time, database) |
| Weather Data | Open-Meteo Archive API |
| Geolocation | ipapi.co |
| Builder | Lovable (GPT Engineer) |
| Hosting | Lovable-hosted (lovable.app subdomain with custom domain) |

---

## Relevance to Etherea

### Direct Code/Team Connection
**None found.** No references to Happy Oyster in the etherea-ai codebase, hermes-agent, or GSHQ repos. No GSHQ team member profiles mention it. The GitHub user W1DEM4N has an unrelated Java "HappyOyster" project from 2020. The Lovable project user ID (oMYSdaAzmdZEivemSCAldAEfyU03) couldn't be traced to a known team member.

### Conceptual Parallels

Despite no direct connection, there are interesting thematic overlaps:

1. **Real-Time Environmental Data → Human Experience**
   - Etherea: transforms speech into visual worlds in real time
   - Happy Oyster: transforms weather/environmental data into eat/don't-eat decisions in real time
   - Both bridge sensor data and lived experience

2. **Safety Through Sensing**
   - Etherea's deployment contexts include medical (Johns Hopkins aphasia research)
   - Happy Oyster is fundamentally about food safety through environmental monitoring
   - Both apply real-time data processing to human wellbeing

3. **AI-Augmented Decision Making**
   - Etherea uses LLMs (Claude, Gemini) to interpret speech and generate visual prompts
   - Happy Oyster uses algorithmic risk scoring (not LLM-based, but data-driven AI-adjacent logic)
   - Both reduce complex data to actionable outputs

4. **European Focus / Cultural Context**
   - Happy Oyster tracks French and Irish oyster appellations — premium food culture
   - Etherea has deployed in culturally rich contexts (music festivals, art events, Soho showrooms)
   - Both operate at the intersection of technology and cultural experience

### Potential Collaboration/Integration Ideas

- **Etherea x Dining Experience:** Imagine an Etherea installation in an oyster bar where the visual environment changes based on the provenance and conditions of the oysters being served — projected terroir
- **Sensor-Driven Generative Art:** Happy Oyster's environmental data (rainfall, temperature, marine conditions) could feed into Etherea's generative pipeline as ambient data inputs
- **Food Safety Visualization:** Etherea's real-time projection system could visualize food safety data in restaurant/commercial kitchen contexts

---

## Assessment

Happy Oyster is a niche but well-executed consumer app in the food safety/transparency space. It's technically simple (no-code Lovable build, pure client-side risk scoring, no ML models) but conceptually sharp — it solves a real problem for European raw oyster consumers.

The connection to Etherea is **thematic rather than technical**. Both products exemplify the pattern of using real-time data processing to enhance human experience and decision-making, but they share no code, infrastructure, team members, or direct business relationship.

If someone on the GSHQ team built this, it was likely as a personal project using Lovable, completely separate from the Etherea codebase.
