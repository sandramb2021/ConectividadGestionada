
import boto3
import json


def list_buckets(config):
    with open(config) as f:
        config = json.load(f)
    s3 = boto3.client('s3', aws_access_key_id=config["aws_access_key_id"],aws_secret_access_key=config["aws_secret_access_key"],region_name=config["region"])
    try:
        response = s3.list_buckets()
        list_buckets_s3 = []
        for bucket in response['Buckets']:
            list_buckets_s3.append(f"- {bucket['Name']}")
        return list_buckets_s3
    except Exception as e:
        print(f'Ocurrió un error al listar los buckets: {e}')
        return e
    
def upload_s3(config, ruta_archivo_local,nombre_bucket,nombre_archivo_s3):
    with open(config) as f:
        config = json.load(f)

    s3 = boto3.client('s3', 
                      aws_access_key_id=config["aws_access_key_id"],
                      aws_secret_access_key=config["aws_secret_access_key"],
                      region_name=config["region"])

    try:
        s3.upload_file(ruta_archivo_local, nombre_bucket, nombre_archivo_s3)
        print(f'Archivo "{nombre_archivo_s3}" cargado exitosamente en el bucket "{nombre_bucket}"')
    except Exception as e:
        print(f'Ocurrió un error al cargar el archivo: {e}')
