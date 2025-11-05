"""
SEO utilities para geração de sitemap e robots.txt
"""
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils import timezone


def robots_txt(request):
    """
    Gera robots.txt dinâmico
    """
    content = f"""# Viação Rota dos Tropeiros - Robots.txt
User-agent: *
Allow: /
Disallow: /admin/
Disallow: /static/admin/

# Crawl-delay para bots
Crawl-delay: 1

# Google
User-agent: Googlebot
Allow: /

# Bing
User-agent: Bingbot
Allow: /

# Sitemap
Sitemap: {request.scheme}://{request.get_host()}/sitemap.xml
"""
    return HttpResponse(content, content_type="text/plain")


def sitemap_xml(request):
    """
    Gera sitemap.xml dinâmico
    """
    from .models import Rota
    
    base_url = f"{request.scheme}://{request.get_host()}"
    current_date = timezone.now().strftime('%Y-%m-%d')
    
    # URLs estáticas
    urls = [
        {
            'loc': base_url + '/',
            'lastmod': current_date,
            'changefreq': 'daily',
            'priority': '1.0'
        },
    ]
    
    # URLs dinâmicas (rotas)
    rotas = Rota.objects.filter(ativo=True)
    for rota in rotas:
        urls.append({
            'loc': base_url + f'/#linha{rota.id}',
            'lastmod': current_date,
            'changefreq': 'daily',
            'priority': '0.8'
        })
    
    xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
"""
    
    for url in urls:
        xml += f"""  <url>
    <loc>{url['loc']}</loc>
    <lastmod>{url['lastmod']}</lastmod>
    <changefreq>{url['changefreq']}</changefreq>
    <priority>{url['priority']}</priority>
  </url>
"""
    
    xml += "</urlset>"
    
    return HttpResponse(xml, content_type="application/xml")
