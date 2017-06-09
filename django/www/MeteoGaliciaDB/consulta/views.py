from django.http import HttpResponse
from django.shortcuts import render
import json
import requests
from . import forms
from datetime import timedelta
from django.contrib.auth.decorators import login_required



from pylab import *


# DataFrame
from pandas import DataFrame, Series


@login_required(login_url='/registro/acceso')
def formulario(request):
    form = forms.FormRequest()
    if request.method == 'POST':
        form = forms.FormRequest(request.POST)
        if form.is_valid():
            lugar = form.cleaned_data['Lugar']
            horas = form.cleaned_data['Prediccion']
            variables_posibles = form.cleaned_data['Variables']
            grafica = form.cleaned_data['Grafica']
            variables = ",".join(str(x) for x in variables_posibles)
            año = form.cleaned_data['Año']
            estacion = form.cleaned_data['Estacion_meteorológica']
            # Preparamos los datos de la petición
            api_code = 'tcZwyEj10Lb5W11usQMSM52QIlCutCCI64LfHv8AeuJsp9aE1F16tsn4yvdK0R52'
            '''
            key = open('meteosix_api_key', 'r')
            clave = ""
            for lineas in key:
                clave = clave + lineas
            '''
            parametros = {'location': lugar, 'API_KEY': api_code, 'format': 'application/json'}
            url = 'http://servizos.meteogalicia.es/apiv3/findPlaces'

            # Enviamos la peticion
            peticion = requests.get(url, parametros)

            # Obtenemos la respuesta
            respuesta = json.loads(peticion.text)

            # Obtenemos nuestras coordenadas
            longitud = str(respuesta['features'][0]['geometry']['coordinates'][0])
            latitud = str(respuesta['features'][0]['geometry']['coordinates'][1])

            # Preparamos los datos de la petición
            url = 'http://servizos.meteogalicia.es/apiv3/getNumericForecastInfo'
            coordenadas = longitud + ',' + latitud
            parametros2 = {'coords': coordenadas, 'API_KEY': api_code}
            # Enviamos la peticion
            peticion2 = requests.get(url, parametros2)

            # Obtenemos la respuesta

            respuesta2 = json.loads(peticion2.text)
            hora_actual = datetime.datetime.now().isoformat()
            hora_actual = hora_actual[:-7]
            hora_siguiente = (datetime.datetime.now() + timedelta(hours=int(horas))).isoformat()
            hora_siguiente = hora_siguiente[:-7]

            # Si queremos obtener unos datos concretos, le pasamos como parámetros las variables que deseamos
            parametros3 = {'coords': coordenadas, 'variables': variables, 'API_KEY': api_code,
                           'format':'text/html', 'endTime':hora_siguiente, 'lang':"es"}
            # Enviamos la peticion
            peticion3 = requests.get(url, parametros3)

            # Peticion a la API de aemet
            # API_KEY
            querystring = {"api_key":"eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJtaWd1ZWxvdXZpbmhhQGdtYWlsLmNvbSIsImp0aSI6ImY2MGY2ZTdhLTcxMmMtNDY0ZS05YTlmLTYzNWUyYjgyNThlYSIsImV4cCI6MTQ5OTE2MjExNiwiaXNzIjoiQUVNRVQiLCJpYXQiOjE0OTEzODYxMTYsInVzZXJJZCI6ImY2MGY2ZTdhLTcxMmMtNDY0ZS05YTlmLTYzNWUyYjgyNThlYSIsInJvbGUiOiIifQ.w0OazTbsiZdI5YQXCMIRnny_f0TwWF7leFvik1WeA8s"}


            # Esto debemos obtenerlo del formulario
            idema = estacion
            anho = año

            url = "https://opendata.aemet.es/opendata/api/valores/climatologicos/mensualesanuales/datos/anioini/" + anho + "/aniofin/" + anho + "/estacion/" + idema
            response = requests.request("GET", url, params=querystring, verify=False)

            cont = json.loads(response.text)
            cont = cont['datos']

            # Obtenemos los datos que nos interesan y los pasamos a formato json
            response = requests.request("GET", cont, verify = False)
            datos = json.loads(response.text)

            """
            ANALISIS DE DATOS CON PANDAS
            """
            # Indices de los DataFrames
            temperaturas = [ 'tm_mes', 'ta_max', 'ta_min', 'fecha', 'indicativo']
            precipitacions = ['p_mes']
            vento = ['w_med', 'w_racha']
            indice = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
                      'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre', 'Resumen']

            '''
            GRAFICAS
            '''

            if ( grafica == "histogramaTemperaturas"):
                '''
                TEMPERATURAS
                '''
                # Creamos el DataFrame
                frame_tem = DataFrame(datos, columns = temperaturas, index = indice)
                # Con esto eliminamos la fila resumen que no nos sirve en nustro caso
                frame_tem = frame_tem.iloc[0:12]
                # Borramos valores nulos
                frame_tem = frame_tem.dropna()
                #Procedemos a limpiar las filas del DataFrame
                temperatura_max = frame_tem.ta_max.map(lambda x: x.replace('(', ',')).map(lambda x: x.split(',')).map(lambda x: x[0]).map(lambda x: float(x))
                temperatura_min = frame_tem.ta_min.map(lambda x: x.replace('(', ',')).map(lambda x: x.split(',')).map(lambda x: x[0]).map(lambda x: float(x))
                temperatura_media = frame_tem.tm_mes
                temperatura_fechas = frame_tem.fecha.map(lambda x: x.replace('-', ',')).map(lambda x: x.split(',')).map(lambda x: x[1])

                data = { 'Temperatura Maxima' : temperatura_max,
                         'Temperatura Media' : temperatura_media,
                         'Temperatura Minima' : temperatura_min }

                # Frame con los datos finales
                finalTemperatura = DataFrame(data)
                finalTemperatura.plot()
                plt.title("Gráfica de Temperaturas año: " + anho)
                plt.xlabel("Mes")
                plt.ylabel("Grados Celsius")
                plt.savefig('/home/user/Escritorio/proyecto pi/pintgrupo16/django/www/MeteoGaliciaDB/consulta/static/consulta/imagenes/histogramaTemperaturas.png')
            elif( grafica == "tablaPrecipitaciones"):
                '''
                PRECIPITACIONES
                '''
                frame_pre = DataFrame(datos, columns = precipitacions, index = indice)
                # Con esto eliminamos la fila resumen que no nos sirve en nustro caso
                frame_pre = frame_pre.iloc[0:12]
                # Borramos valores nulos
                frame_pre = frame_pre.dropna()
                frame_pre = frame_pre.p_mes.map(lambda x: float(x))
            elif( grafica == "rosaVientos"):
                '''
                VENTO
                '''
                frame_vento = DataFrame(datos, columns = vento, index = indice)
                # Con esto eliminamos la fila resumen que no nos sirve en nustro caso
                frame_vento = frame_vento.iloc[0:12]
                # Borramos valores nulos
                frame_vento = frame_vento.dropna()
                # Limpiamos datos y obtenemos los grados completos del resultada
                frame_vento_dir = frame_vento.w_racha.map(lambda x: x.replace('(', '/')).map(lambda x: x.split('/')).map(lambda x: x[0]).map(lambda x: float(x)) * 10
                # Limpiamos datos y pasamos a kilometros por hora
                frame_vento_vel = frame_vento.w_racha.map(lambda x: x.replace('(', '/')).map(lambda x: x.split('/')).map(lambda x: x[1]).map(lambda x: float(x)) / 1000 * 3600

                ## Creamos un conjunto de 1000 datos entre 0 y 1 de forma aleatoria
                ## a partir de una distribución estándar normal
                datos = np.random.randn(1000)
                ## Discretizamos el conjunto de valores en n intervalos,
                ## en este caso 8 intervalos
                datosbin = np.histogram(datos, bins=np.linspace(np.min(datos), np.max(datos), 9))[0]
                ## Los datos los queremos en tanto por ciento
                datosbin = datosbin * 100. / len(datos)
                ## Los datos los queremos en n direcciones/secciones/sectores,
                ## en este caso usamos 8 sectores de una circunferencia
                sect = np.array([90, 45, 0, 315, 270, 225, 180, 135]) * 2. * math.pi / 360.
                nombresect = ['E', 'NE', 'N', 'NW', 'W', 'SW', 'S', 'SE']
                ## Dibujamos la rosa de frecuencias
                plt.axes([0.1, 0.1, 0.8, 0.8], polar=True)
                plt.bar(sect, datosbin, align='center', width=45 * 2 * math.pi / 360.,
                        facecolor='b', edgecolor='k', linewidth=2, alpha=0.5)
                plt.thetagrids(np.arange(0, 360, 45), nombresect, frac=1.1, fontsize=10)
                plt.title(u'Procedencia de las nubes en marzo')
                plt.savefig('/home/user/Escritorio/proyecto pi/pintgrupo16/django/www/MeteoGaliciaDB/consulta/static/consulta/imagenes/rosavientos.png')



            return render(request, 'consulta/resultado/imprimir.html', {'variables': variables,
                                                                        'respuesta3': peticion3.content,
                                                                        'lugar': lugar,
                                                                        'hora_actual': hora_actual,
                                                                        'hora_siguiente': hora_siguiente,
                                                                        'dias': horas,
                                                                        'Variables': variables_posibles,
                                                                        'latitud':latitud,
                                                                        'longitud': longitud,
                                                                        'grafica':grafica})

    return render(request,'consulta/formulario/form.html', {'form': form})



