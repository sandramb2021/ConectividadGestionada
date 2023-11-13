import pandas as pd
import os


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
