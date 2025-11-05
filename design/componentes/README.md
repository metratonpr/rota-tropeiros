# Componentes da Aplicação Rota

Esta pasta contém a documentação dos componentes criados para a aplicação de rotas.

## Estrutura de Componentes

### 1. **base.html**
Template base que inclui:
- Meta tags e configurações de SEO
- Links para Bootstrap 5.3.3 e Google Fonts (Poppins)
- Sistema de blocos para CSS e JS customizados
- Integração com Leaflet para mapas
- Inclusão automática de navbar e footer

**Blocos disponíveis:**
- `{% block title %}` - Título da página
- `{% block description %}` - Meta description
- `{% block leaflet_css %}` - CSS do Leaflet
- `{% block content %}` - Conteúdo principal
- `{% block leaflet_js %}` - JavaScript do Leaflet
- `{% block extra_js %}` - JavaScript adicional

---

### 2. **navbar.html**
Barra de navegação responsiva com:
- Logo "Viação Metropolitana"
- Menu hamburguer para mobile
- Links de navegação com scroll suave
- Destaque do link ativo
- Integrado com {% url %} do Django

---

### 3. **footer.html**
Rodapé com:
- Nome da empresa e slogan
- Links de contato (telefone e email)
- Layout responsivo

---

### 4. **hero.html**
Seção hero (cabeçalho principal) com:
- Badge de destaque "Mobilidade sustentável"
- Título e subtítulo impactantes
- Botões de ação (Ver horários / Acompanhar rota)
- Card flutuante com próximas partidas
- Gradiente de fundo com textura

**Componente incluído:**
- `proximas-partidas.html`

---

### 5. **proximas-partidas.html**
Card que exibe as próximas partidas:
- Lista de até 3 próximas rotas
- Badge colorido com horário
- Informações de origem e destino
- Badge de status "Atualizado agora"
- Dados dinâmicos vindos do backend

**Dados necessários (context):**
```python
proximas_partidas = [
    {
        'rota': <Objeto Rota>,
        'origem': 'Nome da parada',
        'destino': 'Nome da parada',
        'horario': '08:14',
        'badge_color': 'success'  # success, primary, info
    }
]
```

---

### 6. **servicos.html**
Seção de serviços com:
- Título e subtítulo descritivo
- 3 cards de serviços (IoT, App, AI)
- Ícones customizados
- Hover effect nos cards
- Layout responsivo (grid de 3 colunas)

---

### 7. **horarios.html**
Seção de horários por linha com:
- Sistema de tabs dinâmico (Bootstrap)
- Tabela de horários para cada rota
- Informações adicionais em callout
- Integração com modelo Rota e RotaParadaHorario
- Botão para solicitar linha adicional

**Dados necessários (context):**
```python
rotas = Rota.objects.filter(ativo=True).prefetch_related('horarios_parada__parada')
```

**Estrutura do loop:**
- Itera sobre todas as rotas ativas
- Para cada rota, exibe horários das paradas
- Tabs sincronizados com o mapa via data-route

---

### 8. **mapa.html**
Seção do mapa interativo com:
- Descrição do mapa e funcionalidades
- Lista de features
- Div #routeMap para renderização
- Informações de rodapé do mapa
- Botão de call-to-action

**Integração:**
- O mapa é inicializado via `route-map.js`
- Recebe dados via `window.ROUTES_DATA` do backend
- Sincronizado com as tabs de horários

---

### 9. **estatisticas.html**
Seção de estatísticas com:
- Callout "Operação monitorada 24/7"
- 3 cards com métricas:
  - Pontualidade (98%)
  - Passageiros (dinâmico)
  - Número de linhas (dinâmico)
- Layout responsivo

**Dados necessários (context):**
```python
total_passageiros = "140 mil"
total_rotas = 12
```

---

### 10. **contato.html**
Formulário de contato com:
- Campos: nome, email, assunto, mensagem
- Validação HTML5
- CSRF token do Django
- Submit para view `rota:contato`
- Layout responsivo com grid

**View necessária:**
```python
def contato(request):
    if request.method == 'POST':
        # Processar formulário
        pass
```

---

## Arquivos Estáticos

