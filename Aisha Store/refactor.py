import os
import re

html_path = r'e:\Webs\Ropita\index.html'

with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Extract CSS
style_match = re.search(r'<style>(.*?)</style>', content, re.DOTALL)
if style_match:
    css_content = style_match.group(1).strip()
    with open(r'e:\Webs\Ropita\css\style.css', 'w', encoding='utf-8') as f:
        f.write(css_content)

# Extract JS
script_match = re.search(r'<script>(.*?)</script>', content, re.DOTALL)
if script_match:
    js_content = script_match.group(1).strip()

# Update JS for localStorage cart
js_new = js_content

# We need to remove modal logic from JS
# Let's completely rewrite the JS to be modular for multi-page
js_modular = """
const PRODUCTS = [
  {
    id: 1,
    name: 'Camiseta Morley',
    cat: 'Tops',
    price: 10000,
    priceOld: null,
    desc: '<strong>Talle:</strong> Único<br><strong>Detalles:</strong> Camiseta confeccionada en Morley, súper cómoda y adaptable a tu cuerpo.<br><br><a href="https://www.instagram.com/aisha.ssttore/p/DYu8sjoEu-4/" target="_blank" style="color:var(--negro);font-weight:600;text-decoration:underline;">VER POST EN INSTAGRAM ↗</a>',
    imgs: ['img/camiseta MORLEY.jpeg']
  },
  {
    id: 2,
    name: 'Conjunto Tini',
    cat: 'Conjuntos',
    price: 25000,
    priceOld: null,
    desc: '<strong>Talles:</strong> Negro (AGOTADO) | Dulce de Leche (Talle 42)<br><strong>Detalles:</strong> Conjunto Tini. Un clásico que no te puede faltar.<br><br><a href="https://www.instagram.com/aisha.ssttore/p/DYu8dpTkvT0/" target="_blank" style="color:var(--negro);font-weight:600;text-decoration:underline;">VER POST EN INSTAGRAM ↗</a>',
    imgs: ['img/conjunto TINI dulce de leche.jpeg', 'img/conjunto TINI negro.jpeg']
  },
  {
    id: 3,
    name: 'Camiseta con frunce',
    cat: 'Tops',
    price: 7000,
    priceOld: null,
    desc: '<strong>Talle:</strong> Único<br><strong>Detalles:</strong> Camiseta con frunce 🔥.<br>⚠️ <strong>¡AGOTADAS!</strong><br><br><a href="https://www.instagram.com/aisha.ssttore/p/DXuJ8QGjabU/" target="_blank" style="color:var(--negro);font-weight:600;text-decoration:underline;">VER POST EN INSTAGRAM ↗</a>',
    imgs: ['img/Camiseta con frunce.jpeg']
  },
  {
    id: 4,
    name: 'Body escote cuadrado',
    cat: 'Tops',
    price: 7000,
    priceOld: null,
    desc: '<strong>Talle:</strong> Único (sede hasta un talle 3)<br><strong>Colores:</strong> Disponible en Negro y Bordó<br><strong>Detalles:</strong> Body manga corta con escote cuadrado. Se adapta genial a la figura.<br><br><a href="https://www.instagram.com/aisha.ssttore/p/DXuJhcbjVfn/" target="_blank" style="color:var(--negro);font-weight:600;text-decoration:underline;">VER POST EN INSTAGRAM ↗</a>',
    imgs: ['img/Body escote cuadrado.jpeg']
  },
  {
    id: 5,
    name: 'Camiseta corta escote cuadrado',
    cat: 'Tops',
    price: 7000,
    priceOld: null,
    desc: '<strong>Talle:</strong> Único<br><strong>Detalles:</strong> Camiseta corta escote cuadrado 🤎.<br><br><a href="https://www.instagram.com/aisha.ssttore/p/DXuJPDBjf9l/" target="_blank" style="color:var(--negro);font-weight:600;text-decoration:underline;">VER POST EN INSTAGRAM ↗</a>',
    imgs: ['img/Camiseta corta escote cuadrado.jpeg']
  }
];

function formatPrice(n) {
  return '$' + n.toLocaleString('es-AR');
}

// ════════════════════════════════════════
// HEADER & HAMBURGER
// ════════════════════════════════════════
const hdr = document.getElementById('header');
window.addEventListener('scroll', () => {
  hdr.classList.toggle('scrolled', window.scrollY > 30);
}, {passive:true});

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
const toastMsg = document.getElementById('toast-msg');
let tTimer;

function updateCartCount() {
  if (countEl) countEl.textContent = cart.length;
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
  cart.push(p);
  localStorage.setItem('aisha_cart', JSON.stringify(cart));
  updateCartCount();
  bumpCart();
  showToast('🛍️', `"${p.name}" agregado al carrito`);
}

if (cartBtn) {
  cartBtn.addEventListener('click', () => {
    showToast('🛒', cart.length > 0 ? `Tenés ${cart.length} ítem${cart.length > 1 ? 's' : ''} en tu carrito` : 'Tu carrito está vacío');
  });
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
"""

