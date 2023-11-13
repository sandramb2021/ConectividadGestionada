import pandas as pd
import os 

def procesar_archivos(prefa, postfa, periodoNokia, periodoPostfa):
    try:
        tablaNokia = prefa
        tablaPostfa = postfa
   
        if len(periodoNokia) > 2:
            raise Exception("Dos o mas periodos")

        if str(periodoNokia[0]) != str(periodoPostfa):
            raise Exception("No coinciden los periodos de Nokia con Postfa")


        Nokia = tablaNokia.set_index("CUIT")
        Postfa = tablaPostfa.set_index("IDENTIFICACION")
        merge = pd.merge(Nokia, Postfa, how="outer", left_index=True, right_index=True)
        conCeros = merge.fillna("0.0")
        mergeIndex = conCeros.reset_index()
        ## REVISAR ESTA PARTE PORQUE POR AHI ES CUIT O index
        cuit = mergeIndex["CUIT"].tolist()
        totalDeviceCharges = mergeIndex["total_device_charges"].tolist()
        valor = mergeIndex["VALOR"].tolist()
        indice = 0
        listDesvio = []
        while len(cuit) > indice:
            if cuit[indice].startswith("-"):
                listDesvio.append("CUIT INVALIDO")

            elif (float(totalDeviceCharges[indice]) == 0.0) & (float(valor[indice]) == 0.0):
                listDesvio.append("IN TESTING")

            elif totalDeviceCharges[indice] == valor[indice]:
                listDesvio.append("OK")

            elif (
                float(valor[indice]) - 1
                < float(totalDeviceCharges[indice])
                < float(valor[indice]) + 1
            ):
                listDesvio.append("OK-REDONDEO")

            elif totalDeviceCharges[indice] != valor[indice]:
                listDesvio.append("ERROR EN LA FACTURACION")

            else:
                listDesvio.append("VER PROBLEMA")

            indice += 1

        tablaFinal = mergeIndex.assign(RESULTADO=listDesvio)
        print(tablaFinal)
        direc = os.getcwd()+"/storage/"
        tablaFinal.to_excel(direc+f"TablaFinal${periodoNokia}.xlsx", index=False)
        return "hola"
    except Exception as err:
        return err