# parse_csv.py
import csv
import io

def parsear_linea_csv(linea_texto):
    # TODO (TICKET-JR-002): Separar correctamente una línea de CSV, respetando comillas en campos de texto con comas internas.
    return linea_texto.split(',')
