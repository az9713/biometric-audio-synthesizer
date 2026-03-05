# BIOVIZ — Biometric Audio-Reactive WebGL Synthesizer

A real-time 3D terrain visualizer that dances to music and simulated biometric signals. A 64x64 vertex heightmap mesh is displaced by FFT frequency data, modulated by heart rate, breathing, and skin conductance — all rendered in the browser with raw WebGL and GLSL shaders.

https://github.com/user-attachments/assets/PLACEHOLDER-REPLACE-WITH-DEMO-VIDEO-URL

> **Demo video placeholder** — will be replaced with the actual GitHub-hosted video URL via issue.

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
cd bioviz
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
claude_code_build_mark_kashef/
  bioviz/
    index.html          # App layout — topbar, sidebars, canvas, sequencer
    style.css           # Glassmorphism panels, spring animations, sequencer grid
    main.js             # WebGL terrain, GLSL shaders, Web Audio API, UI bindings
  docs/
    gemini3.1_proposal.md   # Original idea from Gemini 3.1
    demo.mp4                # Demo video (placeholder)
  biometric-audio-synth-design.md   # Full ASCII DSL design document
  README.md
```

## Design Document

The full architecture is documented in [`biometric-audio-synth-design.md`](biometric-audio-synth-design.md), which contains:

1. **Spatial Grid** — ASCII wireframe of the complete UI topology
2. **Kinetic Ledger** — Spring physics (stiffness, damping, mass) and intersection observer triggers for every interactive element
3. **Z-Stack & Shader Ledger** — GLSL vertex and fragment shader code, z-index layering, backdrop-filter blur radii
4. **Multimodal I/O Contract** — Complete data pipeline from `getUserMedia` through `AudioContext` to GPU uniforms
5. **Glossary** — Plain-language definitions of every technical term

---

## Acknowledgments

This project exists because of the generosity, creativity, and brilliance of many people and tools. We are deeply grateful to every one of them:

**Mark Kashef** — For the insight that changed how we think about building with AI. Your video ["Every Claude Code Build Should Start Like This"](https://www.youtube.com/watch?v=3qUg57KGSVY) introduced the ASCII-first design methodology that became the foundation of this project. The idea that a simple text wireframe can serve as a rigorous specification — saving tokens, reducing ambiguity, and producing better results — is both elegant and powerful. Thank you for sharing it with the community.

**Google Gemini 3.1** — For the original creative spark. The proposal to extend ASCII wireframing from dashboards into a biometric audio synthesizer was imaginative and ambitious. It pushed the methodology into uncharted territory — real-time WebGL, GLSL shaders, Web Audio API pipelines — and proved that the approach scales far beyond its original scope. Thank you for dreaming big.

**Anthropic and Claude Code (Opus 4.6)** — For the implementation engine that turned a design document into a working application. From architecting the four-section ASCII DSL to writing GLSL shaders, building the Web Audio pipeline, implementing spring physics animations, and debugging WebGL texture sampling — all in a single session. The depth of capability is remarkable. Thank you for building tools that make ambitious projects accessible.

**STAROSTIN** — For the wonderful ["Comedy Cartoon Funny Background Music"](https://pixabay.com/music/comedy-cartoon-funny-background-music-492540/) used in the demo video. Your music brought the terrain to life and made the demo a joy to watch. Thank you for sharing your art freely on Pixabay.

**Pixabay** — For providing a platform where creators share high-quality music and media under generous licenses, making projects like this possible without legal friction. Thank you for fostering creative collaboration.

**The Web Standards Community** — For WebGL, Web Audio API, the `AnalyserNode`, `requestAnimationFrame`, CSS `backdrop-filter`, and the Intersection Observer API. Every piece of this application is built on open web standards that work in any modern browser, with no dependencies or build tools. The open web is a gift. Thank you to everyone who designs, implements, and maintains these specifications.

**The Open Source Community** — For Python's `http.server` (which serves this app with zero configuration), for browsers that run GLSL shaders at 60fps, and for the countless tools and libraries that make modern development possible. Thank you.

**You, the reader** — For taking the time to explore this project. Whether you're here to learn about ASCII-first design, WebGL terrain rendering, Web Audio pipelines, or just to watch a 3D landscape dance to music — thank you. We hope it inspires you to build something wonderful.

---

*Built with care, curiosity, and gratitude.*
