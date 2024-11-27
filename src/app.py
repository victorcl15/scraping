# -*- coding: utf-8 -*-
"""Evidencia de aprendizaje 2. Optimizando la productividad en el mundo del software

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1Ql0DYUr-O3AirPGWn0AfHVJLcU6vcewV
"""

# prompt: instalar la dependencia de from bs4 import BeautifulSoup

import subprocess

# Install beautifulsoup4
subprocess.run(["pip", "install", "beautifulsoup4"])

import requests
from bs4 import BeautifulSoup
import pandas as pd

# URL de la página de búsqueda en Mercado Libre
url = 'https://listado.mercadolibre.com.co/audifonos#D%5BA:Audifonos%5D'

# Realizar la solicitud a la página web
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
}
response = requests.get(url, headers=headers)

# Verificar que la solicitud fue exitosa
if response.status_code == 200:
    soup = BeautifulSoup(response.content, 'html.parser')

    # Variables para almacenar los datos
    nombres = []
    precios = []
    calificaciones = []
    urls = []

    # Buscar los contenedores de cada producto
    productos = soup.find_all('li', class_='ui-search-layout__item')

    for producto in productos:
        # Extraer nombre del producto
        nombre_tag = producto.find('h2', class_='poly-component__title')
        nombre = nombre_tag.find('a').get_text().strip() if nombre_tag else 'N/A'

        # Extraer precio actual del producto
        precio_tag = producto.find('div', class_='poly-price__current')
        precio = precio_tag.find('span', class_='andes-money-amount__fraction').get_text().strip() if precio_tag else 'N/A'

        # Extraer calificación del producto
        calificacion_tag = producto.find('div', class_='poly-component__reviews')
        calificacion = calificacion_tag.find('span', class_='poly-reviews__rating').get_text().strip() if calificacion_tag else 'Sin calificación'

        # Extraer URL del producto
        enlace_tag = nombre_tag.find('a') if nombre_tag else None
        url_producto = enlace_tag['href'] if enlace_tag else 'N/A'

        # Añadir los datos a las listas
        nombres.append(nombre)
        precios.append(precio)
        calificaciones.append(calificacion)
        urls.append(url_producto)

    # Crear el DataFrame con los datos extraídos
    df = pd.DataFrame({
        'Nombre del Producto': nombres,
        'Precio (COP)': precios,
        'Calificación': calificaciones,
        'URL del Producto': urls
    })

    # Guardar los datos en un archivo CSV
    df.to_csv('productos_mercado_libre.csv', index=False)
    print(df)
    print("Datos guardados en 'productos_mercado_libre.csv'")

else:
    print(f"Error al acceder a la página. Código de estado: {response.status_code}")

# Configura pandas para mostrar todas las columnas
pd.set_option('display.max_columns', None)

#Configura pandas para mostrar el total de todas las filas
pd.set_option('display.max_colwidth', None)

#Visualizar DataFrame
df