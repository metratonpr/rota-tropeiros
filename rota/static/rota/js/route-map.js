/**
 * Viação Rota dos Tropeiros - Route Map Module
 * Gerencia o mapa interativo de rotas usando Leaflet
 */

(function() {
  'use strict';

  // Coordenadas de Castro-PR (centro da cidade)
  const CASTRO_CENTER = [-24.7911, -50.0119];

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

    // Inicializa o mapa centralizado em Castro-PR
    const map = L.map('routeMap', {
      center: CASTRO_CENTER,
      zoom: 13,
      scrollWheelZoom: false,
      minZoom: 11,
      maxZoom: 18
    });

    // Adiciona camada de tiles do OpenStreetMap (gratuito)
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      maxZoom: 18,
      attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(map);

    let routePolyline = null;
    let stopMarkers = [];
    const infoElement = document.getElementById('routeMapInfo');
    const infoBaseMessage = infoElement ? infoElement.textContent : '';

    /**
     * Remove rota atual do mapa com animação suave
     */
    function clearCurrentRoute() {
      if (routePolyline) {
        routePolyline.remove();
        routePolyline = null;
      }
      stopMarkers.forEach(marker => marker.remove());
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
        map.fitBounds(bounds, { padding: [30, 30] });
      } else {
        // Se não houver bounds válidos, centraliza em Castro
        map.setView(CASTRO_CENTER, 13);
      }

      // Atualiza informações
      if (infoElement) {
        const baseMsg = 'Mapa das rotas em Castro-PR.';
        infoElement.textContent = `${baseMsg} Rota ativa: ${route.label} — ${route.description}. ${route.stops.length} paradas.`;
      }
    }

    // Carrega rota inicial ou mostra mapa de Castro
    const activeButton = document.querySelector('#lineTabs .nav-link.active[data-route]');
    if (activeButton && Object.keys(routesData).length > 0) {
      const initialRouteId = activeButton.dataset.route || Object.keys(routesData)[0];
      loadRoute(initialRouteId);
    } else {
      // Se não há rotas, apenas mostra o mapa de Castro
      map.setView(CASTRO_CENTER, 13);
      if (infoElement) {
        infoElement.textContent = 'Mapa de Castro-PR. Selecione uma linha para ver o trajeto.';
      }
    }

    // Event listener para mudança de abas (evento do Bootstrap)
    document.querySelectorAll('#lineTabs .nav-link[data-route]').forEach(button => {
      // Evento do Bootstrap quando a tab é exibida
      button.addEventListener('shown.bs.tab', event => {
        const routeId = event.target.dataset.route;
        console.log('Tab shown (Bootstrap event):', routeId);
        loadRoute(routeId);
      });
      
      // Fallback: também escuta cliques diretos
      button.addEventListener('click', event => {
        const routeId = event.currentTarget.dataset.route;
        console.log('Tab clicked:', routeId);
        // Pequeno delay para garantir que o Bootstrap processou primeiro
        setTimeout(() => loadRoute(routeId), 100);
      });
    });

    console.log('Mapa inicializado. Rotas disponíveis:', Object.keys(routesData));
    console.log('Event listeners adicionados a', document.querySelectorAll('#lineTabs .nav-link[data-route]').length, 'botões');
  }

  /**
   * Retorna dados padrão das rotas para Castro-PR (fallback)
   */
  function getDefaultRoutesData() {
    return {
      linha1: {
        label: 'Linha Centro',
        description: 'Centro → Bairros',
        path: [
          [-24.7911, -50.0119], // Centro de Castro
          [-24.7850, -50.0100],
          [-24.7800, -50.0080]
        ],
        stops: [
          {
            name: 'Terminal Central',
            description: 'Ponto de partida no centro de Castro.',
            coords: [-24.7911, -50.0119]
          },
          {
            name: 'Praça Getúlio Vargas',
            description: 'Parada próxima à praça central.',
            coords: [-24.7850, -50.0100]
          },
          {
            name: 'Bairro',
            description: 'Parada em bairro residencial.',
            coords: [-24.7800, -50.0080]
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
