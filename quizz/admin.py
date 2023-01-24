from django.contrib import admin

from .models import Pregunta, ElegirRespuesta, PreguntasRespondidas, QuizUsuario

from .forms import ElegirInLineFormSet

# Register your models here.


class ElegirRespuestaInline(admin.TabularInline):
    model = ElegirRespuesta
    can_delete = False
    max_num = ElegirRespuesta.MAX_RESPUESTAS
    min_num = ElegirRespuesta.MAX_RESPUESTAS
    formset = ElegirInLineFormSet


class PreguntaAdmin(admin.ModelAdmin):
    model = Pregunta
    inlines = (ElegirRespuestaInline, )
    list_display = ['texto', ]
    search_fields = ['texto', 'preguntas_texto']


class PreguntaRespondidaAdmin(admin.ModelAdmin):
    list_display = ['pregunta', 'respuesta', 'correcta', 'puntaje_obtenido']

    class Meta:
        model = PreguntasRespondidas


admin.site.register(PreguntasRespondidas)
admin.site.register(Pregunta, PreguntaAdmin)
admin.site.register(ElegirRespuesta)
admin.site.register(QuizUsuario)