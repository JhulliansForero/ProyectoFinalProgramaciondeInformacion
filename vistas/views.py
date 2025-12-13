from django.shortcuts import render, redirect  # render: muestra templates, redirect: redirige a otra URL
from django.http import HttpResponse
from django.db.models import Count, Q
from .models import Practica, Obra, Capitulo  # Importamos los modelos de la base de datos


# ==============================================================================
# VISTAS PÚBLICAS
# ==============================================================================

def inicio(request):
    """
    Vista de la página de inicio pública.
    Muestra la landing page del sitio.
    """
    return render(request, 'inicio.html')


def buscar(request):
    """
    Motor de búsqueda del sitio.
    Busca coincidencias en títulos, descripciones y nombres de autor.
    """
    query = request.GET.get('q', '')
    resultados = []
    
    if query:
        # Busca coincidencias (case-insensitive) en título, descripción o autor
        resultados = Obra.objects.filter(
            Q(titulo__icontains=query) |
            Q(descripcion__icontains=query) |
            Q(autor__username__icontains=query)
        ).distinct()
    
    # Renderiza la página de resultados con las obras encontradas
    return render(request, 'resultados_busqueda.html', {
        'query': query,
        'resultados': resultados
    })


# ==============================================================================
# VISTAS DE AUTENTICACIÓN (Login y Registro)
# ==============================================================================

def login(request):
    """
    Maneja el inicio de sesión de los usuarios.
    Verifica correo y contraseña contra la base de datos.
    """
    # Si es una petición POST, procesamos los datos del formulario
    if request.method == "POST":
        email = request.POST.get("username")     # Nota: el campo en HTML se llama 'username' pero es el email
        password = request.POST.get("password")
        
        # Verificamos si el usuario existe
        if Practica.objects.filter(email=email).exists():
            usuario = Practica.objects.get(email=email)
            
            # Verificamos la contraseña
            if usuario.password == password:
                # Login exitoso: Guardamos ID en sesión y redirigimos
                request.session['usuario_id'] = usuario.id
                return redirect("dashboard")
            else:
                return render(request, 'login.html', {'error': "La contraseña es incorrecta"})
        else:
            return render(request, 'login.html', {'error': "El usuario no existe"})
    
    # Si es GET, mostramos el formulario de login
    return render(request, 'login.html')


def formulario(request):
    """
    Registro de nuevos usuarios en la plataforma.
    """
    if request.method == "POST":
        usern = request.POST.get("username")
        email = request.POST.get("email")
        passw = request.POST.get("password")

        # Verificamos duplicados
        if Practica.objects.filter(username=usern).exists():
            return render(request, "formulario.html", {'infosms': "El nombre de usuario ya existe"})
        
        # Creamos el nuevo usuario
        Practica.objects.create(
            username=usern,
            email=email,
            password=passw
        )
        return redirect("login")
    
    return render(request, "formulario.html")


# ==============================================================================
# VISTAS PRIVADAS (Requieren sesión)
# ==============================================================================

def dashboard(request):
    """
    Vista principal del usuario logueado (Home privado).
    """
    return render(request, 'dashboard.html')


def perfil(request):
    """
    Perfil del usuario actual.
    Muestra sus obras publicadas y estadísticas.
    """
    usuario_id = request.session.get('usuario_id')
    obras = []
    usuario = None
    
    if usuario_id:
        usuario = Practica.objects.get(id=usuario_id)
        # Obtenemos obras con el conteo de capítulos
        obras = Obra.objects.filter(autor=usuario).annotate(num_capitulos=Count('capitulo'))
        
    return render(request, 'perfil.html', {
        'obras': obras,
        'usuario': usuario
    })


# ==============================================================================
# GESTIÓN DE OBRAS (CRUD)
# ==============================================================================

def publicar(request):
    """
    Crea una nueva obra (libro).
    """
    # Verificar sesión
    usuario_id = request.session.get('usuario_id')
    if not usuario_id:
        return redirect('login')
        
    if request.method == "POST":
        # Recogida de datos del formulario
        titulo = request.POST.get("titulo")
        descripcion = request.POST.get("descripcion")
        categoria = request.POST.get("categoria")
        imagen = request.FILES.get("imagen")
        imagen_url = request.POST.get("imagen_url")
        
        # Procesamiento de listas (personajes y etiquetas)
        personajes = ", ".join(request.POST.getlist("personajes") or [])
        etiquetas = ", ".join(request.POST.getlist("etiquetas") or [])
        
        autor = Practica.objects.get(id=usuario_id)
        
        # Crear la obra en BD
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
        
        # Guardamos el ID en sesión para el siguiente paso (escribir primer capítulo)
        request.session['obra_id'] = obra.id
        return redirect('escribir_contenido')
        
    return render(request, 'publicar.html')


def editar_obra(request, obra_id):
    """
    Permite modificar los detalles de una obra existente.
    """
    obra = Obra.objects.get(id=obra_id)
    
    if request.method == "POST":
        obra.titulo = request.POST.get("titulo")
        obra.descripcion = request.POST.get("descripcion")
        obra.categoria = request.POST.get("categoria")
        
        obra.personajes = ", ".join(request.POST.getlist("personajes") or [])
        obra.etiquetas = ", ".join(request.POST.getlist("etiquetas") or [])
        
        imagen = request.FILES.get("imagen")
        imagen_url = request.POST.get("imagen_url")
        
        if imagen:
            obra.imagen = imagen
        elif imagen_url:
            obra.imagen_url = imagen_url
            obra.imagen = None
            
        obra.save()
        return redirect("perfil")
        
    return render(request, 'editar_obra.html', {'obra': obra})


