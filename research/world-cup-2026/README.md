# FIFA World Cup 2026 — GSHQ Strategy

> NYC is hosting. We are here. This is our moment.

## Overview

The 2026 FIFA World Cup is coming to New York City. Dane is working on the World Cup professionally and is talking about running a shuttle bus between the official venues and the School. This is a massive opportunity to bring people through the doors using soccer as the trojan horse — then blow their minds with what we are actually building.

## Core Strategies

### 1. Watch Parties at the School
- Show multiple games simultaneously in the theater
- Sell lemonade (and other refreshments)
- Create a community gathering point as an alternative to bars/official fan zones
- Dane connection = direct pipeline from official World Cup venues via shuttle

### 2. Generative Stage — Live Game Overlays
- Display live scores and match data on the generative stage
- Real-time visual reactions to goals, cards, big moments
- ETHEREA reacting to the energy of the crowd

### 3. Video-to-Video Style Transfer on Live Games (THE BIG IDEA)
Inspired by the NFL x Pixar "Toy Story Funday Football" broadcast where NFL games were rendered in real-time as Pixar characters in Andy's room by tracking players.

Our version:
- Take the live World Cup broadcast feed
- Run it through a real-time video-to-video model (style transfer)
- People watching can **control the style with their voice** — change the visual aesthetic of the game in real-time
- Candidates:
  - **LSDream model** (by Dick Hart) — real-time style transfer, works great on real video footage. Does not work well with shaders but excellent for live video.
  - **Odyssey world model** — could be another option depending on capabilities
  - Any other real-time vid2vid models we can integrate

This is basically: watch the World Cup, but the entire broadcast looks like a fever dream that the audience collectively controls. Wild.

### 4. Shuttle Bus Pipeline (via Dane)
- Dane wants to run shuttles between official World Cup venues and the School
- People come from the games → walk into our space → experience something completely different
- Converts casual soccer fans into GSHQ community members

## Research & References

- [ ] NFL x Pixar "Toy Story Funday Football" — study how they did real-time player tracking + 3D rendering
- [ ] LSDream / Dick Hart style transfer model — get access, test on live video
- [ ] Odyssey model capabilities for live video style transfer
- [ ] World Cup NYC match schedule — which games are at MetLife/NYC venues
- [ ] Dane's shuttle logistics and timeline
- [ ] Permits/licensing for showing live broadcasts at the School
- [ ] Revenue model: lemonade + donations + sponsorship?

## Timeline
- **Now - June 2026**: R&D on video-to-video pipeline, test with existing streams
- **June 2026**: Echoes festival = dress rehearsal
- **June 11 - July 19, 2026**: FIFA World Cup 2026

## Open Questions
- [ ] What is the broadcast rights situation for showing games at a venue like the School?
- [ ] Can we partner with a bar/restaurant for food+drink to keep it legal and funded?
- [ ] How many people can the theater hold for watch parties?
- [ ] What is the latency on the LSDream model? Can it keep up with live sports?
- [ ] Can we get the match data feed (scores, events) piped into ETHEREA programmatically?
- [ ] Should we livestream our stylized version of the games? (probably copyright issues but worth exploring)