'''
Lo llamo directamente desde el template
'''
def simple(request):
    import random
    import django
    import datetime

    from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
    from matplotlib.figure import Figure
    from matplotlib.dates import DateFormatter

    fig = Figure()
    ax = fig.add_subplot(111)
    x = []
    y = []
    now = datetime.datetime.now()
    delta = datetime.timedelta(days=1)
    for i in range(10):
        x.append(now)
        now += delta
        y.append(random.randint(0, 1000))
    ax.plot_date(x, y, '-')
    ax.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d'))
    fig.autofmt_xdate()
    canvas = FigureCanvas(fig)
    response = django.http.HttpResponse(content_type='image/png')
    canvas.print_png(response)
    return response



def rosaVientos(request):
    import random
    import django
    import datetime
    from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
    from matplotlib.figure import Figure
    ## De la librería estándar
    import math
    ## De librerías de terceros
    import numpy as np
    import matplotlib.pyplot as plt

    fig = Figure()

    ## Creamos un conjunto de 1000 datos entre 0 y 1 de forma aleatoria
    ## a partir de una distribución estándar normal
    datos = np.random.randn(1000)
    ## Discretizamos el conjunto de valores en n intervalos,
    ## en este caso 8 intervalos
    datosbin = np.histogram(datos, bins=np.linspace(np.min(datos), np.max(datos), 9))[0]
    ## Los datos los queremos en tanto por ciento
    datosbin = datosbin * 100. / len(datos)
    ## Los datos los queremos en n direcciones/secciones/sectores,
    ## en este caso usamos 8 sectores de una circunferencia
    sect = np.array([90, 45, 0, 315, 270, 225, 180, 135]) * 2. * math.pi / 360.
    nombresect = ['E', 'NE', 'N', 'NW', 'W', 'SW', 'S', 'SE']
    ## Dibujamos la rosa de frecuencias
    plt.axes([0.1, 0.1, 0.8, 0.8], polar=True)
    plt.bar(sect, datosbin, align='center', width=45 * 2 * math.pi / 360.,
            facecolor='b', edgecolor='k', linewidth=2, alpha=0.5)
    plt.thetagrids(np.arange(0, 360, 45), nombresect, frac=1.1, fontsize=10)
    plt.title(u'Procedencia de las nubes en marzo')
    #plt.show()

    canvas = FigureCanvas(fig)
    response = django.http.HttpResponse(content_type='image/png')
    canvas.print_png(response)
    return response






