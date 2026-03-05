# Biometric Audio-Reactive WebGL Synthesizer — Design Document

## Original Prompt

> Before writing any executable code, architect a "Biometric Audio-Reactive WebGL Synthesizer" using an Annotated Multi-Dimensional ASCII DSL.
>
> 1. **SPATIAL GRID**: Draw the 2D UI topology. Left Sidebar: `<Stream: AudioNode>` input controls and gain staging. Center Canvas: `<WebGL_Viewport>` containing a 3D generative core. Right Sidebar: `<Stream: Biometric>` simulated heart-rate tempo sliders. Bottom Dock: `<Kinetic_Sequencer>` for playback.
>
> 2. **KINETIC LEDGER**: For every interactive node in the ASCII grid, map a `[Kinetic]` tag defining exact spring physics (stiffness, damping, mass) and intersection observer triggers for entry states.
>
> 3. **Z-STACK & SHADER LEDGER**: Define the exact GLSL fragment/vertex shader logic required for the `<WebGL_Viewport>` to mutate its geometry based on the audio's Fast Fourier Transform (FFT) low-frequency data. Define all backdrop-filter blur radii for the floating sidebars.
>
> 4. **MULTIMODAL I/O CONTRACT**: Explicitly map the data transformation pipeline from `navigator.mediaDevices.getUserMedia` -> `AudioContext` -> `AnalyserNode` -> `Uint8Array` -> Uniforms injected into the WebGL material.
>
> **Design choice**: Terrain mesh (FFT drives a heightmap grid, like a living landscape).

---

## Plain-Language Explanation

### What This Design Actually Is

Imagine a **living landscape** on your screen — like a 3D terrain made of mountains and valleys — that **moves and pulses in real-time based on music and your body's signals**.

You open a web page. In the center, there's a 3D surface that looks like a miniature mountain range. When music plays, the mountains **rise and fall with the beat** — bass hits make tall peaks, quiet moments flatten out. At the same time, sliders on the right side simulate your heartbeat, breathing, and stress level, which **change the shape and color** of the terrain too.

### The Four Panels

**Left Sidebar — Sound Controls**
- Pick where sound comes from (your microphone, a music file, or a generated tone)
- A volume knob
- Filters to focus on specific sound ranges (like "only listen to the bass" or "ignore high-pitched sounds")
- A setting for how "jumpy" vs "smooth" the reaction to sound should be

**Center — The 3D Terrain**
- A flat grid of 4,096 tiny points arranged in a square (64 x 64)
- Each point's **height** gets pushed up or down based on what the music is doing at that moment
- The result looks like an ocean of peaks and valleys that dance with the audio
- Colors shift from **deep blue** (quiet) to **bright cyan** (medium) to **white-hot** (loud), with **red flashes** on the beat

**Right Sidebar — Body Signal Simulators**
- Heart rate slider (40-120 BPM) — faster heartbeat = faster terrain pulsing
- Heart rate variability (HRV) — adds randomness and organic feel to the motion
- Breathing rate — creates slow, wave-like undulations across the terrain
- Skin conductance (a stress/arousal measure) — higher values add more fine surface detail and denser grid lines
- A waveform selector (smooth sine wave, jagged sawtooth, or sharp square wave) — changes the *shape* of the pulsing pattern

**Bottom Dock — Playback Timeline**
- Play/stop/loop buttons
- A timeline with 3 tracks that let you **schedule** when different effects kick in:
  - Track 1: controls how strongly music affects terrain height
  - Track 2: controls speed changes tied to BPM
  - Track 3: controls color shifts tied to skin conductance

### The "Spring Physics" Part (Kinetic Ledger)

Every slider, button, and panel has a **bouncy animation** — like a spring on a door. When you drag a slider, it doesn't just jump to the new position; it overshoots slightly and settles back. Three numbers define how each spring behaves:

- **Stiffness** — how strongly it snaps back (higher = snappier)
- **Damping** — how quickly it stops bouncing (higher = less bouncy)
- **Mass** — how heavy it feels (higher = more sluggish)

The panels themselves animate in when the page loads — left sidebar slides from the left, right sidebar from the right, bottom dock rises up from below. Each element inside the panels appears with a slight stagger delay, creating a cascading entrance effect.

An **Intersection Observer** is a browser feature that detects when something scrolls into view. Here it's used to trigger the entrance animations only when a panel becomes visible, and to pause the 3D rendering when the canvas scrolls off-screen (saving battery/GPU).

### The "Shader" Part (Z-Stack & Shader Ledger)

A **shader** is a tiny program that runs on your graphics card (GPU) instead of your main processor. It's what makes the 3D terrain possible at 60 frames per second. There are two:

- **Vertex shader** — takes each of those 4,096 grid points and decides *how high* to push it, based on the current music data + body signals. This is where the terrain shape comes from.
- **Fragment shader** — decides *what color* each pixel should be, based on how high that point was pushed. Low areas are deep blue, peaks glow white, and the strongest beats flash red.

The **Z-Stack** defines layering order — which panels float above which. The sidebars and dock float above the 3D canvas with a frosted-glass blur effect (like looking through textured glass), so the terrain is visible behind them but not distracting.

### The "Pipeline" Part (Multimodal I/O Contract)

This is the journey of sound data through the system, happening 60 times per second:

1. **Capture** — the browser asks permission to use your microphone (or loads a music file, or generates a test tone)
2. **Process** — the sound goes through volume adjustment and frequency filters (removing unwanted bass rumble or high-pitched hiss)
3. **Analyze** — a built-in browser tool (the AnalyserNode) breaks the sound into 64 frequency "buckets" using FFT (Fast Fourier Transform) — a math technique that splits a complex sound wave into its component frequencies, telling you "how much bass, how much midrange, how much treble" at this exact instant
4. **Merge** — combine the 64 frequency values with the body signal slider values into a single packet of numbers
5. **Send to GPU** — push all those numbers (called "uniforms") into the shader so the terrain updates in real-time

### In One Sentence

It's a music visualizer where a 3D landscape dances to audio, and simulated body signals (heartbeat, breathing, stress) add an organic, living quality to the motion and color.

---

## Section 1: SPATIAL GRID — 2D UI Topology

