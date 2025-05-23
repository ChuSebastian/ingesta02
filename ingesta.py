import pymysql
import csv
import os
import boto3

# Parámetros de conexión a MySQL
db_host = "172.31.94.222"
db_user = "root"
db_password = "utec"
db_name = "test_db"
db_port = 8005

# Nombre del archivo CSV y bucket S3
ficheroUpload = "data.csv"
nombreBucket = "scl-output-02"

# Conexión a la base de datos y extracción de datos
connection = pymysql.connect(
    host=db_host,
    user=db_user,
    password=db_password,
    database=db_name,
    port=db_port
)

with connection.cursor() as cursor:
    cursor.execute("SELECT id, name, lastname, age FROM personas")
    rows = cursor.fetchall()

# Guardar en CSV
with open(ficheroUpload, "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["id", "name", "lastname", "age"])
    writer.writerows(rows)

# Verificar e imprimir contenido del CSV
if os.path.exists(ficheroUpload):
    print(f"Archivo CSV '{ficheroUpload}' creado. Contenido:")
    with open(ficheroUpload, "r") as f:
        print(f.read())

    # Subir a S3
    print("Subiendo archivo a S3...")
    s3 = boto3.client('s3')
    s3.upload_file(ficheroUpload, nombreBucket, ficheroUpload)
    print("Ingesta completada y archivo subido a S3.")

else:
    print("Error: No se pudo crear el archivo CSV.")
