# Inventory — ETHEREA Installation BOM

> Source: [ETHEREA_Installation_BOM_v2.xlsx](https://docs.google.com/spreadsheets/d/1DBY2yPrw_iWjbbHyqu7ARG-InSPFjbmI/edit?gid=1088089843#gid=1088089843)
>
> Status key: planned | ordered | shipped | received
>
> Last updated: 2026-04-15

## Main Workstation — ETHEREA Render Engine

| Item | Specs | Qty | Unit Price | Status | Tracking | Received | Notes |
|------|-------|-----|-----------|--------|----------|----------|-------|
| NVIDIA RTX PRO 6000 Blackwell (GPU) | 96 GB GDDR7 ECC (USED) | 1 | $6,292.95 | planned | — | — | Used — verify warranty |
| Intel Core Ultra 9 285K (CPU) | 24-core, 5.7 GHz | 1 | $589.00 | planned | — | — | |
| MSI MEG Z890 ACE (Motherboard) | Z890, PCIe 5.0, WiFi 7 | 1 | $599.00 | planned | — | — | |
| 128 GB DDR5-6400 4x32 (RAM) | Corsair Dominator | 1 | $520.00 | planned | — | — | |
| 4 TB NVMe Gen 5 SSD (Storage) | Crucial T705 | 1 | $380.00 | planned | — | — | |
| Corsair HX1600i 1600W (PSU) | 80+ Titanium | 1 | $349.99 | planned | — | — | |
| Phanteks Enthoo Pro 2 (Case) | Full Tower | 1 | $199.99 | planned | — | — | |
| NZXT Kraken 360 AIO (Cooler) | 360 mm | 1 | $179.99 | planned | — | — | |
| Windows 11 Pro OEM (OS) | | 1 | $199.99 | planned | — | — | |
| Monitor Display | Control / monitoring screens | 2 | $70.00 | planned | — | — | |
| Cables, adapters, paste, risers | PCIe adapters, MX-6, zip ties | 1 | $150.00 | planned | — | — | |

**Subtotal: ~$9,531**

## Projection — 4-Projector Array

| Item | Specs | Qty | Unit Price | Status | Tracking | Received | Notes |
|------|-------|-----|-----------|--------|----------|----------|-------|
| JMGO O2S Ultra (Projector) | 4K UST, 3600 lm, triple laser RGB | 1 | $2,599.00 | planned | — | — | Hero wall — primary surface |
| Optoma GT2100HDR (Projector) | 1080p ST, 4200 lm, 0.49:1, laser 24/7 | 3 | $1,149.00 | planned | — | — | Short throw, RS232 control |
| Ceiling / wall mount bracket | Universal projector mount | 4 | $199.99 | planned | — | — | |
| Short HDMI 2.0 Cable (6ft) | Orin to projector local connect | 4 | $9.99 | planned | — | — | Only short runs needed |

**Subtotal: ~$6,886**

## Sensing & Audio

| Item | Specs | Qty | Unit Price | Status | Tracking | Received | Notes |
|------|-------|-----|-----------|--------|----------|----------|-------|
| Intel RealSense D455 (Camera) | Depth, 87 deg FoV | 2 | $419.00 | planned | — | — | |
| Discreet wall / ceiling mount | Camera mount | 2 | $39.99 | planned | — | — | |
| Shure MV7 (Microphone) | USB/XLR Dynamic | 2 | $249.00 | planned | — | — | |
| Boom Arm / Low-profile mount | Mic mount | 2 | $34.99 | planned | — | — | |

**Subtotal: ~$1,488**

## Edge Compute — 4x Orin Nano Super (NDI Receivers)

| Item | Specs | Qty | Unit Price | Status | Tracking | Received | Notes |
|------|-------|-----|-----------|--------|----------|----------|-------|
| Orin Nano Super Dev Kit 8GB (SBC) | NVIDIA Jetson — NDI decode + output | 4 | $249.00 | planned | — | — | 1 per projector |
| 1TB NVMe Gen3 SSD | Boot + storage | 4 | $70.00 | planned | — | — | |
| Aluminum case w/ fan mount | + camera holder | 4 | $38.00 | planned | — | — | |
| Noctua NF-A4x20 5V PWM (Fan) | PWM fan | 4 | $15.00 | planned | — | — | |
| WiFi 6 / BT 5.0 M.2 card | + dual antennas — NDI transport | 4 | $20.00 | planned | — | — | WiFi 6 for wireless NDI|HX |
| IMX219 8MP CSI camera | Local CV / sensing per node | 4 | $25.00 | planned | — | — | |
| 15.6" 1080p IPS portable display | USB-C powered — setup/debug | 4 | $125.00 | planned | — | — | Can remove after install |
| DP-to-HDMI adapter | | 4 | $10.00 | planned | — | — | |
| Wireless keyboard + mouse combo | Setup/debug | 4 | $25.00 | planned | — | — | Can share post-install |
| USB-C cables, microSD backup | | 4 | $15.00 | planned | — | — | |
| UPS / battery backup module | | 4 | $33.00 | planned | — | — | |

**Subtotal: ~$2,500**

## Network — Wireless NDI Transport Layer

| Item | Specs | Qty | Unit Price | Status | Tracking | Received | Notes |
|------|-------|-----|-----------|--------|----------|----------|-------|
| WiFi 6E Mesh Router | Tri-band, dedicated 6GHz backhaul | 1 | $249.00 | planned | — | — | Dedicated ETHEREA network |
| WiFi 6E Mesh Satellite | Extend coverage across venue | 1 | $149.00 | planned | — | — | If venue footprint requires |
| Managed Gigabit Switch 8-port | VLAN, QoS for NDI priority | 1 | $89.00 | planned | — | — | Fallback wired backbone |
| Cat6a Ethernet (10ft each) | For wired fallback / workstation | 4 | $12.00 | planned | — | — | Backup only |

**Subtotal: ~$535**

## Software & Subscriptions

| Item | Specs | Qty | Unit Price | Status | Tracking | Received | Notes |
|------|-------|-----|-----------|--------|----------|----------|-------|
| Claude Max 5x Plan | $100/mo x 24 months | 1 | $2,400.00 | planned | — | — | 2-year commitment |
| NDI Tools (Vizrt) | NDI SDK / runtime — free | 4 | $0.00 | planned | — | — | Open protocol, no license fee |

**Subtotal: ~$2,400**

## Miscellaneous & Contingency

| Item | Specs | Qty | Unit Price | Status | Tracking | Received | Notes |
|------|-------|-----|-----------|--------|----------|----------|-------|
| Cable management / raceways | Velcro, conduit, labels (power only) | 1 | $80.00 | planned | — | — | Minimal — no HDMI runs |
| Power strips / surge protectors | Rack-mount, filtered | 2 | $65.00 | planned | — | — | |
| Spare cables & connectors | HDMI short, USB-C, Ethernet, audio | 1 | $60.00 | planned | — | — | |
| Mounting hardware misc | Anchors, brackets, screws, velcro | 1 | $45.00 | planned | — | — | |
| Installation contingency | ~5% buffer for unforeseen costs | 1 | $600.00 | planned | — | — | |

**Subtotal: ~$915**

---

## Grand Total: ~$24,323
