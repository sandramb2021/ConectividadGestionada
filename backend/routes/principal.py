from flask import Blueprint, request
import os 
import boto3
import json

from controlers.funtion import read_storage_prefa, read_storage_postfa, load_file_csv, load_file_excel
from controlers.csv import obtenerListaLiquidacion, exportarTablaNokia, periodoNokia
from controlers.xlsx import exportarTablaPrefa, periodoPrefa
from controlers.process import procesar_archivos

principal_bp = Blueprint('principal', __name__)

config_path = "config.json"

@principal_bp.route('/',methods=['GET'])
def listar_buckets():
    with open(config_path) as f:
        config = json.load(f)
    s3 = boto3.client('s3', aws_access_key_id=config["aws_access_key_id"],aws_secret_access_key=config["aws_secret_access_key"],region_name=config["region"])
    try:
        response = s3.list_buckets()
        for bucket in response['Buckets']:
            print(f"- {bucket['Name']}")
        
        return "ok"
    except Exception as e:
        print(f'Ocurrió un error al listar los buckets: {e}')
        return e

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
