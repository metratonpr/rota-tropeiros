/**
 * Viação Metropolitana - Route Map Module
 * Gerencia o mapa interativo de rotas usando Leaflet
 */

(function() {
  'use strict';

  /**
   * Inicializa o mapa de rotas
   */
  function initRouteMap() {
    const mapElement = document.getElementById('routeMap');
    if (!mapElement) {
      console.warn('Elemento #routeMap não encontrado.');
      return;
    }

    // Dados das rotas - em produção, buscar do backend via API
    const routesData = window.ROUTES_DATA || getDefaultRoutesData();

    // Inicializa o mapa
    const map = L.map('routeMap', {
      scrollWheelZoom: false,
      minZoom: 11
    });

    // Adiciona camada de tiles
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      maxZoom: 18,
      attribution: '&copy; OpenStreetMap contributors'
    }).addTo(map);

    let routePolyline = null;
    let stopMarkers = [];
    const infoElement = document.getElementById('routeMapInfo');
    const infoBaseMessage = infoElement ? infoElement.textContent : '';

    /**
     * Remove rota atual do mapa
     */
    function clearCurrentRoute() {
      if (routePolyline) {
        map.removeLayer(routePolyline);
        routePolyline = null;
      }
      stopMarkers.forEach(marker => map.removeLayer(marker));
      stopMarkers = [];
    }

    /**
     * Carrega uma rota no mapa
     * @param {string} routeId - ID da rota
     */
    function loadRoute(routeId) {
      const route = routesData[routeId];
      if (!route) {
        console.warn(`Rota ${routeId} não encontrada.`);
        return;
      }

      clearCurrentRoute();

      // Desenha a linha da rota
      routePolyline = L.polyline(route.path, {
        color: '#2f9c5c',
        weight: 5,
        opacity: 0.9,
        lineJoin: 'round'
      }).addTo(map);

      // Adiciona marcadores de paradas
      stopMarkers = route.stops.map(stop => {
        return L.circleMarker(stop.coords, {
          radius: 6,
          fillColor: '#155f9c',
          color: '#ffffff',
          weight: 2,
          opacity: 1,
          fillOpacity: 0.9
        })
          .addTo(map)
          .bindPopup(`<strong>${stop.name}</strong><br>${stop.description}`);
      });

      // Ajusta o zoom para mostrar toda a rota
      const bounds = routePolyline.getBounds();
      if (bounds.isValid()) {
        map.fitBounds(bounds, { padding: [24, 24] });
      } else {
        map.setView(route.path[0], 13);
      }

      // Atualiza informações
      if (infoElement) {
        infoElement.textContent = `${infoBaseMessage} Rota ativa: ${route.label} — ${route.description}. ${route.stops.length} paradas georreferenciadas.`;
      }
    }

    // Carrega rota inicial
    const activeButton = document.querySelector('#lineTabs .nav-link.active[data-route]');
    const initialRouteId = activeButton ? activeButton.dataset.route : Object.keys(routesData)[0];
    loadRoute(initialRouteId);

    // Event listener para mudança de abas
    document.querySelectorAll('#lineTabs .nav-link[data-route]').forEach(button => {
      button.addEventListener('shown.bs.tab', event => {
        const { route } = event.target.dataset;
        loadRoute(route);
      });
    });
  }

  /**
   * Retorna dados padrão das rotas (fallback)
   */
  function getDefaultRoutesData() {
    return {
      linha410: {
        label: 'Linha 410',
        description: 'Terminal Verde Vida → Parque Atlântico',
        path: [
          [-23.5615, -46.6559],
          [-23.5601, -46.6502],
          [-23.558, -46.6438],
          [-23.5532, -46.6365],
          [-23.5489, -46.6291]
        ],
        stops: [
          {
            name: 'Terminal Verde Vida',
            description: 'Integração com metrô Linha Verde e bicicletário seguro.',
            coords: [-23.5615, -46.6559]
          },
          {
            name: 'Jardim Primavera',
            description: 'Corredor exclusivo com embarque preferencial.',
            coords: [-23.5589, -46.6457]
          },
          {
            name: 'Hub Intermodal Central',
            description: 'Conexão com VLT e linhas intermunicipais.',
            coords: [-23.5556, -46.6399]
          },
          {
            name: 'Parque Atlântico',
            description: 'Ponto final próximo ao centro cultural e área verde.',
            coords: [-23.5489, -46.6291]
          }
        ]
      }
    };
  }

  // Inicializa quando o DOM estiver pronto
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initRouteMap);
  } else {
    initRouteMap();
  }

})();
