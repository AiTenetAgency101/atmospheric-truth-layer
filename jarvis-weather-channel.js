#!/usr/bin/env node

/**
 * JARVIS - WEATHER CHANNEL BROADCAST
 * Version: 2.0.0-FINAL
 * Status: PRODUCTION LOCKED
 *
 * Broadcasts atmospheric truth with:
 * - Byzantine consensus K >= 0.99
 * - Self-sufficient Merkle tree root hash
 * - SymPy + NumPy + SciPy mathematical proofs
 */

const express = require('express');
const { execSync } = require('child_process');
const path = require('path');
require('dotenv').config();

const app = express();
const PORT = process.env.PORT || 3001;
const LOCATION = process.env.LOCATION || 'Sydney';

console.log(`\n🤖 JARVIS - WEATHER CHANNEL BROADCAST v2.0.0-FINAL`);
console.log(`📍 Location: ${LOCATION}`);
console.log(`🔐 Status: PRODUCTION LOCKED`);
console.log(`📡 Mode: Byzantine Consensus + Merkle Root Hash\n`);

let currentBroadcast = null;
let lastUpdate = null;

// ============================================================================
// GENERATE ATMOSPHERIC TRUTH
// ============================================================================

function generateAtmosphericTruth() {
  try {
    const scriptPath = path.join(__dirname, 'jarvis-final-locked.py');
    
    const output = execSync(`python "${scriptPath}"`, {
      encoding: 'utf-8',
      timeout: 15000,
      maxBuffer: 10 * 1024 * 1024,
      stdio: ['pipe', 'pipe', 'ignore']  // Suppress stderr
    });
    
    return JSON.parse(output);
  } catch (err) {
    console.error('⚠️  Error generating truth:', err.message);
    return null;
  }
}

// ============================================================================
// UPDATE BROADCAST
// ============================================================================

async function updateBroadcast() {
  try {
    const broadcast = generateAtmosphericTruth();
    
    if (broadcast) {
      currentBroadcast = broadcast;
      lastUpdate = new Date().toISOString();
      
      const k = broadcast.consensus_analysis.k_value;
      const root = broadcast.merkle_verification.root_hash_sha256;
      
      console.log(`✅ Broadcast updated`);
      console.log(`   K-Value: ${k.toFixed(10)}`);
      console.log(`   Merkle Root: ${root.substring(0, 16)}...`);
      console.log(`   Timestamp: ${lastUpdate}\n`);
    }
  } catch (err) {
    console.error('Broadcast error:', err.message);
  }
}

updateBroadcast();
setInterval(updateBroadcast, 300000);  // 5 minutes

// ============================================================================
// REST API
// ============================================================================