def eliminar_obra(request, obra_id):
    """
    Elimina una obra completamente.
    """
    obra = Obra.objects.get(id=obra_id)
    obra.delete()
    return redirect('perfil')


# ==============================================================================
# GESTIÓN DE CAPÍTULOS Y LECTURA
# ==============================================================================

def escribir_contenido(request):
    """
    Vista para escribir el PRIMER capítulo justo después de crear una obra.
    """
    obra_id = request.session.get('obra_id')
    obra = Obra.objects.get(id=obra_id) if obra_id else None
        
    if request.method == "POST" and obra:
        titulo_capitulo = request.POST.get("titulo_capitulo", "Sin Titulo") or "Sin Titulo"
        contenido = request.POST.get("contenido")
        
        Capitulo.objects.create(
            obra=obra,
            titulo=titulo_capitulo,
            contenido=contenido
        )
        return redirect('perfil')
            
    return render(request, 'escribir_contenido.html', {'obra': obra})


def escribir_capitulo(request, obra_id, capitulo_id=None):
    """
    Crea o edita capítulos adicionales para una obra existente.
    """
    obra = Obra.objects.get(id=obra_id)
    capitulo = None
    if capitulo_id:
        capitulo = Capitulo.objects.get(id=capitulo_id)

    if request.method == "POST":
        titulo = request.POST.get("titulo_capitulo", "Sin Titulo") or "Sin Titulo"
        contenido = request.POST.get("contenido")
        
        if capitulo:
            # Editando existente
            capitulo.titulo = titulo
            capitulo.contenido = contenido
            capitulo.save()
        else:
            # Creando nuevo
            Capitulo.objects.create(obra=obra, titulo=titulo, contenido=contenido)
            
        return redirect('tabla_contenidos', obra_id=obra.id)

    return render(request, 'escribir_contenido.html', {'obra': obra, 'capitulo': capitulo})


def tabla_contenidos(request, obra_id):
    """
    Muestra la lista de capítulos de una obra para gestión del autor.
    """
    obra = Obra.objects.get(id=obra_id)
    capitulos = Capitulo.objects.filter(obra=obra)
    return render(request, 'tabla_contenidos.html', {'obra': obra, 'capitulos': capitulos})


def eliminar_capitulo(request, capitulo_id):
    """
    Elimina un capítulo específico.
    """
    cap = Capitulo.objects.get(id=capitulo_id)
    obra_id = cap.obra.id
    cap.delete()
    return redirect('tabla_contenidos', obra_id=obra_id)


def ver_obra(request, obra_id):
    """
    Vista pública de los detalles de una obra (índice, sinopsis).
    """
    obra = Obra.objects.get(id=obra_id)
    capitulos = Capitulo.objects.filter(obra=obra)
    
    # Verificamos si el visitante es el autor
    es_autor = False
    if 'usuario_id' in request.session:
        if obra.autor.id == request.session['usuario_id']:
            es_autor = True

    return render(request, 'ver_obra.html', {
        'obra': obra, 
        'capitulos': capitulos,
        'es_autor': es_autor
    })


def leer_capitulo(request, obra_id, capitulo_id=None):
    """
    Vista de lectura. Muestra el contenido de un capítulo y navegación entre ellos.
    """
    obra = Obra.objects.get(id=obra_id)
    
    if capitulo_id:
        # Capítulo específico solicitado
        capitulo = Capitulo.objects.get(id=capitulo_id)
    else:
        # Si no se especifica, carga el primer capítulo
        capitulo = Capitulo.objects.filter(obra=obra).order_by('id').first()
        
    # Lógica para botón "Siguiente Capítulo"
    siguiente_capitulo = None
    if capitulo:
        all_caps = list(Capitulo.objects.filter(obra=obra).order_by('id'))
        try:
            current_index = all_caps.index(capitulo)
            if current_index + 1 < len(all_caps):
                siguiente_capitulo = all_caps[current_index + 1]
        except ValueError:
            pass

    return render(request, 'leer_capitulo.html', {
        'obra': obra,
        'capitulo': capitulo,
        'siguiente_capitulo': siguiente_capitulo
    })


# ==============================================================================
# GESTIÓN DE USUARIOS (Admin simple)
# ==============================================================================

def lista_usuarios(request):
    """Listado de todos los usuarios registrados."""
    usuarios = Practica.objects.all()
    return render(request, "lista_usuarios.html", {'usuarios': usuarios})


def eliminar_usuario(request, usuario_id):
    """Elimina un usuario por ID."""
    usuario = Practica.objects.get(id=usuario_id)
    usuario.delete()
    return redirect("lista_usuarios")


def editar_usuario(request, usuario_id):
    """Edita datos de un usuario."""
    usuario = Practica.objects.get(id=usuario_id)
    
    if request.method == "POST":
        usuario.username = request.POST.get("username")
        usuario.email = request.POST.get("email")
        usuario.password = request.POST.get("password")
        usuario.save()
        return redirect("lista_usuarios")
    
    return render(request, "editar_usuario.html", {'usuario': usuario})