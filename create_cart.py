import re

with open(r'e:\Webs\Ropita\index.html', 'r', encoding='utf-8') as f:
    idx_content = f.read()

header = re.search(r'<!-- ══ HEADER ══ -->.*?</header>', idx_content, re.DOTALL).group(0)
footer = re.search(r'<!-- ══ FOOTER ══ -->.*?</footer>', idx_content, re.DOTALL).group(0)

carrito_html = f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Carrito — AISHA STORE</title>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,600;0,700;1,400;1,600&family=Jost:wght@300;400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="css/style.css">
<style>
.cart-page {{ max-width: 900px; margin: 80px auto; padding: 0 40px; min-height: 50vh; }}
.cart-title {{ font-family: var(--font-display); font-size: 2.8rem; font-weight: 700; margin-bottom: 40px; color: var(--negro); letter-spacing: -0.01em; }}
.cart-empty {{ text-align: center; color: var(--gris-texto); font-size: 1.1rem; padding: 60px 0; }}
.cart-empty a {{ display: inline-block; margin-top: 20px; padding: 14px 30px; background: var(--negro); color: var(--blanco); text-decoration: none; border-radius: 999px; font-weight: 600; letter-spacing: 0.1em; text-transform: uppercase; font-size: 0.8rem; }}

.cart-items {{ display: flex; flex-direction: column; gap: 24px; }}
.cart-item {{ display: flex; gap: 20px; padding-bottom: 24px; border-bottom: 1px solid var(--gris-medio); }}
.c-img {{ width: 100px; height: 133px; object-fit: cover; border-radius: 8px; background: var(--crema); }}
.c-info {{ flex: 1; display: flex; flex-direction: column; justify-content: center; }}
.c-name {{ font-weight: 600; font-size: 1.1rem; color: var(--negro); margin-bottom: 4px; }}
.c-cat {{ font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.1em; color: var(--gris-texto); margin-bottom: 12px; }}
.c-price {{ font-weight: 700; font-size: 1rem; color: var(--negro); }}

.c-actions {{ display: flex; align-items: center; justify-content: space-between; margin-top: auto; }}
.btn-remove {{ background: none; border: none; color: var(--bordo); cursor: pointer; font-size: 0.8rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; }}

.cart-summary {{ margin-top: 40px; background: var(--crema); padding: 30px; border-radius: 12px; text-align: right; }}
.summary-total {{ font-family: var(--font-display); font-size: 2.2rem; font-weight: 700; color: var(--negro); margin-bottom: 24px; }}
.summary-total span {{ font-family: var(--font-body); font-size: 1rem; font-weight: 500; color: var(--gris-texto); text-transform: uppercase; letter-spacing: 0.1em; margin-right: 12px; }}

.btn-checkout {{ display: inline-flex; align-items: center; gap: 10px; background: #25D366; color: white; border: none; padding: 16px 40px; border-radius: 999px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.1em; cursor: pointer; font-size: 0.9rem; text-decoration: none; transition: transform 0.2s, box-shadow 0.2s; }}
.btn-checkout:hover {{ transform: translateY(-2px); box-shadow: 0 8px 20px rgba(37, 211, 102, 0.3); }}

@media(max-width: 768px) {{
  .cart-page {{ padding: 0 24px; margin: 40px auto; }}
  .cart-title {{ font-size: 2.2rem; }}
  .summary-total {{ font-size: 1.8rem; }}
  .btn-checkout {{ width: 100%; justify-content: center; }}
}}
</style>
</head>
<body>

{header}

<div class="cart-page">
  <h1 class="cart-title">Tu Carrito</h1>
  
  <div id="cart-content">
    <!-- Generado con JS -->
  </div>
</div>

{footer}

<script src="js/main.js"></script>
<script>
document.addEventListener('DOMContentLoaded', renderCart);

function renderCart() {{
  const container = document.getElementById('cart-content');
  
  if (!cart || cart.length === 0) {{
    container.innerHTML = `
      <div class="cart-empty">
        <p>Aún no agregaste productos a tu carrito.</p>
        <a href="index.html">Ver productos</a>
      </div>
    `;
    return;
  }}

  let html = '<div class="cart-items">';
  let total = 0;

  cart.forEach((item, index) => {{
    total += item.price;
    html += `
      <div class="cart-item">
        <img src="${{item.imgs[0]}}" alt="${{item.name}}" class="c-img">
        <div class="c-info">
          <div class="c-cat">${{item.cat}}</div>
          <div class="c-name">${{item.name}}</div>
          <div class="c-price">${{formatPrice(item.price)}}</div>
          <div class="c-actions">
            <button class="btn-remove" onclick="removeFromCart(${{index}})">Eliminar</button>
          </div>
        </div>
      </div>
    `;
  }});

  html += '</div>';

  html += `
    <div class="cart-summary">
      <div class="summary-total"><span>Total:</span>${{formatPrice(total)}}</div>
      <a href="#" class="btn-checkout" onclick="checkoutWhatsApp()">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 0 1-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 0 1-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 0 1 2.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0 0 12.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 0 0 5.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 0 0-3.48-8.413Z"/></svg>
        Comprar por WhatsApp
      </a>
    </div>
  `;
  container.innerHTML = html;
}}

function removeFromCart(index) {{
  cart.splice(index, 1);
  localStorage.setItem('aisha_cart', JSON.stringify(cart));
  updateCartCount();
  renderCart();
}}

function checkoutWhatsApp() {{
  let msg = "¡Hola! Quisiera comprar los siguientes artículos:\\n\\n";
  let total = 0;
  cart.forEach(item => {{
    msg += `- ${{item.name}} (${{formatPrice(item.price)}})\\n`;
    total += item.price;
  }});
  msg += `\\n*Total: ${{formatPrice(total)}}*`;
  
  const phone = "5491112345678"; // REEMPLAZAR CON NUMERO REAL
  const url = `https://wa.me/${{phone}}?text=${{encodeURIComponent(msg)}}`;
  window.open(url, '_blank');
}}
</script>
</body>
</html>
"""

with open(r'e:\Webs\Ropita\carrito.html', 'w', encoding='utf-8') as f:
    f.write(carrito_html)
