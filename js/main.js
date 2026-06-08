const PRODUCTS = [
  {
    id: 1,
    name: 'Camiseta MORLEY',
    cat: 'Tops',
    price: 10000,
    priceOld: null,
    desc: '<strong>Talle:</strong> Único<br><strong>Detalles:</strong> Camiseta confeccionada en Morley, súper cómoda y adaptable a tu cuerpo.',
    imgs: ['img/camiseta morley.jpeg']
  },
  {
    id: 2,
    name: 'Conjunto TINI',
    cat: 'Conjuntos',
    price: 25000,
    priceOld: null,
    desc: '<strong>Talles:</strong> Negro (AGOTADO) | Dulce de Leche (Talle 42)<br><strong>Detalles:</strong> Conjunto Tini. Un clásico que no te puede faltar.',
    imgs: ['img/conjunto TINI dulce de leche.jpeg', 'img/conjunto TINI negro.jpeg']
  },
  {
    id: 3,
    name: 'Camiseta con frunce',
    cat: 'Tops',
    price: 7000,
    priceOld: null,
    desc: '<strong>Talle:</strong> Único<br><strong>Detalles:</strong> Camiseta con frunce.<br>⚠️ <strong>¡AGOTADAS!</strong>',
    imgs: ['img/camiseta con frunce.jpeg']
  },
  {
    id: 4,
    name: 'Body escote cuadrado',
    cat: 'Tops',
    price: 7000,
    priceOld: null,
    desc: '<strong>Talle:</strong> Único (cede hasta un talle 3)<br><strong>Colores:</strong> Disponible en Negro y Bordó<br><strong>Detalles:</strong> Body manga corta con escote cuadrado.',
    imgs: ['img/body escote cuadrado.jpeg']
  },
  {
    id: 5,
    name: 'Camiseta corta escote cuadrado',
    cat: 'Tops',
    price: 7000,
    priceOld: null,
    desc: '<strong>Talle:</strong> Único<br><strong>Colores:</strong> Marrón<br><strong>Detalles:</strong> Camiseta corta escote cuadrado.',
    imgs: ['img/camiseta corta escote cuadrado.jpeg']
  }
];

function formatPrice(n) {
  return '$' + n.toLocaleString('es-AR');
}

// ════════════════════════════════════════
// HEADER & HAMBURGER
// ════════════════════════════════════════
const hdr = document.getElementById('header');
if(hdr) {
  window.addEventListener('scroll', () => {
    hdr.classList.toggle('scrolled', window.scrollY > 30);
  }, {passive:true});
}

const ham = document.getElementById('hamburger');
const mobNav = document.getElementById('mob-nav');
if (ham && mobNav) {
  ham.addEventListener('click', () => {
    ham.classList.toggle('open');
    mobNav.classList.toggle('open');
  });
  mobNav.querySelectorAll('a').forEach(a => {
    a.addEventListener('click', () => {
      ham.classList.remove('open');
      mobNav.classList.remove('open');
    });
  });
}

// ════════════════════════════════════════
// CART LOCALSTORAGE
// ════════════════════════════════════════
let cart = JSON.parse(localStorage.getItem('aisha_cart')) || [];
const countEl = document.getElementById('cart-count');
const cartBtn = document.getElementById('cart-btn');
const toast   = document.getElementById('toast');
let tTimer;

function updateCartCount() {
  if (countEl) countEl.textContent = cart.reduce((sum, item) => sum + (item.qty || 1), 0);
}
updateCartCount();

function bumpCart() {
  if (!countEl) return;
  countEl.classList.remove('bump');
  void countEl.offsetWidth;
  countEl.classList.add('bump');
}

function showToast(icon, msg) {
  if (!toast) return;
  toast.innerHTML = `<span class="t-icon">${icon}</span><span>${msg}</span>`;
  toast.classList.add('show');
  clearTimeout(tTimer);
  tTimer = setTimeout(() => toast.classList.remove('show'), 3200);
}

function addToCart(pid) {
  const p = PRODUCTS.find(x => x.id === pid);
  if (!p) return;
  
  const existing = cart.find(x => x.id === pid);
  if (existing) {
    existing.qty = (existing.qty || 1) + 1;
  } else {
    cart.push({ ...p, qty: 1 });
  }
  
  localStorage.setItem('aisha_cart', JSON.stringify(cart));
  updateCartCount();
  bumpCart();
  showToast('🛍️', `"${p.name}" agregado al carrito`);
}

