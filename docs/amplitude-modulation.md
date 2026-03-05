# Amplitude Modulation in the Biometric Audio-Reactive Synthesizer

This document explains how the vertex shader uses amplitude modulation (AM) to
blend real-time FFT audio data with biometric signals, producing the animated
terrain visualization at the heart of the application.

---

## Overview

The core displacement equation lives in `main.js` lines 47-48 inside the vertex
shader (`VERT_SRC`):

```glsl
float displacement = fft * u_heightScale * (1.0 + bioMod);
displacement += sin(a_uv.y * u_skin * 20.0 + u_time * 2.0) * 0.05;
```

Each vertex in the 64x64 terrain grid has its Y position (height) set by this
formula every frame. The result is a landscape that reflects both the frequency
content of the audio and the physiological state of the user.

The formula decomposes into three parts:

| Term | Role | Type |
|------|------|------|
| `fft * u_heightScale` | Spectral content (carrier) | Per-vertex |
| `(1.0 + bioMod)` | Biometric envelope (modulator) | Global |
| `sin(...)` additive term | Skin-conductance ripple | Per-vertex, additive |

---

## 1. The Carrier Signal: FFT

```glsl
float fft = texture2D(u_fftTex, vec2(a_uv.x, 0.5)).r;   // line 39
```

Each frame, JavaScript extracts 64 frequency bins from the Web Audio
`AnalyserNode` and uploads them as a 64x1 luminance texture (`main.js`
lines 214-227, 361-369). In the vertex shader, `a_uv.x` maps each column of
the terrain grid to a frequency bin, so the value `fft` is in [0, 1] and
represents the magnitude of that bin.

When no live audio source is connected, a procedural demo generator
(`generateDemoFFT`, lines 229-237) synthesizes plausible data so the terrain
still animates.

---

## 2. The Modulator Signal: Biometric Composite

The biometric modulator (`bioMod`) is computed at lines 41-45:

```glsl
float bpmPhase   = u_time * (u_bpm / 60.0) * 6.2832;
float breathPhase = u_time * (u_breath / 60.0) * 6.2832;

float bioMod = waveShape(bpmPhase, u_waveform) * 0.3
             + sin(breathPhase) * 0.2
             + u_hrv * 0.15;
```

It is the sum of three independent biometric components:

### 2.1 Heart-Rate Component

```
waveShape(bpmPhase, u_waveform) * 0.3
```

