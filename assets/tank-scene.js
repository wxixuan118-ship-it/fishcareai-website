/*
 * FishCare animated tank scene — shared by the site's tools.
 * No dependencies. Usage:
 *   var tank = FishCareTank.mount(containerEl, { label: 'Your tank' });
 *   tank.setTank({ lengthIn: 24, plants: 'some', cloud: 0 });
 *   tank.setFish([{ key: 'neon', name: 'Neon tetra', count: 8, adultIn: 1.5, school: true }]);
 * Fish are drawn at adult length relative to the tank's length, live in
 * their natural water layer, and come to food when the water is clicked.
 */
(function (global) {
  'use strict';

  // ── Species looks ─────────────────────────────────────────────────────────
  // h: body height / length. tail: fork|round|fan|long|double|sword.
  // zone: top|mid|bottom|glass. Patterns are drawn inside the body outline.
  var LOOKS = {
    neon:      { h: .25, tail: 'fork', zone: 'mid', body: '#b9c7d2', pattern: 'neon', c1: '#25c4ff', c2: '#ff3434' },
    cardinal:  { h: .25, tail: 'fork', zone: 'mid', body: '#b9c7d2', pattern: 'neon', c1: '#25c4ff', c2: '#ff2f2f', full: true },
    ember:     { h: .30, tail: 'fork', zone: 'mid', body: '#ff7d3a', belly: '#ffb07a', fin: '#ff6a2a' },
    rummy:     { h: .25, tail: 'fork', zone: 'mid', body: '#cfd9de', pattern: 'head', c1: '#e8302f', tailC: '#f4f4f4', tailBars: '#151515' },
    harlequin: { h: .34, tail: 'fork', zone: 'mid', body: '#f2a07a', pattern: 'patch', c1: '#1d1d2a' },
    chili:     { h: .27, tail: 'fork', zone: 'mid', body: '#e8423a', pattern: 'hstripes', n: 1, c1: '#7a1612' },
    wcmm:      { h: .25, tail: 'fork', zone: 'top', body: '#b6a27a', pattern: 'hstripes', n: 1, c1: '#ece6cc', fin: '#e5533b' },
    guppy:     { h: .27, tail: 'fan',  zone: 'top', body: '#c9c4b8', tailVar: ['#ff7a1a', '#2f86ff', '#ff3a6e', '#ffd23a', '#7a4dff'] },
    endler:    { h: .25, tail: 'round', zone: 'top', body: '#9fa79a', pattern: 'spots', c1: '#ff7a1a', tailC: '#ff7a1a' },
    platy:     { h: .38, tail: 'round', zone: 'mid', bodyVar: ['#ff7a24', '#ffcf33', '#e8382f', '#3c6fd9'] },
    molly:     { h: .36, tail: 'round', zone: 'mid', bodyVar: ['#2a2a30', '#ecebe2', '#e8a33b'] },
    sword:     { h: .30, tail: 'sword', zone: 'mid', body: '#e8452f', fin: '#e8452f', c1: '#1a1a1a' },
    betta:     { h: .30, tail: 'long', zone: 'top', bodyVar: ['#b3122f', '#2747c9', '#e8e8f0', '#6b2fb8'], longFins: true },
    honey:     { h: .42, tail: 'round', zone: 'top', body: '#e9a43a', fin: '#f0c060', feelers: true },
    dwarfg:    { h: .44, tail: 'round', zone: 'top', body: '#e2563d', pattern: 'bars', n: 7, thin: true, c1: '#2f8fe8', feelers: true },
    pearlg:    { h: .42, tail: 'round', zone: 'mid', body: '#b2a690', pattern: 'spots', dense: true, c1: '#f4f0e6', feelers: true },
    cherryb:   { h: .34, tail: 'fork', zone: 'mid', body: '#d8382f', pattern: 'hstripes', n: 1, c1: '#5a1610' },
    tigerb:    { h: .42, tail: 'fork', zone: 'mid', body: '#f2b04a', pattern: 'bars', n: 4, c1: '#1a1a1a', fin: '#e8452f' },
    zebra:     { h: .22, tail: 'fork', zone: 'top', body: '#d9dfe8', pattern: 'hstripes', n: 3, c1: '#2c4fa0' },
    cory:      { h: .38, tail: 'fork', zone: 'bottom', body: '#9a958a', pattern: 'spots', c1: '#3b3a36', barbels: true, sail: .9, pauses: true, speed: .045 },
    pygmyc:    { h: .30, tail: 'fork', zone: 'mid', body: '#c9ccc8', pattern: 'hstripes', n: 1, c1: '#2a2a2a' },
    kuhli:     { kind: 'loach', h: .10, zone: 'bottom', body: '#e88b3a', c1: '#2a1a12', speed: .03, pauses: true },
    oto:       { h: .26, tail: 'round', zone: 'glass', body: '#b5a77d', pattern: 'hstripes', n: 1, c1: '#3a3326', speed: .006 },
    bn:        { h: .30, tail: 'round', zone: 'bottom', body: '#5a4c3c', pattern: 'spots', c1: '#e8e0c8', sail: 1.6, speed: .015, pauses: true },
    commonpl:  { h: .28, tail: 'fork', zone: 'bottom', body: '#6a5a44', pattern: 'spots', dense: true, c1: '#2f251a', sail: 1.8, speed: .015, pauses: true },
    angel:     { h: .90, tail: 'fork', zone: 'mid', body: '#d8dce0', pattern: 'bars', n: 3, c1: '#1f1f22', tallFins: true },
    discus:    { h: .95, tail: 'round', zone: 'mid', body: '#e37a35', pattern: 'bars', n: 9, thin: true, c1: '#2e9fc7', fringe: true },
    gbr:       { h: .42, tail: 'round', zone: 'mid', body: '#f2c24a', pattern: 'spots', c1: '#3aa0ff', fin: '#e8452f' },
    bolram:    { h: .40, tail: 'round', zone: 'mid', body: '#c9b48a', pattern: 'hstripes', n: 1, c1: '#2a2a2a', fin: '#e85a4a' },
    krib:      { h: .30, tail: 'round', zone: 'bottom', body: '#b9a07a', belly: '#e8456a', pattern: 'hstripes', n: 1, c1: '#2a2018', speed: .04 },
    yellowlab: { h: .33, tail: 'round', zone: 'mid', body: '#f5d51d', fin: '#1a1a1a' },
    oscar:     { h: .45, tail: 'round', zone: 'mid', body: '#3a3a2e', pattern: 'spots', c1: '#e8762a' },
    fancygf:   { h: .70, tail: 'double', zone: 'mid', bodyVar: ['#f08a24', '#f5f0e8', '#e8452f'], speed: .04 },
    commongf:  { h: .32, tail: 'fork', zone: 'mid', body: '#f08a24' },
    boes:      { h: .45, tail: 'fork', zone: 'mid', body: '#4f78c9', pattern: 'split', c1: '#f29a2a' },
    cherrys:   { kind: 'shrimp', zone: 'bottom', body: '#d82a2a', speed: .025, pauses: true },
    amano:     { kind: 'shrimp', zone: 'bottom', body: 'rgba(205,210,198,.8)', c1: '#5a5f66', speed: .025, pauses: true },
    nerite:    { kind: 'snail', zone: 'bottom', body: '#5a4a1e', c1: '#1d1a10', speed: .005 },
    mystery:   { kind: 'snail', zone: 'bottom', body: '#e8b93a', c1: '#8a5a1a', speed: .005 },
    clown:     { h: .42, tail: 'round', zone: 'mid', body: '#ff7a1a', pattern: 'clown' },
    koi:       { h: .30, tail: 'fork', zone: 'mid', bodyVar: ['#f4f1ea', '#f4f1ea', '#f08a24', '#f2d24a'], pattern: 'spots', big: true, c1: '#d8352a', barbels: true, speed: .05 },
    // Groupers hang near the rockwork; tangs patrol open water.
    grouper:   { h: .36, tail: 'round', zone: 'bottom', body: '#7a5a3a', pattern: 'spots', dense: true, c1: '#e8d9b0', speed: .025, pauses: true },
    grouper_red: { h: .36, tail: 'round', zone: 'bottom', body: '#c8372d', pattern: 'spots', dense: true, c1: '#5fc8ff', speed: .025, pauses: true },
    grouper_panther: { h: .46, tail: 'round', zone: 'bottom', body: '#ece8e0', pattern: 'spots', c1: '#1c1c1c', speed: .025, pauses: true },
    tang:      { h: .62, tail: 'fork', zone: 'mid', body: '#6b5a48', tailC: '#e8d24a', sail: .5 },
    tang_yellow: { h: .62, tail: 'fork', zone: 'mid', body: '#f7d31a', sail: .5 },
    tang_blue: { h: .55, tail: 'fork', zone: 'mid', body: '#3d7cff', belly: '#7fb0ff', pattern: 'patch', c1: '#0c1424', tailC: '#ffd400', fin: '#1d3f9e' },
    tang_purple: { h: .6, tail: 'fork', zone: 'mid', body: '#5a2a9a', tailC: '#f5d10f', sail: .5 },
    tang_powder: { h: .6, tail: 'fork', zone: 'mid', body: '#5fb3f0', pattern: 'head', c1: '#151a24', fin: '#f2d13a', sail: .5 },
    tang_convict: { h: .6, tail: 'fork', zone: 'mid', body: '#e9ece0', pattern: 'bars', n: 5, thin: true, c1: '#1a1a1a', sail: .5 },
    tang_sailfin: { h: .62, tail: 'fork', zone: 'mid', body: '#d9c58a', pattern: 'bars', n: 6, c1: '#5a3a24', tallFins: true },
    tang_achilles: { h: .58, tail: 'fork', zone: 'mid', body: '#1a1a1e', pattern: 'split', c1: '#ff6a1a', tailC: '#ff6a1a', sail: .4 },
    tang_naso: { h: .45, tail: 'fork', zone: 'mid', body: '#8a8f8f', fin: '#f2c23a', tailC: '#8a8f8f', sail: .4 },
    rb_praecox: { h: .38, tail: 'fork', zone: 'mid', body: '#8fc4f0', fin: '#e8452f' },
    rb_threadfin: { h: .3, tail: 'fan', zone: 'top', body: '#f0e2a0', fin: '#2a2a2a', longFins: true },
    rb_forktail: { h: .3, tail: 'fork', zone: 'top', body: '#c9d4a8', fin: '#f2b23a', tailC: '#e8452f' },
    rb_gertrudae: { h: .32, tail: 'round', zone: 'top', body: '#f0d880', pattern: 'spots', c1: '#3a2a1a', fin: '#f4f0e0' },
    rb_celebes: { h: .3, tail: 'fork', zone: 'mid', body: '#f2e070', pattern: 'hstripes', n: 1, c1: '#2a6ad8' },
    rb_turquoise: { h: .44, tail: 'fork', zone: 'mid', body: '#2ab8b0', pattern: 'hstripes', n: 1, c1: '#1a5a68' },
    rb_neonblue: { h: .42, tail: 'fork', zone: 'mid', body: '#3a7ae0', fin: '#e0e8f0' },
    rb_australian: { h: .42, tail: 'fork', zone: 'mid', body: '#9ab0a0', pattern: 'hstripes', n: 3, c1: '#e05a3a' },
    rb_splendid: { h: .44, tail: 'fork', zone: 'mid', body: '#7ab0c8', pattern: 'hstripes', n: 3, c1: '#f0d040', fin: '#e8452f' },
    rb_parkinsoni: { h: .44, tail: 'fork', zone: 'mid', body: '#c8ccc0', pattern: 'split', c1: '#f2a22a' },
    rb_red: { h: .44, tail: 'fork', zone: 'mid', body: '#d8382a', fin: '#c02a20' }
  };
  var DEFAULT_LOOK = { h: .3, tail: 'fork', zone: 'mid', body: '#9fb3bf' };

  // Standard US tank lengths (inches) by volume, for scaling fish to the tank.
  var STD = [[1, 8], [2.5, 12], [5, 16], [10, 20], [20, 24], [29, 30], [40, 36], [55, 48], [75, 48], [90, 48], [125, 72], [180, 72], [220, 72], [300, 96], [500, 120]];
  function lengthForGallons(g) {
    if (!(g > 0)) return 24;
    if (g <= STD[0][0]) return STD[0][1] * Math.cbrt(g / STD[0][0]);
    for (var i = 1; i < STD.length; i++) {
      if (g <= STD[i][0]) {
        var a = STD[i - 1], b = STD[i];
        return a[1] + (b[1] - a[1]) * (g - a[0]) / (b[0] - a[0]);
      }
    }
    var last = STD[STD.length - 1];
    return last[1] * Math.cbrt(g / last[0]);
  }

  var MAX_SHOWN = 60;
  var ZONES = { top: [.07, .3], mid: [.28, .7], bottom: [1, 1], glass: [.15, .85] };

  function rng(seed) {
    return function () {
      seed |= 0; seed = seed + 0x6D2B79F5 | 0;
      var t = Math.imul(seed ^ seed >>> 15, 1 | seed);
      t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t;
      return ((t ^ t >>> 14) >>> 0) / 4294967296;
    };
  }
  function clamp(v, a, b) { return v < a ? a : v > b ? b : v; }
  function rand(a, b) { return a + Math.random() * (b - a); }
  function pick(arr) { return arr[Math.floor(Math.random() * arr.length)]; }

  var cssDone = false;
  function injectCss() {
    if (cssDone) return; cssDone = true;
    var s = document.createElement('style');
    s.textContent =
      '.fct{position:relative;width:100%;aspect-ratio:16/9.4;border-radius:14px;overflow:hidden;background:#0b3a52;box-shadow:0 10px 30px rgba(0,0,0,.35)}' +
      '.fct canvas{display:block;width:100%;height:100%;cursor:pointer;touch-action:manipulation}' +
      '.fct .fct-feed{position:absolute;right:10px;bottom:10px;width:auto;margin:0;font:600 .78rem/1 system-ui,-apple-system,sans-serif;color:#05202f;background:rgba(247,252,255,.9);background-image:none;border:0;border-radius:999px;padding:7px 12px;cursor:pointer;box-shadow:0 2px 8px rgba(0,0,0,.25)}' +
      '.fct .fct-feed:hover{background:#fff}'+
      '.fct-fig{margin:18px 0 0}' +
      '.fct-fig .fct-views{display:flex;flex-wrap:wrap;gap:6px;margin:0 0 8px}' +
      '.fct-fig .fct-views button{width:auto;margin:0;font:600 .78rem/1 system-ui,-apple-system,sans-serif;padding:7px 12px;border-radius:999px;border:1px solid rgba(127,160,180,.55);background:transparent;background-image:none;box-shadow:none;color:inherit;cursor:pointer;opacity:.75}' +
      '.fct-fig .fct-views button[aria-pressed="true"]{opacity:1;background:rgba(70,182,232,.2);border-color:#46B6E8}' +
      '.fct-fig .fct-cap{font-size:.8rem;line-height:1.5;opacity:.78;margin-top:8px}' +
      '.fct-feed:focus-visible{outline:2px solid #46B6E8;outline-offset:2px}' +
      '.fct-hint{position:absolute;left:50%;top:12px;transform:translateX(-50%);font:500 .78rem/1 system-ui,-apple-system,sans-serif;color:#05202f;background:rgba(247,252,255,.82);border-radius:999px;padding:6px 12px;pointer-events:none;transition:opacity .6s;white-space:nowrap}' +
      '.fct-hint.off{opacity:0}' +
      '@media(prefers-reduced-motion:reduce){.fct-feed,.fct-hint{display:none}}';
    document.head.appendChild(s);
  }

  // ── Drawing helpers (fish faces +x, centred on origin, length L) ──────────
  function bodyPath(c, L, H) {
    c.beginPath();
    c.moveTo(L * .5, 0);
    c.bezierCurveTo(L * .38, -H * 1.08, -L * .12, -H * 1.0, -L * .32, -H * .2);
    c.lineTo(-L * .32, H * .2);
    c.bezierCurveTo(-L * .12, H * 1.0, L * .38, H * 1.08, L * .5, 0);
    c.closePath();
  }

  function tailPath(c, type, L, H, w) {
    var x0 = -L * .3;
    c.beginPath();
    if (type === 'fork' || type === 'sword') {
      c.moveTo(x0 + L * .04, 0);
      c.lineTo(x0 - L * .2, -H * .9 + w);
      c.lineTo(x0 - L * .11, w);
      c.lineTo(x0 - L * .2, H * .9 + w);
    } else {
      var k = { round: [1, .26], fan: [1.6, .38], long: [2.2, .55], double: [1.7, .46] }[type] || [1, .26];
      c.moveTo(x0 + L * .04, -H * .25);
      c.bezierCurveTo(x0 - L * k[1] * .6, -H * k[0] * 1.1 + w, x0 - L * k[1] * 1.1, -H * k[0] * .6 + w, x0 - L * k[1], w);
      c.bezierCurveTo(x0 - L * k[1] * 1.1, H * k[0] * .6 + w, x0 - L * k[1] * .6, H * k[0] * 1.1 + w, x0 + L * .04, H * .25);
    }
    c.closePath();
  }

  function drawPattern(c, F, L, H) {
    var lk = F.look, p = lk.pattern;
    if (!p) return;
    c.fillStyle = lk.c1;
    var i, x;
    if (p === 'neon') {
      c.fillStyle = lk.c2;
      c.fillRect(-L * .34, H * .05, (lk.full ? .78 : .38) * L, H);
      c.fillStyle = lk.c1;
      c.fillRect(-L * .26, -H * .32, L * .68, H * .34);
    } else if (p === 'bars') {
      var n = lk.n || 4, bw = L * (lk.thin ? .03 : .065);
      for (i = 0; i < n; i++) {
        x = L * .32 - (i + .5) * (L * .62 / n);
        c.fillRect(x - bw / 2, -H * 1.2, bw, H * 2.4);
      }
    } else if (p === 'hstripes') {
      var m = lk.n || 1;
      for (i = 0; i < m; i++) {
        var y = m === 1 ? -H * .05 : -H * .55 + i * (H * 1.1 / (m - 1));
        c.fillRect(-L * .34, y - H * .1, L * .8, H * .2);
      }
    } else if (p === 'spots') {
      var cnt = lk.big ? 5 : lk.dense ? 22 : 10, sr = Math.max(.6, H * (lk.big ? .5 : lk.dense ? .1 : .14));
      for (i = 0; i < cnt; i++) {
        c.beginPath();
        c.arc(-L * .3 + F.spots[i * 2] * L * .75, (F.spots[i * 2 + 1] - .5) * H * 1.7, sr, 0, 6.283);
        c.fill();
      }
    } else if (p === 'split') {
      c.fillRect(-L * .4, -H * 1.2, L * .4, H * 2.4);
    } else if (p === 'head') {
      c.fillRect(L * .26, -H * 1.2, L * .3, H * 2.4);
    } else if (p === 'patch') {
      c.fillStyle = lk.c1;
      c.beginPath();
      c.moveTo(-L * .3, -H * .5); c.lineTo(L * .08, -H * .45); c.lineTo(-L * .3, H * .55);
      c.closePath(); c.fill();
    } else if (p === 'clown') {
      var xs = [L * .27, L * .0, -L * .27], ws = [L * .07, L * .1, L * .05];
      for (i = 0; i < 3; i++) {
        c.fillStyle = '#151515'; c.fillRect(xs[i] - ws[i] / 2 - L * .015, -H * 1.2, ws[i] + L * .03, H * 2.4);
        c.fillStyle = '#ffffff'; c.fillRect(xs[i] - ws[i] / 2, -H * 1.2, ws[i], H * 2.4);
      }
    }
  }

  function drawFishBody(c, F, L, alpha) {
    var lk = F.look, H = L * lk.h / 2, w = Math.sin(F.phase) * H * .35;
    var finC = lk.fin || F.bodyC, tailC = F.tailC || lk.tailC || finC;
    c.globalAlpha = alpha * .85;
    c.fillStyle = finC;

    if (lk.tallFins) {
      c.beginPath(); c.moveTo(L * .12, -H * .6); c.lineTo(-L * .45, -H * 2.0 + w * .5); c.lineTo(-L * .25, -H * .4); c.closePath(); c.fill();
      c.beginPath(); c.moveTo(L * .12, H * .6); c.lineTo(-L * .45, H * 2.0 + w * .5); c.lineTo(-L * .25, H * .45); c.closePath(); c.fill();
    }
    if (lk.longFins) {
      c.beginPath(); c.moveTo(L * .05, -H * .85); c.quadraticCurveTo(-L * .25, -H * 1.9 + w, -L * .46, -H * 1.4 + w); c.lineTo(-L * .3, -H * .3); c.closePath(); c.fill();
      c.beginPath(); c.moveTo(L * .18, H * .7); c.quadraticCurveTo(-L * .2, H * 2.4 + w, -L * .5, H * 1.8 + w); c.lineTo(-L * .3, H * .3); c.closePath(); c.fill();
    }
    if (lk.fringe) {
      c.beginPath(); c.ellipse(-L * .02, 0, L * .46, H * 1.12, 0, 0, 6.283); c.fill();
    }
    if (lk.sail) {
      c.beginPath(); c.moveTo(L * .18, -H * .55); c.lineTo(L * .02, -H * (.8 + lk.sail) + w * .3); c.lineTo(-L * .16, -H * .5); c.closePath(); c.fill();
    } else if (!lk.tallFins && !lk.longFins && !lk.fringe) {
      c.beginPath(); c.moveTo(L * .1, -H * .6); c.lineTo(-L * .02, -H * 1.3 + w * .3); c.lineTo(-L * .14, -H * .5); c.closePath(); c.fill();
    }

    c.fillStyle = tailC;
    tailPath(c, lk.tail, L, H, w); c.fill();
    if (lk.tail === 'sword') {
      c.fillStyle = lk.c1 || '#1a1a1a';
      c.beginPath(); c.moveTo(-L * .32, H * .45 + w * .5); c.lineTo(-L * .62, H * .95 + w); c.lineTo(-L * .6, H * 1.1 + w); c.lineTo(-L * .32, H * .7); c.closePath(); c.fill();
    }
    if (lk.tailBars) {
      c.fillStyle = lk.tailBars;
      c.beginPath(); c.moveTo(-L * .3, -H * .1); c.lineTo(-L * .48, -H * .55 + w); c.lineTo(-L * .44, -H * .2 + w); c.closePath(); c.fill();
      c.beginPath(); c.moveTo(-L * .3, H * .1); c.lineTo(-L * .48, H * .55 + w); c.lineTo(-L * .44, H * .2 + w); c.closePath(); c.fill();
    }

    c.globalAlpha = alpha;
    var g = c.createLinearGradient(0, -H, 0, H);
    g.addColorStop(0, shade(F.bodyC, -.18));
    g.addColorStop(.55, F.bodyC);
    g.addColorStop(1, lk.belly || shade(F.bodyC, .25));
    c.fillStyle = g;
    bodyPath(c, L, H); c.fill();

    if (lk.pattern) {
      c.save(); bodyPath(c, L, H); c.clip(); drawPattern(c, F, L, H); c.restore();
    }

    if (lk.feelers) {
      c.strokeStyle = finC; c.lineWidth = Math.max(.6, L * .012);
      c.beginPath(); c.moveTo(L * .22, H * .6); c.quadraticCurveTo(L * .05, H * 1.6, -L * .12, H * 2.2 + w); c.stroke();
    }
    if (lk.barbels) {
      c.strokeStyle = shade(F.bodyC, .3); c.lineWidth = Math.max(.5, L * .015);
      c.beginPath(); c.moveTo(L * .46, H * .25); c.lineTo(L * .56, H * .6); c.stroke();
    }

    if (L > 9) {
      var er = clamp(H * .2, 1, L * .05);
      c.fillStyle = '#f7fbff'; c.beginPath(); c.arc(L * .32, -H * .2, er, 0, 6.283); c.fill();
      c.fillStyle = '#0c1014'; c.beginPath(); c.arc(L * .33, -H * .2, er * .6, 0, 6.283); c.fill();
    }
  }

  function drawLoach(c, F, L, alpha) {
    var H = L * F.look.h / 2, n = 12, pts = [];
    for (var i = 0; i <= n; i++) {
      var t = i / n;
      pts.push([L * .5 - t * L, Math.sin(F.phase - t * 4) * H * 1.3 * t]);
    }
    c.globalAlpha = alpha; c.lineCap = 'round';
    for (var j = 0; j < n; j++) {
      c.strokeStyle = j % 2 ? F.look.c1 : F.bodyC;
      c.lineWidth = H * 2 * (1 - j / n * .55);
      c.beginPath(); c.moveTo(pts[j][0], pts[j][1]); c.lineTo(pts[j + 1][0], pts[j + 1][1]); c.stroke();
    }
    c.lineCap = 'butt';
  }

  function drawShrimp(c, F, L, alpha) {
    var H = L * .12, w = Math.sin(F.phase * 1.5) * H * .3;
    c.globalAlpha = alpha;
    c.strokeStyle = F.bodyC; c.lineCap = 'round';
    c.lineWidth = Math.max(.6, L * .02);
    c.beginPath();
    for (var k = 0; k < 4; k++) {
      var lx = L * (.2 - k * .12);
      c.moveTo(lx, H * .3); c.lineTo(lx + L * .03, H * 1.4 + (k % 2 ? w : -w));
    }
    c.moveTo(L * .4, -H * .2); c.quadraticCurveTo(L * .8, -H * 2.2, L * 1.0, -H * 1.2 + w);
    c.moveTo(L * .4, -H * .1); c.quadraticCurveTo(L * .75, -H * .5, L * .95, H * .6 - w);
    c.stroke();
    c.lineWidth = H * 1.5;
    c.beginPath(); c.moveTo(-L * .38, H * .2); c.quadraticCurveTo(0, -H * 1.5, L * .38, 0); c.stroke();
    c.fillStyle = F.bodyC;
    c.beginPath(); c.moveTo(-L * .36, H * .1); c.lineTo(-L * .55, -H * .4 + w); c.lineTo(-L * .55, H * .9 + w); c.closePath(); c.fill();
    if (F.look.c1) {
      c.fillStyle = F.look.c1;
      for (var d = 0; d < 6; d++) { c.beginPath(); c.arc(-L * .3 + d * L * .12, -H * .25 - Math.sin(d / 5 * 3.1) * H * .5, Math.max(.4, H * .15), 0, 6.283); c.fill(); }
    }
    c.fillStyle = '#111'; c.beginPath(); c.arc(L * .38, -H * .35, Math.max(.6, H * .25), 0, 6.283); c.fill();
    c.lineCap = 'butt';
  }

  function drawSnail(c, F, L, alpha) {
    var r = L * .32;
    c.globalAlpha = alpha;
    c.fillStyle = 'rgba(215,205,182,.95)';
    c.beginPath(); c.ellipse(L * .05, r * .55, L * .48, L * .1, 0, 0, 6.283); c.fill();
    c.strokeStyle = 'rgba(215,205,182,.95)'; c.lineWidth = Math.max(.5, L * .03);
    c.beginPath(); c.moveTo(L * .45, r * .5); c.lineTo(L * .6, r * .05); c.moveTo(L * .4, r * .5); c.lineTo(L * .5, -r * .05); c.stroke();
    c.fillStyle = F.bodyC;
    c.beginPath(); c.arc(-L * .05, 0, r, 0, 6.283); c.fill();
    c.strokeStyle = F.look.c1; c.lineWidth = Math.max(.6, r * .14);
    c.beginPath(); c.arc(-L * .05, 0, r * .62, -.5, 4.2); c.stroke();
    c.beginPath(); c.arc(-L * .05, 0, r * .28, 1, 5.5); c.stroke();
  }

  function shade(hex, amt) {
    if (hex.charAt(0) !== '#') return hex;
    var n = parseInt(hex.slice(1), 16), r = n >> 16, g = n >> 8 & 255, b = n & 255;
    var t = amt < 0 ? 0 : 255, p = Math.abs(amt);
    r = Math.round((t - r) * p + r); g = Math.round((t - g) * p + g); b = Math.round((t - b) * p + b);
    return 'rgb(' + r + ',' + g + ',' + b + ')';
  }

  // ── Scene ────────────────────────────────────────────────────────────────
  function mount(container, opts) {
    opts = opts || {};
    injectCss();
    var reduce = global.matchMedia && global.matchMedia('(prefers-reduced-motion: reduce)').matches;

    var wrap = document.createElement('div');
    wrap.className = 'fct';
    var cv = document.createElement('canvas');
    cv.setAttribute('role', 'img');
    cv.setAttribute('aria-label', opts.label || 'Animated aquarium');
    var hint = document.createElement('div');
    hint.className = 'fct-hint';
    hint.textContent = 'Tap the water to feed your fish';
    var btn = document.createElement('button');
    btn.type = 'button'; btn.className = 'fct-feed'; btn.textContent = 'Feed fish';
    wrap.appendChild(cv); wrap.appendChild(hint); wrap.appendChild(btn);
    container.appendChild(wrap);
    var ctx = cv.getContext('2d');

    var tank = { lengthIn: 24, plants: 'none', cloud: 0 };
    var fish = [], flakes = [], bubbles = [], schools = {}, plants = [], rocks = [];
    var lay = null, running = false, visible = true, raf = 0, last = 0, time = 0, fed = false;

    function layout() {
      var r = wrap.getBoundingClientRect();
      var dpr = Math.min(2, global.devicePixelRatio || 1);
      var W = Math.max(200, r.width), Hh = Math.max(120, r.height);
      cv.width = Math.round(W * dpr); cv.height = Math.round(Hh * dpr);
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      var pad = 6;
      lay = { W: W, H: Hh, wl: pad, wr: W - pad, wt: Hh * .07, wb: Hh * .8, sb: Hh - pad };
      lay.ww = lay.wr - lay.wl; lay.wh = lay.wb - lay.wt; lay.ah = lay.wh / lay.ww;
      fish.forEach(sizeFish);
    }

    function buildDecor() {
      var r = rng(7);
      rocks = [
        { x: .18, w: .13, h: .12, pts: rockPts(r) },
        { x: .7, w: .09, h: .08, pts: rockPts(r) }
      ];
      var n = { none: 1, some: 5, heavy: 11 }[tank.plants] || 1;
      var rp = rng(42);
      plants = [];
      for (var i = 0; i < n; i++) {
        var blades = [];
        var bn = 3 + Math.floor(rp() * 4), ht = .3 + rp() * .45;
        for (var b = 0; b < bn; b++) blades.push({ dx: (rp() - .5) * .025, h: ht * (.6 + rp() * .4), lean: (rp() - .5) * .08, w: 2 + rp() * 3 });
        plants.push({
          x: n === 1 ? .86 : .04 + (i + rp() * .6) / n * .92,
          front: i % 3 === 2,
          hue: 95 + rp() * 40, light: 28 + rp() * 14, blades: blades, ph: rp() * 6
        });
      }
    }
    function rockPts(r) {
      var pts = [], k = 9;
      for (var i = 0; i <= k; i++) {
        var a = Math.PI * (1 - i / k);
        pts.push([Math.cos(a) * (.8 + r() * .25), -Math.sin(a) * (.75 + r() * .3)]);
      }
      return pts;
    }

    function sizeFish(F) {
      if (!lay) return;
      F.Lp = clamp(F.adultIn / tank.lengthIn * lay.ww, 7, lay.ww * .75);
      var lk = F.look, k = lk.kind;
      var hh = k === 'snail' ? F.Lp * .4 : k === 'shrimp' ? F.Lp * .2 : k === 'loach' ? F.Lp * .12 : F.Lp * lk.h / 2 * (lk.tallFins ? 2 : 1.25);
      F.hpx = hh;
      F.halfW = F.Lp / 2 / lay.ww + .01;
    }

    function zoneRange(F) {
      var z = F.look.zone, hy = F.hpx / lay.wh;
      if (z === 'bottom') {
        var base = 1 - hy - 2 / lay.wh;
        return [base - .02, base + .07];
      }
      var r = ZONES[z] || ZONES.mid;
      return [clamp(r[0], hy + .02, .98), clamp(r[1], hy + .04, 1 - hy - .03)];
    }

    function newTarget(F) {
      var zr = zoneRange(F);
      F.tx = rand(F.halfW, 1 - F.halfW);
      F.ty = rand(zr[0], zr[1]);
      F.t = rand(3, 9);
    }

    function makeFish(item, idx) {
      var look = LOOKS[item.key] || DEFAULT_LOOK;
      var sp = [];
      for (var i = 0; i < 44; i++) sp.push(Math.random());
      var F = {
        key: item.key, look: look, adultIn: item.adultIn || 2, school: !!item.school && !look.kind,
        bodyC: look.bodyVar ? pick(look.bodyVar) : look.body,
        tailC: look.tailVar ? pick(look.tailVar) : null,
        spots: sp, phase: Math.random() * 6, f: Math.random() < .5 ? -1 : 1, tilt: 0,
        vx: 0, vy: 0, alpha: reduce || !running ? 1 : 0, dying: false, pause: 0,
        off: { x: rand(-.12, .12), y: rand(-.09, .09) }
      };
      sizeFish(F);
      var zr = lay ? zoneRange(F) : [.4, .6];
      F.x = rand(F.halfW || .1, 1 - (F.halfW || .1));
      F.y = rand(zr[0], zr[1]);
      newTarget(F);
      if (F.look.zone === 'glass') { F.y = rand(zr[0], zr[1]); F.x = rand(.1, .9); }
      void idx;
      return F;
    }

    function setFish(list) {
      list = (list || []).filter(function (it) { return it && it.count > 0; });
      var total = list.reduce(function (s, it) { return s + it.count; }, 0);
      var scale = total > MAX_SHOWN ? MAX_SHOWN / total : 1;
      var shown = 0;
      var want = {};
      list.forEach(function (it) {
        var n = Math.max(1, Math.round(it.count * scale));
        want[it.key] = { n: n, item: it };
        shown += n;
      });
      // Remove species no longer present and trim extras.
      var have = {};
      fish.forEach(function (F) {
        if (F.dying) return;
        var w = want[F.key];
        have[F.key] = (have[F.key] || 0) + 1;
        if (!w || have[F.key] > w.n) { F.dying = true; if (reduce || !running) F.alpha = 0; }
        else { F.adultIn = w.item.adultIn || F.adultIn; F.school = !!w.item.school && !F.look.kind; sizeFish(F); }
      });
      Object.keys(want).forEach(function (k) {
        var cur = have[k] || 0;
        if (cur > want[k].n) cur = want[k].n;
        for (var i = cur; i < want[k].n; i++) fish.push(makeFish(want[k].item, i));
        if (!schools[k]) schools[k] = { x: rand(.25, .75), y: .5, tx: .5, ty: .5, t: 0 };
      });
      fish = fish.filter(function (F) { return !(F.dying && F.alpha <= 0); });
      cv.setAttribute('aria-label', list.length
        ? 'Animated aquarium showing ' + list.map(function (it) { return it.count + ' ' + (it.name || it.key); }).join(', ') + ' at adult size, to scale with the tank.'
        : 'Animated aquarium with no fish yet.');
      if (!running) draw();
      return { shown: shown, total: total };
    }

    function setTank(t) {
      var plantsChanged = t.plants && t.plants !== tank.plants;
      if (t.lengthIn > 0) tank.lengthIn = t.lengthIn;
      if (t.plants) tank.plants = t.plants;
      if (typeof t.cloud === 'number') tank.cloud = clamp(t.cloud, 0, 1);
      if (plantsChanged || !plants.length) buildDecor();
      fish.forEach(sizeFish);
      fish.forEach(function (F) { var zr = zoneRange(F); F.y = clamp(F.y, zr[0], zr[1]); F.x = clamp(F.x, F.halfW, 1 - F.halfW); });
      if (!running) draw();
    }

    function feed(xNorm) {
      if (reduce) return;
      var cx = typeof xNorm === 'number' ? xNorm : rand(.2, .8);
      for (var i = 0; i < 9; i++) {
        flakes.push({ x: clamp(cx + rand(-.05, .05), .02, .98), y: rand(.0, .02), vy: rand(.04, .08), ph: Math.random() * 6, rest: 0, c: Math.random() < .5 ? '#c8742a' : '#e3a24e', s: rand(1.6, 2.8) });
      }
      if (!fed) { fed = true; hint.classList.add('off'); }
    }

    cv.addEventListener('click', function (e) {
      var r = cv.getBoundingClientRect();
      feed((e.clientX - r.left - lay.wl) / lay.ww);
    });
    btn.addEventListener('click', function () { feed(); });

    // ── Simulation ──────────────────────────────────────────────────────────
    function canReach(F, fl) {
      var z = F.look.zone;
      if (z === 'glass') return false;
      if (z === 'bottom') return fl.y > .75;
      if (z === 'top') return fl.y < .65;
      return fl.y < .92;
    }

    function step(dt) {
      time += dt;
      Object.keys(schools).forEach(function (k) {
        var s = schools[k];
        s.t -= dt;
        if (s.t <= 0) { s.tx = rand(.15, .85); s.ty = rand(.2, .8); s.t = rand(4, 9); }
        s.x += (s.tx - s.x) * dt * .25;
        s.y += (s.ty - s.y) * dt * .25;
      });

      for (var i = 0; i < flakes.length; i++) {
        var fl = flakes[i];
        if (fl.y < 1) {
          fl.y += fl.vy * dt; fl.ph += dt * 2; fl.x += Math.sin(fl.ph) * .004 * dt;
          if (fl.y >= 1) { fl.y = 1; fl.rest = 8; }
        } else {
          fl.rest -= dt;
        }
      }
      flakes = flakes.filter(function (f) { return !f.eaten && !(f.y >= 1 && f.rest <= 0); });

      fish.forEach(function (F) {
        if (F.dying) { F.alpha -= running ? dt * 1.6 : 1; return; }
        if (F.alpha < 1) F.alpha = Math.min(1, F.alpha + dt * 1.4);
        var lk = F.look, zr = zoneRange(F);
        var base = lk.speed || clamp(.05 + F.Lp / lay.ww * .35, .05, .16);
        var spd = base, food = null, best = .5;

        for (var j = 0; j < flakes.length; j++) {
          var f = flakes[j];
          if (!canReach(F, f)) continue;
          var d = Math.abs(f.x - F.x) + Math.abs(f.y - F.y) * lay.ah;
          if (d < best) { best = d; food = f; }
        }

        var tx, ty;
        if (food) {
          tx = food.x; ty = clamp(food.y, zr[0] - (lk.zone === 'bottom' ? 0 : .3), zr[1] + .3);
          spd = base * (lk.zone === 'bottom' ? 1.4 : 2);
          F.pause = 0;
        } else if (F.school && schools[F.key]) {
          var s = schools[F.key];
          tx = s.x + F.off.x; ty = s.y + F.off.y;
        } else {
          F.t -= dt;
          if (F.t <= 0 || Math.abs(F.tx - F.x) < .02 && Math.abs(F.ty - F.y) < .03) newTarget(F);
          tx = F.tx; ty = F.ty;
        }
        tx = clamp(tx, F.halfW, 1 - F.halfW);
        ty = clamp(ty, zr[0], Math.max(zr[0], zr[1]));
        if (food) ty = clamp(food.y, F.hpx / lay.wh + .01, 1 - F.hpx / lay.wh);

        if (lk.pauses && !food) {
          if (F.pause > 0) F.pause -= dt;
          else if (Math.random() < dt * .25) F.pause = rand(.6, 2.5);
        }

        var dx = tx - F.x, dy = (ty - F.y) * lay.ah;
        var dist = Math.sqrt(dx * dx + dy * dy) || 1e-6;
        var sp = F.pause > 0 ? 0 : spd * Math.min(1, dist / .05);
        var dvx = dx / dist * sp, dvy = dy / dist * sp;
        var k = Math.min(1, dt * (food ? 3 : 1.6));
        F.vx += (dvx - F.vx) * k; F.vy += (dvy - F.vy) * k;
        F.x = clamp(F.x + F.vx * dt, F.halfW, 1 - F.halfW);
        F.y += F.vy * dt / lay.ah;
        var lo = food ? F.hpx / lay.wh + .01 : zr[0] - .03, hi = food ? 1 - F.hpx / lay.wh : zr[1] + .03;
        F.y = clamp(F.y, Math.min(lo, hi), Math.max(lo, hi));

        var dir = F.vx > .003 ? 1 : F.vx < -.003 ? -1 : (F.f >= 0 ? 1 : -1);
        F.f += (dir - F.f) * Math.min(1, dt * 5);
        var tiltT = lk.zone === 'bottom' || lk.zone === 'glass' ? 0 : clamp(Math.atan2(F.vy, Math.abs(F.vx) + .01), -.35, .35);
        F.tilt += (tiltT - F.tilt) * Math.min(1, dt * 3);
        var speedNow = Math.sqrt(F.vx * F.vx + F.vy * F.vy);
        F.phase += dt * (3 + speedNow / (base || .05) * 7);

        if (food) {
          var ex = Math.abs(food.x - F.x) * lay.ww, ey = Math.abs(food.y - F.y) * lay.wh;
          if (ex < F.Lp * .45 + 3 && ey < F.hpx + 3) food.eaten = true;
        }
      });
      fish = fish.filter(function (F) { return !(F.dying && F.alpha <= 0); });

      if (Math.random() < dt * 7) bubbles.push({ x: .93 + rand(-.006, .006), y: 1, r: rand(1.2, 3.4), ph: Math.random() * 6, v: rand(.28, .45) });
      bubbles.forEach(function (b) { b.y -= b.v * dt; b.ph += dt * 5; });
      bubbles = bubbles.filter(function (b) { return b.y > 0; });
    }

    // ── Rendering ───────────────────────────────────────────────────────────
    function X(n) { return lay.wl + n * lay.ww; }
    function Y(n) { return lay.wt + n * lay.wh; }

    function drawPlants(front) {
      plants.forEach(function (p, pi) {
        if (p.front !== front) return;
        var bx = X(p.x), by = lay.wb + lay.wh * .04;
        p.blades.forEach(function (b, bi) {
          var sway = reduce ? 0 : Math.sin(time * .9 + p.ph + bi * .7) * lay.ww * .012;
          var top = by - b.h * lay.wh, x0 = bx + b.dx * lay.ww;
          var x1 = x0 + b.lean * lay.ww + sway;
          ctx.strokeStyle = 'hsl(' + p.hue + ',55%,' + (p.light + bi * 2) + '%)';
          ctx.lineWidth = b.w; ctx.lineCap = 'round';
          ctx.beginPath(); ctx.moveTo(x0, by);
          ctx.quadraticCurveTo(x0 + sway * .3, (by + top) / 2, x1, top);
          ctx.stroke();
        });
        void pi;
      });
      ctx.lineCap = 'butt';
    }

    function drawOne(F) {
      var x = X(F.x), y = Y(F.y), L = F.Lp, a = clamp(F.alpha, 0, 1);
      ctx.save();
      ctx.translate(x, y);
      ctx.rotate(F.f >= 0 ? F.tilt : -F.tilt);
      var sx = F.f;
      if (Math.abs(sx) < .12) sx = sx < 0 ? -.12 : .12;
      ctx.scale(sx, 1);
      var k = F.look.kind;
      if (k === 'loach') drawLoach(ctx, F, L, a);
      else if (k === 'shrimp') drawShrimp(ctx, F, L, a);
      else if (k === 'snail') drawSnail(ctx, F, L, a);
      else drawFishBody(ctx, F, L, a);
      ctx.restore();
      ctx.globalAlpha = 1;
    }

    function draw() {
      if (!lay) return;
      var W = lay.W, H = lay.H;
      ctx.clearRect(0, 0, W, H);

      // air gap + back glass
      ctx.fillStyle = '#0d2a3a'; ctx.fillRect(0, 0, W, H);
      var wg = ctx.createLinearGradient(0, lay.wt, 0, lay.wb);
      wg.addColorStop(0, '#6cc6df'); wg.addColorStop(.55, '#3d97bb'); wg.addColorStop(1, '#22698d');
      ctx.fillStyle = wg;
      ctx.fillRect(lay.wl, lay.wt, lay.ww, lay.sb - lay.wt);

      // light rays
      ctx.save();
      ctx.globalCompositeOperation = 'lighter';
      for (var r = 0; r < 4; r++) {
        var cx = X(.15 + r * .24 + (reduce ? 0 : Math.sin(time * .12 + r * 1.7) * .04));
        var rg = ctx.createLinearGradient(0, lay.wt, 0, lay.wb);
        rg.addColorStop(0, 'rgba(255,255,240,.10)'); rg.addColorStop(1, 'rgba(255,255,240,0)');
        ctx.fillStyle = rg;
        ctx.beginPath();
        ctx.moveTo(cx - lay.ww * .03, lay.wt); ctx.lineTo(cx + lay.ww * .03, lay.wt);
        ctx.lineTo(cx + lay.ww * .1, lay.wb); ctx.lineTo(cx - lay.ww * .02, lay.wb); ctx.closePath(); ctx.fill();
      }
      ctx.restore();

      drawPlants(false);

      // rocks
      rocks.forEach(function (rk) {
        var bx = X(rk.x), by = lay.wb + lay.wh * .03, rw = rk.w * lay.ww / 2, rh = rk.h * lay.wh * 1.6;
        var g = ctx.createLinearGradient(0, by - rh, 0, by);
        g.addColorStop(0, '#8a8478'); g.addColorStop(1, '#4e4a43');
        ctx.fillStyle = g;
        ctx.beginPath();
        rk.pts.forEach(function (p, i) { var px = bx + p[0] * rw, py = by + p[1] * rh; if (i) ctx.lineTo(px, py); else ctx.moveTo(px, py); });
        ctx.closePath(); ctx.fill();
      });

      // sand
      var sg = ctx.createLinearGradient(0, lay.wb, 0, lay.sb);
      sg.addColorStop(0, '#e0c99a'); sg.addColorStop(.25, '#cdb282'); sg.addColorStop(1, '#8f7652');
      ctx.fillStyle = sg;
      ctx.beginPath();
      ctx.moveTo(lay.wl, lay.wb + lay.wh * .02);
      for (var s = 0; s <= 10; s++) ctx.lineTo(X(s / 10), lay.wb + Math.sin(s * 1.3) * lay.wh * .012);
      ctx.lineTo(lay.wr, lay.sb); ctx.lineTo(lay.wl, lay.sb); ctx.closePath(); ctx.fill();
      ctx.fillStyle = 'rgba(90,70,40,.25)';
      var sr = rng(3);
      for (var d = 0; d < 70; d++) ctx.fillRect(X(sr()), lay.wb + lay.wh * .03 + sr() * (lay.sb - lay.wb - lay.wh * .03), 1.4, 1.4);

      // fish: bottom dwellers first, then by size so small fish stay visible
      var order = fish.slice().sort(function (a, b) {
        var za = a.look.zone === 'bottom' ? 0 : 1, zb = b.look.zone === 'bottom' ? 0 : 1;
        return za - zb || b.Lp - a.Lp;
      });
      order.forEach(drawOne);

      drawPlants(true);

      flakes.forEach(function (f) {
        ctx.globalAlpha = f.y >= 1 ? clamp(f.rest / 2, 0, 1) : 1;
        ctx.fillStyle = f.c;
        ctx.fillRect(X(f.x) - f.s / 2, Y(Math.min(f.y, 1.02)) - f.s / 2, f.s, f.s * .7);
      });
      ctx.globalAlpha = 1;

      ctx.strokeStyle = 'rgba(240,252,255,.6)'; ctx.lineWidth = 1;
      bubbles.forEach(function (b) {
        ctx.beginPath(); ctx.arc(X(b.x + Math.sin(b.ph) * .004), Y(b.y), b.r, 0, 6.283); ctx.stroke();
      });

      // airstone
      ctx.fillStyle = '#3a3f44';
      ctx.fillRect(X(.93) - 7, lay.wb + lay.wh * .01, 14, 5);

      // cloudy water when the tank is overloaded
      if (tank.cloud > 0) {
        ctx.fillStyle = 'rgba(112,118,58,' + (tank.cloud * .45).toFixed(3) + ')';
        ctx.fillRect(lay.wl, lay.wt, lay.ww, lay.sb - lay.wt);
      }

      // surface
      ctx.fillStyle = 'rgba(235,250,255,.35)';
      ctx.beginPath();
      ctx.moveTo(lay.wl, lay.wt);
      for (var q = 0; q <= 24; q++) ctx.lineTo(X(q / 24), lay.wt + Math.sin(q * .9 + time * 1.6) * 1.5 + 2);
      ctx.lineTo(lay.wr, lay.wt - 2); ctx.lineTo(lay.wl, lay.wt - 2); ctx.closePath(); ctx.fill();

      // glass frame
      ctx.strokeStyle = 'rgba(200,235,250,.35)'; ctx.lineWidth = 2;
      ctx.strokeRect(lay.wl - 1, lay.wt - 4, lay.ww + 2, lay.sb - lay.wt + 3);
      var hg = ctx.createLinearGradient(lay.wl, 0, lay.wl + lay.ww * .25, 0);
      hg.addColorStop(0, 'rgba(255,255,255,.10)'); hg.addColorStop(1, 'rgba(255,255,255,0)');
      ctx.fillStyle = hg; ctx.fillRect(lay.wl, lay.wt, lay.ww * .25, lay.sb - lay.wt);
    }

    function loop(ts) {
      raf = 0;
      if (!running) return;
      var dt = last ? Math.min(.05, (ts - last) / 1000) : .016;
      last = ts;
      step(dt);
      draw();
      raf = global.requestAnimationFrame(loop);
    }
    function sync() {
      var should = !reduce && visible && !document.hidden;
      if (should && !running) { running = true; last = 0; raf = global.requestAnimationFrame(loop); }
      else if (!should && running) { running = false; if (raf) global.cancelAnimationFrame(raf); raf = 0; }
    }

    layout(); buildDecor();
    if (global.ResizeObserver) new ResizeObserver(function () { layout(); if (!running) draw(); }).observe(wrap);
    else global.addEventListener('resize', function () { layout(); if (!running) draw(); });
    if (global.IntersectionObserver) {
      new IntersectionObserver(function (es) { visible = es[0].isIntersecting; sync(); }, { rootMargin: '80px' }).observe(wrap);
    }
    document.addEventListener('visibilitychange', sync);
    sync();
    if (reduce) draw();

    return { setFish: setFish, setTank: setTank, feed: feed, el: wrap, _state: function () { return { fish: fish, flakes: flakes, lay: lay, running: running }; },
      _tick: function (n) { for (var i = 0; i < (n || 1); i++) step(1 / 60); draw(); } };
  }

  // ── attach(): tank + caption + optional view toggle after an element ────
  // views: [{ label, gallons, lengthIn?, plants?, fish: [...], note? }]
  function attach(anchor, opts) {
    opts = opts || {};
    injectCss();
    var fig = document.createElement('figure');
    fig.className = 'fct-fig';
    var bar = document.createElement('div');
    bar.className = 'fct-views'; bar.setAttribute('role', 'group'); bar.setAttribute('aria-label', 'Tank to show');
    bar.hidden = true;
    var stage = document.createElement('div');
    var cap = document.createElement('figcaption');
    cap.className = 'fct-cap';
    fig.appendChild(bar); fig.appendChild(stage); fig.appendChild(cap);
    anchor.parentNode.insertBefore(fig, anchor.nextSibling);
    var scene = mount(stage, opts);
    var views = [], sel = 0, labels = '';

    function fmt(n) { return Math.round(n).toLocaleString('en-US'); }
    function caption(v, len, info) {
      var main = v.fish[0];
      if (!main) return v.note || '';
      var parts = v.fish.map(function (f) { return f.count + ' ' + f.name; });
      var names = parts.length > 1 ? parts.slice(0, -1).join(', ') + ' and ' + parts[parts.length - 1] : parts[0];
      var vessel = opts.vessel || 'tank';
      var t = names + ' at adult size, drawn to scale in a ' + fmt(v.gallons) + '-gallon ' + vessel + ' about ' +
        fmt(len) + ' in (' + fmt(len * 2.54) + ' cm) long. ';
      var big = v.fish.reduce(function (a, f) { return f.adultIn > a.adultIn ? f : a; }, main);
      t += 'At ' + big.adultIn + ' in, one ' + (big.single || big.name) + ' is ' + fmt(big.adultIn / len * 100) + '% of the ' + vessel + ' length.';
      if (info.shown < info.total) t += ' Showing ' + info.shown + ' of ' + info.total + ' fish.';
      if (v.note) t += ' ' + v.note;
      return t;
    }
    function apply() {
      var v = views[sel];
      if (!v) return;
      var len = v.lengthIn || lengthForGallons(v.gallons);
      scene.setTank({ lengthIn: len, plants: v.plants || opts.plants || 'some', cloud: v.cloud || 0 });
      var info = scene.setFish(v.fish);
      cap.textContent = caption(v, len, info);
      Array.prototype.forEach.call(bar.children, function (b, i) { b.setAttribute('aria-pressed', i === sel ? 'true' : 'false'); });
    }
    function show(vs) {
      views = vs || [];
      if (sel >= views.length) sel = 0;
      var l = views.map(function (v) { return v.label || ''; }).join('|');
      if (l !== labels) {
        labels = l;
        bar.innerHTML = '';
        views.forEach(function (v, i) {
          var b = document.createElement('button');
          b.type = 'button'; b.textContent = v.label || ('Tank ' + (i + 1));
          b.addEventListener('click', function () { sel = i; apply(); });
          bar.appendChild(b);
        });
        bar.hidden = views.length < 2;
      }
      fig.hidden = !views.length;
      apply();
    }
    return { scene: scene, show: show, el: fig };
  }

  global.FishCareTank = { mount: mount, attach: attach, lengthForGallons: lengthForGallons, LOOKS: LOOKS };
})(window);
