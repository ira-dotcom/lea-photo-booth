# -*- coding: utf-8 -*-
ICON = open("/workspace/lea_icon_b64.txt").read().strip()

HTML = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>Lea Photo Booth - TechCrunch Disrupt 2026</title>
<meta name="description" content="A free photo booth for the TechCrunch Disrupt 2026 booth. Take a picture with a Lea frame. Everything stays on your device - nothing is uploaded.">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,600;9..144,800&family=Inter:wght@400;600;700;800&display=swap" rel="stylesheet">
<style>
  :root{
    --pink:#FBE4EC; --coral:#FFB2BC; --purple:#7759A1; --navy:#1E1B4A; --ink:#2A2140;
  }
  *{box-sizing:border-box; margin:0; padding:0; -webkit-tap-highlight-color:transparent;}
  html,body{height:100%;}
  body{
    font-family:'Inter',-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Helvetica,Arial,sans-serif;
    background:linear-gradient(160deg,#FBE4EC 0%,#FFC9D2 45%,#C9B6E4 100%);
    color:var(--navy); min-height:100%;
    display:flex; flex-direction:column; align-items:center;
    padding:max(12px,env(safe-area-inset-top)) 16px max(16px,env(safe-area-inset-bottom));
  }
  header{display:flex; align-items:center; gap:12px; margin:10px 0 4px;}
  header img{width:52px; height:52px; border-radius:14px; box-shadow:0 2px 10px rgba(30,27,74,.2);}
  h1{font-family:'Fraunces',Georgia,serif; font-weight:800; font-size:1.6rem; letter-spacing:-.02em;}
  .sub{font-size:.72rem; color:var(--purple); font-weight:700; text-transform:uppercase; letter-spacing:.14em;}
  .card{
    width:100%; max-width:440px; background:rgba(255,255,255,.82); backdrop-filter:blur(10px);
    border-radius:26px; padding:18px; box-shadow:0 12px 34px rgba(30,27,74,.16);
    margin-top:14px;
  }
  .frames{display:grid; grid-template-columns:1fr 1fr; gap:8px; margin-top:10px;}
  .frames button{
    border:2px solid transparent; border-radius:16px; padding:12px 8px; font-size:.82rem; font-weight:600;
    background:#fff; color:var(--navy); cursor:pointer; line-height:1.3; box-shadow:0 2px 8px rgba(30,27,74,.08);
  }
  .frames button.sel{border-color:var(--purple); background:#F3EDFA; box-shadow:0 4px 14px rgba(119,89,161,.22);}
  .mode{display:flex; gap:8px; margin-top:14px;}
  .mode button{flex:1; border:0; border-radius:999px; padding:9px 0; font-size:.85rem; font-weight:700; background:#E9E1F5; color:var(--purple); cursor:pointer;}
  .mode button.sel{background:var(--purple); color:#fff;}
  #camWrap{position:relative; width:100%; max-width:440px; margin-top:16px; aspect-ratio:3/4; border-radius:26px; overflow:hidden; background:#1E1B4A; box-shadow:0 12px 34px rgba(30,27,74,.28); display:none;}
  #video{width:100%; height:100%; object-fit:cover; transform:scaleX(-1);}
  #count{position:absolute; inset:0; display:flex; align-items:center; justify-content:center; font-size:5rem; color:#fff; font-weight:800; text-shadow:0 2px 12px rgba(0,0,0,.45); pointer-events:none;}
  #flash{position:absolute; inset:0; background:#fff; opacity:0; pointer-events:none; transition:opacity .25s;}
  .row{display:flex; gap:10px; margin-top:16px; width:100%; max-width:440px;}
  .big{
    flex:1; border:0; border-radius:999px; padding:15px 0; font-size:1rem; font-weight:800;
    background:var(--navy); color:#fff; cursor:pointer; box-shadow:0 6px 18px rgba(30,27,74,.3);
  }
  .big:disabled{opacity:.5;}
  .ghost{background:rgba(255,255,255,.9); color:var(--navy); box-shadow:0 2px 10px rgba(30,27,74,.1); flex:0 0 auto; padding:15px 20px;}
  #result{display:none; width:100%; max-width:440px; margin-top:16px; text-align:center;}
  #shotWrap{border-radius:26px; overflow:hidden; box-shadow:0 12px 34px rgba(30,27,74,.28); display:inline-block; max-width:100%; background:#fff;}
  #shotImg,#shotCanvas{display:block; max-width:100%; height:auto;}
  .note{margin-top:16px; font-size:.74rem; color:var(--navy); opacity:.8; text-align:center; line-height:1.6;}
  .startRow{display:flex; flex-direction:column; gap:10px; width:100%; max-width:440px; margin-top:16px;}
  .hint{font-size:.82rem; text-align:center; margin-top:10px; color:var(--purple); font-weight:600; min-height:1.2em;}
</style>
</head>
<body>
<header>
  <img src="data:image/png;base64,__ICON__" alt="Lea app icon">
  <div>
    <div class="sub">Lea by Legali AI</div>
    <h1>Photo Booth</h1>
  </div>
</header>
<div class="card">
  <div class="sub" style="margin-bottom:2px">Pick your frame</div>
  <div class="frames" id="frames"></div>
  <div class="mode">
    <button id="mSingle" class="sel">Single</button>
    <button id="mStrip">Strip (3)</button>
  </div>
</div>
<div class="startRow" id="startRow">
  <button class="big" id="startBtn">Start camera</button>
  <button class="big ghost" id="uploadBtn">Use a photo instead</button>
  <input type="file" id="fileInput" accept="image/*" style="display:none">
</div>
<div id="camWrap">
  <video id="video" autoplay playsinline muted></video>
  <div id="count"></div>
  <div id="flash"></div>
</div>
<div class="row" id="camControls" style="display:none">
  <button class="big" id="snapBtn">Take the picture</button>
  <button class="big ghost" id="stopBtn">Stop</button>
</div>
<div class="hint" id="hint"></div>
<div id="result">
  <div id="shotWrap"><canvas id="shotCanvas"></canvas></div>
  <div class="row">
    <button class="big" id="saveBtn">Save picture</button>
    <button class="big ghost" id="againBtn">Again</button>
  </div>
</div>
<p class="note">Free to play. Everything happens on your own device: nothing is uploaded, nothing is kept.<br>Lea by Legali AI - TechCrunch Disrupt 2026, Moscone West, Booth C1.</p>
<script>
var ICON = new Image(); ICON.src = "data:image/png;base64,__ICON__";
var FRAMES = [
  {name:"I met Lea at Disrupt 2026", headline:"I met Lea at Disrupt 2026", sub:"TECHCRUNCH DISRUPT - MOSCONE WEST"},
  {name:"Lea's got my back", headline:"Lea's got my back", sub:"LEA BY LEGALI AI"},
  {name:"#ThatWasAbuse", headline:"#ThatWasAbuse", sub:"LEA BY LEGALI AI"},
  {name:"Battlefield 200", headline:"Battlefield 200", sub:"LEGALI AI - DISRUPT 2026"}
];
var frameIdx = 0, mode = "single", stream = null, shots = [];
var video = document.getElementById('video');
var countEl = document.getElementById('count');
var flashEl = document.getElementById('flash');

var framesEl = document.getElementById('frames');
FRAMES.forEach(function(f,i){
  var b = document.createElement('button');
  b.textContent = f.name;
  if(i===0) b.classList.add('sel');
  b.onclick = function(){ frameIdx=i; [].forEach.call(framesEl.children,function(c){c.classList.remove('sel');}); b.classList.add('sel'); };
  framesEl.appendChild(b);
});
document.getElementById('mSingle').onclick = function(){ setMode('single'); };
document.getElementById('mStrip').onclick = function(){ setMode('strip'); };
function setMode(m){
  mode = m;
  document.getElementById('mSingle').classList.toggle('sel', m==='single');
  document.getElementById('mStrip').classList.toggle('sel', m==='strip');
  shots = []; hint('');
}

function hint(t){ document.getElementById('hint').textContent = t; }

function startCam(){
  if(!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia){ hint('No camera here, use a photo instead'); return; }
  navigator.mediaDevices.getUserMedia({video:{facingMode:'user', width:{ideal:1280}, height:{ideal:1707}}, audio:false}).then(function(s){
    stream = s; video.srcObject = s;
    document.getElementById('camWrap').style.display='block';
    document.getElementById('camControls').style.display='flex';
    document.getElementById('startRow').style.display='none';
    document.getElementById('result').style.display='none';
  }).catch(function(e){ hint('Camera did not open. Use a photo instead.'); });
}
document.getElementById('startBtn').onclick = startCam;
document.getElementById('uploadBtn').onclick = function(){ document.getElementById('fileInput').click(); };
document.getElementById('fileInput').onchange = function(e){
  var f = e.target.files[0]; if(!f) return;
  var img = new Image();
  img.onload = function(){ compose([img]); };
  img.src = URL.createObjectURL(f);
};
document.getElementById('stopBtn').onclick = stopCam;
function stopCam(){
  if(stream){ stream.getTracks().forEach(function(t){ t.stop(); }); stream = null; }
  document.getElementById('camWrap').style.display='none';
  document.getElementById('camControls').style.display='none';
  document.getElementById('startRow').style.display='flex';
}
document.getElementById('againBtn').onclick = function(){
  shots = [];
  document.getElementById('result').style.display='none';
  if(stream){ document.getElementById('camWrap').style.display='block'; document.getElementById('camControls').style.display='flex'; }
  else { document.getElementById('startRow').style.display='flex'; }
};
document.getElementById('saveBtn').onclick = function(){
  var c = document.getElementById('shotCanvas');
  var a = document.createElement('a');
  a.download = 'lea-photo-booth-' + Date.now() + '.png';
  a.href = c.toDataURL('image/png');
  a.click();
};
document.getElementById('snapBtn').onclick = countdown;
function countdown(){
  var n = 3;
  countEl.textContent = n;
  var iv = setInterval(function(){
    n--;
    if(n > 0){ countEl.textContent = n; }
    else if(n === 0){ countEl.textContent = ''; }
    else {
      clearInterval(iv);
      flashEl.style.opacity = .9; setTimeout(function(){ flashEl.style.opacity = 0; }, 220);
      capture();
    }
  }, 800);
}
function capture(){
  var c = document.createElement('canvas');
  c.width = video.videoWidth; c.height = video.videoHeight;
  var ctx = c.getContext('2d');
  ctx.translate(c.width, 0); ctx.scale(-1,1);
  ctx.drawImage(video, 0, 0);
  shots.push(c);
  if(mode === 'single'){ compose(shots); }
  else {
    var left = 3 - shots.length;
    if(left > 0){ hint(shots.length + ' of 3 taken, keep going'); }
    else { compose(shots); }
  }
}
function ensureFonts(){
  try {
    return Promise.all([
      document.fonts.load('800 58px Fraunces'),
      document.fonts.load('700 27px Inter'),
      document.fonts.load('800 24px Inter')
    ]).catch(function(e){});
  } catch(e){ return Promise.resolve(); }
}
function compose(parts){
  ensureFonts().then(function(){ doCompose(parts); });
}
function doCompose(parts){
  stopLive();
  var f = FRAMES[frameIdx];
  var strip = parts.length > 1;
  var out = document.createElement('canvas');
  var octx;
  var W = 1080;
  var photoX = 100, photoW = 880;
  if(strip){
    var phH = 1100, gap = 26;
    var head = 0, txtH = 250;
    out.width = W;
    out.height = 90 + 3*phH + 2*gap + txtH + 90;
    octx = out.getContext('2d');
    paintBg(octx, out.width, out.height);
    card(octx, 50, 50, W-100, out.height-100);
    var y = 90;
    for(var i=0;i<parts.length;i++){ drawFitted(octx, parts[i], photoX, y, photoW, phH, 26); y += phH + gap; }
    textBlock(octx, f, y + 10, txtH);
  } else {
    var phH2 = 1173, txtH2 = 250;
    out.width = W;
    out.height = 90 + phH2 + txtH2 + 90;
    octx = out.getContext('2d');
    paintBg(octx, out.width, out.height);
    card(octx, 50, 50, W-100, out.height-100);
    drawFitted(octx, parts[0], photoX, 90, photoW, phH2, 26);
    textBlock(octx, f, 90 + phH2 + 10, txtH2);
  }
  var c = document.getElementById('shotCanvas');
  c.width = out.width; c.height = out.height;
  c.getContext('2d').drawImage(out, 0, 0);
  document.getElementById('camWrap').style.display='none';
  document.getElementById('camControls').style.display='none';
  document.getElementById('startRow').style.display='none';
  document.getElementById('result').style.display='block';
  hint('');
}
function paintBg(ctx, w, h){
  var g = ctx.createLinearGradient(0,0,w,h);
  g.addColorStop(0,'#FBE4EC'); g.addColorStop(.55,'#F6DCF0'); g.addColorStop(1,'#DCCEF3');
  ctx.fillStyle = g; ctx.fillRect(0,0,w,h);
  function blob(x,y,r,color,alpha){
    ctx.save(); ctx.globalAlpha = alpha; ctx.fillStyle = color;
    ctx.beginPath(); ctx.arc(x,y,r,0,Math.PI*2); ctx.fill(); ctx.restore();
  }
  blob(120, 140, 220, '#FFB2BC', .35);
  blob(960, 200, 150, '#C9B6E4', .4);
  blob(930, h-160, 240, '#B9A5E8', .32);
  blob(150, h-220, 160, '#FFC9D2', .4);
}
function card(ctx, x, y, w, h){
  ctx.save();
  ctx.shadowColor = 'rgba(30,27,74,.30)';
  ctx.shadowBlur = 50; ctx.shadowOffsetY = 22;
  ctx.fillStyle = '#FFFFFF';
  ctx.beginPath(); roundRect(ctx, x, y, w, h, 46); ctx.fill();
  ctx.restore();
}
function textBlock(ctx, f, y, h){
  var cx = 540;
  var isz = 92;
  try { roundImage(ctx, ICON, cx - isz/2, y + 14, isz, 22); } catch(e){ ctx.drawImage(ICON, cx - isz/2, y + 14, isz, isz); }
  var headlineY = y + 14 + isz + 64;
  ctx.fillStyle = '#1E1B4A';
  ctx.font = '800 58px Fraunces, Georgia, serif';
  ctx.textAlign = 'center'; ctx.textBaseline = 'alphabetic';
  ctx.fillText(f.headline, cx, headlineY);
  var subY = headlineY + 52;
  ctx.fillStyle = '#7759A1';
  ctx.font = '800 27px Inter, Arial, sans-serif';
  var spaced = f.sub.split('').join(' ');
  ctx.fillText(spaced, cx, subY);
  ctx.fillStyle = 'rgba(119,89,161,.75)';
  ctx.font = '700 24px Inter, Arial, sans-serif';
  ctx.fillText('lea.legali.ai', cx, y + h - 28);
}
function roundImage(ctx, img, x, y, s, r){
  ctx.save();
  ctx.beginPath(); roundRect(ctx, x, y, s, s, r); ctx.clip();
  ctx.drawImage(img, x, y, s, s);
  ctx.restore();
}
function stopLive(){
  document.getElementById('camWrap').style.display='none';
  document.getElementById('camControls').style.display='none';
}
function drawFitted(ctx, img, x, y, w, h, r){
  var iw = img.width, ih = img.height;
  var s = Math.max(w/iw, h/ih);
  var dw = iw*s, dh = ih*s;
  ctx.save();
  ctx.beginPath(); roundRect(ctx, x, y, w, h, r); ctx.clip();
  ctx.fillStyle = '#1E1B4A'; ctx.fillRect(x, y, w, h);
  ctx.drawImage(img, x + (w-dw)/2, y + (h-dh)/2, dw, dh);
  ctx.restore();
}
function roundRect(ctx, x, y, w, h, r){
  ctx.moveTo(x+r, y);
  ctx.arcTo(x+w, y, x+w, y+h, r);
  ctx.arcTo(x+w, y+h, x, y+h, r);
  ctx.arcTo(x, y+h, x, y, r);
  ctx.arcTo(x, y, x+w, y, r);
  ctx.closePath();
}
</script>
</body>
</html>
"""
open("/workspace/photo-booth/index.html","w").write(HTML.replace("__ICON__", ICON))
print("index.html written", len(HTML))
