from flask import Blueprint, request
import os 
principal_bp = Blueprint('principal', __name__)

@principal_bp.route('/',methods=['GET'])
def index():
    return "desde un blueprint"

@principal_bp.route('/postfa', methods=['POST'])
def upload_file_postfa():
    if 'file' not in request.files:
        return 'No se proporcionó ningún archivo'
    file = request.files['file']
    if file.filename == '':
        return 'Nombre de archivo no válido'
    
    upload_folder = os.path.join(os.getcwd(), 'storage')
    file.save(os.path.join(upload_folder, "POSTFA"+file.filename))
    return 'Archivo cargado con éxito'

  
@principal_bp.route('/prefa', methods=['POST'])
def upload_file_prefa():
    if 'file' not in request.files:
        return 'No se proporcionó ningún archivo'
    file = request.files['file']
    if file.filename == '':
        return 'Nombre de archivo no válido'
    
    upload_folder = os.path.join(os.getcwd(), 'storage')
    file.save(os.path.join(upload_folder, "PREFA"+file.filename))

    return 'Archivo cargado con éxito'


