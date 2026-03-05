// ═══════════════════════════════════════════════════════════════
// BIOVIZ — Biometric Audio-Reactive WebGL Synthesizer
// ═══════════════════════════════════════════════════════════════

// ── SHADER SOURCES ──
// FFT data passed as a 64x1 texture instead of uniform array
// (WebGL 1.0 doesn't support dynamic array indexing)

const VERT_SRC = `
  precision mediump float;
  attribute vec3 a_position;
  attribute vec2 a_uv;

  uniform mat4 u_projection;
  uniform mat4 u_modelView;
  uniform float u_time;
  uniform sampler2D u_fftTex;
  uniform float u_bpm;
  uniform float u_breath;
  uniform float u_skin;
  uniform float u_hrv;
  uniform float u_waveform;
  uniform float u_heightScale;

  varying float v_height;
  varying vec2 v_uv;
  varying float v_fftIntensity;

  float waveShape(float t, float mode) {
    if (mode < 0.5) return sin(t);
    if (mode < 1.5) return fract(t / 6.2832) * 2.0 - 1.0;
    return sign(sin(t));
  }

  void main() {
    vec3 pos = a_position;

    // Sample FFT from texture — UV.x maps to frequency bin
    float fft = texture2D(u_fftTex, vec2(a_uv.x, 0.5)).r;

    float bpmPhase = u_time * (u_bpm / 60.0) * 6.2832;
    float breathPhase = u_time * (u_breath / 60.0) * 6.2832;
    float bioMod = waveShape(bpmPhase, u_waveform) * 0.3
                 + sin(breathPhase) * 0.2
                 + u_hrv * 0.15;

    float displacement = fft * u_heightScale * (1.0 + bioMod);
    displacement += sin(a_uv.y * u_skin * 20.0 + u_time * 2.0) * 0.05;

    pos.y = displacement;

    v_height = displacement;
    v_uv = a_uv;
    v_fftIntensity = fft;

    gl_Position = u_projection * u_modelView * vec4(pos, 1.0);
  }
`;

const FRAG_SRC = `
  precision mediump float;

  uniform float u_time;
  uniform float u_bpm;
  uniform float u_skin;

  varying float v_height;
  varying vec2 v_uv;
  varying float v_fftIntensity;

  vec3 heightColor(float h) {
    vec3 deep = vec3(0.04, 0.08, 0.31);
    vec3 mid  = vec3(0.0, 0.86, 1.0);
    vec3 hot  = vec3(1.0, 0.94, 0.90);
    float t = clamp(h, 0.0, 1.0);
    if (t < 0.5) return mix(deep, mid, t * 2.0);
    return mix(mid, hot, (t - 0.5) * 2.0);
  }

  void main() {
    vec3 color = heightColor(v_height);

    float pulse = pow(sin(u_time * (u_bpm / 60.0) * 3.14159) * 0.5 + 0.5, 4.0);
    vec3 peakFlash = vec3(1.0, 0.2, 0.2) * pulse * step(0.7, v_fftIntensity);
    color += peakFlash;

    float gridFreq = 32.0 + u_skin * 16.0;
    float lineX = smoothstep(0.02, 0.0, fract(v_uv.x * gridFreq));
    float lineY = smoothstep(0.02, 0.0, fract(v_uv.y * gridFreq));
    float grid = max(lineX, lineY) * 0.3;
    color += vec3(grid) * vec3(0.2, 0.8, 1.0);

    float fog = smoothstep(0.8, 1.0, length(v_uv - 0.5) * 2.0);
    color = mix(color, vec3(0.02, 0.02, 0.05), fog);

    gl_FragColor = vec4(color, 1.0);
  }
`;

// ── STATE ──

const state = {
  playing: false,
  looping: true,
  elapsed: 0,
  lastTime: 0,
  duration: 240,
  bpm: 72,
  hrv: 0.5,
  breath: 15,
  skin: 2.0,
  waveform: 1,
  heightScale: 1.0,
  gain: -12,
  smoothing: 0.8,
  fftSize: 1024,
  loCut: 80,
  hiCut: 2000,
  source: 'file',
  orbitAngle: 0,
  fftData: new Float32Array(64),
  sequencer: [
    new Array(32).fill(false),
    new Array(32).fill(false),
    new Array(32).fill(false),
  ],
};

