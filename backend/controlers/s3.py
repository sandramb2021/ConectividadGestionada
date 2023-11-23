import boto3
import json
import pandas as pd
import os

ec2 = "/storage"

def get_aws_credentials(file_path='config.json'):
    with open(file_path, 'r') as config_file:
        config_data = json.load(config_file)
        return config_data.get('aws_access_key_id'), config_data.get('aws_secret_access_key'), config_data.get('region_name')


def upload_nokia_s3(archivo_local, nombre_bucket, nombre_archivo_s3):
    aws_access_key_id, aws_secret_access_key, region_name = get_aws_credentials()

    s3 = boto3.client("s3", aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key, region_name=region_name)

    try:
        s3.upload_file(archivo_local, nombre_bucket, nombre_archivo_s3)
        return("Subida exitosa a S3")

    except Exception as err:
        return("El archivo no se encontró",err)


def upload_file_nokia_s3(request):
    try:
        if 'file' not in request.files:
            return 'No se proporcionó ningún archivo'
        file = request.files['file']
        if file.filename == '':
            return 'Nombre de archivo no válido'
        ## para probar desde ec2 usar la ruta /backend/storage
        upload_folder = os.path.join(os.getcwd()+ec2)
        print(upload_folder)
        try:
            file.save(os.path.join(upload_folder, "NOKIA"))
            upload_nokia_s3(upload_folder+"/NOKIA"+file.filename,"fact-nokia","NOKIA")
            print("Se cargo todo ok")
            return "Se cargo todo ok"
        except Exception as err:
            return err
    except Exception as err:
        return(err)
    
def upload_file_facturacion_s3(request):
    try:
        if 'file' not in request.files:
            return 'No se proporcionó ningún archivo'
        file = request.files['file']
        if file.filename == '':
            return 'Nombre de archivo no válido'
        ## para probar desde ec2 usar la ruta /backend/storage
        upload_folder = os.path.join(os.getcwd()+ec2)
        print("path facturacion",upload_folder)
        try:
            file.save(os.path.join(upload_folder, "FACT"))
            upload_nokia_s3(upload_folder+"/FACT"+file.filename,"fact-prefa-postfa","FACT")
        except Exception as err:
            return err
        return "Archivo cargado con éxito"
    except Exception as err:
        return(err)