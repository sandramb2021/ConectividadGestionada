from flask import Blueprint, request
import os 
import boto3
import json

from s3.list_buckets import list_buckets, upload_s3, leer_csv, leer_xlxs
from controlers.funtion import read_storage_prefa, read_storage_postfa, load_file_csv, load_file_excel
from controlers.csv import obtenerListaLiquidacion, exportarTablaNokia, periodoNokia
from controlers.xlsx import exportarTablaPrefa, periodoPrefa
from controlers.process import procesar_archivos

principal_bp = Blueprint('principal', __name__)

## RUTA DONDE ESTAN LAS CONFIGURACIONES DE MIS CREDENCIALES
config_path = "config.json"

## RURA QUE DEVUELVE LOS BUCKETS
@principal_bp.route('/',methods=['GET'])
def listar_buckets():
    lista = list_buckets(config_path)
    return lista

## quiero probar cuanto tiempo tarda en leer un s3 con un archivo csv
@principal_bp.route('/prueba_tiempo',methods=['GET'])
def leer_csv_prueba():
    lista = leer_csv(config_path)
    return lista

@principal_bp.route('/prueba_tiempo_xlxs',methods=['GET'])
def leer_csv_prueba_xlxs():
    lista = leer_xlxs(config_path)
    return lista

local = "/backend/storage"
ec2 = "/storage"


@principal_bp.route('/postfa', methods=['POST'])
def upload_file_postfa_csv():
    try:
        if 'file' not in request.files:
            return 'No se proporcionó ningún archivo'
        file = request.files['file']
        if file.filename == '':
            return 'Nombre de archivo no válido'
        ## para probar desde local usar la ruta /backend/storage
        upload_folder = os.path.join(os.getcwd()+ec2)
        print(upload_folder)
        try:
            file.save(os.path.join(upload_folder, "POSTFA"+file.filename))
            ruta_archivo = upload_folder+"/POSTFA"+file.filename
            upload_s3(config_path,ruta_archivo,"postfa-csv","POSTFA.csv")
        except Exception as err:
            return err
        return "Archivo cargado con éxito"
    except Exception as err:
        return(err)


  
@principal_bp.route('/prefa', methods=['POST'])
def upload_file_prefa_xlsx():
    try:
        if 'file' not in request.files:
            return 'No se proporcionó ningún archivo'
        file = request.files['file']
        if file.filename == '':
            return 'Nombre de archivo no válido'
        upload_folder = os.path.join(os.getcwd()+ec2)
        try:
            file.save(os.path.join(upload_folder, "PREFA"+file.filename))
            ruta_archivo = upload_folder+"/PREFA"+file.filename
            upload_s3(config_path,ruta_archivo,"prefa-xlxs","PREFA.xlsx")
        except Exception as err:
            return err
        return "Archivo cargado con éxito"
    except Exception as err:
        return(err)


@principal_bp.route('/process', methods=['GET'])
def process_file():
    try:
        ## POSTFA CSV
        path_postfa = read_storage_postfa()
        ## POSTFA XLSX
        path_prefa = read_storage_prefa()

        try:
            postfa_file = load_file_csv(path_postfa)
            liquidacion = obtenerListaLiquidacion(postfa_file)
            tabla_postfa_final = exportarTablaNokia(postfa_file,liquidacion)
            periodo_nokia = periodoNokia(postfa_file)

            prefa_file = load_file_excel(path_prefa)
            tabla_xlxs_final = exportarTablaPrefa(prefa_file)
            periodo_prefa = periodoPrefa(prefa_file)
            print(prefa_file)
            process = procesar_archivos(tabla_postfa_final,tabla_xlxs_final,periodo_nokia,periodo_prefa)
            # print(process)
            return "Se proceso correctamente el archivo"
        except Exception as err:
            return "Error en la lectura"+err
    except Exception as err:
        return err
