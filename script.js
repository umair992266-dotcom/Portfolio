// ---------- Background node graph ----------
(function(){
  const canvas = document.getElementById('graph-bg');
  const ctx = canvas.getContext('2d');
  let w,h, nodes = [];
  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  function resize(){
    w = canvas.width = window.innerWidth;
    h = canvas.height = Math.max(window.innerHeight, document.body.scrollHeight);
  }
  function initNodes(){
    const count = Math.min(50, Math.floor((w*h)/55000));
    nodes = Array.from({length: count}, () => ({
      x: Math.random()*w,
      y: Math.random()*h,
      vx: (Math.random()-0.5)*0.18,
      vy: (Math.random()-0.5)*0.18,
      r: Math.random()*1.4 + 0.6,
      pulse: Math.random()*Math.PI*2,
      hue: Math.random() > 0.5 ? 'a' : 'b'
    }));
  }
  function step(){
    ctx.clearRect(0,0,w,h);
    for(const n of nodes){
      n.x += n.vx; n.y += n.vy;
      if(n.x<0||n.x>w) n.vx*=-1;
      if(n.y<0||n.y>h) n.vy*=-1;
      n.pulse += 0.02;
    }
    for(let i=0;i<nodes.length;i++){
      for(let j=i+1;j<nodes.length;j++){
        const a=nodes[i], b=nodes[j];
        const d = Math.hypot(a.x-b.x, a.y-b.y);
        if(d < 150){
          ctx.strokeStyle = `rgba(139,147,167,${(1 - d/150)*0.09})`;
          ctx.lineWidth = 1;
          ctx.beginPath();
          ctx.moveTo(a.x,a.y);
          ctx.lineTo(b.x,b.y);
          ctx.stroke();
        }
      }
    }
    for(const n of nodes){
      const glow = (Math.sin(n.pulse)+1)/2;
      const color = n.hue === 'a' ? '94,234,212' : '167,139,250';
      ctx.beginPath();
      ctx.fillStyle = `rgba(${color},${0.15 + glow*0.25})`;
      ctx.arc(n.x,n.y,n.r + glow*0.8,0,Math.PI*2);
      ctx.fill();
    }
    if(!reduceMotion) requestAnimationFrame(step);
  }
  resize();
  initNodes();
  step();
  window.addEventListener('resize', () => { resize(); initNodes(); });
})();

// ---------- Scroll reveal ----------
(function(){
  const items = document.querySelectorAll('.reveal-up');
  items.forEach(el => {
    const delay = el.getAttribute('data-delay');
    if(delay !== null) el.style.setProperty('--d', delay);
  });
  const io = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if(entry.isIntersecting){
        entry.target.classList.add('in-view');
        io.unobserve(entry.target);
      }
    });
  }, { threshold: 0.15, rootMargin: '0px 0px -40px 0px' });
  items.forEach(el => io.observe(el));

  // language bar fill
  const bars = document.querySelectorAll('.lang-bar-fill');
  const barIo = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if(entry.isIntersecting){
        entry.target.classList.add('in-view');
        barIo.unobserve(entry.target);
      }
    });
  }, { threshold: 0.5 });
  bars.forEach(el => barIo.observe(el));
})();

// ---------- Animated stat counters ----------
(function(){
  const nums = document.querySelectorAll('.stat .num');
  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const io = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if(entry.isIntersecting){
        const el = entry.target;
        const target = parseInt(el.getAttribute('data-count'), 10);
        if(reduceMotion){ el.textContent = target; io.unobserve(el); return; }
        let cur = 0;
        const dur = 1400;
        const start = performance.now();
        function tick(now){
          const p = Math.min((now-start)/dur, 1);
          const eased = 1 - Math.pow(1-p, 3);
          cur = Math.round(eased * target);
          el.textContent = cur;
          if(p < 1) requestAnimationFrame(tick);
        }
        requestAnimationFrame(tick);
        io.unobserve(el);
      }
    });
  }, { threshold: 0.6 });
  nums.forEach(el => io.observe(el));
})();