// ════════════════════════════════════════
// CART DRAWER (estilo 47 Street)
// ════════════════════════════════════════
function buildDrawer() {
  if (document.getElementById('cart-drawer')) return;
  const overlay = document.createElement('div');
  overlay.id = 'drawer-overlay';
  overlay.style.cssText = 'display:none;position:fixed;inset:0;background:rgba(0,0,0,0.5);z-index:1999;transition:opacity 0.3s;opacity:0;';

  const drawer = document.createElement('div');
  drawer.id = 'cart-drawer';
  drawer.innerHTML = `
    <div class="cd-header">
      <span class="cd-title">Mi carrito (<span id="cd-count">0</span>)</span>
      <button class="cd-close" id="cd-close">×</button>
    </div>
    <div class="cd-items" id="cd-items"></div>
    <div class="cd-footer">
      <div class="cd-progress-wrap" id="cd-progress-wrap">
        <div class="cd-progress-bar"><div class="cd-progress-fill" id="cd-fill"></div></div>
        <p class="cd-progress-txt" id="cd-progress-txt"></p>
      </div>
      <div class="cd-total-row"><span>Total</span><span id="cd-total">$0</span></div>
      <a href="carrito.html" class="cd-btn-pay">Ver carrito y pagar</a>
      <button class="cd-btn-keep" id="cd-btn-keep">Seguir comprando</button>
    </div>`;

  document.body.appendChild(overlay);
  document.body.appendChild(drawer);

  document.getElementById('cd-close').addEventListener('click', closeDrawer);
  document.getElementById('cd-btn-keep').addEventListener('click', closeDrawer);
  overlay.addEventListener('click', closeDrawer);
}

function openDrawer() {
  renderDrawer();
  const overlay = document.getElementById('drawer-overlay');
  const drawer = document.getElementById('cart-drawer');
  overlay.style.display = 'block';
  requestAnimationFrame(() => {
    overlay.style.opacity = '1';
    drawer.classList.add('open');
  });
  document.body.style.overflow = 'hidden';
}

function closeDrawer() {
  const overlay = document.getElementById('drawer-overlay');
  const drawer = document.getElementById('cart-drawer');
  overlay.style.opacity = '0';
  drawer.classList.remove('open');
  document.body.style.overflow = '';
  setTimeout(() => { overlay.style.display = 'none'; }, 300);
}

const FREE_SHIPPING = 15000;
function renderDrawer() {
  buildDrawer();
  const itemsEl = document.getElementById('cd-items');
  const countEl2 = document.getElementById('cd-count');
  const totalEl = document.getElementById('cd-total');
  const fillEl = document.getElementById('cd-fill');
  const txtEl = document.getElementById('cd-progress-txt');

  const total = cart.reduce((s, i) => s + i.price * (i.qty || 1), 0);
  const totalQty = cart.reduce((s, i) => s + (i.qty || 1), 0);
  if (countEl2) countEl2.textContent = totalQty;
  if (totalEl) totalEl.textContent = formatPrice(total);

  // Barra de envío gratis
  const pct = Math.min(100, (total / FREE_SHIPPING) * 100);
  if (fillEl) fillEl.style.width = pct + '%';
  if (txtEl) {
    if (total >= FREE_SHIPPING) {
      txtEl.innerHTML = '🎉 ¡Llegaste! Tenés <strong>ENVÍO GRATIS</strong>.';
    } else {
      const falta = formatPrice(FREE_SHIPPING - total);
      txtEl.innerHTML = `Te faltan <strong>${falta}</strong> para envío gratis.`;
    }
  }

  if (!itemsEl) return;
  if (cart.length === 0) {
    itemsEl.innerHTML = '<p class="cd-empty">Tu carrito está vacío.</p>';
    return;
  }

  itemsEl.innerHTML = cart.map((item, idx) => `
    <div class="cd-item">
      <img src="${item.imgs[0]}" alt="${item.name}" class="cd-item-img">
      <div class="cd-item-info">
        <div class="cd-item-name">${item.name}</div>
        <div class="cd-item-price">${formatPrice(item.price)}</div>
        <div class="cd-item-qty">
          <button class="cd-qty-btn" onclick="changeQty(${idx}, -1)">-</button>
          <span>${item.qty || 1}</span>
          <button class="cd-qty-btn" onclick="changeQty(${idx}, 1)">+</button>
        </div>
      </div>
      <button class="cd-item-del" onclick="removeFromCart(${idx})">×</button>
    </div>`).join('');
}

function changeQty(idx, delta) {
  if (!cart[idx]) return;
  cart[idx].qty = Math.max(1, (cart[idx].qty || 1) + delta);
  localStorage.setItem('aisha_cart', JSON.stringify(cart));
  updateCartCount();
  renderDrawer();
}

