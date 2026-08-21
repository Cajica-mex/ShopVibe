# parse_csv.py
import csv
import io

def parsear_linea_csv(linea_texto):
    # TODO (TICKET-JR-008): Corregir y separar correctamente una línea de CSV, respetando comillas en campos de texto.
    return linea_texto.split(',')
