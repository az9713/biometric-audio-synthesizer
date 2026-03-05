# Biometric Audio-Reactive WebGL Synthesizer

A real-time 3D terrain visualizer that dances to music and simulated biometric signals. A 64x64 vertex heightmap mesh is displaced by FFT frequency data, modulated by heart rate, breathing, and skin conductance — all rendered in the browser with raw WebGL and GLSL shaders.

https://github.com/user-attachments/assets/2ceb1554-931f-45cf-8a78-7f42befb7671

### Original ASCII Wireframe (from Gemini 3.1)

The design started as this ASCII specification — compare it with the final application above:

```
====================================================================
                        SPATIAL GRID (Z-INDEX MAP)
====================================================================
[z:50] ┌─────────────────┐ [z:10] <WebGL_Viewport>  ┌─────────────────┐ [z:50]
       │ AUDIO <Stream>  │                          │ BIOMETRIC       │
       │ ├─ Mic Input    │      /\      /\          │ <Stream>        │
       │ ├─ Gain: 0.8    │     /  \____/  \         │ ├─ BPM: 120     │
       │ ├─ LowPass: On  │    |   CORE     |        │ ├─ Sync: [Kin]  │
       │ └─ [Kinetic_1]  │     \  /    \  /         │ └─ [Kinetic_2]  │
       └─────────────────┘      \/      \/          └─────────────────┘
             |                                              |
[z:100] ┌────┴──────────────────────────────────────────────┴────┐
        │ <Kinetic_Sequencer> [ > ] Play   [ || ] Pause          │
        └────────────────────────────────────────────────────────┘

====================================================================
                        KINETIC LEDGER
====================================================================
[Kinetic_1] HoverState: { scale: 1.05, transition: { type: "spring", stiffness: 400, damping: 10 } }
[Kinetic_2] ToggleState: { backgroundColor: "#FF3366", transition: { ease: [0.32, 0.72, 0, 1], duration: 0.6 } }
<Kinetic_Sequencer> Entry: { y: 100 -> 0, opacity: 0 -> 1, type: "spring", mass: 1.2 }

====================================================================
                    Z-STACK & SHADER LEDGER
====================================================================
Layer 10 (Base): R3F Canvas.
-> Vertex Shader: `position += normal * (u_audioLowFreq * 2.0) * sin(time);`
-> Fragment Shader: `gl_FragColor = vec4(u_bpmPulse, u_audioHighFreq, 1.0, 1.0);`
Layer 50 (Sidebars): CSS `backdrop-filter: blur(24px) saturate(150%);` background `rgba(10,10,10,0.4)`.

====================================================================
                    MULTIMODAL I/O CONTRACT
====================================================================
1. Web Audio API requested via `navigator.mediaDevices.getUserMedia({ audio: true })`.
2. Stream piped to `AudioContext.createMediaStreamSource()`.
3. Routed to `AnalyserNode` (fftSize: 1024).
4. `requestAnimationFrame` loop extracts `getByteFrequencyData` into `Uint8Array`.
5. Low-frequency bins (0-10) averaged and normalized (0.0 - 1.0).
6. Value bound to R3F `useFrame` hook and injected into shader uniform `u_audioLowFreq`.
```

---

## Inspiration

This project was inspired by Mark Kashef's YouTube video **["Every Claude Code Build Should Start Like This"](https://www.youtube.com/watch?v=3qUg57KGSVY)**, which demonstrates an ASCII-first design methodology — using ASCII wireframes as the specification before writing any code. The video shows this approach applied to SaaS dashboards, landing pages, slide decks, and ER diagrams.

**We extended this idea beyond simple dashboards and landing pages into multimodal, real-time applications** — proving that ASCII wireframes can serve as rigorous design specifications even for complex systems involving WebGL shaders, Web Audio API pipelines, spring physics animations, and GPU uniform injection.

## Origin Story

1. **The original idea came from Gemini 3.1** ([docs/gemini3.1_proposal.md](docs/gemini3.1_proposal.md)), which proposed a biometric audio synthesizer and suggested using an annotated ASCII wireframe as the design specification — applying the wireframe-first methodology from the YouTube video to a far more ambitious, multimodal application.