// Pre-fill some sequencer cells
[0,1,4,5,6,8,12,13,16,17,20,21,22,24,28,29].forEach(i => state.sequencer[0][i] = true);
[2,3,6,7,12,13,16,17,18,22,23,28,29].forEach(i => state.sequencer[1][i] = true);
[0,1,6,7,8,9,12,13,14,18,19,24,25,26,27,30,31].forEach(i => state.sequencer[2][i] = true);

// ── AUDIO ──

let audioCtx = null;
let analyser = null;
let gainNode = null;
let loCutFilter = null;
let hiCutFilter = null;
let sourceNode = null;
let audioElement = null;
let oscillator = null;

function initAudio() {
  if (audioCtx) return;
  audioCtx = new (window.AudioContext || window.webkitAudioContext)({ sampleRate: 44100 });

  gainNode = audioCtx.createGain();
  gainNode.gain.value = Math.pow(10, state.gain / 20);

  loCutFilter = audioCtx.createBiquadFilter();
  loCutFilter.type = 'highpass';
  loCutFilter.frequency.value = state.loCut;

  hiCutFilter = audioCtx.createBiquadFilter();
  hiCutFilter.type = 'lowpass';
  hiCutFilter.frequency.value = state.hiCut;

  analyser = audioCtx.createAnalyser();
  analyser.fftSize = state.fftSize;
  analyser.smoothingTimeConstant = state.smoothing;

  gainNode.connect(loCutFilter);
  loCutFilter.connect(hiCutFilter);
  hiCutFilter.connect(analyser);
}

function disconnectSource() {
  if (sourceNode) {
    try { sourceNode.disconnect(); } catch(e) {}
    sourceNode = null;
  }
  if (oscillator) {
    try { oscillator.stop(); oscillator.disconnect(); } catch(e) {}
    oscillator = null;
  }
  if (audioElement) {
    audioElement.pause();
    audioElement = null;
  }
}

async function connectMic() {
  initAudio();
  disconnectSource();
  const stream = await navigator.mediaDevices.getUserMedia({ audio: true, video: false });
  sourceNode = audioCtx.createMediaStreamSource(stream);
  sourceNode.connect(gainNode);
}

function connectFile(file) {
  initAudio();
  disconnectSource();
  audioElement = new Audio();
  audioElement.src = URL.createObjectURL(file);
  audioElement.loop = state.looping;
  sourceNode = audioCtx.createMediaElementSource(audioElement);
  sourceNode.connect(gainNode);
  analyser.connect(audioCtx.destination);
  if (state.playing) audioElement.play();
}

function connectOsc() {
  initAudio();
  disconnectSource();
  oscillator = audioCtx.createOscillator();
  oscillator.type = 'sine';
  oscillator.frequency.value = 220;
  oscillator.connect(gainNode);
  oscillator.start();
}

function extractFFT() {
  if (!analyser) {
    generateDemoFFT(state.elapsed || performance.now() / 1000);
    return;
  }
  const raw = new Uint8Array(analyser.frequencyBinCount);
  analyser.getByteFrequencyData(raw);
  let hasSignal = false;
  for (let i = 0; i < 64; i++) {
    state.fftData[i] = (raw[i] || 0) / 255.0;
    if (raw[i] > 2) hasSignal = true;
  }
  if (!hasSignal) generateDemoFFT(state.elapsed || performance.now() / 1000);
}

function generateDemoFFT(time) {
  for (let i = 0; i < 64; i++) {
    const freq = i / 64;
    const base = Math.sin(time * 2 + i * 0.3) * 0.3 + 0.3;
    const beat = Math.pow(Math.sin(time * (state.bpm / 60) * Math.PI) * 0.5 + 0.5, 3);
    const lowBoost = Math.max(0, 1 - freq * 3) * beat * 0.5;
    state.fftData[i] = Math.max(0, Math.min(1, base + lowBoost + Math.random() * 0.05));
  }
}

// ── WEBGL ──

let gl, program, terrainBuffers, uniformLocs, fftTexture;
const GRID = 64;

