# Script para agregar libros de ejemplo
# Ejecutar con: python manage.py shell < agregar_libros_ejemplo.py

from vistas.models import Practica, Obra, Capitulo

# Crear un usuario de ejemplo para los libros
try:
    autor = Practica.objects.get(username="BookMoraAdmin")
except Practica.DoesNotExist:
    autor = Practica.objects.create(
        username="BookMoraAdmin",
        email="admin@bookmora.com",
        password="admin123"
    )

# Lista de libros de ejemplo
libros = [
    {
        "titulo": "El Susurro de las Runas",
        "descripcion": "Una novela de misterio sobre runas ancestrales descubiertas en Londres. El arco comienza con la inmimente partida del Oceana...",
        "categoria": "Misterio",
        "etiquetas": "Misterio, Suspense, Roma",
        "imagen_url": "https://images.unsplash.com/photo-1543002588-bfa74002ed7e?w=400",
    },
    {
        "titulo": "Crónicas de Sombras",
        "descripcion": "Una épica aventura de fantasía oscura donde la luz y la oscuridad batallan por el destino del mundo.",
        "categoria": "Fantasía",
        "etiquetas": "Fantasía, Aventura, Magia",
        "imagen_url": "https://images.unsplash.com/photo-1532012197267-da84d127e765?w=400",
    },
    {
        "titulo": "La Canción de Leviatán",
        "descripcion": "Una historia épica sobre criaturas marinas legendarias y los secretos del océano profundo.",
        "categoria": "Aventura",
        "etiquetas": "Aventura, Mar, Mitología",
        "imagen_url": "https://images.unsplash.com/photo-1544947950-fa07a98d237f?w=400",
    },
    {
        "titulo": "Forjados en Bruma",
        "descripcion": "En un mundo cubierto de niebla eterna, los héroes deben encontrar la luz perdida.",
        "categoria": "Fantasía",
        "etiquetas": "Fantasía, Épica, Héroes",
        "imagen_url": "https://images.unsplash.com/photo-1512820790803-83ca734da794?w=400",
    },
    {
        "titulo": "El Último Ocaso de Eterna",
        "descripcion": "El último amanecer antes del fin del mundo. Una historia de redención y esperanza.",
        "categoria": "Ciencia Ficción",
        "etiquetas": "Sci-Fi, Apocalipsis, Drama",
        "imagen_url": "https://images.unsplash.com/photo-1519791883288-dc8bd696e667?w=400",
    },
]

print("Agregando libros de ejemplo...")

for libro_data in libros:
    # Verificar si ya existe
    if not Obra.objects.filter(titulo=libro_data["titulo"]).exists():
        obra = Obra.objects.create(
            titulo=libro_data["titulo"],
            descripcion=libro_data["descripcion"],
            categoria=libro_data["categoria"],
            etiquetas=libro_data["etiquetas"],
            imagen_url=libro_data["imagen_url"],
            autor=autor
        )
        
        # Agregar un capítulo inicial
        Capitulo.objects.create(
            obra=obra,
            titulo="Parte I: El Comienzo",
            contenido=f"Este es el inicio de {libro_data['titulo']}. La historia comienza cuando nuestro protagonista descubre un secreto que cambiará su vida para siempre..."
        )
        
        print(f"✓ Creado: {libro_data['titulo']}")
    else:
        print(f"- Ya existe: {libro_data['titulo']}")

print("\n¡Libros de ejemplo agregados exitosamente!")
