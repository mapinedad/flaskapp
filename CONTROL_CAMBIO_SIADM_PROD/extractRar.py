import os
import shutil
import subprocess
from loadCredentialsPaths import load_paths


# Ruta al archivo de rutas
paths_path = 'C:\\Users\\mapinedad\\Documents\\work_scripts\\PYTHON\\CONTROL_CAMBIO_SIADM_PROD\\paths\\paths.json'

# Cargar rutas
paths = load_paths(paths_path)

# Ruta al ejecutable 7z
seven_zip_executable = r"C:\Program Files\7-Zip\7z.exe"

# Ruta al directorio donde se encuentran los archivos .rar
# rar_directory = r"C:\Users\mapinedad\Documents\KENTRON\CONTROL_CAMBIO"
rar_path = paths['rar_directory']

# Directorio de salida donde se extraerán los archivos
# output_directory = r"C:\Users\mapinedad\Documents\KENTRON\CONTROL_CAMBIO\extracted"
output_directory = paths['extracted_directory']

# Ruta al directorio de administración
# admin_path = r"C:\Users\mapinedad\Documents\KENTRON\ADMIN"
admin_path = paths['admin_directory']


def extractRAR():
    # Obtener la lista de archivos .rar en el directorio
    rar_files = [f for f in os.listdir(rar_path) if f.endswith('.rar')]
    
    # Verificar si hay archivos .rar en la ruta
    if not rar_files:
        print("No se encontró ningún archivo .rar en la ruta especificada.")
        return
    else:
        # Iterar sobre cada archivo .rar encontrado
        for rar_file in rar_files:
            # Obtener el nombre del archivo .rar sin la extensión
            rar_name = os.path.splitext(rar_file)[0]
            
            # Extraer la parte del nombre del archivo antes de la fecha (si existe)
            folder_name = rar_name.split('_')[0]

            # Comando para descomprimir el archivo .rar usando 7-Zip
            command = [seven_zip_executable, "x", os.path.join(rar_path, rar_file), f"-o{output_directory}", "-y"]
            
            # Ejecutar el comando
            subprocess.run(command, check=True)

            # Ruta completa del directorio extraído
            extracted_folder = os.path.join(output_directory, folder_name)
            
            # Verificar si el directorio extraído existe
            if os.path.exists(extracted_folder):
                # Copiar el directorio extraído al directorio de administración
                shutil.copytree(extracted_folder, os.path.join(admin_path, folder_name))
                print(f"Copiada la carpeta {folder_name} al directorio de administración.")
            else:
                print(f"No se encontró el directorio extraído para el archivo {rar_file}.")

if __name__ == "__main__":
    extractRAR()
