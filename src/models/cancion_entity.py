# Archivo: src/models/cancion_entity.py

class CancionEntity:
    """
    Clase que representa una canción en la aplicación.
    Cada instancia corresponde a un registro en la tabla `canciones` de la base de datos.

    Métodos disponibles:
    - _to_dict(): Convierte la instancia en un diccionario para facilitar la manipulación de datos.
    - _from_dict(data): Crea una instancia de CancionEntity a partir de un diccionario.
    - __str__(): Representación legible para humanos.
    - __repr__(): Representación técnica detallada del objeto.
    - __eq__(): Compara dos canciones basándose en su atributo 'codigo'.
    - __hash__(): Genera un hash único basado en 'codigo', útil para conjuntos y diccionarios.
    """

    def __init__(self, codigo, titulo, artista, album, duracion, precio, ventas, id_genero, fecha_agregado):
        """
        Inicializa un objeto CancionEntity con los datos de una canción.

        Parámetros:
        - codigo (str): Código único de la canción.
        - titulo (str): Título de la canción.
        - artista (str): Artista de la canción.
        - album (str): Álbum al que pertenece la canción.
        - duracion (str): Duración de la canción en formato 'mm:ss'.
        - precio (float): Precio de la canción.
        - ventas (int): Cantidad de veces que la canción se ha vendido.
        - id_genero (int): ID del género al que pertenece la canción.
        - fecha_agregado (str): Fecha en la que se agregó la canción.
        """
        self._codigo = codigo
        self._titulo = titulo
        self._artista = artista
        self._album = album
        self._duracion = duracion
        self._precio = precio
        self._ventas = ventas
        self._id_genero = id_genero
        self._fecha_agregado = fecha_agregado
    # __init__ (fin)

    def _to_dict(self):
        """
        Convierte la instancia actual en un diccionario.

        Esto es útil para preparar los datos para operaciones como:
        - Serialización (e.g., guardar en JSON o enviar a una API).
        - Interacción con la base de datos para insertar o actualizar registros.

        Retorno:
        - dict: Representación de la canción como un diccionario.
        """
        return {
            "codigo": self._codigo,
            "titulo": self._titulo,
            "artista": self._artista,
            "album": self._album,
            "duracion": self._duracion,
            "precio": self._precio,
            "ventas": self._ventas,
            "id_genero": self._id_genero,
            "fecha_agregado": self._fecha_agregado
        }
    # _to_dict (fin)

    @classmethod
    def _from_dict(cls, data):
        """
        Crea una instancia de CancionEntity a partir de un diccionario.

        Esto es útil al recibir datos desde una API o al obtener registros de la base de datos.

        Parámetros:
        - cls: Hace referencia a la clase `CancionEntity`. Se usa en métodos de clase para crear instancias
               de la clase en lugar de usar una instancia existente (`self`).
        - data (dict): Diccionario con los datos de la canción.

        Retorno:
        - CancionEntity: Instancia creada con los datos proporcionados.

        Nota:
        - Usamos `cls` para garantizar que el método funcione correctamente incluso si la clase
          es heredada o renombrada en algún momento.
        """
        return cls(
            codigo=data.get("codigo"),
            titulo=data.get("titulo"),
            artista=data.get("artista"),
            album=data.get("album"),
            duracion=data.get("duracion"),
            precio=data.get("precio"),
            ventas=data.get("ventas"),
            id_genero=data.get("id_genero"),
            fecha_agregado=data.get("fecha_agregado")
        )
    # _from_dict (fin)

    def __str__(self):
        """
        Devuelve una representación legible de la canción.

        Esto es útil para:
        - Mostrar datos de la canción en la interfaz de usuario.
        - Generar registros de logs o mensajes de depuración.

        Retorno:
        - str: Representación en formato legible.
        """
        return f"Canción: {self._titulo} por {self._artista}, Código: {self._codigo}, Precio: {self._precio:.2f}€, Ventas: {self._ventas}"
    # __str__ (fin)

    def __repr__(self):
        """
        Devuelve una representación técnica de la canción.

        Esto es útil al depurar o inspeccionar el objeto en entornos interactivos.

        Retorno:
        - str: Representación en formato técnico.
        """
        return (
            f"CancionEntity(codigo='{self._codigo}', titulo='{self._titulo}', artista='{self._artista}', "
            f"album='{self._album}', duracion='{self._duracion}', precio={self._precio}, ventas={self._ventas}, "
            f"id_genero={self._id_genero}, fecha_agregado='{self._fecha_agregado}')"
        )
    # __repr__ (fin)

    def __eq__(self, other):
        """
        Comprueba si dos instancias de CancionEntity son iguales, basándose en su código.

        Esto permite comparar canciones directamente para verificar si son equivalentes.

        Parámetros:
        - other (CancionEntity): Otra instancia a comparar.

        Retorno:
        - bool: True si los códigos son iguales, False en caso contrario.
        """
        if not isinstance(other, CancionEntity):
            return False
        return self._codigo == other._codigo
    # __eq__ (fin)

    def __hash__(self):
        """
        Devuelve el hash de la instancia, basado en su código.

        Esto permite usar instancias de CancionEntity en estructuras como:
        - Conjuntos (set) para evitar duplicados.
        - Diccionarios (dict) como claves.

        Retorno:
        - int: Valor hash de la instancia.
        """
        return hash(self._codigo)
    # __hash__ (fin)
# CancionEntity (fin)
