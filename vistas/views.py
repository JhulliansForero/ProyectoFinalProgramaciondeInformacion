from django.shortcuts import render, redirect  # render: muestra templates, redirect: redirige a otra URL
from django.http import HttpResponse
from django.db.models import Count
from .models import Practica, Obra, Capitulo  # Importamos el modelo Practica de la base de datos


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
    usuario_id = request.session.get('usuario_id')
    obras = []
    usuario = None
    if usuario_id:
        usuario = Practica.objects.get(id=usuario_id)
        obras = Obra.objects.filter(autor=usuario).annotate(num_capitulos=Count('capitulo'))
        
    info = {
        'obras': obras,
        'usuario': usuario
    }
    return render(request, 'perfil.html', info)





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
                request.session['usuario_id'] = usuario.id
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
    
    info = {
        'usuario': usuario
    }
    return render(request, "editar_usuario.html", info)


def editar_obra(request, obra_id):
    obra = Obra.objects.get(id=obra_id)
    
    if request.method == "POST":
        obra.titulo = request.POST.get("titulo")
        obra.descripcion = request.POST.get("descripcion")
        personajes_list = request.POST.getlist("personajes")
        obra.personajes = ", ".join(personajes_list) if personajes_list else ""
        
        obra.categoria = request.POST.get("categoria")
        
        etiquetas_list = request.POST.getlist("etiquetas")
        obra.etiquetas = ", ".join(etiquetas_list) if etiquetas_list else ""
        
        imagen = request.FILES.get("imagen")
        imagen_url = request.POST.get("imagen_url")
        
        if imagen:
            obra.imagen = imagen
        elif imagen_url:
            # Si no hay nueva imagen PERO hay nueva URL, usamos la URL y quitamos la imagen anterior
            obra.imagen_url = imagen_url
            obra.imagen = None
            
        obra.save()
        return redirect("perfil")
        
    info = { 'obra': obra }
    return render(request, 'editar_obra.html', info)


#---------------------------------------------------
# VISTA DE PUBLICAR OBRA
#---------------------------------------------------
def publicar(request):
    if request.method == "POST":
        titulo = request.POST.get("titulo")
        descripcion = request.POST.get("descripcion")
        personajes_list = request.POST.getlist("personajes")
        personajes = ", ".join(personajes_list) if personajes_list else ""
        
        categoria = request.POST.get("categoria")
        
        etiquetas_list = request.POST.getlist("etiquetas")
        etiquetas = ", ".join(etiquetas_list) if etiquetas_list else ""
        imagen = request.FILES.get("imagen")
        imagen_url = request.POST.get("imagen_url")
        
        usuario_id = request.session.get('usuario_id')
        if not usuario_id:
            return redirect('login')
            
        autor = Practica.objects.get(id=usuario_id)
        
        obra = Obra.objects.create(
            titulo=titulo,
            descripcion=descripcion,
            personajes=personajes,
            categoria=categoria,
            etiquetas=etiquetas,
            imagen=imagen,
            imagen_url=imagen_url,
            autor=autor
        )
        
        request.session['obra_id'] = obra.id
        return redirect('escribir_contenido')
        
    return render(request, 'publicar.html')


#---------------------------------------------------
# VISTA DE ESCRIBIR CONTENIDO
#---------------------------------------------------
def escribir_contenido(request):
    # Recuperamos la obra que estamos editando
    obra_id = request.session.get('obra_id')
    obra = None
    if obra_id:
        obra = Obra.objects.get(id=obra_id)
        
    if request.method == "POST":
        contenido = request.POST.get("contenido")
        titulo_capitulo = request.POST.get("titulo_capitulo", "Sin Titulo") 
        if not titulo_capitulo: titulo_capitulo = "Sin Titulo"
        
        # Ahora creamos el PRIMER CAPITULO en lugar de guardar en obra.contenido
        if obra:
            Capitulo.objects.create(
                obra=obra,
                titulo=titulo_capitulo,
                contenido=contenido
            )
            # obra.contenido = contenido # Ya no usamos esto
            # obra.save()
            return redirect('perfil')
            
    info = { 'obra': obra } # Pasamos la obra al template para mostrar titulo o portada
    return render(request, 'escribir_contenido.html', info)

def ver_obra(request, obra_id):
    obra = Obra.objects.get(id=obra_id)
    # Contar capitulos
    num_capitulos = Capitulo.objects.filter(obra=obra).count()
    obra.num_capitulos = num_capitulos # Attach count manually or reuse annotate if efficient
    
    capitulos = Capitulo.objects.filter(obra=obra)
    
    # Check if author
    es_autor = False
    if 'usuario_id' in request.session:
        if obra.autor.id == request.session['usuario_id']:
            es_autor = True

    return render(request, 'ver_obra.html', {
        'obra': obra, 
        'capitulos': capitulos,
        'es_autor': es_autor
    })

def tabla_contenidos(request, obra_id):
    obra = Obra.objects.get(id=obra_id)
    capitulos = Capitulo.objects.filter(obra=obra)
    return render(request, 'tabla_contenidos.html', {'obra': obra, 'capitulos': capitulos})

def eliminar_capitulo(request, capitulo_id):
    cap = Capitulo.objects.get(id=capitulo_id)
    obra_id = cap.obra.id
    cap.delete()
    return redirect('tabla_contenidos', obra_id=obra_id)

def eliminar_obra(request, obra_id):
    obra = Obra.objects.get(id=obra_id)
    obra.delete()
    return redirect('perfil')

def escribir_capitulo(request, obra_id, capitulo_id=None):
    obra = Obra.objects.get(id=obra_id)
    capitulo = None
    if capitulo_id:
        capitulo = Capitulo.objects.get(id=capitulo_id)

    if request.method == "POST":
        # Usamos titulo_capitulo del form o default
        titulo = request.POST.get("titulo_capitulo", "Sin Titulo") 
        if not titulo: titulo = "Sin Titulo"
        
        contenido = request.POST.get("contenido")
        
        if capitulo:
            capitulo.titulo = titulo
            capitulo.contenido = contenido
            capitulo.save()
        else:
            Capitulo.objects.create(obra=obra, titulo=titulo, contenido=contenido)
            
        return redirect('tabla_contenidos', obra_id=obra.id)

    return render(request, 'escribir_contenido.html', {'obra': obra, 'capitulo': capitulo})

def leer_capitulo(request, obra_id, capitulo_id=None):
    obra = Obra.objects.get(id=obra_id)
    
    # Logic to get the correct chapter
    if capitulo_id:
        capitulo = Capitulo.objects.get(id=capitulo_id)
    else:
        # If no ID provided, get the first chapter
        capitulo = Capitulo.objects.filter(obra=obra).order_by('id').first()
        
    # Logic to find the next chapter (for the button)
    siguiente_capitulo = None
    if capitulo:
        # Get all chapters ordered by ID (assuming creation order)
        all_caps = list(Capitulo.objects.filter(obra=obra).order_by('id'))
        try:
            current_index = all_caps.index(capitulo)
            if current_index + 1 < len(all_caps):
                siguiente_capitulo = all_caps[current_index + 1]
        except ValueError:
            pass # Chapter not in list (?)

    return render(request, 'leer_capitulo.html', {
        'obra': obra,
        'capitulo': capitulo,
        'siguiente_capitulo': siguiente_capitulo
    })