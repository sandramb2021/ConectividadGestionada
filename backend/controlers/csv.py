import pandas as pd
import os


def obtenerListaLiquidacion(tabla):
    df1 = tabla
    dfNuevo = df1.groupby(
        [("external_cost_center"), "wing_customer_name"]
    ).total_device_charges.sum()
    dfNuevoFrame = dfNuevo.to_frame().astype(str)
    dfReseteado = dfNuevoFrame.reset_index()
    dfConIndex = dfReseteado.set_index("external_cost_center")
    # CUIC QUE SI O SI TIENEN $COSTOS
    lista = dfConIndex.index

    listaCuic = []

    for x in lista:
        converString = str(x)
        try:
            if converString.endswith(".0"):
                sinPunto = converString.split(sep=".0", maxsplit=1)
                cuitFinal = sinPunto[0]
                if len(cuitFinal) > 10:
                    if cuitFinal.startswith("10"):
                        sinDiez = cuitFinal.split(sep="10", maxsplit=1)

                        listaCuic.append(sinDiez[1])

                    else:
                        listaCuic.append(cuitFinal)
                else:
                    listaCuic.append("-" + cuitFinal)
            else:
                if len(converString) > 10:
                    if converString.startswith("10"):
                        sinDiez = converString.split(sep="10", maxsplit=1)

                        listaCuic.append(sinDiez[1])

                    else:
                        listaCuic.append(converString)

                else:
                    listaCuic.append("-" + converString)
        except:
            print("Except")
    return listaCuic


def exportarTablaNokia (tabla,liquidacion):

    try:

        dfNuevo = tabla.groupby([('external_cost_center'),'wing_customer_name']).total_device_charges.sum()
        dfNuevoFrame = dfNuevo.to_frame().astype(str)
        dfReseteado = dfNuevoFrame.reset_index()
        tablaFinalNokiaF = dfReseteado.assign(CUIT = liquidacion)
        tablaFinalNokiaF = tablaFinalNokiaF.set_index("CUIT")
        return tablaFinalNokiaF.reset_index()

    except Exception as error:

        return error

def periodoNokia (tabla) :
    listaPeriodos = tabla['bill_period'].tolist()
    return list(set(listaPeriodos))

def exportarTablaPrefa(tabla):
    try:
        tablaPostfa = tabla
        nuevaTabla = tablaPostfa[
            (tablaPostfa.CONCDESC == "Gestor SIMs IoT Datos")
            | (tablaPostfa.CONCDESC == "Gestor SIMs IoT P. MÃ³vil")
            | (tablaPostfa.CONCDESC == "Gestor SIMs IoT P. Datos")
            | (tablaPostfa.CONCDESC == "Gestor SIMs IoT SMS")
        ]
        lista = nuevaTabla["IDENTIFICATION"].tolist()
        listaNUeva = []
        for x in lista:
            listaNUeva.append(str(x))
        tablaPostfaIot = nuevaTabla.assign(IDENTIFICACION=listaNUeva)
        dfAgrupado = tablaPostfaIot.groupby("IDENTIFICACION").VALOR.sum()
        dfToFrame = dfAgrupado.to_frame().astype(str)
        return dfToFrame.reset_index()

    except Exception as error:
        return error


def periodoPrefa(tabla):
    try:
        tablaPostfa = tabla
        nuevaTabla = tablaPostfa[
            (tablaPostfa.CONCDESC == "Gestor SIMs IoT Datos")
            | (tablaPostfa.CONCDESC == "Gestor SIMs IoT P. MÃ³vil")
            | (tablaPostfa.CONCDESC == "Gestor SIMs IoT P. Datos")
            | (tablaPostfa.CONCDESC == "Gestor SIMs IoT SMS")
        ]

        lista = nuevaTabla["IDENTIFICATION"].tolist()

        listaNUeva = []

        for x in lista:
            listaNUeva.append(str(x))

        tablaPostfaIot = nuevaTabla.assign(IDENTIFICACION=listaNUeva)

        listaPeriodos = tablaPostfaIot["CARGFECR"].tolist()[0]

        listaCortada = listaPeriodos.split("-", 2)

        periodoFinal = listaCortada[0] + listaCortada[1]

        return periodoFinal
    except Exception as err:
        return err