```
╔══════════════════════════════════════════════════════════════════════════════════════════════╗
║ z:999  TOPBAR  [blur:20px sat:1.8]                                          H:48px FIXED   ║
║ ┌──────────────────────────────────────────────────────────────────────────────────────────┐ ║
║ │ ◈ BIOVIZ          ┃  ♫ Input: ■■■■░░░░  -12dB  ┃  ♥ 72 BPM  ┃  ⚙  ┃  👤 Session      │ ║
║ └──────────────────────────────────────────────────────────────────────────────────────────┘ ║
╠════════════════╦═══════════════════════════════════════════════╦═══════════════╦═════════════╣
║                ║                                               ║               ║             ║
║  LEFT SIDEBAR  ║          CENTER CANVAS                        ║ RIGHT SIDEBAR ║             ║
║  W:260px       ║          flex:1                               ║ W:240px       ║             ║
║  z:50          ║          z:1                                  ║ z:50          ║             ║
║  [blur:16px]   ║                                               ║ [blur:16px]   ║             ║
║                ║                                               ║               ║             ║
║ ┌────────────┐ ║  ┌─────────────────────────────────────────┐  ║ ┌───────────┐ ║             ║
║ │<Stream:    │ ║  │                                         │  ║ │<Stream:   │ ║             ║
║ │ AudioNode> │ ║  │         <WebGL_Viewport>                │  ║ │ Biometric>│ ║             ║
║ │            │ ║  │                                         │  ║ │           │ ║             ║
║ │ ┌────────┐ │ ║  │    ╱╲    ╱╲╱╲    ╱╲                    │  ║ │ ♥ BPM     │ ║             ║
║ │ │SRC SEL │ │ ║  │   ╱  ╲  ╱    ╲  ╱  ╲   ╱╲             │  ║ │ ┌───────┐ │ ║             ║
║ │ │○ Mic   │ │ ║  │  ╱    ╲╱      ╲╱    ╲ ╱  ╲            │  ║ │ │ 40    │ │ ║             ║
║ │ │● File  │ │ ║  │ ╱      TERRAIN MESH    ╲    ╲           │  ║ │ │───●──│ │ ║             ║
║ │ │○ Osc   │ │ ║  │╱       FFT heightmap    ╲    ╲──        │  ║ │ │   120 │ │ ║             ║
║ │ └────────┘ │ ║  │        driven grid        ╲              │  ║ │ └───────┘ │ ║             ║
║ │            │ ║  │                                         │  ║ │           │ ║             ║
║ │ GAIN STAGE │ ║  │   Grid: 64×64 vertices                 │  ║ │ HRV Var   │ ║             ║
║ │ ┌────────┐ │ ║  │   Y = f(FFT[bin], time)                │  ║ │ ┌───────┐ │ ║             ║
║ │ │ Input  │ │ ║  │                                         │  ║ │ │ Lo    │ │ ║             ║
║ │ │ ■■■■░░ │ │ ║  │   Camera: orbit @ radius 3.0           │  ║ │ │──●───│ │ ║             ║
║ │ │ -12 dB │ │ ║  │                                         │  ║ │ │   Hi  │ │ ║             ║
║ │ └────────┘ │ ║  └─────────────────────────────────────────┘  ║ │ └───────┘ │ ║             ║
║ │            │ ║                                               ║ │           │ ║             ║
║ │ PRE-FFT   │ ║                                               ║ │ BREATH    │ ║             ║
║ │ ┌────────┐ │ ║                                               ║ │ RATE      │ ║             ║
║ │ │ Lo Cut │ │ ║                                               ║ │ ┌───────┐ │ ║             ║
║ │ │──●─────│ │ ║                                               ║ │ │ 8     │ │ ║             ║
║ │ │ 80 Hz  │ │ ║                                               ║ │ │──●───│ │ ║             ║
║ │ └────────┘ │ ║                                               ║ │ │   30  │ │ ║             ║
║ │ ┌────────┐ │ ║                                               ║ │ └───────┘ │ ║             ║
║ │ │ Hi Cut │ │ ║                                               ║ │           │ ║             ║
║ │ │────●───│ │ ║                                               ║ │ SKIN COND │ ║             ║
║ │ │ 2kHz   │ │ ║                                               ║ │ ┌───────┐ │ ║             ║
║ │ └────────┘ │ ║                                               ║ │ │ 0.1   │ │ ║             ║
║ │            │ ║                                               ║ │ │──●───│ │ ║             ║
║ │ FFT SIZE  │ ║                                               ║ │ │   5.0 │ │ ║             ║
║ │ ┌────────┐ │ ║                                               ║ │ └───────┘ │ ║             ║
║ │ │ 256    │ │ ║                                               ║ │           │ ║             ║
║ │ │ 512    │ │ ║                                               ║ │ ─────────── ║             ║
║ │ │●1024   │ │ ║                                               ║ │ TEMPO MAP │ ║             ║
║ │ │ 2048   │ │ ║                                               ║ │ BPM→hz:   │ ║             ║
║ │ │ 4096   │ │ ║                                               ║ │ ●linked   │ ║             ║
║ │ └────────┘ │ ║                                               ║ │ ○manual   │ ║             ║
║ │            │ ║                                               ║ │           │ ║             ║
║ │ SMOOTHING │ ║                                               ║ │ WAVE MOD  │ ║             ║
║ │ ──●─────── │ ║                                               ║ │ ┌───────┐ │ ║             ║
║ │  0.8       │ ║                                               ║ │ │○ Sin  │ │ ║             ║
║ └────────────┘ ║                                               ║ │ │● Saw  │ │ ║             ║
║                ║                                               ║ │ │○ Sqr  │ │ ║             ║
║                ║                                               ║ │ └───────┘ │ ║             ║
║                ║                                               ║ └───────────┘ ║             ║
╠════════════════╩═══════════════════════════════════════════════╩═══════════════╩═════════════╣
║  z:80  BOTTOM DOCK  <Kinetic_Sequencer>                            H:120px  [blur:12px]     ║
║ ┌──────────────────────────────────────────────────────────────────────────────────────────┐ ║
║ │  ◀◀  ▶ PLAY  ▶▶  ■ STOP  │  ⟳ LOOP   │ BPM: [  72  ]  │  TIME: 00:00 / 04:00         │ ║
║ │ ─────────────────────────────────────────────────────────────────────────────────────── │ ║
║ │ TRK1 │▓▓▓▓░░░░▓▓▓▓▓▓░░▓▓░░░░▓▓▓▓░░░░▓▓▓▓▓▓░░▓▓░░░░▓▓▓▓░░░░▓▓▓▓▓▓░░▓▓│ FFT→Hght  │ ║
║ │ TRK2 │░░▓▓▓▓░░░░░░▓▓▓▓░░░░▓▓▓▓░░▓▓░░░░▓▓▓▓░░░░░░▓▓▓▓░░░░▓▓▓▓░░▓▓░░░░│ BPM→Spd   │ ║
║ │ TRK3 │▓▓░░░░▓▓▓▓▓▓░░░░▓▓▓▓░░▓▓▓▓▓▓░░▓▓░░░░▓▓▓▓▓▓░░░░▓▓▓▓░░▓▓▓▓▓▓░░▓▓│ Skin→Clr  │ ║
║ │      ▲ playhead                                                                        │ ║
║ └──────────────────────────────────────────────────────────────────────────────────────────┘ ║
╚══════════════════════════════════════════════════════════════════════════════════════════════╝
```