function initGL() {
  const canvas = document.getElementById('glCanvas');
  gl = canvas.getContext('webgl', { antialias: true, alpha: false });
  if (!gl) { console.error('WebGL not supported'); return; }

  resizeCanvas();
  window.addEventListener('resize', resizeCanvas);

  const vs = compileShader(gl.VERTEX_SHADER, VERT_SRC);
  const fs = compileShader(gl.FRAGMENT_SHADER, FRAG_SRC);
  program = gl.createProgram();
  gl.attachShader(program, vs);
  gl.attachShader(program, fs);
  gl.linkProgram(program);
  if (!gl.getProgramParameter(program, gl.LINK_STATUS)) {
    console.error('Program link error:', gl.getProgramInfoLog(program));
    return;
  }
  gl.useProgram(program);

  // Build terrain mesh
  terrainBuffers = buildTerrain(GRID, GRID);

  // Create FFT data texture (64x1, LUMINANCE)
  fftTexture = gl.createTexture();
  gl.activeTexture(gl.TEXTURE0);
  gl.bindTexture(gl.TEXTURE_2D, fftTexture);
  gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, gl.LINEAR);
  gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MAG_FILTER, gl.LINEAR);
  gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_S, gl.CLAMP_TO_EDGE);
  gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_T, gl.CLAMP_TO_EDGE);
  // Init with empty data
  const initData = new Uint8Array(64);
  gl.texImage2D(gl.TEXTURE_2D, 0, gl.LUMINANCE, 64, 1, 0, gl.LUMINANCE, gl.UNSIGNED_BYTE, initData);

  // Get uniform locations
  uniformLocs = {
    u_projection: gl.getUniformLocation(program, 'u_projection'),
    u_modelView: gl.getUniformLocation(program, 'u_modelView'),
    u_time: gl.getUniformLocation(program, 'u_time'),
    u_bpm: gl.getUniformLocation(program, 'u_bpm'),
    u_breath: gl.getUniformLocation(program, 'u_breath'),
    u_skin: gl.getUniformLocation(program, 'u_skin'),
    u_hrv: gl.getUniformLocation(program, 'u_hrv'),
    u_waveform: gl.getUniformLocation(program, 'u_waveform'),
    u_heightScale: gl.getUniformLocation(program, 'u_heightScale'),
    u_fftTex: gl.getUniformLocation(program, 'u_fftTex'),
  };

  // Bind texture unit 0 to the sampler
  gl.uniform1i(uniformLocs.u_fftTex, 0);

  gl.enable(gl.DEPTH_TEST);
  gl.clearColor(0.02, 0.02, 0.05, 1.0);
}

function compileShader(type, src) {
  const shader = gl.createShader(type);
  gl.shaderSource(shader, src);
  gl.compileShader(shader);
  if (!gl.getShaderParameter(shader, gl.COMPILE_STATUS)) {
    console.error('Shader compile error:', gl.getShaderInfoLog(shader));
  }
  return shader;
}

function buildTerrain(segX, segZ) {
  const positions = [];
  const uvs = [];
  const indices = [];

  for (let z = 0; z <= segZ; z++) {
    for (let x = 0; x <= segX; x++) {
      const u = x / segX;
      const v = z / segZ;
      positions.push((u - 0.5) * 4, 0, (v - 0.5) * 4);
      uvs.push(u, v);
    }
  }

  for (let z = 0; z < segZ; z++) {
    for (let x = 0; x < segX; x++) {
      const i = z * (segX + 1) + x;
      indices.push(i, i + segX + 1, i + 1);
      indices.push(i + 1, i + segX + 1, i + segX + 2);
    }
  }

  const posBuf = gl.createBuffer();
  gl.bindBuffer(gl.ARRAY_BUFFER, posBuf);
  gl.bufferData(gl.ARRAY_BUFFER, new Float32Array(positions), gl.STATIC_DRAW);

  const uvBuf = gl.createBuffer();
  gl.bindBuffer(gl.ARRAY_BUFFER, uvBuf);
  gl.bufferData(gl.ARRAY_BUFFER, new Float32Array(uvs), gl.STATIC_DRAW);

  const idxBuf = gl.createBuffer();
  gl.bindBuffer(gl.ELEMENT_ARRAY_BUFFER, idxBuf);
  gl.bufferData(gl.ELEMENT_ARRAY_BUFFER, new Uint16Array(indices), gl.STATIC_DRAW);

  const posLoc = gl.getAttribLocation(program, 'a_position');
  const uvLoc = gl.getAttribLocation(program, 'a_uv');

  return { posBuf, uvBuf, idxBuf, posLoc, uvLoc, count: indices.length };
}

