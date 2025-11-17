"""
Arquivo: rota/admin.py

Comentário profissional (para não-programadores):

Este arquivo customiza a área administrativa do sistema — a interface interna que pessoas
autorizadas usam para criar, editar e remover rotas, paradas e horários.

O que foi feito aqui:
- Personalização dos títulos e cabeçalhos do painel para Português e com o nome da empresa.
- Definição de ações em lote (por exemplo, "Marcar como ativo/inativo") para facilitar manutenção.
- Inserção de informações úteis nas listas (colunas, filtros e pesquisas) para encontrar dados rapidamente.

Observações importantes:
- Esse arquivo não altera o site público; impacta somente quem tem acesso ao painel administrativo.
- Só pessoas com conta administrativa devem acessar essa área.

Sequência sugerida para edição (se precisar alterar):
1) Alterações de texto (títulos) são seguras — revise somente a parte textual.
2) Alterações nas ações que modificam registros em massa devem ser testadas em ambiente de
    desenvolvimento antes de aplicar em produção.
3) Ao incluir novos campos nas listagens, confirme com o time que o campo existe nas models.

"""

from django.contrib import admin
from .models import Rota, Parada, RotaParadaHorario

# Configuração do Admin em Português
admin.site.site_header = "Viação Rota dos Tropeiros - Administração"
admin.site.site_title = "Admin Rota dos Tropeiros"
admin.site.index_title = "Painel de Controle"

@admin.action(description="Marcar como ativo")
def marcar_ativo(modeladmin, request, queryset):
    queryset.update(ativo=True)

@admin.action(description="Marcar como inativo")
def marcar_inativo(modeladmin, request, queryset):
    queryset.update(ativo=False)

class RotaParadaHorarioInline(admin.TabularInline):
    model = RotaParadaHorario
    extra = 1
    fields = ("parada", "horario", "ativo")
    autocomplete_fields = ("parada",)
    show_change_link = True
    verbose_name = "Horário na Parada"
    verbose_name_plural = "Horários nas Paradas"

@admin.register(Rota)
class RotaAdmin(admin.ModelAdmin):
    list_display = ("nome", "ativo", "qtd_horarios")
    list_filter = ("ativo",)
    search_fields = ("nome",)
    ordering = ("nome",)
    inlines = (RotaParadaHorarioInline,)
    actions = (marcar_ativo, marcar_inativo)

    def qtd_horarios(self, obj):
        return obj.horarios_parada.count()
    qtd_horarios.short_description = "Quantidade de horários"

class RotaParadaHorarioInlineParaParada(RotaParadaHorarioInline):
    fk_name = "parada"
    fields = ("rota", "horario", "ativo")
    autocomplete_fields = ("rota",)

@admin.register(Parada)
class ParadaAdmin(admin.ModelAdmin):
    list_display = ("endereco", "latitude_longitude", "ativo")
    list_filter = ("ativo",)
    search_fields = ("endereco", "latitude_longitude")
    ordering = ("endereco",)
    inlines = (RotaParadaHorarioInlineParaParada,)
    actions = (marcar_ativo, marcar_inativo)