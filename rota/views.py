import json
from datetime import datetime, timedelta
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Count
from .models import Rota, Parada, RotaParadaHorario


def index(request):
    """
    View principal que exibe a página inicial com rotas, horários e mapa.
    """
    # Busca todas as rotas ativas
    rotas = Rota.objects.filter(ativo=True).prefetch_related('horarios_parada__parada')
    
    # Gera dados de próximas partidas (exemplo estático - ajustar para tempo real)
    proximas_partidas = get_proximas_partidas(rotas)
    
    # Estatísticas
    total_rotas = rotas.count()
    total_passageiros = "140 mil"  # Pode vir de um modelo de estatísticas
    
    # Gera dados das rotas para o mapa (formato JSON)
    routes_data = generate_routes_data(rotas)
    
    context = {
        'rotas': rotas,
        'proximas_partidas': proximas_partidas,
        'total_rotas': total_rotas,
        'total_passageiros': total_passageiros,
        'routes_data': json.dumps(routes_data),
    }
    
    return render(request, 'rota/index.html', context)


def contato(request):
    """
    View para processar o formulário de contato.
    """
    if request.method == 'POST':
        nome = request.POST.get('nome')
        email = request.POST.get('email')
        assunto = request.POST.get('assunto')
        mensagem = request.POST.get('mensagem')
        
        # Aqui você pode salvar em um modelo ou enviar por e-mail
        # Por enquanto, apenas exibe uma mensagem de sucesso
        
        messages.success(request, f'Obrigado {nome}! Sua mensagem foi enviada com sucesso.')
        return redirect('rota:index')
    
    return redirect('rota:index')


def get_proximas_partidas(rotas, limit=3):
    """
    Retorna as próximas partidas das rotas.
    Em produção, isso deve buscar de um sistema de tempo real.
    """
    partidas = []
    badge_colors = ['success', 'primary', 'info']
    
    for idx, rota in enumerate(rotas[:limit]):
        # Pega o primeiro horário ativo da rota
        primeiro_horario = rota.horarios_parada.filter(ativo=True).first()
        
        if primeiro_horario:
            # Busca origem e destino (primeira e última parada)
            horarios_ordenados = list(rota.horarios_parada.filter(ativo=True).order_by('horario'))
            
            origem = horarios_ordenados[0].parada.endereco if horarios_ordenados else "Terminal"
            destino = horarios_ordenados[-1].parada.endereco if len(horarios_ordenados) > 1 else "Destino"
            
            partidas.append({
                'rota': rota,
                'origem': origem[:30] + '...' if len(origem) > 30 else origem,
                'destino': destino[:30] + '...' if len(destino) > 30 else destino,
                'horario': primeiro_horario.horario.strftime('%H:%M'),
                'badge_color': badge_colors[idx % len(badge_colors)]
            })
    
    return partidas


def generate_routes_data(rotas):
    """
    Gera os dados das rotas no formato esperado pelo JavaScript do mapa.
    """
    routes_data = {}
    
    for rota in rotas:
        horarios = rota.horarios_parada.filter(ativo=True).order_by('horario')
        
        if not horarios.exists():
            continue
        
        # Converte QuerySet para lista para permitir indexação negativa
        horarios_list = list(horarios)
        
        # Extrai coordenadas das paradas
        stops = []
        path = []
        
        for horario in horarios_list:
            parada = horario.parada
            
            # Tenta extrair latitude e longitude do campo latitude_longitude
            # Formato esperado: "-23.5615,-46.6559" ou similar
            if parada.latitude_longitude:
                try:
                    coords_str = parada.latitude_longitude.strip()
                    # Remove parênteses se existirem
                    coords_str = coords_str.replace('(', '').replace(')', '')
                    
                    # Tenta separar por vírgula ou espaço
                    if ',' in coords_str:
                        lat, lng = coords_str.split(',')
                    else:
                        lat, lng = coords_str.split()
                    
                    lat = float(lat.strip())
                    lng = float(lng.strip())
                    
                    coords = [lat, lng]
                    path.append(coords)
                    
                    stops.append({
                        'name': parada.endereco,
                        'description': f'Horário: {horario.horario.strftime("%H:%M")}',
                        'coords': coords
                    })
                except (ValueError, AttributeError):
                    # Se não conseguir parsear, usa coordenadas padrão de São Paulo
                    pass
        
        # Se não tiver coordenadas válidas, usa dados de exemplo
        if not path:
            # Coordenadas de exemplo (região de São Paulo)
            path = [
                [-23.5615, -46.6559],
                [-23.5589, -46.6457],
                [-23.5556, -46.6399],
            ]
            stops = [
                {
                    'name': horarios_list[0].parada.endereco if horarios_list else 'Início',
                    'description': 'Parada inicial',
                    'coords': path[0]
                },
                {
                    'name': horarios_list[-1].parada.endereco if len(horarios_list) > 1 else 'Fim',
                    'description': 'Parada final',
                    'coords': path[-1]
                }
            ]
        
        primeira_parada = horarios_list[0].parada.endereco if horarios_list else ''
        ultima_parada = horarios_list[-1].parada.endereco if len(horarios_list) > 1 else ''
        
        routes_data[f'linha{rota.id}'] = {
            'label': rota.nome,
            'description': f'{primeira_parada} → {ultima_parada}',
            'path': path,
            'stops': stops
        }
    
    return routes_data
