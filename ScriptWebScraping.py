# Propiedad de Adrian Fdz

# Importamos las librerías necesarias:
import sys
import os
import re # Librería para expresiones regulares
import requests
from bs4 import BeautifulSoup
#import time # Librería para hacer pausas en el script. Se ejecuta: time.sleep(segundos) Ej.: time.sleep(1)

# Hay que instalar antes de ejecutar las siguientes librerías y curl:
#   sudo apt install python3-pip
#   pip install requests beautifulsoup4 csv
#   sudo apt install curl

# - - PARTE 1 - - - - - - - - - - - - - - - - - - 

# Comprobamos que se ha proporcionado una URL como argumento al script
if len(sys.argv) != 2:
    print("Por favor, proporciona la URL de la página web de Youtube.")
    sys.exit(1)

url = sys.argv[1] # URL proporcionada como argumento

# Comprobamos que la URL es de youtube:
if not url.startswith("https://www.youtube.com"):
    print("La dirección URL introducida no es válida.")
    sys.exit(1)

archivo = "01_codigo_fuente.txt" # Nombre del archivo de texto en el que se guardará la información

# Exportamos el código HTML a un archivo txt
os.system(f"curl {url} > {archivo}")

try:
    # Exportamos el código HTML a un archivo txt
    os.system(f"curl {url} > {archivo}")
    print("- - - - - - - - - - - - - - - - - - - - - - - - - - - - -")
    print(f"El código fuente se ha descargado en: {archivo}.")
    print("Ahora será procesado para obtener los resultados.")
    print("- - - - - - - - - - - - - - - - - - - - - - - - - - - - -")
except Exception as e:
    print(f"Ha ocurrido un error al descargar el código fuente: {str(e)}")
    sys.exit(1)

# - - PARTE 2 - - - - - - - - - - - - - - - - - -

# Comprobamos que existe el archivo 01_codigo_fuente.txt y podemos leerlo
if not os.path.exists(archivo):
    print(f"No se ha podido encontrar el archivo {archivo}")
    sys.exit(1)

# Realizamos un control de errores para comprobar que se puede leer el archivoS
try:
    with open(archivo, "r") as f:
        codigo_fuente = f.read()
except IOError:
    print(f"No se ha podido leer el archivo {archivo}")
    sys.exit(1)

# Realizamos un control de errores para comprobar que se procesan bien los enlaces:
try:
    # Leemos el archivo 01_codigo_fuente.txt y almacenamos su contenido en una variable
    with open(archivo, "r") as f:
        codigo_fuente = f.read()

    # Buscamos todas las ocurrencias de la etiqueta "videoId" en el archivo
    videoIds = re.findall(r'"videoId":"([^\"]+)"', codigo_fuente)

    # Eliminamos valores repetidos
    videoIds = list(set(videoIds))

    #Añadimos la primera parte de la URL
    comienzo_url="https://www.youtube.com/watch?v="

    #Creamos una variable con el nombre del archivo que procesará las URLs completas
    url_videos="02_url_videos.txt"

    # Escribimos los videoIds en el archivo url_videos.txt
    with open(url_videos, "w") as f:
        for videoId in videoIds:
            f.write(comienzo_url+videoId + "\n")

    # Mostramos mensaje de que se ha realizado con éxito:
    print(f"Los enlaces se han procesado correctamente en: {url_videos}.")
    print("Procesando el fichero csv...")

except Exception as e:
    print(f"Ha ocurrido un error al procesar los enlaces: {str(e)}")
    sys.exit(1)

# - - PARTE 3 - - - - - - - - - - - - - - - - - -

# Damos un tiempo específico para que se procese el archivo anterior
#time.sleep(1)

# Realizamos un control de errores para comprobar
# que se crea correctamente el archivo csv
try:
    # Abrimos el archivo url_videos,
    # leemos las líneas y las pasamos a un array vacío
    # hacemos un for buscando en cada url 
    with open(url_videos, "r") as f:
        lineas = f.readlines()
        titulos = []
        for linea in lineas:
            # Obtenemos el código HTML:
            htmlRaw = requests.get(linea[:-1], cookies={'CONSENT': 'YES+1'}) #Hay que quitar un valor al final de cada fila con [:-1]
            # Creamos el objeto con la librería BeautifulSoup
            html = BeautifulSoup(htmlRaw.text, "html.parser")
            # Obtenemos con la siguiente línea el contenido de la etiqueta <title>
            titulos.append(f'"{linea[:-1]}";"{html.title.text.rstrip(" - YouTube")}"') #Hay que quitar con rstrip("Youtube") al final de cada título

    videos_csv = "03_videos.csv"

    # Escribimos los resultados en el archivo videos.csv
    with open(videos_csv, "w") as f:
        for titulo in titulos:
            f.write(titulo+"\n")

    print("- - - - - - - - - - - - - - - - - - - - - - - - - - - - -")
    print(f"El fichero {videos_csv} se ha procesado correctamente.")
    print("- - - - - - - - - - - - - - - - - - - - - - - - - - - - -")

except Exception as e:
    print(f"Ha ocurrido un error al crear el archivo csv: {str(e)}")
    sys.exit(1)