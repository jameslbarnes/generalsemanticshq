# Nouriel Installation — ETHEREA @ Lightning Society

45 Howard St, NYC

## Overview

Full ETHEREA installation build: a 4-projector immersive system driven by a single render workstation, with 4x Orin Nano edge nodes handling wireless NDI decode, dual depth cameras, and a dedicated WiFi 6E network.

## Budget

Grand total: ~$24,323 (USD, tax not included, March 2026 pricing)

## Architecture

- Workstation renders → NDI|HX encode → WiFi 6E → Orin Nano decode → projector output
- Zero long cable runs. Each Orin Nano sits at its projector with a short HDMI connection
- NDI|HX2 (H.265) recommended over full NDI — lower bandwidth, better for wireless
- Dedicated WiFi 6E network isolates ETHEREA traffic from venue WiFi
- Wired Ethernet fallback via Cat6a short runs + managed switch with QoS
- Orin Nano GPU (1024 CUDA cores) handles NDI decode + local CV sensing

## Key Files

- [inventory.md](inventory.md) — Full parts list with order/shipping status
- Source BOM: [Google Sheet](https://docs.google.com/spreadsheets/d/1DBY2yPrw_iWjbbHyqu7ARG-InSPFjbmI/edit?gid=1088089843#gid=1088089843)

## Related Issues

- [#1 — Order parts for Nouriel](https://github.com/jameslbarnes/generalsemanticshq/issues/1)

## Notes

- GPU is USED — confirm seller warranty / return policy
- Claude Max 5x at $100/mo. Upgrade to 20x ($200/mo) if generation demands it
- Portable displays + keyboards can be removed after install
