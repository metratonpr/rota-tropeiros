# Arquitetura Técnica - Sistema de Rotas

## Visão Geral

O sistema foi completamente refatorado do arquivo HTML monolítico para uma arquitetura componentizada Django profissional.

## Estrutura de Diretórios

```
rota/
├── templates/
│   └── rota/
│       ├── base.html                 # Template base
│       ├── index.html                # Página principal
│       └── components/               # Componentes reutilizáveis
│           ├── navbar.html
│           ├── footer.html
│           ├── hero.html
│           ├── proximas-partidas.html
│           ├── servicos.html
│           ├── horarios.html
│           ├── mapa.html
│           ├── estatisticas.html
│           └── contato.html
├── static/
│   └── rota/
│       ├── css/
│       │   └── styles.css           # Estilos extraídos
│       └── js/
│           └── route-map.js         # JavaScript do mapa
├── models.py                         # Models (Rota, Parada, RotaParadaHorario)
├── views.py                          # Views e lógica de negócio
├── urls.py                           # Rotas URL
└── admin.py                          # Admin customizado
```

## Componentes Criados

### Templates (10 arquivos)
1. `base.html` - Template pai com estrutura HTML
2. `index.html` - Página principal que orquestra componentes
3. `navbar.html` - Barra de navegação
4. `footer.html` - Rodapé
5. `hero.html` - Seção hero
6. `proximas-partidas.html` - Card de próximas partidas
7. `servicos.html` - Seção de serviços
8. `horarios.html` - Tabela de horários com tabs
9. `mapa.html` - Mapa interativo
10. `estatisticas.html` - Cards de estatísticas
11. `contato.html` - Formulário de contato

### Arquivos Estáticos (2 arquivos)
- `styles.css` (175 linhas) - Todo CSS extraído e organizado
- `route-map.js` (150 linhas) - JavaScript modular do mapa

### Backend (2 arquivos modificados)
- `views.py` - 3 views criadas (index, contato, helpers)
- `urls.py` - Rotas da aplicação

## Padrões Implementados

### 1. Separação de Responsabilidades
- **Templates**: Apenas apresentação
- **Views**: Lógica de negócio e preparação de dados
- **Models**: Camada de dados
- **Static**: Assets (CSS/JS)

### 2. Componentização
Cada seção é um componente independente que pode ser:
- Reutilizado em outras páginas
- Testado isoladamente
- Modificado sem afetar outros componentes

### 3. DRY (Don't Repeat Yourself)
- Template base evita duplicação de HTML
- Componentes reutilizáveis
- CSS com variáveis
- JavaScript modular

### 4. Template Inheritance
```django
base.html (pai)
    ↓
index.html (filho)
    ↓
componentes (includes)
```

### 5. Integração Backend-Frontend
```python
# Backend (views.py)
routes_data = generate_routes_data(rotas)
context = {'routes_data': json.dumps(routes_data)}

# Frontend (index.html)
window.ROUTES_DATA = {{ routes_data|safe }};

# JavaScript (route-map.js)
const routesData = window.ROUTES_DATA || getDefaultRoutesData();
```

## Fluxo de Requisição

```
1. Cliente → GET /
2. urls.py → rota.views.index
3. views.index():
   - Busca rotas do DB
   - Gera próximas partidas
   - Calcula estatísticas
   - Converte rotas para JSON
   - Retorna context
4. Template index.html:
   - Extende base.html
   - Inclui componentes
   - Injeta dados
5. Browser:
   - Carrega CSS/JS
   - Inicializa mapa
   - Renderiza página
```

## Melhorias Implementadas

### Do HTML Original → Novo Sistema

| Aspecto | Antes | Depois |
|---------|-------|--------|
| **Estrutura** | 1 arquivo HTML (752 linhas) | 13 arquivos organizados |
| **CSS** | Inline no `<style>` | Arquivo separado modular |
| **JavaScript** | Inline no `<script>` | Arquivo separado com IIFE |
| **Dados** | Hardcoded no HTML | Dinâmico do banco de dados |
| **Manutenção** | Difícil (tudo junto) | Fácil (componentes isolados) |
| **Reutilização** | Impossível | Total (componentes) |
| **SEO** | Básico | Avançado (meta tags dinâmicas) |
| **Performance** | Boa | Ótima (cache, prefetch) |

