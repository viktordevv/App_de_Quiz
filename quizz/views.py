from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from .forms import RegistroFormulario, UsuarioLoginForm
from .models import QuizUsuario, Pregunta, ElegirRespuesta, PreguntasRespondidas
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404

# Create your views here.


def inicio(request):
    context = {
        'bienvenida': 'Bienvenido a la pagina de inicio'
    }

    return render(request, 'inicio.html')


def HomeUsuario(request):
    return render(request, 'Usuario/home.html')


def tablero(request):
    total_usuarios_quiz = QuizUsuario.objects.all()
    contador = total_usuarios_quiz.count()

    context = {
        'usuario_quiz': total_usuarios_quiz,
        'contar_user': contador
    }

    return render(request, 'play/tablero.html', context)


def jugar(request):

    QuizUser, created = QuizUsuario.objects.get_or_create(usuario=request.user)

    if request.method == 'POST':
        pregunta_pk = request.POST.get('pregunta_pk')
        pregunta_respondida = QuizUser.intentos.select_related(
            'pregunta').get(pregunta__pk=pregunta_pk)
        respuesta_pk = request.POST.get('respuesta_pk')

        try:
            opcion_seleccionada = pregunta_respondida.pregunta.opciones.get(
                pk=respuesta_pk)

        except ObjectDoesNotExist:
            raise Http404

        QuizUser.validar_intentos(pregunta_respondida, opcion_seleccionada)
        return redirect('resultado', pregunta_respondida_pk=pregunta_respondida.pk)

    else:
        pregunta = QuizUser.obtener_nuevas_preguntas()
        if pregunta is not None:
            QuizUser.crear_intentos(pregunta)

        context = {
            'pregunta': pregunta
        }

    return render(request, 'play/jugar.html', context)


def resultado_pregunta(request, pregunta_respondida_pk):
    respondida = get_object_or_404(
        PreguntasRespondidas, pk=pregunta_respondida_pk)
    context = {
        'respondida': respondida
    }
    return render(request, 'play/resultado.html', context)


def loginViews(request):
    titulo = 'Login'
    form = UsuarioLoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        login(request, user)
        return redirect('home')

    context = {
        'form': form,
        'titulo': titulo
    }

    return render(request, 'Usuario/login.html', {'form': form, 'titulo': titulo})


def registro(request):

    titulo = 'Crear registro'
    if request.method == 'POST':
        form = RegistroFormulario(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')

    else:
        form = RegistroFormulario()

    context = {
        'form': form,
        'titulo': titulo
    }

    return render(request, 'Usuario/registro.html', context)


def logoutViews(request):
    logout(request)
    return redirect('inicio')

def contacto(request):
    return render(request, 'Usuario/contacto.html')
