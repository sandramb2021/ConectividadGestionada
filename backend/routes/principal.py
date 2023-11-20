from flask import Blueprint, request, send_file
import os 
import boto3
import json

from controlers.funtion import read_storage_nokia, read_storage_facturacion, load_file_csv, load_file_excel, upload_file_nokia, upload_file_facturacion, delete_storage, read_merge_storage
from controlers.csv import obtenerListaLiquidacion, exportarTablaNokia, periodoNokia, exportarTablaPrefa, periodoPrefa
from controlers.process import procesar_archivos

principal_bp = Blueprint('principal', __name__)

## RUTA DONDE ESTAN LAS CONFIGURACIONES DE MIS CREDENCIALES
config_path = "config.json"
local = "/backend/storage"
ec2 = "/storage"


## RURA QUE DEVUELVE UN MSJ DE PRUEBA
@principal_bp.route('/',methods=['GET'])
def listar_buckets():
    return "prueba"


## RUTA QUE CARGA EL ARCHIVO CSV EN EC2
@principal_bp.route('/nokia', methods=['POST'])
def upload_file_nokia_csv():
    upload_file_nokia(request)
    return "Se cargo correctamente el archivo NOKIA"

 
@principal_bp.route('/facturacion', methods=['POST'])
def upload_file_facturacion_csv():
    try:
        upload_file_facturacion(request)
    except:
        return "error"
    return "Se cargo correctamente el archivo de PRE o POST FACTURACION"


@principal_bp.route('/process', methods=['GET'])
def process_file():
    try:
        ## ARCHVO NOKIA
        path_nokia = read_storage_nokia()
        ## ARCHIVO PREFA O POSTFA
        path_facturacion = read_storage_facturacion()

        try:
            nokia_file = load_file_csv(path_nokia)
            liquidacion = obtenerListaLiquidacion(nokia_file)
            tabla_nokia_final = exportarTablaNokia(nokia_file,liquidacion)
            periodo_nokia = periodoNokia(nokia_file)

            facturacion_file = load_file_excel(path_facturacion)
            tabla_facturacion_final = exportarTablaPrefa(facturacion_file)
            periodo_facturacion = periodoPrefa(facturacion_file)
            
            process = procesar_archivos(tabla_nokia_final,tabla_facturacion_final,periodo_nokia,periodo_facturacion)
            delete_storage()
            return "Se proceso correctamente el archivo"
        except Exception as err:
            return "Error en la lectura"+err
    except Exception as err:
        return err

@principal_bp.route('/download', methods=['GET'])
def download_file():
    directory = read_merge_storage()
    return send_file(directory, as_attachment=True, download_name="TablaFinal")