2. **Claude Code powered by Opus 4.6** took the proposal and implemented the full design — from the four-section ASCII DSL architecture (Spatial Grid, Kinetic Ledger, Shader Ledger, Multimodal I/O Contract) to the working WebGL application with all controls, shaders, and audio pipeline functional.

## Demo

The demo video ([docs/demo.mp4](docs/demo.mp4)) features music by **STAROSTIN** — ["Comedy Cartoon Funny Background Music"](https://pixabay.com/music/comedy-cartoon-funny-background-music-492540/) from Pixabay.

---

## Quick Start

### 1. Serve the app

No build tools, no dependencies. Just a static file server:

```bash
python -m http.server 3001
```

Then open **http://localhost:3001** in your browser.

### 2. Choose an audio source

The app supports three audio input modes:

#### Option A: Audio File (recommended for demos)

- Click **Choose File** in the left sidebar
- Select any audio file from your computer (mp3, wav, ogg, m4a, flac — any format your browser supports)
- Click **PLAY** in the bottom transport bar
- You'll hear the music and see the terrain react to it in real-time

#### Option B: Microphone (live input)

- Click **Mic** in the source selector
- Allow the browser microphone permission when prompted
- Play music from your speakers, sing, clap, or talk — the terrain reacts to any live sound
- Note: no audio is sent anywhere — all processing happens locally in the browser

#### Option C: Oscillator (test tone)

- Click **Osc** in the source selector
- A 220 Hz sine wave test tone is generated
- Useful for verifying the audio pipeline and shader response are working
- The terrain will show a steady, rhythmic displacement pattern

#### No audio source? No problem.

The app starts in **demo mode** automatically — it generates synthetic FFT data that simulates music, so the terrain animates immediately without any audio input. Just open the page and watch.

### 3. Play with the controls

| Control | What it does |
|---------|-------------|
| **Gain** (-48 to 0 dB) | Controls terrain height amplitude |
| **Lo Cut / Hi Cut** | Filters which frequencies reach the terrain |
| **FFT Size** | More bins = finer frequency detail, fewer = faster response |
| **Smoothing** | Higher = smoother terrain movement, lower = more reactive |
| **BPM** (40-120) | Simulated heart rate — drives the pulsing rhythm |
| **HRV** | Heart rate variability — adds organic randomness |
| **Breath Rate** (8-30) | Creates slow wave-like undulations |
| **Skin Conductance** | Higher = more wireframe grid detail and visual complexity |
| **Wave Mod** (Sin/Saw/Sqr) | Changes the shape of the biometric pulse |
| **Sequencer tracks** | Click cells to toggle — modulates height, speed, and color over time |

---

## Project Structure

```
biometric-audio-synthesizer/
  index.html              # App layout — topbar, sidebars, canvas, sequencer
  style.css               # Glassmorphism panels, spring animations, sequencer grid
  main.js                 # WebGL terrain, GLSL shaders, Web Audio API, UI bindings
  docs/
    gemini3.1_proposal.md             # Original idea from Gemini 3.1
    biometric-audio-synth-design.md   # Full ASCII DSL design document
    demo_compressed.mp4               # Demo video
  README.md
```

## Design Document

The full architecture is documented in [`docs/biometric-audio-synth-design.md`](docs/biometric-audio-synth-design.md), which contains:

1. **Spatial Grid** — ASCII wireframe of the complete UI topology
2. **Kinetic Ledger** — Spring physics (stiffness, damping, mass) and intersection observer triggers for every interactive element
3. **Z-Stack & Shader Ledger** — GLSL vertex and fragment shader code, z-index layering, backdrop-filter blur radii
4. **Multimodal I/O Contract** — Complete data pipeline from `getUserMedia` through `AudioContext` to GPU uniforms
5. **Glossary** — Plain-language definitions of every technical term

---

## Acknowledgments

- **[Mark Kashef](https://www.youtube.com/watch?v=3qUg57KGSVY)** — for the ASCII-first design methodology that inspired this project
- **STAROSTIN** — for the fun ["Comedy Cartoon Funny Background Music"](https://pixabay.com/music/comedy-cartoon-funny-background-music-492540/) used in the demo
- **Google Gemini 3.1** — for the creative idea of applying ASCII art design to a multimodal application
- **Claude Code (Opus 4.6)** — for the implementation, shaders, audio pipeline, and documentation
