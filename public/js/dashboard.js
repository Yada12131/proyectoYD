/**
 * DASHBOARD ANALYTICS JS - YD PROTECCIÓN
 */

document.addEventListener('DOMContentLoaded', () => {
  fetchAnalytics();

  // Recargar métricas cada 10 segundos
  setInterval(fetchAnalytics, 10000);
});

function fetchAnalytics() {
  fetch('/api/analytics')
    .then(res => res.json())
    .then(data => {
      // Actualizar contadores
      document.getElementById('metricTotalViews').textContent = data.total_views || 0;
      document.getElementById('metricTotalQuotes').textContent = data.total_quotes || 0;

      // Renderizar Top Vistos
      const topViewedList = document.getElementById('topViewedList');
      topViewedList.innerHTML = '';
      if (data.top_viewed && data.top_viewed.length > 0) {
        data.top_viewed.forEach(item => {
          const li = document.createElement('li');
          li.className = 'rank-item';
          li.innerHTML = `
            <span class="rank-item-title">${item.title}</span>
            <span class="rank-badge">${item.views} clics</span>
          `;
          topViewedList.appendChild(li);
        });
      } else {
        topViewedList.innerHTML = '<li class="rank-item"><span class="rank-item-title" style="color:#94A3B8;">Aún no hay suficientes clics registrados</span></li>';
      }

      // Renderizar Top Cotizados
      const topQuotedList = document.getElementById('topQuotedList');
      topQuotedList.innerHTML = '';
      if (data.top_quoted && data.top_quoted.length > 0) {
        data.top_quoted.forEach(item => {
          const li = document.createElement('li');
          li.className = 'rank-item';
          li.innerHTML = `
            <span class="rank-item-title">${item.title}</span>
            <span class="rank-badge" style="background: rgba(37,211,102,0.15); color: #25D366;">${item.quotes} WhatsApp</span>
          `;
          topQuotedList.appendChild(li);
        });
      } else {
        topQuotedList.innerHTML = '<li class="rank-item"><span class="rank-item-title" style="color:#94A3B8;">Aún no hay cotizaciones iniciadas</span></li>';
      }

      // Renderizar Búsquedas Recientes
      const recentSearchesCloud = document.getElementById('recentSearchesCloud');
      recentSearchesCloud.innerHTML = '';
      if (data.recent_searches && data.recent_searches.length > 0) {
        data.recent_searches.forEach(term => {
          const span = document.createElement('span');
          span.className = 'tag-search';
          span.textContent = term;
          recentSearchesCloud.appendChild(span);
        });
      } else {
        recentSearchesCloud.innerHTML = '<span class="rank-item-title" style="color:#94A3B8;">No hay búsquedas recientes</span>';
      }
    })
    .catch(err => console.log('Error fetching analytics:', err));
}
