import ssl
from django.db.models import Avg
from datetime import timedelta, datetime
from receiver.models import Data, Station, Measurement
import paho.mqtt.client as mqtt
import schedule
import time
from django.conf import settings
from dateutil.relativedelta import relativedelta
import pandas as pd

client = mqtt.Client(settings.MQTT_USER_PUB)


def job():
    analyze_data()
    evalue_outlier()

def evalue_outlier():
    # Consulta todos los datos del último mes, los agrupa por estación y variable
    # Compara el promedio de la ultima hora con la desviacion estandar para determinar si en un valor atipico.
    # Si el promedio se excede de los límites, se envia un mensaje de alerta.

    print("Calculando valores atípicos...")

    # obtiene los datos del último mes
    data = pd.DataFrame(
        list(
            Data.objects.filter(
                base_time__gte=datetime.now() - relativedelta(months = 1)
                ).order_by('time').values()
            )
        )
    
    # hace ciclo por las estaciones
    alerts = 0
    i = 0
    for estacion in data['station_id'].unique():
        print(f"Procesando estacion : {estacion}")
        # hace ciclo por las medidas de la estacion
        for medida in data[data['station_id']==estacion]['measurement_id'].unique():
            print(f"Procesando medida : {medida}")
            i += 1
            # describe los valores de la medida
            valores = data.loc[(data['station_id']==estacion) & (data['measurement_id']==medida)]['values'].values
            # une todos los arrays en uno solo
            lista = []
            for item in valores:
                lista += item
            # crea un dataframe con los datos medidos
            df = pd.DataFrame(lista, columns=['valores'])
            # obtiene la informacion estadistica
            describe = df.describe()
            # obtiene los cuartiles
            q1 = describe.loc["25%", "valores"]
            q3 = describe.loc["75%", "valores"]
            # calcula el rango intercuartil
            rango = q3 - q1
            # calcula los limites para valores atipicos
            lim_sup = q3 + rango * 1.5
            lim_inf = q1 - rango * 1.5
            
            # determina si el último dato es atipico y con ello genera alarma
            if lista[-1] < lim_inf or lista[-1] > lim_sup:
                station = Station.objects.filter(pk=estacion)[0]
                measure = Measurement.objects.filter(pk=medida)[0]
                variable = measure.name
                country = station.location.country.name
                state = station.location.state.name
                city = station.location.city.name
                user = station.user.username

                message = f"ALERT {variable} {lim_inf} {lim_sup}"
                topic = f'{country}/{state}/{city}/{user}/in'
                print(datetime.now(), f"Sending alert to {topic} {variable}")
                client.publish(topic, message)
                alerts += 1

    print(f"{i} dispositivos revisados")
    print(f"{alerts} alertas enviadas")


def analyze_data():
    # Consulta todos los datos de la última hora, los agrupa por estación y variable
    # Compara el promedio con los valores límite que están en la base de datos para esa variable.
    # Si el promedio se excede de los límites, se envia un mensaje de alerta.

    print("Calculando alertas...")

    data = Data.objects.filter(
        base_time__gte=datetime.now() - timedelta(hours=1))
    aggregation = data.annotate(check_value=Avg('avg_value')) \
        .select_related('station', 'measurement') \
        .select_related('station__user', 'station__location') \
        .select_related('station__location__city', 'station__location__state',
                        'station__location__country') \
        .values('check_value', 'station__user__username',
                'measurement__name',
                'measurement__max_value',
                'measurement__min_value',
                'station__location__city__name',
                'station__location__state__name',
                'station__location__country__name')
    alerts = 0
    for item in aggregation:
        alert = False

        variable = item["measurement__name"]
        max_value = item["measurement__max_value"] or 0
        min_value = item["measurement__min_value"] or 0

        country = item['station__location__country__name']
        state = item['station__location__state__name']
        city = item['station__location__city__name']
        user = item['station__user__username']

        if item["check_value"] > max_value or item["check_value"] < min_value:
            alert = True

        if alert:
            message = "ALERT {} {} {}".format(variable, min_value, max_value)
            topic = '{}/{}/{}/{}/in'.format(country, state, city, user)
            print(datetime.now(), "Sending alert to {} {}".format(topic, variable))
            client.publish(topic, message)
            alerts += 1

    print(len(aggregation), "dispositivos revisados")
    print(alerts, "alertas enviadas")


def on_connect(client, userdata, flags, rc):
    '''
    Función que se ejecuta cuando se conecta al bróker.
    '''
    print("Conectando al broker MQTT...", mqtt.connack_string(rc))


def on_disconnect(client: mqtt.Client, userdata, rc):
    '''
    Función que se ejecuta cuando se desconecta del broker.
    Intenta reconectar al bróker.
    '''
    print("Desconectado con mensaje:" + str(mqtt.connack_string(rc)))
    print("Reconectando...")
    client.reconnect()


def setup_mqtt():
    '''
    Configura el cliente MQTT para conectarse al broker.
    '''

    print("Iniciando cliente MQTT...", settings.MQTT_HOST, settings.MQTT_PORT)
    global client
    try:
        client = mqtt.Client(settings.MQTT_USER_PUB)
        client.on_connect = on_connect
        client.on_disconnect = on_disconnect

        if settings.MQTT_USE_TLS:
            client.tls_set(ca_certs=settings.CA_CRT_PATH,
                           tls_version=ssl.PROTOCOL_TLSv1_2, cert_reqs=ssl.CERT_NONE)

        client.username_pw_set(settings.MQTT_USER_PUB,
                               settings.MQTT_PASSWORD_PUB)
        client.connect(settings.MQTT_HOST, settings.MQTT_PORT)

    except Exception as e:
        print('Ocurrió un error al conectar con el bróker MQTT:', e)


def start_cron():
    '''
    Inicia el cron que se encarga de ejecutar la función analyze_data cada minuto.
    '''
    print("Iniciando cron...")
    schedule.every().hour.do(job)
    
    print("Servicio de control iniciado")
    while 1:
        schedule.run_pending()
        time.sleep(1)
