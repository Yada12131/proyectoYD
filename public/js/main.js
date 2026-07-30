/**
 * YD PROTECCIÓN - INTERACTIVIDAD DEL CATÁLOGO & RASTREO DE CLIENTES
 */

document.addEventListener('DOMContentLoaded', () => {
  const searchInput = document.getElementById('searchInput');
  const categoryPills = document.querySelectorAll('.category-pill');
  const productCards = document.querySelectorAll('.product-card');
  const productCountEl = document.getElementById('productCount');
  const modalBackdrop = document.getElementById('modalBackdrop');
  const modalCloseBtn = document.getElementById('modalCloseBtn');
  
  let currentCategory = 'todos';
  let currentSearch = '';

  // Configuración de número de WhatsApp (Reemplazar con el teléfono real de YD Protección)
  const WHATSAPP_PHONE = '573000000000'; 

  // 1. FILTRADO EN TIEMPO REAL
  function filterProducts() {
    let visibleCount = 0;

    productCards.forEach(card => {
      const cardCategory = card.getAttribute('data-category');
      const title = card.querySelector('.product-title').textContent.toLowerCase();
      const desc = card.querySelector('.product-desc').textContent.toLowerCase();

      const matchesCategory = (currentCategory === 'todos') || (cardCategory === currentCategory);
      const matchesSearch = title.includes(currentSearch) || desc.includes(currentSearch);

      if (matchesCategory && matchesSearch) {
        card.style.display = 'flex';
        visibleCount++;
      } else {
        card.style.display = 'none';
      }
    });

    if (productCountEl) {
      productCountEl.textContent = `${visibleCount} producto${visibleCount !== 1 ? 's' : ''} disponible${visibleCount !== 1 ? 's' : ''}`;
    }
  }

  // Búsqueda
  if (searchInput) {
    let debounceTimer;
    searchInput.addEventListener('input', (e) => {
      currentSearch = e.target.value.toLowerCase().trim();
      filterProducts();

      clearTimeout(debounceTimer);
      if (currentSearch.length >= 3) {
        debounceTimer = setTimeout(() => {
          trackEvent('search', null, currentCategory, currentSearch);
        }, 1000);
      }
    });
  }

  // Filtro por píldoras de categoría
  categoryPills.forEach(pill => {
    pill.addEventListener('click', () => {
      categoryPills.forEach(p => p.classList.remove('active'));
      pill.classList.add('active');

      currentCategory = pill.getAttribute('data-category');
      filterProducts();
      trackEvent('view_category', null, currentCategory);
    });
  });

  // 2. MODAL VISTA RÁPIDA DE PRODUCTO
  window.openProductModal = function(productId) {
    const card = document.querySelector(`.product-card[data-id="${productId}"]`);
    if (!card) return;

    const title = card.querySelector('.product-title').textContent;
    const desc = card.querySelector('.product-desc').textContent;
    const imgSrc = card.querySelector('img').src;
    const categoryName = card.querySelector('.product-category-tag').textContent;
    const category = card.getAttribute('data-category');
    const specsHTML = card.querySelector('.product-specs-list').innerHTML;

    document.getElementById('modalTitle').textContent = title;
    document.getElementById('modalDesc').textContent = desc;
    document.getElementById('modalCategory').textContent = categoryName;
    document.getElementById('modalImage').src = imgSrc;
    document.getElementById('modalSpecs').innerHTML = specsHTML;

    // Configurar botón cotizar dentro del modal
    const modalQuoteBtn = document.getElementById('modalQuoteBtn');
    modalQuoteBtn.onclick = () => sendWhatsAppQuote(productId, title, category);

    modalBackdrop.classList.add('active');
    document.body.style.overflow = 'hidden';

    // Registrar interés en el backend
    trackEvent('view_product', productId, category);
  };

  if (modalCloseBtn) {
    modalCloseBtn.addEventListener('click', closeModal);
  }

  if (modalBackdrop) {
    modalBackdrop.addEventListener('click', (e) => {
      if (e.target === modalBackdrop) closeModal();
    });
  }

  function closeModal() {
    modalBackdrop.classList.remove('active');
    document.body.style.overflow = 'auto';
  }

  // 3. GENERADOR DE MENSAJE INTELIGENTE DE WHATSAPP
  window.sendWhatsAppQuote = function(productId, productTitle, category) {
    // Registrar evento de intención de compra / cotización
    trackEvent('quote_whatsapp', productId, category);

    const message = `Hola *YD Protección*, estoy interesado en cotizar el siguiente producto del catálogo web:\n\n` +
                    `📌 *Producto:* ${productTitle}\n` +
                    `🆔 *Código:* ${productId}\n\n` +
                    `Por favor me comparten precio, disponibilidad y tiempo de entrega. Muchas gracias!`;

    const encodedMsg = encodeURIComponent(message);
    const waUrl = `https://wa.me/${WHATSAPP_PHONE}?text=${encodedMsg}`;
    
    window.open(waUrl, '_blank');
  };

  // 4. RASTREO EN BACKEND (FASTAPI API)
  function trackEvent(eventType, productId = null, category = null, search = null) {
    fetch('/api/track', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        event: eventType,
        product_id: productId,
        category: category,
        query: search,
        timestamp: new Date().toISOString()
      })
    }).catch(err => console.log('Tracking debug:', err));
  }
});