## Recursos Adicionais

### 1. Sistema de Mensagens Django
```python
from django.contrib import messages
messages.success(request, 'Mensagem enviada!')
```

### 2. CSRF Protection
```django
<form method="post">
    {% csrf_token %}
    ...
</form>
```

### 3. URL Reversa
```django
<a href="{% url 'rota:index' %}">Home</a>
```

### 4. Filters e Tags Django
```django
{{ horario.horario|date:"H:i" }}
{{ routes_data|safe }}
{% if forloop.first %}...{% endif %}
```

### 5. Prefetch Related (otimização)
```python
rotas = Rota.objects.filter(ativo=True)\
    .prefetch_related('horarios_parada__parada')
# Evita N+1 queries
```

## Configuração Necessária

### settings.py
```python
INSTALLED_APPS = [
    ...
    'rota',
]

TEMPLATES = [{
    'DIRS': [],  # Usa app_directories loader
    'APP_DIRS': True,
}]

STATIC_URL = '/static/'
```

### Arquivos estáticos em produção
```python
# settings.py
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Comando
python manage.py collectstatic
```

## Testes

### Views
```python
from django.test import TestCase, Client

class RotaViewsTest(TestCase):
    def test_index_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'rota/index.html')
```

### Models
```python
class RotaModelTest(TestCase):
    def test_create_rota(self):
        rota = Rota.objects.create(nome='Linha 100', ativo=True)
        self.assertTrue(rota.ativo)
```

## Deploy

### Checklist
- [ ] DEBUG = False
- [ ] ALLOWED_HOSTS configurado
- [ ] collectstatic executado
- [ ] Banco de dados em produção
- [ ] Variáveis de ambiente (.env)
- [ ] HTTPS configurado
- [ ] Logs configurados

### Comandos
```bash
# Coletar arquivos estáticos
python manage.py collectstatic --noinput

# Criar banco
python manage.py migrate

# Criar superuser
python manage.py createsuperuser
```

## Extensibilidade

### Adicionar nova funcionalidade

1. **Criar componente**
```html
<!-- templates/rota/components/novo-componente.html -->
<section>...</section>
```

2. **Incluir no index**
```django
{% include 'rota/components/novo-componente.html' %}
```

3. **Adicionar dados na view**
```python
def index(request):
    context = {
        'novo_dado': get_novo_dado(),
    }
```

4. **Adicionar estilos**
```css
/* static/rota/css/styles.css */
.novo-componente { ... }
```

## Performance Tips

1. **Use select_related/prefetch_related**
```python
# Ruim (N+1 queries)
rotas = Rota.objects.all()
for rota in rotas:
    print(rota.horarios_parada.count())

# Bom (2 queries)
rotas = Rota.objects.prefetch_related('horarios_parada').all()
```

2. **Cache de templates**
```python
TEMPLATES = [{
    'OPTIONS': {
        'loaders': [
            ('django.template.loaders.cached.Loader', [
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
            ]),
        ],
    },
}]
```

3. **Compressão de assets**
```bash
pip install django-compressor
```

## Segurança

- ✅ CSRF tokens em todos os forms
- ✅ XSS protection (Django auto-escape)
- ✅ SQL Injection protection (ORM)
- ✅ Validação de inputs
- ⏳ Rate limiting (adicionar django-ratelimit)
- ⏳ HTTPS only (produção)

## Acessibilidade (a11y)

- ✅ Semantic HTML (header, nav, section, footer)
- ✅ ARIA labels
- ✅ Keyboard navigation
- ✅ Color contrast (WCAG AA)
- ✅ Responsive design
- ✅ Reduced motion support

## Browser Support

- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+
- Mobile browsers (iOS Safari, Chrome Android)

## Licença

Projeto interno - Viação Metropolitana

## Contribuindo

1. Fork do repositório
2. Criar branch feature (`git checkout -b feature/nova-feature`)
3. Commit changes (`git commit -m 'Add nova feature'`)
4. Push to branch (`git push origin feature/nova-feature`)
5. Criar Pull Request

---

**Versão**: 1.0  
**Última atualização**: Novembro 2025  
**Autor**: Sistema automatizado de componentização
