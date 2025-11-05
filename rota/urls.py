from django.urls import path
from . import views
from . import seo

app_name = 'rota'

urlpatterns = [
    path('', views.index, name='index'),
    path('contato/', views.contato, name='contato'),
    
    # SEO
    path('robots.txt', seo.robots_txt, name='robots_txt'),
    path('sitemap.xml', seo.sitemap_xml, name='sitemap_xml'),
]