### Grid Layout Summary

| Zone | Position | Width | Purpose |
|------|----------|-------|---------|
| Topbar | Top, full width | 100%, H:48px | App name, live meters, session info |
| Left Sidebar | Left column | 260px fixed | Audio source, gain, filters, FFT config |
| Center Canvas | Center, fills remaining space | flex:1 | WebGL 3D terrain viewport |
| Right Sidebar | Right column | 240px fixed | Biometric sliders, tempo map, waveform |
| Bottom Dock | Bottom, full width | 100%, H:120px | Transport controls, sequencer tracks |

---

## Section 2: KINETIC LEDGER — Spring Physics & Intersection Triggers

Every interactive element has two properties defined:

1. **Spring physics** — how it animates when interacted with (stiffness/damping/mass)
2. **Intersection entry state** — how it animates when first appearing on screen

```
╔════════════════════════╦═══════════════════════════╦════════════════════════════════════╗
║  NODE ID               ║  [Kinetic] SPRING PHYSICS ║  INTERSECTION / ENTRY STATE       ║
╠════════════════════════╬═══════════════════════════╬════════════════════════════════════╣
║                        ║                           ║                                    ║
║  TOPBAR                ║  stiffness: 300           ║  trigger: none (always visible)    ║
║                        ║  damping:   30            ║  entry: opacity 1 → 1 (static)     ║
║                        ║  mass:      1.0           ║  scroll-hide: translateY(-48px)    ║
║                        ║  response:  scroll-y      ║  threshold: 0                      ║
║                        ║                           ║                                    ║
╠════════════════════════╬═══════════════════════════╬════════════════════════════════════╣
║                        ║                           ║                                    ║
║  LEFT_SIDEBAR          ║  stiffness: 220           ║  trigger: DOMContentLoaded         ║
║  (container)           ║  damping:   26            ║  entry: translateX(-260px) → 0     ║
║                        ║  mass:      1.2           ║  delay: 0ms                        ║
║                        ║  response:  mount         ║  threshold: 0                      ║
║                        ║                           ║                                    ║
╠════════════════════════╬═══════════════════════════╬════════════════════════════════════╣
║                        ║                           ║                                    ║
║  LEFT_SIDEBAR.         ║  stiffness: 400           ║  trigger: parent visible           ║
║  SRC_SEL               ║  damping:   35            ║  entry: scale(0.9) → scale(1)      ║
║  (radio group)         ║  mass:      0.6           ║  delay: 80ms                       ║
║                        ║  response:  click         ║  threshold: 0.5                    ║
║                        ║  on-select: scale(1.05)   ║                                    ║
║                        ║  → settle:  scale(1.0)    ║                                    ║
║                        ║                           ║                                    ║
╠════════════════════════╬═══════════════════════════╬════════════════════════════════════╣
║                        ║                           ║                                    ║
║  LEFT_SIDEBAR.         ║  stiffness: 180           ║  trigger: parent visible           ║
║  GAIN_SLIDER           ║  damping:   20            ║  entry: opacity(0) → opacity(1)    ║
║                        ║  mass:      0.8           ║  delay: 120ms                      ║
║                        ║  response:  drag-y        ║  threshold: 0.5                    ║
║                        ║  clamp:     [-48, 0] dB   ║                                    ║
║                        ║  snap:      1 dB steps    ║                                    ║
║                        ║                           ║                                    ║
╠════════════════════════╬═══════════════════════════╬════════════════════════════════════╣
║                        ║                           ║                                    ║
║  LEFT_SIDEBAR.         ║  stiffness: 350           ║  trigger: parent visible           ║
║  LO_CUT / HI_CUT      ║  damping:   28            ║  entry: translateY(10px) → 0       ║
║  (filter knobs)        ║  mass:      0.5           ║  delay: 200ms                      ║
║                        ║  response:  drag-x        ║  threshold: 0.5                    ║
║                        ║  clamp-lo:  [20, 800] Hz  ║                                    ║
║                        ║  clamp-hi:  [1k, 20k] Hz  ║                                    ║
║                        ║                           ║                                    ║
╠════════════════════════╬═══════════════════════════╬════════════════════════════════════╣
║                        ║                           ║                                    ║
║  LEFT_SIDEBAR.         ║  stiffness: 500           ║  trigger: parent visible           ║
║  FFT_SIZE              ║  damping:   40            ║  entry: opacity(0) → opacity(1)    ║
║  (radio group)         ║  mass:      0.4           ║  delay: 280ms stagger: 40ms/item   ║
║                        ║  response:  click         ║  threshold: 0.5                    ║
║                        ║  on-select: spring-pop    ║                                    ║
║                        ║                           ║                                    ║
╠════════════════════════╬═══════════════════════════╬════════════════════════════════════╣
║                        ║                           ║                                    ║
║  LEFT_SIDEBAR.         ║  stiffness: 200           ║  trigger: parent visible           ║
║  SMOOTHING             ║  damping:   22            ║  entry: scaleX(0) → scaleX(1)      ║
║  (range slider)        ║  mass:      0.7           ║  delay: 340ms                      ║
║                        ║  response:  drag-x        ║  threshold: 0.5                    ║
║                        ║  clamp:     [0.0, 0.99]   ║                                    ║
║                        ║                           ║                                    ║
╠════════════════════════╬═══════════════════════════╬════════════════════════════════════╣
║                        ║                           ║                                    ║
║  WEBGL_VIEWPORT        ║  stiffness: N/A           ║  trigger: DOMContentLoaded         ║
║  (canvas element)      ║  damping:   N/A           ║  entry: opacity(0) → opacity(1)    ║
║                        ║  mass:      N/A           ║  delay: 100ms                      ║
║                        ║  response:  rAF loop      ║  threshold: 0.1                    ║
║                        ║  note: physics handled    ║  on-visible: start render loop     ║
║                        ║  inside GLSL uniforms     ║  on-hidden:  pause render loop     ║
║                        ║                           ║                                    ║
╠════════════════════════╬═══════════════════════════╬════════════════════════════════════╣
║                        ║                           ║                                    ║
║  RIGHT_SIDEBAR         ║  stiffness: 220           ║  trigger: DOMContentLoaded         ║
║  (container)           ║  damping:   26            ║  entry: translateX(+240px) → 0     ║
║                        ║  mass:      1.2           ║  delay: 60ms                       ║
║                        ║  response:  mount         ║  threshold: 0                      ║
║                        ║                           ║                                    ║
╠════════════════════════╬═══════════════════════════╬════════════════════════════════════╣
║                        ║                           ║                                    ║
║  RIGHT_SIDEBAR.        ║  stiffness: 280           ║  trigger: parent visible           ║
║  BPM_SLIDER            ║  damping:   24            ║  entry: translateX(20px) → 0       ║
║                        ║  mass:      0.8           ║  delay: 100ms                      ║
║                        ║  response:  drag-x        ║  threshold: 0.5                    ║
║                        ║  clamp:     [40, 120]     ║                                    ║
║                        ║  emit:      bpm-change    ║                                    ║
║                        ║                           ║                                    ║
╠════════════════════════╬═══════════════════════════╬════════════════════════════════════╣
║                        ║                           ║                                    ║
║  RIGHT_SIDEBAR.        ║  stiffness: 280           ║  trigger: parent visible           ║
║  HRV_SLIDER            ║  damping:   24            ║  entry: translateX(20px) → 0       ║
║                        ║  mass:      0.8           ║  delay: 160ms                      ║
║                        ║  response:  drag-x        ║  threshold: 0.5                    ║
║                        ║  clamp:     [Lo, Hi]      ║                                    ║
║                        ║  maps-to:   u_hrv         ║                                    ║
║                        ║                           ║                                    ║
╠════════════════════════╬═══════════════════════════╬════════════════════════════════════╣
║                        ║                           ║                                    ║
║  RIGHT_SIDEBAR.        ║  stiffness: 280           ║  trigger: parent visible           ║
║  BREATH_RATE           ║  damping:   24            ║  entry: translateX(20px) → 0       ║
║                        ║  mass:      0.8           ║  delay: 220ms                      ║
║                        ║  response:  drag-x        ║  threshold: 0.5                    ║
║                        ║  clamp:     [8, 30]       ║                                    ║
║                        ║  maps-to:   u_breath      ║                                    ║
║                        ║                           ║                                    ║
╠════════════════════════╬═══════════════════════════╬════════════════════════════════════╣
║                        ║                           ║                                    ║
║  RIGHT_SIDEBAR.        ║  stiffness: 280           ║  trigger: parent visible           ║
║  SKIN_COND             ║  damping:   24            ║  entry: translateX(20px) → 0       ║
║                        ║  mass:      0.8           ║  delay: 280ms                      ║
║                        ║  response:  drag-x        ║  threshold: 0.5                    ║
║                        ║  clamp:     [0.1, 5.0]    ║                                    ║
║                        ║  maps-to:   u_skin        ║                                    ║
║                        ║                           ║                                    ║
╠════════════════════════╬═══════════════════════════╬════════════════════════════════════╣
║                        ║                           ║                                    ║
║  RIGHT_SIDEBAR.        ║  stiffness: 400           ║  trigger: parent visible           ║
║  TEMPO_MAP             ║  damping:   35            ║  entry: scale(0.9) → scale(1)      ║
║  (radio: linked/manual)║  mass:      0.6           ║  delay: 340ms                      ║
║                        ║  response:  click         ║  threshold: 0.5                    ║
║                        ║  on-linked: sync BPM      ║                                    ║
║                        ║  slider → sequencer BPM   ║                                    ║
║                        ║                           ║                                    ║
╠════════════════════════╬═══════════════════════════╬════════════════════════════════════╣
║                        ║                           ║                                    ║
║  RIGHT_SIDEBAR.        ║  stiffness: 400           ║  trigger: parent visible           ║
║  WAVE_MOD              ║  damping:   35            ║  entry: opacity(0) → opacity(1)    ║
║  (radio: sin/saw/sqr)  ║  mass:      0.6           ║  delay: 400ms stagger: 30ms/item   ║
║                        ║  response:  click         ║  threshold: 0.5                    ║
║                        ║  maps-to:   u_waveform    ║                                    ║
║                        ║                           ║                                    ║
╠════════════════════════╬═══════════════════════════╬════════════════════════════════════╣
║                        ║                           ║                                    ║
║  BOTTOM_DOCK           ║  stiffness: 260           ║  trigger: DOMContentLoaded         ║
║  (container)           ║  damping:   28            ║  entry: translateY(+120px) → 0     ║
║                        ║  mass:      1.4           ║  delay: 150ms                      ║
║                        ║  response:  mount         ║  threshold: 0                      ║
║                        ║                           ║                                    ║
╠════════════════════════╬═══════════════════════════╬════════════════════════════════════╣
║                        ║                           ║                                    ║
║  BOTTOM_DOCK.          ║  stiffness: 500           ║  trigger: parent visible           ║
║  TRANSPORT             ║  damping:   38            ║  entry: scale(0.85) → scale(1)     ║
║  (play/stop/loop)      ║  mass:      0.5           ║  delay: 200ms stagger: 50ms/btn    ║
║                        ║  response:  click         ║  threshold: 0.5                    ║
║                        ║  on-press:  scale(0.92)   ║                                    ║
║                        ║  on-release: spring-back  ║                                    ║
║                        ║                           ║                                    ║
╠════════════════════════╬═══════════════════════════╬════════════════════════════════════╣
║                        ║                           ║                                    ║
║  BOTTOM_DOCK.          ║  stiffness: 150           ║  trigger: parent visible           ║
║  PLAYHEAD              ║  damping:   18            ║  entry: opacity(0) → opacity(1)    ║
║  (scrub indicator)     ║  mass:      0.3           ║  delay: 300ms                      ║
║                        ║  response:  drag-x + rAF  ║  threshold: 0.5                    ║
║                        ║  clamp:     [0, duration] ║                                    ║
║                        ║  on-drag:   snap to beat  ║                                    ║
║                        ║                           ║                                    ║
╠════════════════════════╬═══════════════════════════╬════════════════════════════════════╣
║                        ║                           ║                                    ║
║  BOTTOM_DOCK.          ║  stiffness: 180           ║  trigger: parent visible           ║
║  TRACK_LANES           ║  damping:   20            ║  entry: scaleY(0) → scaleY(1)      ║
║  (TRK1/TRK2/TRK3)     ║  mass:      1.0           ║  delay: 250ms stagger: 60ms/trk    ║
║                        ║  response:  click-cell    ║  threshold: 0.3                    ║
║                        ║  on-toggle: spring-pop    ║  transform-origin: bottom          ║
║                        ║                           ║                                    ║
╚════════════════════════╩═══════════════════════════╩════════════════════════════════════╝
```

