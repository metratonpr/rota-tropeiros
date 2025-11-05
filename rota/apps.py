"""
Arquivo: rota/apps.py

Comentário profissional (para não-programadores):

Este pequeno arquivo fornece um nome legível (rótulo) para o aplicativo "rota" dentro do projeto.
O Django usa essa informação para exibir o nome do aplicativo em telas administrativas e relatórios.

O que mudou:
- Foi incluído um `verbose_name` mais descritivo: "Sistema de Rotas e Horários". Isso melhora a
    compreensão do conteúdo do aplicativo por pessoas não técnicas.

Impacto:
- Alteração puramente estética/usabilidade no painel administrativo; não modifica dados nem lógica.

Quando editar:
- Altere o texto de `verbose_name` se quiser outro rótulo. Mudanças aqui são de baixo risco.
"""

from django.apps import AppConfig


class RotaConfig(AppConfig):
        default_auto_field = "django.db.models.BigAutoField"
        name = "rota"
        verbose_name = "Sistema de Rotas e Horários"
