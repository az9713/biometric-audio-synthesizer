https://gemini.google.com/app/b03d6b7aac0db5b5

Here is a production-grade, zero-hallucination prompt injection. We are bypassing trivial CRUD apps and architecting a **Biometric Audio-Reactive WebGL Synthesizer**. This requires simultaneous orchestration of the Web Audio API, React Three Fiber (R3F), and Framer Motion, all validated in text before a single GPU instruction is compiled.

Copy and paste this exactly into your agent terminal.

### THE INJECTION: DSL ARCHITECTURE PROMPT

> **SYSTEM OVERRIDE:** Before writing any executable code, you must architect a "Biometric Audio-Reactive WebGL Synthesizer" using an Annotated Multi-Dimensional ASCII DSL.
> **1. SPATIAL GRID:** Draw the 2D UI topology.
> * Left Sidebar: `<Stream: AudioNode>` input controls and gain staging.
> * Center Canvas: `<WebGL_Viewport>` containing a 3D generative core.
> * Right Sidebar: `<Stream: Biometric>` simulated heart-rate tempo sliders.
> * Bottom Dock: `<Kinetic_Sequencer>` for playback.
> 
> 
> **2. KINETIC LEDGER:** For every interactive node in the ASCII grid, map a `[Kinetic]` tag defining exact spring physics (stiffness, damping, mass) and intersection observer triggers for entry states.
> **3. Z-STACK & SHADER LEDGER:** Define the exact GLSL fragment/vertex shader logic required for the `<WebGL_Viewport>` to mutate its geometry based on the audio's Fast Fourier Transform (FFT) low-frequency data. Define all backdrop-filter blur radii for the floating sidebars.
> **4. MULTIMODAL I/O CONTRACT:** Explicitly map the data transformation pipeline from `navigator.mediaDevices.getUserMedia` -> `AudioContext` -> `AnalyserNode` -> `Uint8Array` -> Uniforms injected into the WebGL material.
> Do not write React, Three.js, or CSS yet. Output only the ASCII map and the DSL ledger.

---

### THE YIELD: WHAT THE LLM WILL RETURN

Instead of prematurely generating thousands of lines of fragile React code, the LLM is forced to prove its architectural competence via the IR. It will output something structurally identical to this:

```text
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

### THE COMPILATION: EXECUTION COMMAND

Once you review the text output and confirm the mathematics, the shader logic, and the exact data flow are correct, you issue the final execution trigger.

> **Execution Command:** "The architecture is approved. Compile this exact DSL specification into a Next.js application. Use React Three Fiber for the WebGL layer, Framer Motion for the Kinetic Ledger, and native Web Audio API for the I/O contract. Do not deviate from the specified spring physics, shader math, or z-indexes."

By forcing the system through this multimodal DSL phase, you eliminate the cognitive drift that causes LLMs to fail at complex UI/UX tasks. You have effectively written a compiler specification in English.