### Kinetic Summary

| Feel | Stiffness | Damping | Mass | Example |
|------|-----------|---------|------|---------|
| Snappy (buttons) | 400-500 | 35-40 | 0.4-0.6 | Transport, FFT radio, source select |
| Medium (sliders) | 180-350 | 20-28 | 0.5-0.8 | Gain, filters, biometric sliders |
| Heavy (panels) | 220-260 | 26-28 | 1.2-1.4 | Sidebar containers, bottom dock |
| Feather (playhead) | 150 | 18 | 0.3 | Scrub indicator |

---

## Section 3: Z-STACK & SHADER LEDGER

### Z-Stack — Layer Order & Glass Effects

```
╔═══════════════════════╦════════════╦═══════════════════════════════════════════════════╗
║  LAYER                ║  z-index   ║  backdrop-filter                                  ║
╠═══════════════════════╬════════════╬═══════════════════════════════════════════════════╣
║  TOPBAR               ║  999       ║  blur(20px) saturate(1.8)                         ║
║  BOTTOM_DOCK          ║  80        ║  blur(12px) saturate(1.4)                         ║
║  LEFT_SIDEBAR         ║  50        ║  blur(16px) saturate(1.6)                         ║
║  RIGHT_SIDEBAR        ║  50        ║  blur(16px) saturate(1.6)                         ║
║  WEBGL_VIEWPORT       ║  1         ║  none (raw canvas)                                ║
╠═══════════════════════╩════════════╩═══════════════════════════════════════════════════╣
║  All overlay panels: background rgba(12, 12, 15, 0.72)                                ║
║  Border: 1px solid rgba(255, 255, 255, 0.06)                                          ║
╚══════════════════════════════════════════════════════════════════════════════════════════╝
```

