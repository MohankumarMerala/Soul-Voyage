// master.js — Soul Voyage
// Particles loop in smooth sinusoidal/orbital paths.
// Uses its OWN canvas (#particles-canvas) — never touches #canvas (Milky Way).

document.querySelectorAll('[data-bg]').forEach(function (el) {
  el.style.backgroundImage = 'url("' + el.getAttribute('data-bg') + '")';
});

(function () {

  /* ── Create dedicated particle canvas ── */
  var pc = document.createElement('canvas');
  pc.id = 'particles-canvas';
  pc.style.position = 'fixed';
  pc.style.top = '0';
  pc.style.left = '0';
  pc.style.width = '100%';
  pc.style.height = '100%';
  pc.style.pointerEvents = 'none';
  pc.style.zIndex = '1';
  document.body.insertBefore(pc, document.body.firstChild);

  var ctx = pc.getContext('2d');
  var W, H;
  var mouse = { x: -9999, y: -9999 };

  function rand(a, b) { return a + Math.random() * (b - a); }

  var COLORS = [
    'rgba(249,241,204,',
    'rgba(201,168,76,',
    'rgba(232,210,150,',
    'rgba(255,248,220,',
    'rgba(180,155,85,',
    'rgba(255,235,160,',
  ];

  /* ── Particle ── */
  function Particle(fromClick, cx, cy) {
    this.born = !!fromClick;

    if (fromClick) {
      /* Click-burst — explodes outward then fades */
      this.x = cx;
      this.y = cy;
      this.size = rand(2, 5);
      this.alpha = rand(0.7, 1.0);
      this.decay = rand(0.012, 0.022);
      this.vx = rand(-3.0, 3.0);
      this.vy = rand(-3.0, 3.0);
      this.glow = rand(6, 22);
      this.color = COLORS[Math.floor(Math.random() * COLORS.length)];
      /* no loop params needed */
    } else {
      /* Ambient — loops in a smooth sinusoidal orbital path */
      this.size = rand(1.2, 3.8);
      this.color = COLORS[Math.floor(Math.random() * COLORS.length)];
      this.alpha = rand(0.15, 0.70);
      this.glow = rand(5, 22);

      /* base position — random across screen */
      this.bx = Math.random() * W;   /* base x (centre of x oscillation) */
      this.by = Math.random() * H;   /* base y (centre of y oscillation) */

      /* loop parameters */
      this.ax = rand(20, 180);     /* x amplitude */
      this.ay = rand(15, 120);     /* y amplitude */
      this.speedX = rand(0.003, 0.012); /* x angular speed */
      this.speedY = rand(0.004, 0.014); /* y angular speed (different → Lissajous) */
      this.phaseX = Math.random() * Math.PI * 2; /* x phase offset */
      this.phaseY = Math.random() * Math.PI * 2; /* y phase offset */

      /* current position (computed each frame) */
      this.x = this.bx;
      this.y = this.by;

      /* pulse */
      this.pulse = Math.random() * Math.PI * 2;
      this.pulseSpeed = rand(0.008, 0.025);

      /* mouse repulsion velocity (added on top of loop) */
      this.vx = 0;
      this.vy = 0;
    }
  }

  Particle.prototype.update = function () {
    if (this.born) {
      /* click burst */
      this.vx *= 0.96;
      this.vy *= 0.96;
      this.x += this.vx;
      this.y += this.vy;
      this.alpha -= this.decay;
      return;
    }

    /* Advance loop angles */
    this.phaseX += this.speedX;
    this.phaseY += this.speedY;

    /* Target position from Lissajous loop */
    var tx = this.bx + Math.cos(this.phaseX) * this.ax;
    var ty = this.by + Math.sin(this.phaseY) * this.ay;

    /* Mouse attraction — gentle pull */
    var dx = mouse.x - tx;
    var dy = mouse.y - ty;
    var dist = Math.sqrt(dx * dx + dy * dy);
    if (dist < 220 && dist > 1) {
      var f = (220 - dist) / 220 * 0.025;
      this.vx += dx / dist * f;
      this.vy += dy / dist * f;
    }

    /* Dampen mouse velocity so loop dominates */
    this.vx *= 0.92;
    this.vy *= 0.92;

    /* Final position = loop target + mouse nudge */
    this.x = tx + this.vx;
    this.y = ty + this.vy;

    /* Pulse alpha */
    this.pulse += this.pulseSpeed;
    this.alpha = Math.max(0.05, Math.min(0.85,
      this.alpha + Math.sin(this.pulse) * 0.004
    ));

    /* If loop wanders offscreen, re-anchor base */
    if (this.bx + this.ax < 0 || this.bx - this.ax > W) {
      this.bx = Math.random() * W;
    }
    if (this.by + this.ay < 0 || this.by - this.ay > H) {
      this.by = Math.random() * H;
    }
  };

  Particle.prototype.draw = function () {
    var a = Math.max(0, this.alpha);
    ctx.save();
    ctx.globalAlpha = a;
    ctx.shadowColor = this.color + a + ')';
    ctx.shadowBlur = this.glow;
    ctx.fillStyle = this.color + a + ')';
    ctx.beginPath();
    ctx.arc(this.x, this.y, this.size / 2, 0, Math.PI * 2);
    ctx.fill();
    ctx.restore();
  };

  Particle.prototype.dead = function () {
    return this.born && this.alpha <= 0;
  };

  /* ── Pool management ── */
  var AMBIENT = 65;
  var pool = [];

  function fill() {
    var ambient = pool.filter(function (p) { return !p.born; }).length;
    while (ambient < AMBIENT) {
      pool.push(new Particle(false));
      ambient++;
    }
  }

  function burst(cx, cy, n) {
    for (var i = 0; i < n; i++) pool.push(new Particle(true, cx, cy));
  }

  /* ── Resize ── */
  function resize() {
    W = pc.width = window.innerWidth;
    H = pc.height = window.innerHeight;
    /* re-anchor all ambient base positions proportionally */
    pool.forEach(function (p) {
      if (!p.born) {
        p.bx = Math.random() * W;
        p.by = Math.random() * H;
      }
    });
  }
  window.addEventListener('resize', resize);
  resize();
  fill();

  /* ── Input ── */
  window.addEventListener('mousemove', function (e) {
    mouse.x = e.clientX;
    mouse.y = e.clientY;
  });

  window.addEventListener('mouseleave', function () {
    mouse.x = -9999;
    mouse.y = -9999;
  });

  window.addEventListener('click', function (e) {
    burst(e.clientX, e.clientY, 32);
  });

  window.addEventListener('touchmove', function (e) {
    if (e.touches.length) {
      mouse.x = e.touches[0].clientX;
      mouse.y = e.touches[0].clientY;
    }
  }, { passive: true });

  window.addEventListener('touchend', function (e) {
    if (e.changedTouches.length) {
      burst(e.changedTouches[0].clientX, e.changedTouches[0].clientY, 22);
    }
    mouse.x = -9999;
    mouse.y = -9999;
  }, { passive: true });

  /* ── Animation loop ── */
  function loop() {
    requestAnimationFrame(loop);
    ctx.clearRect(0, 0, W, H);

    pool = pool.filter(function (p) {
      p.update();
      if (!p.dead()) {
        p.draw();
        return true;
      }
      return false;
    });

    fill();
  }

  loop();
}());