'''


##################################################################################

   Dejo esto por aquí por si bokeh porque arriba voy a probar con otro método

##################################################################################



@login_required(login_url='/registro/acceso')
def formulario(request):
    form = forms.FormRequest()
    if request.method == 'POST':
        form = forms.FormRequest(request.POST)
        if form.is_valid():
            lugar = form.cleaned_data['Lugar']
            horas = form.cleaned_data['Prediccion']
            variables_posibles = form.cleaned_data['Variables']
            variables = ",".join(str(x) for x in variables_posibles)
            # Preparamos los datos de la petición
            api_code = 'tcZwyEj10Lb5W11usQMSM52QIlCutCCI64LfHv8AeuJsp9aE1F16tsn4yvdK0R52'
            ''''''
            key = open('meteosix_api_key', 'r')
            clave = ""
            for lineas in key:
                clave = clave + lineas
            ''''''
            parametros = {'location': lugar, 'API_KEY': api_code, 'format': 'application/json'}
            url = 'http://servizos.meteogalicia.es/apiv3/findPlaces'

            # Enviamos la peticion
            peticion = requests.get(url, parametros)

            # Obtenemos la respuesta
            respuesta = json.loads(peticion.text)

            # Obtenemos nuestras coordenadas
            longitud = str(respuesta['features'][0]['geometry']['coordinates'][0])
            latitud = str(respuesta['features'][0]['geometry']['coordinates'][1])

            # Preparamos los datos de la petición
            url = 'http://servizos.meteogalicia.es/apiv3/getNumericForecastInfo'
            coordenadas = longitud + ',' + latitud
            parametros2 = {'coords': coordenadas, 'API_KEY': api_code}
            # Enviamos la peticion
            peticion2 = requests.get(url, parametros2)

            # Obtenemos la respuesta

            respuesta2 = json.loads(peticion2.text)
            hora_actual = datetime.datetime.now().isoformat()
            hora_actual = hora_actual[:-7]
            hora_siguiente = (datetime.datetime.now() + timedelta(hours=int(horas))).isoformat()
            hora_siguiente = hora_siguiente[:-7]

            # Si queremos obtener unos datos concretos, le pasamos como parámetros las variables que deseamos
            parametros3 = {'coords': coordenadas, 'variables': variables, 'API_KEY': api_code,
                           'format':'text/html', 'endTime':hora_siguiente, 'lang':"es"}
            # Enviamos la peticion
            peticion3 = requests.get(url, parametros3)
            # Obtenemos la respuesta
            #respuesta3 = json.loads(peticion3.text)

            # Just an example

            datos = np.random.randn(1000)
            ## Discretizamos el conjunto de valores en n intervalos,
            ## en este caso 8 intervalos
            datosbin = np.histogram(datos,
                                    bins=np.linspace(np.min(datos), np.max(datos), 9))[0]
            ## Los datos los queremos en tanto por ciento
            datosbin = datosbin * 100. / len(datos)
            ## Los datos los queremos en n direcciones/secciones/sectores,
            ## en este caso usamos 8 sectores de una circunferencia
            sect = np.array([90, 45, 0, 315, 270, 225, 180, 135]) * 2. * math.pi / 360.
            nombresect = ['E', 'NE', 'N', 'NW', 'W', 'SW', 'S', 'SE']
            ## Dibujamos la rosa de frecuencias
            plt.axes([0.1, 0.1, 0.8, 0.8], polar=True)
            plt.bar(sect, datosbin, align='center', width=45 * 2 * math.pi / 360.,
                    facecolor='b', edgecolor='k', linewidth=2, alpha=0.5)
            plt.thetagrids(np.arange(0, 360, 45), nombresect, frac=1.1, fontsize=10)
            plt.title(u'Procedencia de las nubes en marzo')
            #plt.show()
            #plot = figure()
            #plot.circle([1, 2], [3, 4])
            script, div = components(plt, CDN)
            return render(request, 'consulta/resultado/imprimir.html', {'variables': variables,
                                                                        'respuesta3': peticion3.content,
                                                                        'lugar': lugar,
                                                                        'hora_actual': hora_actual,
                                                                        'hora_siguiente': hora_siguiente,
                                                                        'dias': horas,
                                                                        'Variables': variables_posibles,
                                                                        'latitud':latitud,
                                                                        'longitud': longitud,
                                                                        "the_script": script,
                                                                        "the_div": div})

    return render(request,'consulta/formulario/form.html', {'form': form})


'''