with open(r'e:\Webs\Ropita\js\main.js', 'w', encoding='utf-8') as f:
    f.write(js_modular)


# ----------------------------------------
# UPDATE INDEX.HTML
# ----------------------------------------
# Remove style content, replace with link
content = re.sub(r'<style>.*?</style>', '<link rel="stylesheet" href="css/style.css">', content, flags=re.DOTALL)
# Remove script content, replace with script src
content = re.sub(r'<script>.*?</script>', '<script src="js/main.js"></script>', content, flags=re.DOTALL)
# Remove modal HTML completely
content = re.sub(r'<!-- ══ MODAL DE PRODUCTO ══ -->.*?<!-- TOAST -->', '<!-- TOAST -->', content, flags=re.DOTALL)

# Update product links in index.html (replace buttons with links)
import re
# We need to map data-name to ID to fix the links
name_to_id = {
  'Camiseta Morley': 1,
  'Conjunto Tini': 2,
  'Camiseta con frunce': 3,
  'Body escote cuadrado': 4,
  'Camiseta corta escote cuadrado': 5
}

def replace_card(match):
    name = match.group(1)
    card_content = match.group(2)
    pid = name_to_id.get(name, 1)
    
    # Change onclick to href inside card
    # We will wrap the image and everything in an anchor, or just change the cta button
    card_content = re.sub(r'<button class="prod-cta"[^>]*>.*?</button>', f'<a href="producto.html?id={pid}" class="prod-cta">+ Ver detalle</a>', card_content)
    
    return f'<div class="prod-card fade-in" data-name="{name}">{card_content}</div>'

# Regex to find all prod-cards. This can be tricky. Let's just do a simpler replace.
content = re.sub(r'<button class="prod-cta"[^>]*>.*?</button>', '', content) # Remove old buttons
# And let's wrap the prod-img-box img in an anchor? Actually, better to just let the script do it or add an anchor button
for name, pid in name_to_id.items():
    content = content.replace(
        f'<img src="img/{name}', 
        f'<a href="producto.html?id={pid}"><img src="img/{name}'
    )
    # The above is not safe enough. Let's just use string replacement on known blocks
    
# Let's fix the product cards in a cleaner way by writing them directly
index_grid_1 = """
  <div class="prod-grid">
    <a href="producto.html?id=1" class="prod-card fade-in" style="text-decoration:none;">
      <div class="prod-img-box">
        <span class="prod-badge badge-new">NUEVO</span>
        <button class="prod-wish">♡</button>
        <img src="img/camiseta MORLEY.jpeg" alt="Camiseta Morley" loading="lazy">
        <div class="prod-cta">+ Ver detalle</div>
      </div>
      <div class="prod-info">
        <div class="prod-name">Camiseta Morley</div>
        <div class="prod-prices"><span class="price">$10.000</span></div>
      </div>
    </a>

    <a href="producto.html?id=2" class="prod-card fade-in d1" style="text-decoration:none;">
      <div class="prod-img-box">
        <span class="prod-badge badge-new">NUEVO</span>
        <button class="prod-wish">♡</button>
        <img src="img/conjunto TINI dulce de leche.jpeg" alt="Conjunto Tini" loading="lazy">
        <div class="prod-cta">+ Ver detalle</div>
      </div>
      <div class="prod-info">
        <div class="prod-name">Conjunto Tini</div>
        <div class="prod-prices"><span class="price">$25.000</span></div>
      </div>
    </a>

    <a href="producto.html?id=4" class="prod-card fade-in d2" style="text-decoration:none;">
      <div class="prod-img-box">
        <span class="prod-badge badge-new">NUEVO</span>
        <button class="prod-wish">♡</button>
        <img src="img/Body escote cuadrado.jpeg" alt="Body escote cuadrado" loading="lazy">
        <div class="prod-cta">+ Ver detalle</div>
      </div>
      <div class="prod-info">
        <div class="prod-name">Body escote cuadrado</div>
        <div class="prod-prices"><span class="price">$7.000</span></div>
      </div>
    </a>

    <a href="producto.html?id=5" class="prod-card fade-in d3" style="text-decoration:none;">
      <div class="prod-img-box">
        <span class="prod-badge badge-new">NUEVO</span>
        <button class="prod-wish">♡</button>
        <img src="img/Camiseta corta escote cuadrado.jpeg" alt="Camiseta corta escote cuadrado" loading="lazy">
        <div class="prod-cta">+ Ver detalle</div>
      </div>
      <div class="prod-info">
        <div class="prod-name">Camiseta corta escote cuadrado</div>
        <div class="prod-prices"><span class="price">$7.000</span></div>
      </div>
    </a>
  </div>
"""

