import urllib.request
import tarfile
import os
import shutil

def download_mobilenet_pb():
    """Descarga el archivo mobilenet_graph.pb"""
    
    print("Descargando MobileNet v1...")
    
    # URL del modelo MobileNet v1
    url = "https://storage.googleapis.com/download.tensorflow.org/models/mobilenet_v1_2018_02_22/mobilenet_v1_1.0_224.tgz"
    filename = "mobilenet_v1.tgz"
    
    try:
        # Descargar el archivo
        print("Descargando archivo...")
        urllib.request.urlretrieve(url, filename)
        print(f"Archivo descargado: {filename}")
        
        # Extraer el contenido
        print("Extrayendo archivos...")
        with tarfile.open(filename, 'r:gz') as tar:
            tar.extractall()
        
        # Buscar el archivo .pb
        pb_files = []
        for root, dirs, files in os.walk('.'):
            for file in files:
                if file.endswith('.pb'):
                    pb_files.append(os.path.join(root, file))
        
        print("Archivos .pb encontrados:")
        for pb_file in pb_files:
            print(f"- {pb_file}")
        
        # Copiar el archivo principal como mobilenet_graph.pb
        if pb_files:
            main_pb = None
            for pb_file in pb_files:
                if 'frozen' in pb_file.lower():
                    main_pb = pb_file
                    break
            
            if main_pb is None:
                main_pb = pb_files[0]  # Tomar el primero si no hay 'frozen'
            
            # Copiar con el nombre esperado
            shutil.copy2(main_pb, 'mobilenet_graph.pb')
            print(f"Archivo copiado como: mobilenet_graph.pb")
            print(f"Tamaño: {os.path.getsize('mobilenet_graph.pb') / (1024*1024):.1f} MB")
        
        # Limpiar archivos temporales
        if os.path.exists(filename):
            os.remove(filename)
        
        # Limpiar directorios extraídos
        for item in os.listdir('.'):
            if os.path.isdir(item) and 'mobilenet' in item.lower():
                shutil.rmtree(item)
        
        return True
        
    except Exception as e:
        print(f"Error durante la descarga: {e}")
        return False

def verify_pb_file():
    """Verifica que el archivo .pb sea válido"""
    if not os.path.exists('mobilenet_graph.pb'):
        print("El archivo mobilenet_graph.pb no existe")
        return False
    
    try:
        import tensorflow as tf
        
        # Intentar cargar el grafo para verificar
        with tf.io.gfile.GFile('mobilenet_graph.pb', 'rb') as f:
            graph_def = tf.compat.v1.GraphDef()
            graph_def.ParseFromString(f.read())
        
        print("Archivo mobilenet_graph.pb verificado correctamente")
        print(f"Número de nodos en el grafo: {len(graph_def.node)}")
        return True
        
    except Exception as e:
        print(f"Error al verificar el archivo: {e}")
        return False

# Ejecutar la descarga
if __name__ == "__main__":
    print("=== DESCARGA DE MOBILENET ===")
    
    # Verificar si ya existe
    if os.path.exists('mobilenet_graph.pb'):
        print("El archivo mobilenet_graph.pb ya existe")
        if verify_pb_file():
            print("El archivo está listo para usar")
        else:
            print("El archivo existe pero parece estar corrupto")
            download_mobilenet_pb()
    else:
        print("Descargando MobileNet...")
        if download_mobilenet_pb():
            verify_pb_file()
        else:
            print("Error en la descarga")
    
    print("\n=== ARCHIVOS EN EL DIRECTORIO ===")
    for file in os.listdir('.'):
        if os.path.isfile(file):
            size = os.path.getsize(file) / (1024*1024)
            print(f"- {file} ({size:.1f} MB)")