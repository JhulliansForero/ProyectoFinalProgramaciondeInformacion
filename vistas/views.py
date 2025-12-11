from django.shortcuts import render, redirect  # render: muestra templates, redirect: redirige a otra URL
from django.http import HttpResponse
from .models import Practica  # Importamos el modelo Practica de la base de datos


#---------------------------------------------------
# VISTA DE INICIO (PÁGINA PÚBLICA)
#---------------------------------------------------
def inicio(request):
    return render(request, 'inicio.html')


#---------------------------------------------------
# VISTA PRIVADA (DASHBOARD - después de login)
#---------------------------------------------------
def dashboard(request):
    return render(request, 'dashboard.html')


#---------------------------------------------------
# VISTA DE PERFIL
#---------------------------------------------------
def perfil(request):
    return render(request, 'perfil.html')


def saludo(request):
    return render(request, 'saludo.html')


def petro(request):
    return render(request, 'petro.html')


def uribe(request):
    return render(request, 'uribe.html')


#---------------------------------------------------
# VISTA DE LOGIN
#---------------------------------------------------
def login(request):
    # Verificamos si el formulario fue enviado (método POST)
    if request.method == "POST":
        # Obtenemos los datos del formulario
        email = request.POST.get("username")  # Obtiene el valor del campo email
        password = request.POST.get("password")  # Obtiene el valor del campo password
        
        # Verificamos si el usuario existe en la base de datos (buscando por email)
        if Practica.objects.filter(email=email).exists():
            # Si existe, lo obtenemos
            usuario = Practica.objects.get(email=email)
            
            # Verificamos si la contraseña es correcta
            if usuario.password == password:
                # Si es correcta, redirigimos al dashboard (vista privada)
                return redirect("dashboard")
            else:
                # Si la contraseña es incorrecta, mostramos error
                error = "La contraseña es incorrecta"
                info = {
                    'error': error
                }
                return render(request, 'login.html', info)
        else:
            # Si el usuario no existe, mostramos error
            error = "El usuario no existe"
            info = {
                'error': error
            }
            return render(request, 'login.html', info)
    
    # Si no es POST (primera vez que carga la página), solo mostramos el formulario
    return render(request, 'login.html')


#---------------------------------------------------
# VISTA DE FORMULARIO (REGISTRO)
#---------------------------------------------------
def formulario(request):
    # Verificamos si el formulario fue enviado (método POST)
    if request.method == "POST":
        # Obtenemos los datos del formulario
        usern = request.POST.get("username")      # Nombre de usuario
        email = request.POST.get("email")          # Email
        passw = request.POST.get("password")       # Contraseña

        # Verificamos si el usuario ya existe
        if Practica.objects.filter(username=usern).exists():
            sms = "El nombre de usuario ya existe"
            info = {
                  'infosms': sms
            }
            return render(request, "formulario.html", info)
        
        # Guardamos el nuevo usuario en la base de datos
        Practica.objects.create(
            username=usern,
            email=email,
            password=passw
        )
        return redirect("login")  # Redirigimos al login
    
    # Si no es POST, mostramos el formulario vacío
    return render(request, "formulario.html")


#---------------------------------------------------
# VISTA DE LISTA DE USUARIOS
#---------------------------------------------------
def lista_usuarios(request):
    # Obtenemos todos los usuarios de la base de datos
    usuarios = Practica.objects.all()
    
    # Enviamos los usuarios al template en un diccionario
    info = {
        'usuarios': usuarios
    }
    return render(request, "lista_usuarios.html", info)


#---------------------------------------------------
# VISTA PARA ELIMINAR USUARIO
#---------------------------------------------------
def eliminar_usuario(request, usuario_id):
    # Obtenemos el usuario por su ID
    usuario = Practica.objects.get(id=usuario_id)
    
    # Eliminamos el usuario de la base de datos
    usuario.delete()
    
    # Redirigimos de vuelta a la lista de usuarios
    return redirect("lista_usuarios")


#---------------------------------------------------
# VISTA PARA EDITAR USUARIO
#---------------------------------------------------
def editar_usuario(request, usuario_id):
    # Obtenemos el usuario por su ID
    usuario = Practica.objects.get(id=usuario_id)
    
    # Verificamos si el formulario fue enviado (método POST)
    if request.method == "POST":
        # Obtenemos los datos del formulario
        nuevo_username = request.POST.get("username")
        nuevo_email = request.POST.get("email")
        nueva_password = request.POST.get("password")
        
        # Actualizamos los datos del usuario
        usuario.username = nuevo_username
        usuario.email = nuevo_email
        usuario.password = nueva_password
        
        # Guardamos los cambios en la base de datos
        usuario.save()
        
        # Redirigimos a la lista de usuarios
        return redirect("lista_usuarios")
    
    # Si no es POST, mostramos el formulario con los datos actuales
    info = {
        'usuario': usuario
    }
    return render(request, "editar_usuario.html", info)