index_grid_2 = """
  <div class="prod-grid">
    <a href="producto.html?id=3" class="prod-card fade-in" style="text-decoration:none;">
      <div class="prod-img-box">
        <span class="prod-badge badge-best" style="background:var(--bordo);color:var(--blanco);">AGOTADO</span>
        <button class="prod-wish">♡</button>
        <img src="img/Camiseta con frunce.jpeg" alt="Camiseta con frunce" loading="lazy" style="filter: grayscale(1);">
        <div class="prod-cta">+ Ver detalle</div>
      </div>
      <div class="prod-info">
        <div class="prod-name">Camiseta con frunce</div>
        <div class="prod-prices">
          <span class="price" style="text-decoration:line-through;color:var(--gris-texto);">$7.000</span>
        </div>
      </div>
    </a>
  </div>
"""

# Replace in content using re
content = re.sub(r'<div class="prod-grid">.*?</div>\s*</div>\s*<!-- ══ CATEGORIES ══ -->', index_grid_1 + '\n</div>\n\n<!-- ══ CATEGORIES ══ -->', content, flags=re.DOTALL)
content = re.sub(r'<div class="prod-grid">.*?</div>\s*</div>\s*<!-- ══ GIFT CARD ══ -->', index_grid_2 + '\n</div>\n\n<!-- ══ GIFT CARD ══ -->', content, flags=re.DOTALL)


with open(r'e:\Webs\Ropita\index.html', 'w', encoding='utf-8') as f:
    f.write(content)

# ----------------------------------------
# CREATE PRODUCTO.HTML
# ----------------------------------------
header_html = re.search(r'<!-- ══ HEADER ══ -->.*?</header>', content, re.DOTALL).group(0)
footer_html = re.search(r'<!-- ══ FOOTER ══ -->.*?</footer>', content, re.DOTALL).group(0)

producto_html = f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Producto — AISHA STORE</title>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,600;0,700;1,400;1,600&family=Jost:wght@300;400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="css/style.css">
<style>
/* Estilos específicos de producto.html (reutilizamos la estructura del modal) */
.product-page {{ max-width: 1100px; margin: 60px auto; padding: 0 40px; }}
.product-body {{ display: grid; grid-template-columns: 1fr 1fr; gap: 40px; min-height: 500px; }}

.prod-gallery {{ display: flex; flex-direction: column; gap: 14px; position: sticky; top: 100px; align-self: start; }}
.prod-main-img {{ position: relative; aspect-ratio: 3/4; border-radius: 10px; overflow: hidden; background: var(--crema); }}
.prod-main-img img {{ width: 100%; height: 100%; object-fit: cover; display: block; transition: opacity 0.25s ease, transform 0.4s ease; }}
.prod-main-img img.switching {{ opacity: 0; transform: scale(0.97); }}

.gallery-arrows {{ position: absolute; inset: 0; display: flex; align-items: center; justify-content: space-between; padding: 0 10px; pointer-events: none; }}
.g-arrow {{ width: 32px; height: 32px; border-radius: 50%; background: rgba(255,255,255,0.88); border: none; cursor: pointer; display: flex; align-items: center; justify-content: center; font-size: 0.85rem; color: var(--negro); pointer-events: all; transition: background var(--transition), transform var(--transition); box-shadow: 0 2px 12px rgba(0,0,0,0.12); }}
.g-arrow:hover {{ background: var(--blanco); transform: scale(1.1); }}

.prod-thumbs {{ display: flex; gap: 10px; }}
.prod-thumb {{ flex: 1; aspect-ratio: 1; border-radius: 8px; overflow: hidden; background: var(--crema); cursor: pointer; border: 2px solid transparent; transition: border-color var(--transition), transform var(--transition); }}
.prod-thumb:hover {{ transform: scale(1.04); }}
.prod-thumb.active {{ border-color: var(--rosa-acento); }}
.prod-thumb img {{ width: 100%; height: 100%; object-fit: cover; display: block; }}

