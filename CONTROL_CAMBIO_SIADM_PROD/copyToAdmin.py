import os
import shutil
from extractRar import *
from loadCredentialsPaths import load_paths


# Ruta al archivo de rutas
paths_path = 'C:\\Users\\mapinedad\\Documents\\work_scripts\\PYTHON\\CONTROL_CAMBIO_SIADM_PROD\\paths\\paths.json'

# Cargar rutas
paths = load_paths(paths_path)

# Ruta al directorio donde se encuentra la carpeta extraída
# extracted_directory = r"C:\Users\mapinedad\Documents\KENTRON\CONTROL_CAMBIO\extracted"
extracted_path = paths['extracted_directory']

# Ruta al directorio de administración
# admin_path = r"C:\Users\mapinedad\Documents\KENTRON\ADMIN"
admin_path = paths['admin_directory']


def copyToAdmin():

    # Extraer el rar
    print(f"Ejecutando la extracción del archivo rar...")
    extractRAR()
    print(f"Terminó correctamente la ejecución...")

    # Obtener la lista de carpetas extraídas en el directorio
    extracted_folders = [f for f in os.listdir(extracted_path) if os.path.isdir(os.path.join(extracted_path, f))]
    
    print (extracted_folders)
    # Iterar sobre cada carpeta extraída encontrada
    for folder in extracted_folders:
        # Obtener el nombre de la carpeta sin la parte de la fecha (si existe)
        folder_name = folder.split('_')[0]
        print(folder_name)

        # Solo copiar carpetas cuyo nombre comience con "$ACT"
        if folder_name.startswith("$ACT"):
            # Ruta completa de la carpeta extraída
            source_folder = os.path.join(extracted_path, folder)
            
            # Ruta completa de destino en el directorio de administración
            destination_folder = os.path.join(admin_path, folder_name)
            
            print(source_folder, '\n', destination_folder)
            # Si la carpeta de destino ya existe, eliminarla
            if os.path.exists(destination_folder):
                shutil.rmtree(destination_folder)
            
            # Copiar la carpeta extraída al directorio de administración
            shutil.copytree(source_folder, destination_folder)
            print(f"Copiada la carpeta {folder_name} al directorio de ADMIN.")
            
            # Eliminar la carpeta del directorio de extracción
            shutil.rmtree(source_folder)
            print(f"Eliminada la carpeta {folder} del directorio de extracción.")
        else:
            print(f"Carpeta {folder_name} no cumple con el criterio y no será copiada.")


if __name__ == "__main__":
    copyToAdmin()