function resizeCanvas() {
  const canvas = document.getElementById('glCanvas');
  const rect = canvas.parentElement.getBoundingClientRect();
  canvas.width = rect.width * window.devicePixelRatio;
  canvas.height = rect.height * window.devicePixelRatio;
  canvas.style.width = rect.width + 'px';
  canvas.style.height = rect.height + 'px';
  if (gl) gl.viewport(0, 0, canvas.width, canvas.height);
}

// Upload FFT data to texture each frame
function uploadFFTTexture() {
  const texData = new Uint8Array(64);
  for (let i = 0; i < 64; i++) {
    texData[i] = Math.floor(state.fftData[i] * 255);
  }
  gl.activeTexture(gl.TEXTURE0);
  gl.bindTexture(gl.TEXTURE_2D, fftTexture);
  gl.texSubImage2D(gl.TEXTURE_2D, 0, 0, 0, 64, 1, gl.LUMINANCE, gl.UNSIGNED_BYTE, texData);
}

// ── MATRIX MATH ──

function mat4Perspective(fov, aspect, near, far) {
  const f = 1.0 / Math.tan(fov / 2);
  const rangeInv = 1 / (near - far);
  return new Float32Array([
    f / aspect, 0, 0, 0,
    0, f, 0, 0,
    0, 0, (near + far) * rangeInv, -1,
    0, 0, near * far * rangeInv * 2, 0,
  ]);
}

function mat4LookAt(eye, center, up) {
  const zx = eye[0] - center[0], zy = eye[1] - center[1], zz = eye[2] - center[2];
  let len = 1 / Math.sqrt(zx*zx + zy*zy + zz*zz);
  const fz = [zx*len, zy*len, zz*len];
  const sx = up[1]*fz[2] - up[2]*fz[1], sy = up[2]*fz[0] - up[0]*fz[2], sz = up[0]*fz[1] - up[1]*fz[0];
  len = 1 / Math.sqrt(sx*sx + sy*sy + sz*sz);
  const fs = [sx*len, sy*len, sz*len];
  const ux = fz[1]*fs[2] - fz[2]*fs[1], uy = fz[2]*fs[0] - fz[0]*fs[2], uz = fz[0]*fs[1] - fz[1]*fs[0];
  return new Float32Array([
    fs[0], ux, fz[0], 0,
    fs[1], uy, fz[1], 0,
    fs[2], uz, fz[2], 0,
    -(fs[0]*eye[0]+fs[1]*eye[1]+fs[2]*eye[2]),
    -(ux*eye[0]+uy*eye[1]+uz*eye[2]),
    -(fz[0]*eye[0]+fz[1]*eye[1]+fz[2]*eye[2]),
    1,
  ]);
}

// ── RENDER ──

