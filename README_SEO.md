# 🔍 Guia de SEO - Viação Rota dos Tropeiros

## 📋 Resumo das Implementações

Este documento descreve todas as otimizações de SEO (Search Engine Optimization) implementadas no site da Viação Rota dos Tropeiros para melhorar a visibilidade nos mecanismos de busca.

---

## ✅ Meta Tags Implementadas

### 1. Meta Tags Básicas
```html
<title>Viação Rota dos Tropeiros - Horários e Rotas Castro-PR</title>
<meta name="description" content="...">
<meta name="keywords" content="ônibus castro pr, transporte público castro paraná, ...">
<meta name="author" content="Viação Rota dos Tropeiros">
<meta name="robots" content="index, follow">
```

### 2. Geolocalização
```html
<meta name="geo.region" content="BR-PR">
<meta name="geo.placename" content="Castro, Paraná">
<meta name="geo.position" content="-24.7911;-50.0119">
<meta name="ICBM" content="-24.7911, -50.0119">
```

### 3. Open Graph (Facebook, LinkedIn)
```html
<meta property="og:type" content="website">
<meta property="og:title" content="Viação Rota dos Tropeiros...">
<meta property="og:description" content="...">
<meta property="og:image" content="/static/rota/img/og-image.jpg">
<meta property="og:locale" content="pt_BR">
```

### 4. Twitter Card
```html
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="...">
<meta name="twitter:description" content="...">
<meta name="twitter:image" content="...">
```

---

## 🗺️ Sitemap e Robots.txt

### Sitemap.xml
- **URL**: `/sitemap.xml`
- **Atualização**: Dinâmica (gerada pelo Django)
- **Conteúdo**: Página inicial + todas as rotas ativas
- **Formato**: XML válido para Google Search Console

### Robots.txt
- **URL**: `/robots.txt`
- **Configuração**: Permite todos os bots
- **Bloqueios**: `/admin/`, `/static/admin/`
- **Sitemap**: Referência automática ao sitemap.xml

---

## 📊 Schema.org (JSON-LD)

### 1. TransitSystem Schema
Define o sistema de transporte público:
```json
{
  "@type": "TransitSystem",
  "name": "Viação Rota dos Tropeiros",
  "address": { "addressLocality": "Castro", "addressRegion": "PR" },
  "geo": { "latitude": "-24.7911", "longitude": "-50.0119" }
}
```

### 2. Organization Schema
Define a empresa:
```json
{
  "@type": "Organization",
  "name": "Viação Rota dos Tropeiros",
  "telephone": "+55-42-3542-1234",
  "openingHours": "Mo-Sa 05:00-23:00, Su 06:00-22:00"
}
```

### 3. WebSite Schema
Define o site com busca:
```json
{
  "@type": "WebSite",
  "potentialAction": {
    "@type": "SearchAction",
    "target": "/busca?q={search_term_string}"
  }
}
```

---

## 🎯 Palavras-chave Otimizadas

### Principais Keywords:
1. **ônibus castro pr**
2. **transporte público castro paraná**
3. **horários ônibus castro**
4. **rotas urbanas castro**
5. **viação castro**
6. **mapa ônibus castro**
7. **linhas de ônibus castro pr**
8. **transporte coletivo castro**

### Long-tail Keywords:
- "consultar horários ônibus castro pr"
- "mapa rotas ônibus castro tempo real"
- "viação rota dos tropeiros horários"
- "transporte público castro paraná hoje"

---

## 📱 Otimizações de Performance

### 1. Compressão Gzip (.htaccess)
- HTML, CSS, JS comprimidos
- Redução de ~70% no tamanho dos arquivos

### 2. Cache de Browser
- Imagens: 1 ano
- CSS/JS: 1 mês
- HTML: sem cache (conteúdo dinâmico)

### 3. Headers de Segurança
- X-Content-Type-Options: nosniff
- X-Frame-Options: SAMEORIGIN
- X-XSS-Protection: 1; mode=block

---

## 🔗 URLs Canônicas

Cada página tem URL canônica para evitar conteúdo duplicado:
```html
<link rel="canonical" href="{{ request.build_absolute_uri }}">
```

---

## 🌐 Acessibilidade SEO

### Tags Semânticas HTML5:
- `<header role="banner">` - Cabeçalho principal
- `<nav role="navigation">` - Navegação
- `<main role="main">` - Conteúdo principal
- `<footer role="contentinfo">` - Rodapé

### ARIA Labels:
```html
<a href="#horarios" aria-label="Ver horários de ônibus">Ver horários</a>
```

---

## 📈 Como Monitorar SEO

### 1. Google Search Console
- Cadastre o site em: https://search.google.com/search-console
- Envie o sitemap: `https://seudominio.com/sitemap.xml`
- Monitore: Impressões, cliques, posições

### 2. Google Analytics
- Rastreie: Tráfego orgânico, palavras-chave, conversões

### 3. Ferramentas de Teste

#### Teste de Schema.org:
```
https://validator.schema.org/
```
Cole o HTML da página para validar JSON-LD

#### Teste de Open Graph:
```
https://developers.facebook.com/tools/debug/
```
Cole a URL para ver preview no Facebook

#### Teste de Rich Results (Google):
```
https://search.google.com/test/rich-results
```
Verifica se o Google consegue ler seus dados estruturados

#### PageSpeed Insights:
```
https://pagespeed.web.dev/
```
Analisa velocidade e SEO técnico

---

## 🚀 Próximos Passos para Melhorar SEO

### 1. Conteúdo
- [ ] Criar blog com dicas de transporte público
- [ ] Adicionar FAQs (Perguntas Frequentes)
- [ ] Criar páginas para cada linha de ônibus

### 2. Links
- [ ] Parceria com sites de Castro-PR
- [ ] Cadastro em diretórios locais
- [ ] Perfis em redes sociais (Facebook, Instagram)

### 3. Local SEO
- [ ] Google My Business (Google Maps)
- [ ] Bing Places
- [ ] Avaliações de usuários

### 4. Technical SEO
- [ ] Implementar HTTPS em produção
- [ ] AMP (Accelerated Mobile Pages)
- [ ] Service Worker (PWA)

---

## 📞 Contato

Para dúvidas sobre SEO do site:
- **Telefone**: (42) 3542-1234
- **Localização**: Castro-PR
- **Coordenadas**: -24.7911, -50.0119

---

## 🔖 Arquivos Relacionados

- `/rota/templates/rota/base.html` - Meta tags principais
- `/rota/templates/rota/index.html` - Schema.org JSON-LD
- `/rota/seo.py` - Funções de sitemap e robots.txt
- `/rota/urls.py` - Rotas SEO
- `/.htaccess` - Configurações de servidor

---

**Última atualização**: 05/11/2025  
**Versão**: 1.0.0
