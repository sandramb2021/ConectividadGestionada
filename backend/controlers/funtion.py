import pandas as pd
import os

directorio_final = os.getcwd()+"/ConectividadGestionada/backend/storage"

local = "/ConectividadGestionada/backend/storage"
ec2 = "/storage"

def read_storage_facturacion():
    try:
        hola = os.getcwd()+ec2
        directory = os.listdir(hola)
        for file in directory:
            if file.startswith("FACT"):
                return hola+"/"+file
        return "No se encontro archivo PREFA o POSTFA"
    except Exception as err:
        return err

def read_storage_nokia():
    try:
        hola = os.getcwd()+ec2
        directory = os.listdir(hola)
        for file in directory:
            if file.startswith("NOKIA"):
                return hola+"/"+file
        return "No se encontro archivo NOKIA"
    except Exception as err:
        return err

def load_file_csv(path):
    try:
        df= pd.read_csv(path, delimiter=";")
        return df
    except Exception as err:
        return err

def load_file_excel(path):
    try:
        df= pd.read_csv(path, delimiter=",")
        return df
    except Exception as err:
        return err

def upload_file_nokia(request):
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
            file.save(os.path.join(upload_folder, "NOKIA"+file.filename))
        except Exception as err:
            return err
        return "Archivo cargado con éxito"
    except Exception as err:
        return(err)
    
def upload_file_facturacion(request):
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
            file.save(os.path.join(upload_folder, "FACT"+file.filename))
        except Exception as err:
            return err
        return "Archivo cargado con éxito"
    except Exception as err:
        return(err)
    
def delete_storage():
    dir = 'storage'
    archivos = os.listdir(dir)
    try:
        for archivo in archivos:
            ruta_completa = os.path.join(dir, archivo)
            try:
                if os.path.isfile(ruta_completa):
                    os.remove(ruta_completa)
            except Exception as e:
                return e    
    except Exception as e:
        return e

def read_merge_storage():
    try:
        dir = os.getcwd()+"/merge"
        directory = os.listdir(dir)
        for file in directory:
            if file.startswith("Tabla"):
                return dir+"/"+file
    except Exception as e:
        return "Error en descar" + e    

   