.prod-info-col {{ display: flex; flex-direction: column; gap: 0; }}
.prod-breadcrumb {{ font-size: 0.65rem; font-weight: 600; letter-spacing: 0.20em; text-transform: uppercase; color: var(--gris-texto); margin-bottom: 8px; }}
.prod-title {{ font-family: var(--font-display); font-size: 2.4rem; font-weight: 700; line-height: 1.1; letter-spacing: -0.01em; color: var(--negro); margin-bottom: 16px; }}

.prod-price-block {{ display: flex; align-items: baseline; gap: 12px; margin-bottom: 6px; }}
.prod-price {{ font-size: 1.8rem; font-weight: 700; color: var(--negro); }}
.prod-cuotas {{ font-size: 0.80rem; color: var(--gris-texto); margin-bottom: 20px; letter-spacing: 0.01em; }}
.prod-cuotas strong {{ color: var(--negro); font-weight: 600; }}

.prod-pay-info {{ display: flex; align-items: center; gap: 8px; font-size: 0.72rem; color: var(--gris-texto); padding: 10px 14px; background: var(--crema); border-radius: 8px; margin-bottom: 20px; }}
.prod-pay-info svg {{ flex-shrink: 0; color: var(--rosa-acento); }}
.prod-divider {{ height: 1px; background: var(--gris-medio); margin: 16px 0; }}

.prod-desc-text {{ font-size: 0.85rem; line-height: 1.75; color: var(--gris-texto); font-weight: 300; margin-bottom: 20px; }}

/* ACORDEONES reusados */
.accordions {{ margin-top: 20px; }}

@media(max-width: 768px) {{
  .product-page {{ padding: 0 24px; margin: 30px auto; }}
  .product-body {{ grid-template-columns: 1fr; gap: 30px; }}
  .prod-gallery {{ position: static; }}
}}
</style>
</head>
<body>

{header_html}

<div class="product-page">
  <div class="product-body">
    <!-- GALERIA -->
    <div class="prod-gallery">
      <div class="prod-main-img">
        <img id="p-img-main" src="" alt="Producto">
        <div class="gallery-arrows">
          <button class="g-arrow" id="p-prev">‹</button>
          <button class="g-arrow" id="p-next">›</button>
        </div>
      </div>
      <div class="prod-thumbs" id="p-thumbs"></div>
    </div>

    <!-- INFO -->
    <div class="prod-info-col">
      <div class="prod-breadcrumb">Inicio > <span id="p-cat">Categoría</span></div>
      <h1 class="prod-title" id="p-name">Cargando...</h1>
      
      <div class="prod-price-block">
        <span class="prod-price" id="p-price"></span>
      </div>
      <div class="prod-cuotas" id="p-cuotas"></div>
      
      <div class="prod-pay-info">
        <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><rect x="1" y="4" width="22" height="16" rx="2"/><line x1="1" y1="10" x2="23" y2="10"/></svg>
        Hasta 3 cuotas sin interés con todas las tarjetas
      </div>
      
      <div class="prod-divider"></div>
      
      <button class="btn-agregar" id="btn-add-product" style="width:100%; margin-top:10px;">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M6 2 3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4Z"/><line x1="3" y1="6" x2="21" y2="6"/><path d="M16 10a4 4 0 0 1-8 0"/></svg>
        Agregar al carrito
      </button>

      <div class="prod-divider"></div>
      
      <p class="prod-desc-text" id="p-desc"></p>
      
      <div class="accordions">
        <div class="accordion" id="acc-envios">
          <button class="accordion-btn" onclick="toggleAcc('acc-envios')">
            <span>📦 &nbsp;Envíos</span>
            <span class="accordion-icon">+</span>
          </button>
          <div class="accordion-body">
            <p>Envíos a todo el país. Gratis en CABA en compras desde $15.000. Interior del país entre 3 y 7 días hábiles. Podés coordinar punto de encuentro sin costo extra.</p>
          </div>
        </div>
        <div class="accordion" id="acc-cambios">
          <button class="accordion-btn" onclick="toggleAcc('acc-cambios')">
            <span>🔄 &nbsp;Cambios y devoluciones</span>
            <span class="accordion-icon">+</span>
          </button>
          <div class="accordion-body">
            <p>Tenés 30 días para cambios desde la fecha de compra. El primer cambio es gratis. La prenda debe estar en perfectas condiciones, sin uso y con etiquetas.</p>
          </div>
        </div>
        <div class="accordion" id="acc-pago">
          <button class="accordion-btn" onclick="toggleAcc('acc-pago')">
            <span>💳 &nbsp;Medios de pago</span>
            <span class="accordion-icon">+</span>
          </button>
          <div class="accordion-body">
            <p>Aceptamos todas las tarjetas de crédito y débito, transferencia bancaria, MercadoPago y efectivo. Hasta 3 cuotas sin interés con tarjeta de crédito.</p>
          </div>
        </div>
      </div>
    </div>
  </div>
  
  <div class="modal-related" style="margin-top:60px;">
    <div class="modal-related-title">✦ También te puede gustar</div>
    <div class="related-grid" id="related-grid"></div>
  </div>
