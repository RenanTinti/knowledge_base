from django.contrib import admin

from .forms import SuggestionForm

# Importação do procedimento. Perceba que é preciso colocar um ponto antes do models, indicando que o arquivo models está no mesmo caminho desse arquivo vigente, o admin.py
from .models import Ferramenta, Procedimento
from .models import Comunicado, Link, Suggestion
from .models import Documento

# Register your models here.
# Comando para registrar um model para que ele seja apresentado no banco de dados.

@admin.register(Procedimento)
class ProcedimentoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'ativo')
    search_fields = ('titulo',)
    list_filter = ('grupo',)
    readonly_fields = ('data_criacao', 'data_atualizacao', 'visualizacoes')

@admin.register(Comunicado)
class ComunicadoAdmin(admin.ModelAdmin):
    list_display = ('titulo',)
    search_fields = ('titulo',)
    list_filter = ('grupo',)
    readonly_fields = ('data_criacao',)

@admin.register(Ferramenta)
class FerramentaAdmin(admin.ModelAdmin):
    list_display = ('nome',)
    search_fields = ('nome',)
    readonly_fields = ('data_criacao',)

admin.site.register(Link)
admin.site.register(Suggestion)
admin.site.register(Documento)