// ---------- 3D tilt on photo (mouse + gyro-free pointer tracking) ----------
(function(){
  const wrap = document.getElementById('photo3d');
  if(!wrap) return;
  const inner = wrap.querySelector('.photo-3d-inner');
  const shadow = wrap.querySelector('.photo-3d-shadow');
  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if(reduceMotion) return;

  let bounds;
  function setBounds(){ bounds = wrap.getBoundingClientRect(); }
  setBounds();
  window.addEventListener('resize', setBounds);

  function onMove(x, y){
    const px = (x - bounds.left) / bounds.width;
    const py = (y - bounds.top) / bounds.height;
    const rotY = (px - 0.5) * 22;
    const rotX = (0.5 - py) * 22;
    inner.style.transform = `rotateX(${rotX}deg) rotateY(${rotY}deg) scale(1.02)`;
    shadow.style.transform = `translateX(${(px-0.5)*30}px) scale(${1 - Math.abs(px-0.5)*0.2})`;
  }
  function reset(){
    inner.style.transform = 'rotateX(0deg) rotateY(0deg) scale(1)';
    shadow.style.transform = 'translateX(0) scale(1)';
  }

  wrap.addEventListener('mousemove', (e) => { setBounds(); onMove(e.clientX, e.clientY); });
  wrap.addEventListener('mouseleave', reset);
  wrap.addEventListener('touchmove', (e) => {
    if(e.touches[0]){ setBounds(); onMove(e.touches[0].clientX, e.touches[0].clientY); }
  }, { passive: true });
  wrap.addEventListener('touchend', reset);

  // gentle ambient drift when idle
  let driftT = 0, idle = true;
  wrap.addEventListener('mouseenter', () => idle = false);
  wrap.addEventListener('mouseleave', () => idle = true);
  function ambient(){
    if(idle){
      driftT += 0.012;
      const rotY = Math.sin(driftT) * 5;
      const rotX = Math.cos(driftT*0.8) * 3;
      inner.style.transform = `rotateX(${rotX}deg) rotateY(${rotY}deg) scale(1)`;
    }
    requestAnimationFrame(ambient);
  }
  ambient();
})();

// ---------- 3D tilt on cards (skills, projects, exp, edu, contact) ----------
(function(){
  const cards = document.querySelectorAll('.tilt-card');
  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const isTouch = window.matchMedia('(hover: none)').matches;
  if(reduceMotion || isTouch) return;

  cards.forEach(card => {
    card.addEventListener('mousemove', (e) => {
      const r = card.getBoundingClientRect();
      const px = (e.clientX - r.left) / r.width;
      const py = (e.clientY - r.top) / r.height;
      const rotY = (px - 0.5) * 8;
      const rotX = (0.5 - py) * 8;
      card.style.transform = `perspective(1000px) rotateX(${rotX}deg) rotateY(${rotY}deg) translateY(-4px)`;
      card.style.setProperty('--mx', `${px*100}%`);
      card.style.setProperty('--my', `${py*100}%`);
    });
    card.addEventListener('mouseleave', () => {
      card.style.transform = 'perspective(1000px) rotateX(0deg) rotateY(0deg) translateY(0)';
    });
  });
})();

// ---------- Scroll progress bar ----------
(function(){
  const fill = document.getElementById('progressFill');
  function update(){
    const scrollTop = window.scrollY;
    const max = document.body.scrollHeight - window.innerHeight;
    const pct = max > 0 ? (scrollTop/max)*100 : 0;
    fill.style.width = pct + '%';
  }
  window.addEventListener('scroll', update, { passive:true });
  update();
})();

// ---------- Mobile menu ----------
(function(){
  const toggle = document.getElementById('menuToggle');
  const nav = document.getElementById('mobileNav');
  if(!toggle || !nav) return;
  toggle.addEventListener('click', () => {
    const open = nav.classList.toggle('open');
    toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
  });
  nav.querySelectorAll('a').forEach(a => a.addEventListener('click', () => {
    nav.classList.remove('open');
    toggle.setAttribute('aria-expanded', 'false');
  }));
})();
