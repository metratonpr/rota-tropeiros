from django.contrib import admin
from .models import Rota, Parada, RotaParadaHorario

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