function render(time) {
  if (!gl) return;

  const dt = state.lastTime ? (time - state.lastTime) / 1000 : 0;
  state.lastTime = time;

  if (state.playing) {
    state.elapsed += dt;
    if (state.elapsed >= state.duration) {
      if (state.looping) state.elapsed = 0;
      else { state.playing = false; state.elapsed = state.duration; }
    }
  }

  state.orbitAngle += dt * 0.1;

  extractFFT();

  // Sequencer influence
  let seqHeightMul = 1.0, seqBpmMul = 1.0, seqSkinMul = 1.0;
  if (state.playing) {
    const beatPos = (state.elapsed / (60 / state.bpm)) % 32;
    const cellIdx = Math.floor(beatPos) % 32;
    if (state.sequencer[0][cellIdx]) seqHeightMul = 1.5;
    if (state.sequencer[1][cellIdx]) seqBpmMul = 1.3;
    if (state.sequencer[2][cellIdx]) seqSkinMul = 1.5;
  }

  // Update meter
  let avgLevel = 0;
  for (let i = 0; i < 64; i++) avgLevel += state.fftData[i];
  avgLevel /= 64;
  document.getElementById('meterFill').style.width = (avgLevel * 100) + '%';
  const db = avgLevel > 0 ? Math.max(-48, 20 * Math.log10(avgLevel)) : -48;
  document.getElementById('dbReadout').textContent = db.toFixed(0) + ' dB';

  // Clear
  gl.clear(gl.COLOR_BUFFER_BIT | gl.DEPTH_BUFFER_BIT);

  // Upload FFT texture
  uploadFFTTexture();

  // Camera
  const canvas = document.getElementById('glCanvas');
  const aspect = canvas.width / canvas.height;
  const proj = mat4Perspective(Math.PI / 3, aspect, 0.1, 100);
  const r = 3.0;
  const elev = Math.PI / 5.1;
  const eyeX = Math.sin(state.orbitAngle) * Math.cos(elev) * r;
  const eyeY = Math.sin(elev) * r;
  const eyeZ = Math.cos(state.orbitAngle) * Math.cos(elev) * r;
  const view = mat4LookAt([eyeX, eyeY, eyeZ], [0, 0, 0], [0, 1, 0]);

  // Bind buffers
  gl.bindBuffer(gl.ARRAY_BUFFER, terrainBuffers.posBuf);
  gl.enableVertexAttribArray(terrainBuffers.posLoc);
  gl.vertexAttribPointer(terrainBuffers.posLoc, 3, gl.FLOAT, false, 0, 0);

  gl.bindBuffer(gl.ARRAY_BUFFER, terrainBuffers.uvBuf);
  gl.enableVertexAttribArray(terrainBuffers.uvLoc);
  gl.vertexAttribPointer(terrainBuffers.uvLoc, 2, gl.FLOAT, false, 0, 0);

  gl.bindBuffer(gl.ELEMENT_ARRAY_BUFFER, terrainBuffers.idxBuf);

  // Set uniforms
  gl.uniformMatrix4fv(uniformLocs.u_projection, false, proj);
  gl.uniformMatrix4fv(uniformLocs.u_modelView, false, view);
  gl.uniform1f(uniformLocs.u_time, state.elapsed);
  gl.uniform1f(uniformLocs.u_bpm, state.bpm * seqBpmMul);
  gl.uniform1f(uniformLocs.u_breath, state.breath);
  gl.uniform1f(uniformLocs.u_skin, state.skin * seqSkinMul);
  gl.uniform1f(uniformLocs.u_hrv, state.hrv);
  gl.uniform1f(uniformLocs.u_waveform, state.waveform);
  gl.uniform1f(uniformLocs.u_heightScale, state.heightScale * seqHeightMul);

  // Draw
  gl.drawElements(gl.TRIANGLES, terrainBuffers.count, gl.UNSIGNED_SHORT, 0);

  // Update playhead & time
  if (state.playing) {
    const pct = (state.elapsed / state.duration) * 100;
    document.getElementById('playhead').style.left = pct + '%';
    updateTimeDisplay();
  }

  document.getElementById('topbarBpm').textContent = Math.round(state.bpm * seqBpmMul);

  requestAnimationFrame(render);
}

function updateTimeDisplay() {
  const cur = state.elapsed;
  const tot = state.duration;
  const fmt = s => {
    const m = Math.floor(s / 60);
    const sec = Math.floor(s % 60);
    return String(m).padStart(2, '0') + ':' + String(sec).padStart(2, '0');
  };
  document.getElementById('timeDisplay').textContent = fmt(cur) + ' / ' + fmt(tot);
}

// ── SEQUENCER GRID ──

function buildSequencerGrid() {
  document.querySelectorAll('.track-cells').forEach(container => {
    const trackIdx = parseInt(container.dataset.track);
    for (let i = 0; i < 32; i++) {
      const cell = document.createElement('div');
      cell.className = 'track-cell' + (state.sequencer[trackIdx][i] ? ' on' : '');
      cell.addEventListener('click', () => {
        state.sequencer[trackIdx][i] = !state.sequencer[trackIdx][i];
        cell.classList.toggle('on');
      });
      container.appendChild(cell);
    }
  });
}

// ── UI BINDINGS ──