function removeFromCart(idx) {
  cart.splice(idx, 1);
  localStorage.setItem('aisha_cart', JSON.stringify(cart));
  updateCartCount();
  renderDrawer();
}

// Inyectar estilos del drawer
(function injectDrawerStyles() {
  const s = document.createElement('style');
  s.textContent = `
    #cart-drawer {
      position: fixed; top: 0; right: 0; bottom: 0; width: 380px; max-width: 95vw;
      background: #fff; z-index: 2000; display: flex; flex-direction: column;
      transform: translateX(100%); transition: transform 0.35s cubic-bezier(0.4,0,0.2,1);
      box-shadow: -4px 0 40px rgba(0,0,0,0.15);
    }
    #cart-drawer.open { transform: translateX(0); }
    .cd-header { display: flex; align-items: center; justify-content: space-between; padding: 20px 20px 16px; border-bottom: 1px solid #ede8e3; }
    .cd-title { font-size: 1rem; font-weight: 700; color: #1a1a1a; letter-spacing: 0.02em; }
    .cd-close { background: none; border: none; font-size: 1.6rem; cursor: pointer; color: #888; line-height: 1; padding: 0 4px; transition: color 0.2s; }
    .cd-close:hover { color: #1a1a1a; }
    .cd-items { flex: 1; overflow-y: auto; padding: 16px 20px; display: flex; flex-direction: column; gap: 16px; }
    .cd-empty { text-align: center; color: #888; padding: 40px 0; font-size: 0.88rem; }
    .cd-item { display: flex; gap: 14px; align-items: flex-start; position: relative; }
    .cd-item-img { width: 80px; height: 100px; object-fit: cover; border-radius: 6px; flex-shrink: 0; background: #f5f0eb; }
    .cd-item-info { flex: 1; min-width: 0; }
    .cd-item-name { font-size: 0.82rem; font-weight: 600; color: #1a1a1a; margin-bottom: 4px; line-height: 1.3; }
    .cd-item-price { font-size: 0.90rem; font-weight: 700; color: #1a1a1a; margin-bottom: 10px; }
    .cd-item-qty { display: flex; align-items: center; gap: 10px; }
    .cd-qty-btn { width: 26px; height: 26px; border-radius: 50%; border: 1.5px solid #e0d8d0; background: #fff; cursor: pointer; font-size: 1rem; display: flex; align-items: center; justify-content: center; font-weight: 600; color: #1a1a1a; transition: all 0.2s; }
    .cd-qty-btn:hover { background: #f5f0eb; border-color: #1a1a1a; }
    .cd-item-qty span { font-size: 0.88rem; font-weight: 600; min-width: 20px; text-align: center; }
    .cd-item-del { position: absolute; top: 0; right: 0; background: none; border: none; color: #bbb; font-size: 1.3rem; cursor: pointer; transition: color 0.2s; line-height: 1; padding: 2px; }
    .cd-item-del:hover { color: #c0392b; }
    .cd-footer { padding: 16px 20px 24px; border-top: 1px solid #ede8e3; display: flex; flex-direction: column; gap: 12px; }
    .cd-progress-wrap { background: #f5f5f5; border-radius: 10px; padding: 12px 14px; }
    .cd-progress-bar { height: 6px; background: #e0d8d0; border-radius: 3px; overflow: hidden; margin-bottom: 8px; }
    .cd-progress-fill { height: 100%; background: #4caf8a; border-radius: 3px; transition: width 0.6s ease; }
    .cd-progress-txt { font-size: 0.78rem; color: #555; line-height: 1.4; }
    .cd-progress-txt strong { color: #1a1a1a; }
    .cd-total-row { display: flex; justify-content: space-between; align-items: center; font-size: 1rem; font-weight: 700; color: #1a1a1a; }
    .cd-btn-pay { display: block; text-align: center; background: #1a1a1a; color: #fff; border: none; border-radius: 8px; padding: 15px; font-size: 0.80rem; font-weight: 700; letter-spacing: 0.12em; text-transform: uppercase; cursor: pointer; text-decoration: none; transition: background 0.2s; }
    .cd-btn-pay:hover { background: #D4849E; }
    .cd-btn-keep { background: #fff; color: #1a1a1a; border: 1.5px solid #e0d8d0; border-radius: 8px; padding: 13px; font-size: 0.78rem; font-weight: 600; letter-spacing: 0.10em; text-transform: uppercase; cursor: pointer; transition: border-color 0.2s; }
    .cd-btn-keep:hover { border-color: #1a1a1a; }
  `;
  document.head.appendChild(s);
})();