The topbar has the highest z-index (999) so it always stays on top. The sidebars and dock float above the 3D canvas (z:1) with a frosted-glass effect — a CSS `backdrop-filter: blur()` that makes the terrain visible but softly blurred behind each panel. The `saturate` value boosts colors slightly through the glass for visual richness.

### Shader Ledger — GLSL Programs

These are the two GPU programs that generate the 3D terrain visuals. They run on the graphics card at 60 frames per second.

#### Vertex Shader — `terrain_vert.glsl`

The vertex shader runs once per grid point (4,096 times per frame). It reads the current music frequency data and biometric values, then pushes each point up or down to create the terrain shape.

```
╔═════════════════════════════════════════════════════════════════════════════════════╗
║  VERTEX SHADER — terrain_vert.glsl                                                ║
╠═════════════════════════════════════════════════════════════════════════════════════╣
║                                                                                    ║
║  // ── UNIFORMS (values pushed from JavaScript every frame) ──                     ║
║  uniform mat4  u_projection;       // camera lens shape                            ║
║  uniform mat4  u_modelView;        // camera position & rotation                   ║
║  uniform float u_time;             // seconds since start                          ║
║  uniform float u_fftData[64];      // 64 frequency buckets [0..1]                  ║
║  uniform float u_bpm;              // heart rate [40..120]                         ║
║  uniform float u_breath;           // breath rate [8..30]                          ║
║  uniform float u_skin;             // skin conductance [0.1..5.0]                  ║
║  uniform float u_hrv;              // heart rate variability [0..1]                ║
║  uniform float u_waveform;         // 0=sine 1=sawtooth 2=square                   ║
║  uniform float u_heightScale;      // master height multiplier                     ║
║  uniform float u_smoothing;        // FFT smoothing constant                       ║
║                                                                                    ║
║  // ── ATTRIBUTES (per-vertex data from the mesh) ──                               ║
║  attribute vec3 a_position;        // grid vertex XZ position                      ║
║  attribute vec2 a_uv;             // texture coordinate [0..1]                     ║
║                                                                                    ║
║  // ── VARYINGS (passed to fragment shader) ──                                     ║
║  varying float v_height;           // how high this point was pushed               ║
║  varying vec2  v_uv;              // texture coordinate                            ║
║  varying float v_fftIntensity;     // FFT strength at this point                   ║
║                                                                                    ║
║  // ── WAVEFORM FUNCTION ──                                                        ║
║  // Generates different pulse shapes based on selected waveform                    ║
║  float waveShape(float t, float mode) {                                            ║
║      if (mode < 0.5) return sin(t);                    // smooth sine              ║
║      if (mode < 1.5) return fract(t / 6.2832) * 2.0 - 1.0;  // jagged saw         ║
║      return sign(sin(t));                               // hard square             ║
║  }                                                                                 ║
║                                                                                    ║
║  // ── MAIN ──                                                                     ║
║  void main() {                                                                     ║
║      vec3 pos = a_position;                                                        ║
║                                                                                    ║
║      // Map this vertex's X position to one of 64 FFT frequency bins               ║
║      int bin = int(a_uv.x * 63.0);                                                ║
║      float fft = u_fftData[bin];           // [0..1] how loud this freq is         ║
║                                                                                    ║
║      // Create biometric modulation signal                                         ║
║      // - BPM drives the main pulse                                                ║
║      // - Breath adds a slow undulation                                            ║
║      // - HRV adds organic randomness                                              ║
║      float bpmPhase = u_time * (u_bpm / 60.0) * 6.2832;                           ║
║      float breathPhase = u_time * (u_breath / 60.0) * 6.2832;                     ║
║      float bioMod = waveShape(bpmPhase, u_waveform) * 0.3                         ║
║                    + sin(breathPhase) * 0.2                                        ║
║                    + u_hrv * 0.15;                                                 ║
║                                                                                    ║
║      // Final height = FFT loudness * scale * biometric influence                  ║
║      float displacement = fft * u_heightScale * (1.0 + bioMod);                   ║
║                                                                                    ║
║      // Skin conductance adds fine ripples (higher stress = more detail)           ║
║      displacement += sin(a_uv.y * u_skin * 20.0 + u_time * 2.0) * 0.05;          ║
║                                                                                    ║
║      pos.y = displacement;                                                         ║
║                                                                                    ║
║      v_height = displacement;                                                      ║
║      v_uv = a_uv;                                                                  ║
║      v_fftIntensity = fft;                                                         ║
║                                                                                    ║
║      gl_Position = u_projection * u_modelView * vec4(pos, 1.0);                   ║
║  }                                                                                 ║
╚═════════════════════════════════════════════════════════════════════════════════════╝
```