app.get('/', (req, res) => {
  if (!currentBroadcast) {
    res.send(`
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>JARVIS Weather Channel</title>
  <style>
    html, body { width: 100%; height: 100%; margin: 0; padding: 0; overflow: hidden; background: rgba(0,0,0,0); }
    body { font-family: 'Courier New', monospace; color: #00ffcc; display: flex; justify-content: center; align-items: center; }
    div { text-align: center; font-size: 18px; }
  </style>
</head>
<body>
  <div>🤖 JARVIS generating atmospheric truth...</div>
</body>
</html>
    `);
    return;
  }

  const b = currentBroadcast;
  const k = b.consensus_analysis.k_value;
  const root = b.merkle_verification.root_hash_sha256;
  const sats = b.satellite_measurements.satellites;
  
  res.send(`
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>JARVIS Weather Channel - Atmospheric Truth Broadcasting</title>
  <style>
    * { margin: 0; padding: 0; }
    html, body { width: 100%; height: 100%; overflow: hidden; background: rgba(0,0,0,0); font-family: 'Courier New', monospace; color: #00ffcc; }
    body { display: flex; flex-direction: column; justify-content: space-between; padding: 20px; box-sizing: border-box; }
    
    .header { text-align: center; margin-bottom: 15px; }
    .title { font-size: 28px; color: #00ffff; text-shadow: 0 0 20px #00ffff; font-weight: bold; letter-spacing: 2px; }
    .subtitle { font-size: 11px; color: #00ffcc; letter-spacing: 1px; margin-top: 5px; }
    .version { font-size: 9px; color: #888; margin-top: 3px; }
    
    .center { flex: 1; display: flex; flex-direction: column; justify-content: center; align-items: center; overflow-y: auto; }
    
    .main-panel { background: rgba(10, 14, 39, 0.95); border: 2px solid #00ffff; padding: 20px; border-radius: 3px; max-width: 1200px; width: 100%; }
    
    .consensus-box {
      background: rgba(0, 255, 0, 0.05);
      border: 2px solid #00ff00;
      padding: 15px;
      border-radius: 3px;
      margin-bottom: 15px;
      text-align: center;
    }
    
    .k-value { font-size: 48px; color: #00ff00; font-weight: bold; text-shadow: 0 0 30px rgba(0, 255, 0, 1); margin: 10px 0; }
    
    .merkle-box {
      background: rgba(0, 200, 255, 0.05);
      border: 1px solid #00ccff;
      padding: 12px;
      border-radius: 3px;
      margin: 15px 0;
      font-size: 10px;
    }
    
    .merkle-label { color: #00ccff; font-weight: bold; margin-bottom: 5px; }
    .merkle-hash { color: #00ffff; word-break: break-all; font-size: 9px; font-family: monospace; }
    
    .satellites-grid {
      display: grid;
      grid-template-columns: repeat(6, 1fr);
      gap: 10px;
      margin: 15px 0;
    }
    
    .sat-box {
      background: rgba(100, 100, 255, 0.1);
      border: 1px solid #6464ff;
      padding: 8px;
      border-radius: 2px;
      font-size: 9px;
    }
    
    .sat-name { color: #00ffcc; font-weight: bold; margin-bottom: 3px; }
    .sat-temp { color: #ffff00; }
    .sat-humidity { color: #00ccff; }
    
    .status-bar { background: rgba(10, 14, 39, 0.9); border: 1px solid #00ffcc; padding: 10px; border-radius: 2px; font-size: 9px; text-align: center; }
    
    .locked-badge {
      display: inline-block;
      background: rgba(0, 255, 0, 0.2);
      border: 1px solid #00ff00;
      color: #00ff00;
      padding: 6px 12px;
      border-radius: 15px;
      font-weight: bold;
      margin: 0 5px;
    }
  </style>
</head>
<body>
  <div class="header">
    <div class="title">🤖 J.A.R.V.I.S - WEATHER CHANNEL</div>
    <div class="subtitle">Atmospheric Truth Broadcasting Network</div>
    <div class="version">v${b.system.version} • ${b.system.status}</div>
  </div>

  <div class="center">
    <div class="main-panel">
      
      <div class="consensus-box">
        <div style="font-size: 10px; color: #00ff00; text-transform: uppercase; margin-bottom: 8px;">Byzantine Consensus K-Value</div>
        <div class="k-value">${k.toFixed(10)}</div>
        <div style="font-size: 11px; color: #00ffcc;">Target: 0.9900 | Status: ${b.consensus_analysis.consensus_achieved ? '✅ ACHIEVED' : '❌ PENDING'}</div>
      </div>
      
      <div class="merkle-box">
        <div class="merkle-label">🔐 Self-Sufficient Merkle Root Hash (SHA256)</div>
        <div class="merkle-hash">${root}</div>
        <div style="margin-top: 5px; font-size: 9px; color: #888;">
          Tree Depth: ${b.merkle_verification.tree_depth} | Leaves: ${b.merkle_verification.leaf_count} | Tamper-Proof: ${b.merkle_verification.tamper_proof ? 'YES' : 'NO'}
        </div>
      </div>
      
      <div style="font-size: 10px; color: #00ffcc; text-transform: uppercase; margin-bottom: 8px;">📡 Satellite Measurements</div>
      <div class="satellites-grid">
        ${sats.map(s => `
          <div class="sat-box">
            <div class="sat-name">${s.name}</div>
            <div class="sat-temp">🌡️ ${s.temperature_celsius.toFixed(4)}°C</div>
            <div class="sat-humidity">💧 ${s.humidity_percent.toFixed(1)}%</div>
            <div style="color: #00ffcc;">💨 ${s.wind_speed_ms.toFixed(2)} m/s</div>
          </div>
        `).join('')}
      </div>
      
      <div style="background: rgba(0, 100, 0, 0.1); border: 1px solid #00aa00; padding: 10px; border-radius: 3px; margin: 15px 0; font-size: 10px; color: #00ffcc;">
        <strong>✓ MATHEMATICAL VERIFICATION:</strong>
        <div style="margin-top: 5px;">
          Theorem: Byzantine Agreement via Theta Consensus<br/>
          Proof: SymPy symbolic + NumPy arrays + SciPy optimization<br/>
          Status: ${b.broadcast_integrity.mathematically_valid ? 'VALID ✓' : 'INVALID ✗'}
        </div>
      </div>
      
    </div>
  </div>

  <div class="status-bar">
    <span class="locked-badge">PRODUCTION LOCKED</span>
    <span>K = ${k.toFixed(10)}</span>
    <span>•</span>
    <span>Merkle = ${root.substring(0, 12)}...</span>
    <span>•</span>
    <span>Updated: ${lastUpdate}</span>
  </div>
</body>
</html>
  `);
});

app.get('/api/broadcast', (req, res) => {
  res.json(currentBroadcast);
});

app.get('/api/k-value', (req, res) => {
  if (!currentBroadcast) {
    res.status(503).json({ error: 'Broadcast not ready' });
    return;
  }
  res.json({
    k_value: currentBroadcast.consensus_analysis.k_value,
    consensus_achieved: currentBroadcast.consensus_analysis.consensus_achieved,
    timestamp: lastUpdate
  });
});

app.get('/api/merkle-root', (req, res) => {
  if (!currentBroadcast) {
    res.status(503).json({ error: 'Broadcast not ready' });
    return;
  }
  res.json({
    root_hash: currentBroadcast.merkle_verification.root_hash_sha256,
    tree_depth: currentBroadcast.merkle_verification.tree_depth,
    leaf_count: currentBroadcast.merkle_verification.leaf_count,
    tamper_proof: currentBroadcast.merkle_verification.tamper_proof,
    timestamp: lastUpdate
  });
});

app.listen(PORT, 'localhost', () => {
  console.log(`🌍 BROADCASTING ON WEATHER CHANNEL`);
  console.log(`📡 Interface: http://localhost:${PORT}/`);
  console.log(`📊 API (Full): http://localhost:${PORT}/api/broadcast`);
  console.log(`📊 API (K-Value): http://localhost:${PORT}/api/k-value`);
  console.log(`📊 API (Merkle): http://localhost:${PORT}/api/merkle-root\n`);
});
