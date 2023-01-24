from django.db import models
from django.conf import settings

from django.contrib.auth.models import User

import random

# Create your models here.


class Pregunta(models.Model):
    NUMERO_RESPUESTAS_PERMITIDAS = 1

    texto = models.CharField(
        verbose_name='Aqui va la pregunta', max_length=200)
    max_puntaje = models.DecimalField(
        verbose_name='Maximo Puntaje', default=3, decimal_places=2, max_digits=6)

    def __str__(self):
        return self.texto


class ElegirRespuesta(models.Model):

    MAX_RESPUESTAS = 4

    pregunta = models.ForeignKey(
        Pregunta, related_name='opciones', on_delete=models.CASCADE)
    correcta = models.BooleanField(
        verbose_name='¿Es correcta?', default=False, null=False)
    texto = models.TextField(
        verbose_name='Aqui va la respuesta', max_length=200)

    def __str__(self):
        return self.texto


class QuizUsuario(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    total = models.DecimalField(verbose_name='Puntaje obtenido', default=0, null=False, decimal_places=2, max_digits=10)

    def crear_intentos(self, pregunta):
        intento = PreguntasRespondidas(pregunta=pregunta, quizUser=self)
        intento.save()

    def obtener_nuevas_preguntas(self):
        respondidas = PreguntasRespondidas.objects.filter(
            quizUser=self).values_list('pregunta__pk', flat=True)
        preguntas_restantes = Pregunta.objects.exclude(pk__in=respondidas)
        if not preguntas_restantes.exists():
            return None
        return random.choice(preguntas_restantes)

    def validar_intentos(self, pregunta_respondida, respuesta_seleccionada):
        if pregunta_respondida.pregunta_id != respuesta_seleccionada.pregunta_id:
            return

        pregunta_respondida.respuesta_seleccionada = respuesta_seleccionada
        if respuesta_seleccionada.correcta is True:
            pregunta_respondida.correcta = True
            pregunta_respondida.puntaje_obtenido = respuesta_seleccionada.pregunta.max_puntaje
            pregunta_respondida.respuesta = respuesta_seleccionada

        else:
            pregunta_respondida.respuesta = respuesta_seleccionada

        pregunta_respondida.save()

        self.actualizar_puntaje()

    def actualizar_puntaje(self):
        puntaje_actualizado = PreguntasRespondidas.objects.filter(
            quizUser=self, correcta=True).aggregate(models.Sum('puntaje_obtenido'))
        self.total = puntaje_actualizado['puntaje_obtenido__sum']
        self.save()


class PreguntasRespondidas(models.Model):
    quizUser = models.ForeignKey(
        QuizUsuario, on_delete=models.CASCADE, related_name='intentos')
    pregunta = models.ForeignKey(Pregunta, on_delete=models.CASCADE)
    respuesta = models.ForeignKey(
        ElegirRespuesta, on_delete=models.CASCADE, null=True)
    correcta = models.BooleanField(
        verbose_name='¿Es correcta?', default=False, null=False)
    puntaje_obtenido = models.DecimalField(
        verbose_name='Puntaje obtenido', default=0, null=False, decimal_places=2, max_digits=6)

    def __str__(self):
        return self.pregunta.texto
