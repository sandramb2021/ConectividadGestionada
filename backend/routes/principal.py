from flask import Blueprint, request
import os 

from controlers.funtion import read_storage_prefa, read_storage_postfa, load_file_csv, load_file_excel
from controlers.table import obtenerListaLiquidacion, exportarTablaNokia

principal_bp = Blueprint('principal', __name__)

@principal_bp.route('/',methods=['GET'])
def index():
    return "desde un blueprint"

@principal_bp.route('/postfa', methods=['POST'])
def upload_file_postfa():
    try:
        if 'file' not in request.files:
            return 'No se proporcionó ningún archivo'
        file = request.files['file']
        if file.filename == '':
            return 'Nombre de archivo no válido'
        upload_folder = os.path.join(os.getcwd(), 'backend/storage')
        try:
            file.save(os.path.join(upload_folder, "PREFA"+file.filename))
        except Exception as err:
            return err
        return "Archivo cargado con éxito"
    except Exception as err:
        return(err)


  
@principal_bp.route('/prefa', methods=['POST'])
def upload_file_prefa():
    try:
        if 'file' not in request.files:
            return 'No se proporcionó ningún archivo'
        file = request.files['file']
        if file.filename == '':
            return 'Nombre de archivo no válido'
        upload_folder = os.path.join(os.getcwd(), 'backend/storage')
        try:
            file.save(os.path.join(upload_folder, "POSTFA"+file.filename))
        except Exception as err:
            return err
        return "Archivo cargado con éxito"
    except Exception as err:
        return(err)


@principal_bp.route('/process', methods=['GET'])
def process_file():
    try:
        ## POSTFA XLSX
        path_prefa = read_storage_prefa()
        ## PREFA CSV - NOKIA
        path_postfa = read_storage_postfa()
        try:
            nokia_file = load_file_csv(path_postfa)
            liquidacion = obtenerListaLiquidacion(nokia_file)
            tabla_nokia_final = exportarTablaNokia(nokia_file,liquidacion)
            print(tabla_nokia_final)
            return "hola"
        except Exception as err:
            return "Error en la lectura"+err
    except Exception as err:
        return err