buildDrawer();

if (cartBtn) {
  cartBtn.addEventListener('click', (e) => {
    e.preventDefault();
    openDrawer();
  });
}

function updateCartBadge() {
  updateCartCount();
  if (document.getElementById('cart-drawer') && document.getElementById('cart-drawer').classList.contains('open')) {
    renderDrawer();
  }
}

// ════════════════════════════════════════
// NEWSLETTER
// ════════════════════════════════════════
function subNL() {
  const emailInput = document.getElementById('nl-email');
  if(!emailInput) return;
  const val = emailInput.value.trim();
  if (!val || !val.includes('@')) return;
  document.getElementById('nl-ok').style.display = 'block';
  emailInput.value = '';
  setTimeout(() => document.getElementById('nl-ok').style.display = 'none', 6000);
}

const emailInput = document.getElementById('nl-email');
if(emailInput) {
  emailInput.addEventListener('keydown', e => {
    if (e.key === 'Enter') subNL();
  });
}

// ════════════════════════════════════════
// ACORDEONES
// ════════════════════════════════════════
function toggleAcc(id) {
  const acc = document.getElementById(id);
  if(!acc) return;
  const isOpen = acc.classList.contains('open');
  document.querySelectorAll('.accordion').forEach(a => a.classList.remove('open'));
  if (!isOpen) acc.classList.add('open');
}

// ════════════════════════════════════════
// INTERSECTION OBSERVER (Animaciones)
// ════════════════════════════════════════
const fades = document.querySelectorAll('.fade-in');
const obs = new IntersectionObserver((entries) => {
  entries.forEach(e => {
    if (e.isIntersecting) { e.target.classList.add('vis'); obs.unobserve(e.target); }
  });
}, {threshold: 0.10});
fades.forEach(el => obs.observe(el));

// ════════════════════════════════════════
// HERO CAROUSEL LOGIC
// ════════════════════════════════════════
function initHeroCarousel() {
  const track = document.getElementById('hero-track');
  if (!track) return;
  const slides = Array.from(track.children);
  const nextButton = document.getElementById('hero-next');
  const prevButton = document.getElementById('hero-prev');
  const dotsContainer = document.getElementById('hero-dots');
  
  if (slides.length <= 1) {
    if (nextButton) nextButton.style.display = 'none';
    if (prevButton) prevButton.style.display = 'none';
    return;
  }

  let currentIdx = 0;
  let autoplayTimer;

  // Create dots
  slides.forEach((_, i) => {
    const dot = document.createElement('button');
    if (i === 0) dot.classList.add('active');
    dot.addEventListener('click', () => moveToSlide(i));
    dotsContainer.appendChild(dot);
  });
  const dots = Array.from(dotsContainer.children);

  function updateActiveClasses() {
    slides.forEach((s, i) => {
      if (i === currentIdx) s.classList.add('active');
      else s.classList.remove('active');
    });
    dots.forEach((d, i) => {
      if (i === currentIdx) d.classList.add('active');
      else d.classList.remove('active');
    });
  }

  function moveToSlide(index) {
    if (index < 0) index = slides.length - 1;
    if (index >= slides.length) index = 0;
    currentIdx = index;
    updateActiveClasses();
    resetAutoplay();
  }

  if (nextButton) {
    nextButton.addEventListener('click', () => moveToSlide(currentIdx + 1));
  }
  if (prevButton) {
    prevButton.addEventListener('click', () => moveToSlide(currentIdx - 1));
  }

  function startAutoplay() {
    autoplayTimer = setInterval(() => {
      moveToSlide(currentIdx + 1);
    }, 6000);
  }
  function resetAutoplay() {
    clearInterval(autoplayTimer);
    startAutoplay();
  }

  // SWIPE TÁCTIL (mobile)
  let touchStartX = 0;
  let touchEndX = 0;
  const heroSection = document.getElementById('hero-section');
  heroSection.addEventListener('touchstart', e => {
    touchStartX = e.changedTouches[0].clientX;
  }, { passive: true });
  heroSection.addEventListener('touchend', e => {
    touchEndX = e.changedTouches[0].clientX;
    const diff = touchStartX - touchEndX;
    if (Math.abs(diff) > 50) { // mínimo 50px para contar como swipe
      if (diff > 0) moveToSlide(currentIdx + 1); // swipe izquierda = siguiente
      else moveToSlide(currentIdx - 1);           // swipe derecha = anterior
    }
  }, { passive: true });

  // Initialize
  slides[0].classList.add('active');
  startAutoplay();
}

document.addEventListener('DOMContentLoaded', () => {
  initHeroCarousel();
});
