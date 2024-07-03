import time
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from pronosticosWebApp.models import Productos

productos = list(Productos.objects.values()) # Se obtienen los productos de la base de datos en forma de lista
df_demanda = pd.DataFrame(productos) # Se convierten los productos en un DataFrame de pandas para su manipulación

class PronosticoExpSimple:
    
    def __init__(self):
        pass
    
    def pronosticoExpSimple(alpha, cantidadMeses):
        print('espere un momento...')
        demanda = df_demanda.iloc[:, 4:cantidadMeses+4] #se toma desde 4 porque es la posición donde inicia el primer mes en el excel y a la cantidadMeses se le suma 4 porque hay 3 columnas que no se deben tener en cuenta
        
        valores_demanda = demanda.values.flatten().tolist() #faltten aplana la matriz resultante y tolist convierte en lista
        
        #Ft = Ft-1 + alpha*(Xt-1 - Ft-1)
        pronostico_ses = []
        for i in range(0, len(valores_demanda), cantidadMeses):
            grupo = valores_demanda[i:i+(cantidadMeses)]
            pronostico_ses.append(grupo[0])
            for item in range(len(grupo)):        
                pronostico_ses.append(pronostico_ses[-1] + alpha*(grupo[item] - pronostico_ses[-1]))
        # print(pronostico_ses[:20])
        
        #valores del pronostico del siguiente mes
        valores_pronostico_mes_siguiente = [pronostico_ses[i] for i in range(cantidadMeses, len(pronostico_ses), cantidadMeses+1)]
       
        # Asignar los valores del pronostico al siguiente mes y se agrega al dataframe demanda
        demanda['MAYO_2'] = valores_pronostico_mes_siguiente
        
        lista_nombre_columnas = demanda.columns.to_list()  #lista de los nombres de las columnas
        # Dividir la lista de valores en segmentos de longitud 8(cantidad de meses más el pronostico)
        segmentos_valores = [pronostico_ses[i:i+(cantidadMeses+1)] for i in range(0, len(pronostico_ses), cantidadMeses+1)]
        # print(segmentos_valores[:20])
        # segmentos_valores = pronostico_ses.reshape(-1, cantidadMeses)
        # print(segmentos_valores[:20])
        
        # Crear un DataFrame con los segmentos de valores y los nombres de las columnas
        df_pronostico_ses = pd.DataFrame(segmentos_valores, columns=lista_nombre_columnas)
        # print(df_pronostico_ses)
        
        #guardar los pronosticos del siguiente mes en una lista
        lista_pronosticos=[demanda.iloc[i,cantidadMeses] for i in demanda.index]
        #lista de pronosticos redondeado
        lista_pronosticos_redondeo = [round(i*2) for i in lista_pronosticos]
        
        errores, erroresMape, erroresMapePrima, erroresCuadraticoMedio = [], [], [], []
        MAD=[] #mean absolute deviation
        MAPE=[] #mean absolute percentage error
        MAPE_prima=[] #mean absolute percentage error prima
        ECM=[] #error cuadratico medio
        
        # Crear una nueva lista sin los valores de los pronosticos del siguiente mes
        pronostico_ses_filtrado = df_pronostico_ses.iloc[:, :-1].values
        pronostico_ses_filtrado = pronostico_ses_filtrado.flatten().tolist()
        
        # Optimización del cálculo de errores utilizando operaciones vectorizadas
        errores = (demanda.iloc[:, 1:cantidadMeses].values - df_pronostico_ses.iloc[:, 1:cantidadMeses].values).flatten().tolist()
        # print(errores[:5])
        erroresAbs = np.abs(errores) #errores absolutos |e|
        
        total_meses_pronostico = cantidadMeses - 1 #total de meses a pronosticar menos el siguiente
        #CALCULO DEL MAD(MEAN ABSOLUTE DEVIATION) 
        MAD = [np.mean(erroresAbs[i:i+total_meses_pronostico]) for i in range(0, len(erroresAbs), total_meses_pronostico)]
        # print('MAD: ',MAD[:5])
        
        #CALCULO DEL MAPE(MEAN ABSOLUTE PERCENTAGE ERROR)
        valores_demanda_mape = demanda.iloc[:,1:cantidadMeses].values.flatten().tolist()
    
        #guardar erroresMape |e|/xt(demanda)
        erroresMape = [ea / vd if vd != 0 else 1 for ea, vd in zip(erroresAbs, valores_demanda_mape)]
        MAPE = [np.mean(erroresMape[i:i+total_meses_pronostico]) * 100 for i in range(0, len(erroresMape), total_meses_pronostico)]
        # print('MAPE: ',MAPE[:5])
        
        #CALCULO DEL MAPE' (MAPE PRIMA)
        # Indices a eliminar (multiplos de 7 iniciando desde 0), es decir, retorna el indice donde están los valores de los pronosticos del siguiente mes
        indices_a_eliminar = [i for i, valor in enumerate(pronostico_ses) if (i) % cantidadMeses == 0]
        
        # Crear una nueva lista sin los elementos en los indices a eliminar
        pronostico_ses_filtrado = [valor for i, valor in enumerate(pronostico_ses_filtrado) if i not in indices_a_eliminar]
        
        #guardar erroresMapePrima |e|/Mt(promedio_movil)
        erroresMapePrima = [ea / psf if psf != 0 else 1 for ea, psf in zip(erroresAbs, pronostico_ses_filtrado)]
        MAPE_prima = [np.mean(erroresMapePrima[i:i+total_meses_pronostico]) * 100 for i in range(0, len(erroresMapePrima), total_meses_pronostico)]
        # print(MAPE_prima[:5])
        
        #EMC(CALCULO DEL ERROR CUADRATICO MEDIO) |e|^2
        erroresCuadraticoMedio = erroresAbs ** 2
        ECM = [np.mean(erroresCuadraticoMedio[i:i+total_meses_pronostico]) for i in range(0, len(erroresCuadraticoMedio), total_meses_pronostico)]
        # print(ECM[:5])
        # print(df_pronostico_ses.iloc[:,-1]) #retorna los valores del última columna
        # print(df_pronostico_ses.iloc[:, :-1]) #retorna todos los valores menos la última columna

        return MAD, MAPE, MAPE_prima, ECM, df_pronostico_ses, lista_pronosticos, lista_pronosticos_redondeo

    def productos():
        items = df_demanda.iloc[:, 0].tolist()
        proveedor = df_demanda.iloc[:,1].tolist()
        productos = df_demanda.iloc[:, 2].tolist()
        sede = df_demanda.iloc[:, 3].tolist()
        return items, proveedor, productos, sede

    def prueba():
        start_time = time.perf_counter()
        MAD, MAPE, MAPE_prima, ECM, df_pronostico_ses, lista_pronosticos, lista_pronosticos_redondeo = PronosticoExpSimple.pronosticoExpSimple(0.5, 12)
        items, proveedor, productos, sede = PronosticoExpSimple.productos()
        
        # serie = pd.concat([pd.Series(productos), pd.Series(MAD), pd.Series(MAPE)], axis=1)
        # serie.columns = ["Productos", "MAD", "Mejor pronostico"]
        # df = pd.DataFrame({"Items": items, "Proveedor": proveedor, "Productos": productos, "Sede": sede, "MAD": MAD, "MAPE": MAPE, "MAPE_Prima": MAPE_prima, "ECM": ECM, "Pronostico": lista_pronosticos, "Pronostico_redondeo": lista_pronosticos_redondeo})
    
        # # Especifica la ruta del archivo Excel donde deseas guardar el DataFrame
        # ruta_archivo_excel = 'suavizacion_exp_simple.xlsx'

        # # Usa el método to_excel() para guardar el DataFrame en el archivo Excel
        # df.to_excel(ruta_archivo_excel, index=False)  # Si no deseas incluir el índice en el archivo Excel, puedes establecer index=False
        end_time = time.perf_counter()
        print(f"Tiempo de ejecución: {end_time - start_time} segundos")
        
# PronosticoExpSimple.prueba()