### CSS: `rota/static/rota/css/styles.css`
Contém:
- Variáveis CSS (cores da marca)
- Estilos da navbar
- Estilos do hero
- Cards (floating, service, schedule)
- Tabs de horários
- Callouts
- Mapa
- Footer
- Media queries responsivas
- Acessibilidade (prefers-reduced-motion)

**Variáveis principais:**
```css
--vm-primary: #2f9c5c;    /* Verde principal */
--vm-blue: #155f9c;       /* Azul secundário */
--vm-dark: #0d1722;       /* Texto escuro */
--vm-light: #f7faf8;      /* Background claro */
```

### JavaScript: `rota/static/rota/js/route-map.js`
Módulo para mapa interativo com:
- Inicialização do Leaflet
- Função `initRouteMap()`
- Função `clearCurrentRoute()`
- Função `loadRoute(routeId)`
- Event listeners para tabs
- Dados de fallback

**Uso:**
```javascript
// Dados injetados pelo Django
window.ROUTES_DATA = {
    linha410: {
        label: 'Linha 410',
        description: 'Terminal → Destino',
        path: [[lat, lng], ...],
        stops: [{name, description, coords}]
    }
}
```

---

## Fluxo de Dados

### Backend → Frontend

1. **View `index()`**
   - Busca rotas ativas do banco
   - Gera próximas partidas
   - Calcula estatísticas
   - Converte rotas para formato JSON
   - Passa tudo via context

2. **Template `index.html`**
   - Recebe context da view
   - Injeta `routes_data` no JavaScript
   - Inclui todos os componentes
   - Carrega CSS e JS

3. **JavaScript `route-map.js`**
   - Lê `window.ROUTES_DATA`
   - Inicializa mapa Leaflet
   - Renderiza rotas e paradas
   - Sincroniza com tabs

---

## Integração com Models Django

### Models utilizados:
- **Rota**: Linha de ônibus
- **Parada**: Ponto de parada
- **RotaParadaHorario**: Relacionamento com horários

### Exemplo de query:
```python
rotas = Rota.objects.filter(ativo=True)\
    .prefetch_related('horarios_parada__parada')\
    .order_by('nome')
```

---

## Como Usar

### 1. Criar nova rota no admin
```
/admin/rota/rota/add/
```

### 2. Adicionar paradas
```
/admin/rota/parada/add/
```

### 3. Vincular horários
```
/admin/rota/rota/<id>/change/
# Usar inline para adicionar horários
```

### 4. Ver resultado
```
/ (página inicial)
```

---

## Customização

### Mudar cores:
Editar `styles.css`:
```css
:root {
  --vm-primary: #sua-cor;
}
```

### Adicionar nova seção:
1. Criar `componente-nome.html` em `templates/rota/components/`
2. Incluir em `index.html`: `{% include 'rota/components/componente-nome.html' %}`
3. Adicionar estilos em `styles.css`

### Adicionar dados ao mapa:
Editar `views.py` → `generate_routes_data()`:
- Adicionar mais propriedades ao dicionário
- Atualizar `route-map.js` para usar novos dados

---

## Dependências Externas

- **Bootstrap 5.3.3** - Framework CSS
- **Leaflet 1.9.4** - Biblioteca de mapas
- **Google Fonts (Poppins)** - Tipografia
- **OpenStreetMap** - Tiles do mapa

---

## Responsividade

Breakpoints:
- **Mobile**: < 768px
- **Tablet**: 768px - 991px
- **Desktop**: > 992px

Todos os componentes são totalmente responsivos.

---

## Acessibilidade

- Tags semânticas (header, nav, section, footer)
- ARIA labels nos botões
- Alt text em imagens (quando aplicável)
- Suporte a `prefers-reduced-motion`
- Contraste adequado de cores
- Navegação por teclado

---

## Performance

- Uso de `prefetch_related` nas queries
- CSS minificado em produção
- Lazy loading de imagens
- Cache de templates Django
- Otimização de queries N+1

---

## Próximos Passos

1. ✅ Componentização completa
2. ✅ Extração de CSS/JS
3. ✅ Integração com models
4. ⏳ API REST para dados em tempo real
5. ⏳ WebSocket para atualizações live
6. ⏳ PWA (Progressive Web App)
7. ⏳ Sistema de notificações push

---

Criado em: Novembro 2025
Versão: 1.0
