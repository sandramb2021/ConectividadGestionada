import pandas as pd
import os

directorio_final = os.getcwd()+"/ConectividadGestionada/backend/storage"


def read_storage_prefa():
    try:
        hola = os.getcwd()+"/backend/storage"
        directory = os.listdir(hola)
        for file in directory:
            if file.startswith("PREFA"):
                return hola+"/"+file
        return "No se encontro archivo PREFA"
    except Exception as err:
        return err

def read_storage_postfa():
    try:
        hola = os.getcwd()+"/backend/storage"
        directory = os.listdir(hola)
        for file in directory:
            if file.startswith("POSTFA"):
                return hola+"/"+file
        return "No se encontro archivo PREFA"
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
        df= pd.read_excel(path)
        return df
    except Exception as err:
        return err