#### Fragment Shader — `terrain_frag.glsl`

The fragment shader runs once per visible pixel. It colors each pixel based on how high the terrain is at that point, adds beat-synced red flashes, draws wireframe grid lines, and fades edges into darkness.

```
╔═════════════════════════════════════════════════════════════════════════════════════╗
║  FRAGMENT SHADER — terrain_frag.glsl                                              ║
╠═════════════════════════════════════════════════════════════════════════════════════╣
║                                                                                    ║
║  uniform float u_time;                                                             ║
║  uniform float u_bpm;                                                              ║
║  uniform float u_skin;                                                             ║
║                                                                                    ║
║  varying float v_height;                                                           ║
║  varying vec2  v_uv;                                                               ║
║  varying float v_fftIntensity;                                                     ║
║                                                                                    ║
║  // ── COLOR PALETTE ──                                                            ║
║  //  Height-mapped gradient (quiet to loud):                                       ║
║  //    low  → deep blue   #0A1450  (valleys / silence)                             ║
║  //    mid  → cyan        #00DCFF  (moderate activity)                             ║
║  //    high → hot white   #FFF0E6  (loud peaks)                                    ║
║  //    peak → pulse red   #FF3232  (beat-synced flash on strongest hits)           ║
║                                                                                    ║
║  vec3 heightColor(float h) {                                                       ║
║      vec3 deep = vec3(0.04, 0.08, 0.31);      // dark blue                        ║
║      vec3 mid  = vec3(0.0, 0.86, 1.0);         // bright cyan                     ║
║      vec3 hot  = vec3(1.0, 0.94, 0.90);        // white-hot                       ║
║      float t = clamp(h, 0.0, 1.0);                                                ║
║      if (t < 0.5) return mix(deep, mid, t * 2.0);                                 ║
║      return mix(mid, hot, (t - 0.5) * 2.0);                                       ║
║  }                                                                                 ║
║                                                                                    ║
║  void main() {                                                                     ║
║      vec3 color = heightColor(v_height);                                           ║
║                                                                                    ║
║      // BPM-synced pulse: red flash on the loudest peaks, timed to heartbeat       ║
║      float pulse = pow(sin(u_time * (u_bpm/60.0) * 3.14159) * 0.5 + 0.5, 4.0);   ║
║      vec3 peakFlash = vec3(1.0, 0.2, 0.2) * pulse * step(0.7, v_fftIntensity);    ║
║      color += peakFlash;                                                           ║
║                                                                                    ║
║      // Wireframe grid lines (skin conductance controls density)                   ║
║      // Higher stress → more grid lines → busier visual texture                    ║
║      float gridFreq = 32.0 + u_skin * 16.0;                                       ║
║      float lineX = smoothstep(0.02, 0.0, fract(v_uv.x * gridFreq));               ║
║      float lineY = smoothstep(0.02, 0.0, fract(v_uv.y * gridFreq));               ║
║      float grid = max(lineX, lineY) * 0.3;                                        ║
║      color += vec3(grid) * vec3(0.2, 0.8, 1.0);                                   ║
║                                                                                    ║
║      // Fog: fade edges to near-black for depth                                    ║
║      float fog = smoothstep(0.8, 1.0, length(v_uv - 0.5) * 2.0);                 ║
║      color = mix(color, vec3(0.02, 0.02, 0.05), fog);                              ║
║                                                                                    ║
║      gl_FragColor = vec4(color, 1.0);                                              ║
║  }                                                                                 ║
╚═════════════════════════════════════════════════════════════════════════════════════╝
```

#### Geometry Specification

| Property | Value | Meaning |
|----------|-------|---------|
| Mesh type | Plane, 64x64 segments | A flat grid subdivided into 4,096 points |
| Triangle count | 8,192 | Each grid square = 2 triangles |
| World extent | X: [-2, 2], Z: [-2, 2] | 4 units wide and deep |
| Y range | 0 to dynamic | Flat at rest, peaks driven by audio |
| Draw mode | TRIANGLES + LINES overlay | Solid terrain with wireframe on top |
| Camera | Perspective 60 FOV, orbit r=3.0, elevation 35 deg | Angled top-down view, slowly auto-rotating |
| Auto-rotate | 0.1 rad/s with drag-to-orbit | Spins slowly; user can grab and rotate |

---

## Section 4: MULTIMODAL I/O CONTRACT — Data Transformation Pipeline

This section defines exactly how sound goes from your microphone (or a file) through the browser's audio processing, gets analyzed into frequency data, and ends up as numbers that the GPU uses to shape the terrain — all 60 times per second.

### Stage 1: Capture — Getting the Audio

```
╔═════════════════════════════════════════════════════════════════════════════════════╗
║  STAGE 1: CAPTURE                                                                  ║
║                                                                                    ║
║  Three possible audio sources (selected via SRC_SEL radio buttons):                ║
║                                                                                    ║
║  ● Mic  → navigator.mediaDevices.getUserMedia({ audio: true, video: false })       ║
║           Browser asks permission, then streams live microphone input               ║
║                                                                                    ║
║  ● File → new Audio("file.mp3")                                                   ║
║           User selects a local audio file to play                                  ║
║                                                                                    ║
║  ● Osc  → OscillatorNode                                                          ║
║           Browser generates a test tone (useful for testing/demos)                 ║
║                                                                                    ║
║  OUTPUT: MediaStream (a live stream of audio data)                                 ║
╚═════════════════════════════════════════════════════════════════════════════════════╝
```