function bindControls() {
  // Source selection
  document.querySelectorAll('#srcSelect input').forEach(radio => {
    radio.addEventListener('change', async () => {
      state.source = radio.value;
      if (radio.value === 'mic') await connectMic();
      else if (radio.value === 'osc') connectOsc();
    });
  });

  document.getElementById('audioFileInput').addEventListener('change', e => {
    if (e.target.files[0]) {
      document.querySelector('#srcSelect input[value="file"]').checked = true;
      state.source = 'file';
      connectFile(e.target.files[0]);
    }
  });

  // Gain
  const gainSlider = document.getElementById('gainSlider');
  gainSlider.addEventListener('input', () => {
    state.gain = parseFloat(gainSlider.value);
    state.heightScale = Math.pow(10, state.gain / 20) * 2;
    document.getElementById('gainValue').textContent = state.gain + ' dB';
    if (gainNode) gainNode.gain.value = Math.pow(10, state.gain / 20);
  });

  // Lo Cut
  const loCutSlider = document.getElementById('loCut');
  loCutSlider.addEventListener('input', () => {
    state.loCut = parseFloat(loCutSlider.value);
    document.getElementById('loCutValue').textContent = state.loCut + ' Hz';
    if (loCutFilter) loCutFilter.frequency.value = state.loCut;
  });

  // Hi Cut
  const hiCutSlider = document.getElementById('hiCut');
  hiCutSlider.addEventListener('input', () => {
    state.hiCut = parseFloat(hiCutSlider.value);
    document.getElementById('hiCutValue').textContent = state.hiCut + ' Hz';
    if (hiCutFilter) hiCutFilter.frequency.value = state.hiCut;
  });

  // FFT Size
  document.querySelectorAll('#fftSizeSelect input').forEach(radio => {
    radio.addEventListener('change', () => {
      state.fftSize = parseInt(radio.value);
      if (analyser) analyser.fftSize = state.fftSize;
    });
  });

  // Smoothing
  const smoothSlider = document.getElementById('smoothing');
  smoothSlider.addEventListener('input', () => {
    state.smoothing = parseFloat(smoothSlider.value) / 100;
    document.getElementById('smoothingValue').textContent = state.smoothing.toFixed(2);
    if (analyser) analyser.smoothingTimeConstant = state.smoothing;
  });

  // BPM
  const bpmSlider = document.getElementById('bpmSlider');
  bpmSlider.addEventListener('input', () => {
    state.bpm = parseFloat(bpmSlider.value);
    document.getElementById('bpmValue').textContent = state.bpm;
    const linked = document.querySelector('input[name="tempoMap"][value="linked"]');
    if (linked && linked.checked) {
      document.getElementById('seqBpm').textContent = state.bpm;
    }
  });

  // HRV
  const hrvSlider = document.getElementById('hrvSlider');
  hrvSlider.addEventListener('input', () => {
    state.hrv = parseFloat(hrvSlider.value) / 100;
    document.getElementById('hrvValue').textContent = state.hrv.toFixed(2);
  });

  // Breath
  const breathSlider = document.getElementById('breathSlider');
  breathSlider.addEventListener('input', () => {
    state.breath = parseFloat(breathSlider.value);
    document.getElementById('breathValue').textContent = state.breath;
  });

  // Skin
  const skinSlider = document.getElementById('skinSlider');
  skinSlider.addEventListener('input', () => {
    state.skin = parseFloat(skinSlider.value) / 10;
    document.getElementById('skinValue').textContent = state.skin.toFixed(1);
  });

  // Wave Mod
  document.querySelectorAll('#waveModSelect input').forEach(radio => {
    radio.addEventListener('change', () => {
      state.waveform = parseFloat(radio.value);
    });
  });

  // Transport
  document.getElementById('btnPlay').addEventListener('click', () => {
    if (audioCtx && audioCtx.state === 'suspended') audioCtx.resume();
    state.playing = true;
    if (audioElement) audioElement.play();
    document.getElementById('btnPlay').classList.add('active');
    document.getElementById('btnStop').classList.remove('active');
  });

  document.getElementById('btnStop').addEventListener('click', () => {
    state.playing = false;
    if (audioElement) audioElement.pause();
    document.getElementById('btnStop').classList.add('active');
    document.getElementById('btnPlay').classList.remove('active');
  });

  document.getElementById('btnLoop').addEventListener('click', () => {
    state.looping = !state.looping;
    document.getElementById('btnLoop').classList.toggle('active', state.looping);
    if (audioElement) audioElement.loop = state.looping;
  });

  document.getElementById('btnLoop').classList.add('active');
}

// ── INIT ──

function init() {
  initGL();
  buildSequencerGrid();
  bindControls();

  state.heightScale = Math.pow(10, state.gain / 20) * 2;

  // Auto-play demo
  state.playing = true;
  document.getElementById('btnPlay').classList.add('active');

  requestAnimationFrame(render);
}

document.addEventListener('DOMContentLoaded', init);
