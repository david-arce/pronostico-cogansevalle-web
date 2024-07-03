from django.shortcuts import render
from django.http.response import JsonResponse, HttpResponse
from .models import Productos
from django.views.decorators.csrf import csrf_exempt
import json

import pandas as pd
from pronosticosWebApp.pronosticos.promedioMovil import PronosticoMovil as pm
from pronosticosWebApp.pronosticos.suavizacionExpSimple import PronosticoExpSimple as ses
from pronosticosWebApp.pronosticos.suavizacionExpDoble import PronosticoExpDoble as sed
from pronosticosWebApp.pronosticos.pronosticos import Pronosticos

selected_index = 0 # Variable global para almacenar el índice seleccionado
list_demanda, list_promedio_movil, list_ses, list_sed = [], [], [], []
# Create your views here.
def dashboard(request):
    return render(request, "index.html")

@csrf_exempt
def send_data(request):
    
    if request.method == 'POST':
        data = json.loads(request.body)
        selected_rows = data.get('selectedRows', [])
        #retornar el indice de la tabla menos 1
        global selected_index
        selected_index = int(selected_rows[0]) - 1
        
        return JsonResponse({"status": "success", "message": "Datos recibidos correctamente"}) 
    else:
        return JsonResponse({"status": "error", "message": "Método no permitido"}, status=405)
# def lista(request):
#     productos = Productos.objects.values('item', 'proveedor', 'descripción', 'sede', 'mayo', 'junio', 'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre', 'enero', 'febrero', 'marzo', 'abril', 'total', 'promedio')
#     return render(request, 'template.html', {'productos': productos})

def lista_productos(request):
    # productos = list(Productos.objects.values())
    # data = {"productos": productos}
    global mejor_ECM, origen_ECM, serie, MAD, MAPE, MAPE_prima, ECM, demanda, promedio_movil, lista_pronostico_movil, datos_excel, MAD1, MAPE1, MAPE_prima1, ECM1, df_pronostico_ses, MAD2, MAPE2, MAPE_prima2, ECM2, df_pronostico_sed, pronostico_final, MAD_final, MAPE_final, MAPE_PRIMA_final, ECM_final, pronostico_seleccionado, df_pronosticos, pronostico_final_redondeado
    global items, proveedor, productos, sede
    
    mejor_ECM, origen_ECM, serie, MAD, MAPE, MAPE_prima, ECM, demanda, promedio_movil, lista_pronostico_movil, datos_excel, MAD1, MAPE1, MAPE_prima1, ECM1, df_pronostico_ses, MAD2, MAPE2, MAPE_prima2, ECM2, df_pronostico_sed, pronostico_final, MAD_final, MAPE_final, MAPE_PRIMA_final, ECM_final, pronostico_seleccionado, df_pronosticos, pronostico_final_redondeado = Pronosticos.pronosticos()
    items, proveedor, productos, sede = pm.productos()
    
    # Convertir el DataFrame a JSON
    df_pronosticos_json = df_pronosticos.to_dict(orient='records')
    data = {"productos":df_pronosticos_json}
    
    return JsonResponse(data, safe=False)
  
def df_productos():
  productos = list(Productos.objects.values())
  df_productos = pd.DataFrame(productos)
  return df_productos

def meses():
  # productos = list(Productos.objects.values_list('descripción', flat=True))
  # data = {"productos": productos}
  nombres_columnas = [field.name for field in Productos._meta.get_fields()]
  # Definir los campos a eliminar
  campos_a_eliminar = {'item', 'proveedor', 'descripción', 'sede', 'total', 'promedio'}
  
  # Filtrar los nombres de las columnas
  nombres_columnas = [col for col in nombres_columnas if col not in campos_a_eliminar]
  #agregar un valor mas a la lista
  nombres_columnas.append('Pronóstico')
  return nombres_columnas

def get_chart(request):
    
    if selected_index is None:
        return JsonResponse({"status": "error", "message": "Por favor selecciona una fila de la tabla para generar la gráfica"}, status=400)
    # list_demanda, list_promedio_movil, list_ses, list_sed = grafica(selected_index)
    
    global list_demanda, list_promedio_movil, list_ses, list_sed
    list_demanda = demanda.iloc[selected_index][:-1].fillna(0).astype(int).tolist()
    list_promedio_movil = promedio_movil.iloc[selected_index].fillna(0).astype(int).tolist()
    list_ses = df_pronostico_ses.iloc[selected_index].fillna(0).astype(int).tolist()
    list_sed = df_pronostico_sed.iloc[selected_index].fillna(0).astype(int).tolist()
    
    list_sed.insert(0, '')
    # list_demanda = [1,2,3,4]
    # list_promedio_movil = [2,3,4,5]
    # list_ses = [3,4,5,6]
    # list_sed = [4,5,6,7]
    xAxis = meses()
    chart = {
        "title": {"text": "Pronósticos", "subtext": "Pronóstico del item: {}".format(items[selected_index])},
        "tooltip": {"trigger": "axis"},
        "legend": {
            "data": ["Demanda", "Promedio móvil", "Suavización exponencial simple", "Suaización exponencial doble"]
        },
        "grid": {"left": "3%", "right": "4%", "bottom": "3%", "containLabel": True},
        "toolbox": {"feature": {"saveAsImage": {}}},
        "xAxis": {
            "type": "category",
            "boundaryGap": False,
            "data": xAxis,
        },
        "yAxis": {"type": "value"},
        "series": [
            {
                "name": "Demanda",
                "type": "line",
                "data": list_demanda,
            },
            {
                "name": "Promedio móvil",
                "type": "line",
                "data": list_promedio_movil,
            },
            {
                "name": "Suavización exponencial simple",
                "type": "line",
                "data": list_ses,
            },
            {
                "name": "Suaización exponencial doble",
                "type": "line",
                "data": list_sed,
            },
        ],
    }
    return JsonResponse(chart)