### Stage 2: Audio Processing Graph — Shaping the Sound

```
╔═════════════════════════════════════════════════════════════════════════════════════╗
║  STAGE 2: AUDIO CONTEXT GRAPH                                                      ║
║                                                                                    ║
║  const ctx = new AudioContext({ sampleRate: 44100 });                               ║
║                                                                                    ║
║  The audio flows through a chain of processing nodes:                              ║
║                                                                                    ║
║  MediaStream                                                                       ║
║       │                                                                            ║
║       ▼                                                                            ║
║  ┌──────────────────────┐                                                          ║
║  │ MediaStreamSourceNode│  Converts the raw stream into something                  ║
║  │                      │  the audio graph can work with                            ║
║  └──────────┬───────────┘                                                          ║
║             │                                                                      ║
║             ▼                                                                      ║
║  ┌──────────────────────┐                                                          ║
║  │ GainNode             │  Volume control                                          ║
║  │                      │  Maps GAIN_SLIDER dB to linear:                          ║
║  │                      │  gain.value = Math.pow(10, dB / 20)                      ║
║  │                      │  Range: -48 dB (nearly silent) to 0 dB (full volume)     ║
║  └──────────┬───────────┘                                                          ║
║             │                                                                      ║
║             ▼                                                                      ║
║  ┌──────────────────────┐                                                          ║
║  │ BiquadFilterNode     │  High-pass filter (Lo Cut)                               ║
║  │ type: "highpass"     │  Removes frequencies BELOW the cutoff                    ║
║  │                      │  LO_CUT slider: 20 Hz to 800 Hz                          ║
║  │                      │  Example: set to 80 Hz to remove room rumble             ║
║  └──────────┬───────────┘                                                          ║
║             │                                                                      ║
║             ▼                                                                      ║
║  ┌──────────────────────┐                                                          ║
║  │ BiquadFilterNode     │  Low-pass filter (Hi Cut)                                ║
║  │ type: "lowpass"      │  Removes frequencies ABOVE the cutoff                    ║
║  │                      │  HI_CUT slider: 1,000 Hz to 20,000 Hz                   ║
║  │                      │  Example: set to 2 kHz to focus on bass + mids only      ║
║  └──────────┬───────────┘                                                          ║
║             │                                                                      ║
║             ▼                                                                      ║
║  ┌──────────────────────┐                                                          ║
║  │ AnalyserNode         │  The frequency analyzer                                  ║
║  │                      │  fftSize: 256 | 512 | 1024 | 2048 | 4096                ║
║  │                      │  (larger = more detail but slower)                       ║
║  │                      │  smoothingTimeConstant: 0 to 0.99                        ║
║  │                      │  (higher = smoother/slower reaction)                     ║
║  │                      │  frequencyBinCount: fftSize / 2                          ║
║  └──────────┬───────────┘                                                          ║
║             │                                                                      ║
║             │  NOTE: AnalyserNode is a "tap" — it reads the audio                  ║
║             │  without sending it to speakers (silent analysis)                     ║
╚═════════════╧══════════════════════════════════════════════════════════════════════╝
```

### Stage 3: FFT Extraction — Breaking Sound into Frequencies

```
╔═════════════════════════════════════════════════════════════════════════════════════╗
║  STAGE 3: FFT EXTRACTION (runs every frame — 60 times per second)                  ║
║                                                                                    ║
║  // Get raw frequency data as integers 0-255                                       ║
║  const raw = new Uint8Array(analyser.frequencyBinCount);                           ║
║  analyser.getByteFrequencyData(raw);                                               ║
║                                                                                    ║
║  // Take the first 64 bins (the low-to-mid frequency range)                        ║
║  // At 44100 Hz sample rate with fftSize 1024:                                     ║
║  //   Each bin covers ~43 Hz                                                       ║
║  //   64 bins = 0 Hz to ~2,752 Hz                                                  ║
║  //   This covers bass, kick drums, vocals, guitar fundamentals                    ║
║  //                                                                                ║
║  // Why only 64? The terrain grid is 64 vertices wide, so each                     ║
║  // vertex column maps to exactly one frequency bin.                                ║
║                                                                                    ║
║  const fftSlice = new Float32Array(64);                                            ║
║  for (let i = 0; i < 64; i++) {                                                    ║
║      fftSlice[i] = raw[i] / 255.0;    // normalize to [0..1]                       ║
║  }                                                                                 ║
║                                                                                    ║
║  OUTPUT: Float32Array of 64 values, each between 0.0 (silent) and 1.0 (max)       ║
╚═════════════════════════════════════════════════════════════════════════════════════╝
```

### Stage 4: Biometric Merge — Combining Audio with Body Signals

```
╔═════════════════════════════════════════════════════════════════════════════════════╗
║  STAGE 4: BIOMETRIC MERGE (runs every frame)                                       ║
║                                                                                    ║
║  // Read current slider values from the right sidebar                              ║
║  const bio = {                                                                     ║
║      bpm:    BPM_SLIDER.value,         // heart rate, 40 to 120                    ║
║      hrv:    HRV_SLIDER.value,         // variability, 0 to 1                      ║
║      breath: BREATH_RATE.value,        // breaths per minute, 8 to 30              ║
║      skin:   SKIN_COND.value,          // skin conductance, 0.1 to 5.0             ║
║  };                                                                                ║
║                                                                                    ║
║  // Read waveform selection (affects pulse shape)                                  ║
║  const waveform = WAVE_MOD.selected;   // 0 = sine, 1 = saw, 2 = square           ║
║                                                                                    ║
║  // Derive height scale from audio gain                                            ║
║  const heightScale = gain.gain.value * 2.0;   // range [0..2]                      ║
║                                                                                    ║
║  // All these values are now ready to send to the GPU                              ║
╚═════════════════════════════════════════════════════════════════════════════════════╝
```

### Stage 5: Uniform Injection — Sending Data to the GPU