- **Frequency**: `u_bpm / 60` Hz. At the default 72 BPM this is 1.2 Hz.
- **Range**: [-0.3, +0.3].
- **Wave shape**: Determined by the `u_waveform` uniform (set via the "Wave
  Mod" radio buttons in the right sidebar).

The `waveShape` function (lines 29-33) selects the modulation character:

| Mode | Shape | Visual Effect |
|------|-------|---------------|
| 0 (Sin) | `sin(t)` | Smooth, organic pulsing; gradual rise and fall |
| 1 (Saw) | `fract(t / 2π) * 2 - 1` | Slow ramp up then sharp drop, mimicking the systolic/diastolic pressure curve of a heartbeat |
| 2 (Sqr) | `sign(sin(t))` | Hard binary switching between two height levels, creating a rhythmic gating effect |

### 2.2 Breath-Rate Component

```
sin(breathPhase) * 0.2
```

- **Frequency**: `u_breath / 60` Hz. At the default 15 breaths/min this is
  0.25 Hz (one full cycle every 4 seconds).
- **Range**: [-0.2, +0.2].
- Always a pure sine wave — breathing is naturally sinusoidal.

### 2.3 Heart-Rate Variability (HRV) Component

```
u_hrv * 0.15
```

- **Range**: [0, +0.15] (the HRV slider maps 0-100 to 0.0-1.0).
- This is a DC (constant) offset — it does not oscillate. It raises the
  baseline of the modulator, making the terrain globally taller when HRV is
  high.

### 2.4 Combined Modulator Range

Summing the three components:

| | Minimum | Maximum |
|---|---------|---------|
| BPM | -0.30 | +0.30 |
| Breath | -0.20 | +0.20 |
| HRV | 0.00 | +0.15 |
| **bioMod** | **-0.50** | **+0.65** |

---

## 3. The 1.0 Offset: Why It Matters

The multiplication factor applied to the carrier is `(1.0 + bioMod)`, not
`bioMod` alone. This DC offset shifts the modulator from [-0.50, +0.65] to
[0.50, 1.65].

Without the offset, negative `bioMod` values would invert the terrain — peaks
would become valleys. The `1.0 +` ensures the modulator acts as a **scaling
envelope** rather than a sign-flipping ring modulator. The terrain breathes
between approximately 50% and 165% of the raw FFT height, but never flips
upside down.

---

## 4. The Multiplication: Classic Amplitude Modulation

```glsl
float displacement = fft * u_heightScale * (1.0 + bioMod);
```

In signal-processing terms, this is `output = carrier × modulator`:

- **The modulator is global**: Every frequency bin receives the same multiplier
  in a given frame. The spectral *shape* is preserved — if bin 5 is louder than
  bin 30, it stays louder regardless of biometric state. Only the overall
  *magnitude* changes.
- **The modulator is slow**: At 72 BPM the heart component is 1.2 Hz; at 15
  breaths/min the breath component is 0.25 Hz. Both are far below the 60 Hz
  frame rate, so the modulation appears as smooth terrain "breathing" rather
  than flickering.
- **The modulator is quasi-periodic**: Because the BPM and breath components
  oscillate at incommensurate frequencies (e.g., 1.2 Hz vs 0.25 Hz), their
  sum produces a beating pattern that never exactly repeats, yielding organic,
  non-mechanical motion.

---

## 5. Skin-Conductance Ripple (Additive, Not AM)

```glsl
displacement += sin(a_uv.y * u_skin * 20.0 + u_time * 2.0) * 0.05;
```

This is **not** amplitude modulation — it is an **additive** signal layered on
top of the AM result:

- `a_uv.y * u_skin * 20.0`: A spatial sine wave along the terrain's Z-axis.
  `u_skin` (slider range 0.1-5.0) controls the spatial frequency, producing
  2-100 ripple cycles across the terrain.
- `u_time * 2.0`: The wave travels forward at a constant 2 rad/s, creating a
  scrolling ripple effect.
- `* 0.05`: The amplitude is fixed and small, ensuring the ripple remains a
  subtle surface texture rather than a dominant feature.

This term is independent of the FFT signal — it adds micro-detail even where
the FFT value is zero, simulating electrodermal surface texture.

---

## 6. Sequencer Interaction

The sequencer in the bottom dock can further scale the AM parameters on a
per-beat basis (`main.js` lines 423-431):

```js
if (state.sequencer[0][cellIdx]) seqHeightMul = 1.5;   // Track 1: FFT → Height
if (state.sequencer[1][cellIdx]) seqBpmMul   = 1.3;   // Track 2: BPM → Speed
if (state.sequencer[2][cellIdx]) seqSkinMul  = 1.5;   // Track 3: Skin → Color
```

These multipliers are applied before the uniforms are sent to the shader
(lines 473-478). Track 1 scales `u_heightScale` by 1.5× on active beats,
causing rhythmic height accents. Track 2 scales `u_bpm` by 1.3×, increasing
the heart-rate modulation frequency and creating a tempo-synced pulsing effect.

---

## 7. Complete Displacement Model

Putting it all together, each vertex's height per frame is:

```
height = (fft_bin × heightScale × (1.0 + bioMod)) + skin_ripple
              │            │              │                │
         spectral     user gain     slow biometric    additive
         content      + sequencer   AM envelope       detail
```

The biometrics never reshape the frequency spectrum — they modulate the entire
terrain's magnitude with the heartbeat and breathing cycle, while skin
conductance adds a fine-grained traveling wave on top.

---

## 8. Fragment Shader Reinforcement

The fragment shader (`FRAG_SRC`, lines 60-98) reinforces the AM effect
visually:

- **Height-based coloring** (`heightColor`, lines 71-78): Vertices displaced
  higher by the AM envelope shift from deep blue through cyan to warm white,
  so biometric modulation directly affects the color palette.
- **BPM peak flash** (line 83-85): A red flash on high-FFT vertices pulsed at
  the BPM rate. This is a second, visual-only AM applied in color space.
- **Skin-conductance grid** (lines 87-91): Grid line density scales with
  `u_skin`, tying the wireframe overlay density to electrodermal activity.
