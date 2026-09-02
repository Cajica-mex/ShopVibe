# clean_data.py
import re

def es_correo_valido(email):
    # TODO (TICKET-JR-002): Retornar False si el correo está vacío, nulo o no contiene un carácter @. De lo contrario, retorna True.
    return True

def es_importe_valido(monto):
    # TODO (TICKET-JR-002): Retornar True si el monto es estrictamente mayor a 0, y False si es menor, igual a 0 o nulo.
    return True

def eliminar_duplicados(registros):
    # TODO (TICKET-JR-002): Eliminar duplicados exactos según 'id' conservando solo el primer registro.
    return registros

def aplanar_orden(orden):
    # TODO (TICKET-JR-002): Extraer la lista de productos de la clave "articulos" y retornar una lista de registros planos.
    return []

def estandarizar_fecha(fecha_str):
    # TODO (TICKET-JR-002): Normalizar formatos del tipo YYYY.MM.DD o YYYY/MM/DD a YYYY-MM-DD.
    return fecha_str

def validar_contrato(fila, esquema):
    # TODO (TICKET-JR-002): Retornar True si la fila contiene todas las claves de esquema y con el tipo esperado.
    return True

def normalizar_estado(direccion):
    # TODO (TICKET-JR-002): Extraer y retornar un código de estado de 2 letras en mayúsculas (ej. "CA", "NY") o "UNKNOWN".
    return "UNKNOWN"