```
╔═════════════════════════════════════════════════════════════════════════════════════╗
║  STAGE 5: UNIFORM INJECTION (runs every frame inside requestAnimationFrame)        ║
║                                                                                    ║
║  // "Uniforms" are variables sent from JavaScript to the GPU shaders               ║
║  // They're called "uniform" because every vertex/pixel sees the same value        ║
║                                                                                    ║
║  gl.uniform1fv(loc.u_fftData,     fftSlice);      // 64 frequency values          ║
║  gl.uniform1f (loc.u_time,        elapsed);        // seconds since start          ║
║  gl.uniform1f (loc.u_bpm,         bio.bpm);        // heart rate                   ║
║  gl.uniform1f (loc.u_hrv,         bio.hrv);        // heart variability            ║
║  gl.uniform1f (loc.u_breath,      bio.breath);     // breathing rate               ║
║  gl.uniform1f (loc.u_skin,        bio.skin);       // skin conductance             ║
║  gl.uniform1f (loc.u_waveform,    waveform);       // pulse shape                  ║
║  gl.uniform1f (loc.u_heightScale, heightScale);    // terrain amplitude            ║
║  gl.uniform1f (loc.u_smoothing,   smoothing);      // reaction smoothness          ║
║                                                                                    ║
║  // Draw the terrain                                                               ║
║  gl.drawElements(gl.TRIANGLES, indexCount, gl.UNSIGNED_SHORT, 0);                  ║
╚═════════════════════════════════════════════════════════════════════════════════════╝
```

### Full Pipeline — Single Frame Timing

```
╔═════════════════════════════════════════════════════════════════════════════════════╗
║  FULL PIPELINE — WHAT HAPPENS IN ONE FRAME (16.6 ms budget at 60fps)               ║
║                                                                                    ║
║  ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐      ║
║  │getUserMe-│    │AudioCtx  │    │getByteF- │    │bio merge │    │gl.uniform│      ║
║  │dia       │───▶│graph     │───▶│reqData   │───▶│+ normalize───▶│+ drawEl  │      ║
║  │(once)    │    │(once)    │    │(per frame│    │(per frame│    │(per frame│      ║
║  └──────────┘    └──────────┘    └──────────┘    └──────────┘    └──────────┘      ║
║                                                                                    ║
║  Timing breakdown per frame:                                                       ║
║  ┌─────────────────────────┬───────────┐                                           ║
║  │ FFT read                │  ~0.1 ms  │                                           ║
║  │ Normalize + bio merge   │  ~0.05 ms │                                           ║
║  │ Set uniforms            │  ~0.02 ms │                                           ║
║  │ GPU draw call           │  ~2-4 ms  │  (8,192 triangles, simple shader)         ║
║  │ ─────────────────────── │ ───────── │                                           ║
║  │ Total                   │  ~2-4 ms  │                                           ║
║  │ Headroom remaining      │  ~12 ms   │  (plenty of room for 60fps)               ║
║  └─────────────────────────┴───────────┘                                           ║
╚═════════════════════════════════════════════════════════════════════════════════════╝
```

### Sequencer Sync Contract — How the Timeline Controls the Pipeline

```
╔═════════════════════════════════════════════════════════════════════════════════════╗
║  SEQUENCER ↔ PIPELINE SYNC CONTRACT                                                ║
║                                                                                    ║
║  Transport button actions:                                                         ║
║  ┌──────────────────────────────────────────────────────────────────────────────┐   ║
║  │  PLAY  → resume audio context + start render loop                           │   ║
║  │  STOP  → suspend audio context + stop render loop (saves CPU/GPU)           │   ║
║  │  LOOP  → when playhead reaches end, reset to beginning automatically        │   ║
║  │  BPM   → if TEMPO_MAP is "linked", BPM slider drives sequencer tempo too    │   ║
║  └──────────────────────────────────────────────────────────────────────────────┘   ║
║                                                                                    ║
║  Track lane mapping (what each sequencer track controls):                          ║
║  ┌──────────────────────────────────────────────────────────────────────────────┐   ║
║  │  TRK1 (FFT→Hght)  │ Active cells multiply terrain height by cell's gain    │   ║
║  │                    │ Dark cells = normal height, bright cells = boosted      │   ║
║  │                    │                                                         │   ║
║  │  TRK2 (BPM→Spd)   │ Active cells override BPM at that beat position        │   ║
║  │                    │ Allows tempo changes throughout the timeline            │   ║
║  │                    │                                                         │   ║
║  │  TRK3 (Skin→Clr)  │ Active cells override skin conductance at that beat    │   ║
║  │                    │ Controls color intensity and grid density over time     │   ║
║  └──────────────────────────────────────────────────────────────────────────────┘   ║
║                                                                                    ║
║  Beat resolution: 16th notes at current BPM                                        ║
║  Playhead advance: (BPM / 60) * (1/4) beats per second                             ║
╚═════════════════════════════════════════════════════════════════════════════════════╝
```

---

## Glossary

| Term | Plain Meaning |
|------|---------------|
| **FFT** (Fast Fourier Transform) | Math that splits a sound wave into individual frequencies — tells you how much bass, midrange, and treble exist at any instant |
| **Shader** | A tiny program that runs on the GPU (graphics card) instead of the CPU, enabling real-time 3D graphics |
| **Vertex shader** | Decides *where* each 3D point goes (the terrain shape) |
| **Fragment shader** | Decides *what color* each pixel is |
| **Uniform** | A value sent from JavaScript to a shader — "uniform" because every vertex/pixel sees the same value that frame |
| **AnalyserNode** | A built-in browser audio tool that reads frequency data without producing sound |
| **AudioContext** | The browser's audio processing engine — you build a chain of nodes (volume, filters, analyzer) |
| **Intersection Observer** | A browser API that fires a callback when an element scrolls into or out of the visible area |
| **Spring physics** | Animation style where elements overshoot their target and bounce back, like a physical spring |
| **backdrop-filter** | CSS property that applies a blur/saturation effect to everything *behind* an element (frosted glass look) |
| **z-index** | CSS stacking order — higher numbers appear in front of lower numbers |
| **rAF** (requestAnimationFrame) | Browser function that calls your code exactly once per screen refresh (~60 times/second) |
| **BPM** | Beats per minute — heart rate or musical tempo |
| **HRV** | Heart Rate Variability — how irregular the spacing between heartbeats is (more variability = more relaxed) |
| **Skin conductance** | How well skin conducts electricity — increases with sweat/stress/arousal |
| **Heightmap** | A 2D grid where each cell's value represents height — like a topographic map that becomes 3D geometry |