</div>

<!-- TOAST -->
<div class="toast" id="toast">
  <span class="t-icon">🛍️</span>
  <span id="toast-msg">¡Producto agregado!</span>
</div>

{footer_html}

<script src="js/main.js"></script>
<script>
document.addEventListener('DOMContentLoaded', () => {{
  const params = new URLSearchParams(window.location.search);
  const id = parseInt(params.get('id')) || 1;
  
  const p = PRODUCTS.find(x => x.id === id);
  if(!p) {{
    document.getElementById('p-name').textContent = "Producto no encontrado";
    return;
  }}

  // Set Info
  document.getElementById('p-cat').textContent = p.cat;
  document.getElementById('p-name').textContent = p.name;
  document.getElementById('p-price').textContent = formatPrice(p.price);
  
  const cuota = Math.ceil(p.price / 3);
  document.getElementById('p-cuotas').innerHTML = `3 cuotas sin interés de <strong>${{formatPrice(cuota)}}</strong>`;
  
  document.getElementById('p-desc').innerHTML = p.desc;

  // Gallery
  const mainImg = document.getElementById('p-img-main');
  const thumbsEl = document.getElementById('p-thumbs');
  let currentImgIdx = 0;

  function setMainImg(idx) {{
    currentImgIdx = (idx + p.imgs.length) % p.imgs.length;
    mainImg.classList.add('switching');
    setTimeout(() => {{
      mainImg.src = p.imgs[currentImgIdx];
      mainImg.classList.remove('switching');
    }}, 200);

    document.querySelectorAll('.prod-thumb').forEach((t, i) => {{
      t.classList.toggle('active', i === currentImgIdx);
    }});
  }}

  setMainImg(0);

  p.imgs.forEach((src, i) => {{
    const div = document.createElement('div');
    div.className = 'prod-thumb' + (i === 0 ? ' active' : '');
    div.innerHTML = `<img src="${{src}}" alt="Vista ${{i+1}}" loading="lazy">`;
    div.addEventListener('click', () => setMainImg(i));
    thumbsEl.appendChild(div);
  }});

  document.getElementById('p-prev').addEventListener('click', () => setMainImg(currentImgIdx - 1));
  document.getElementById('p-next').addEventListener('click', () => setMainImg(currentImgIdx + 1));

  // Add to cart
  const btnAdd = document.getElementById('btn-add-product');
  btnAdd.addEventListener('click', () => {{
    addToCart(p.id);
    btnAdd.classList.add('added');
    btnAdd.innerHTML = `✅ &nbsp;¡Agregado!`;
    setTimeout(() => {{
      btnAdd.classList.remove('added');
      btnAdd.innerHTML = `<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M6 2 3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4Z"/><line x1="3" y1="6" x2="21" y2="6"/><path d="M16 10a4 4 0 0 1-8 0"/></svg> Agregar al carrito`;
    }}, 2200);
  }});

  // Related
  const related = PRODUCTS.filter(x => x.id !== p.id).slice(0, 4);
  const relatedGrid = document.getElementById('related-grid');
  related.forEach(r => {{
    const d = document.createElement('a');
    d.href = `producto.html?id=${{r.id}}`;
    d.className = 'related-card';
    d.style.textDecoration = 'none';
    d.innerHTML = `
      <div class="related-img"><img src="${{r.imgs[0]}}" alt="${{r.name}}" loading="lazy"></div>
      <div class="related-name">${{r.name}}</div>
      <div class="related-price">${{formatPrice(r.price)}}</div>
    `;
    relatedGrid.appendChild(d);
  }});
}});
</script>
</body>
</html>
"""

with open(r'e:\Webs\Ropita\producto.html', 'w', encoding='utf-8') as f:
    f.write(producto_html)

print("SUCCESS")
