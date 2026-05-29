import psutil
import os

def obtener_ram_global():
    mem =psutil.virtual_memory()
    #psutil devuelve los valores en bytes, se divide para obtener los GB
    gb_const = 1024**3 

    #Guardado en un diccionario para mejorar acceso con JavaScript

    datos_ram = { 
        "total_gb" : round(mem.total / gb_const, 2),
        "usado_gb" : round(mem.used / gb_const, 2),
        "porcentaje_uso": mem.percent,
        "cache_gb" : round(getattr(mem, 'cached', 0) / gb_const, 2)
    }
    return datos_ram



def obtener_ssd(ruta = 'C:\\'):
    #Si se usa linux o mac, cambias la ruta por /
    try:
        disco = psutil.disk_usage(ruta)
        gb_const = 1024 **3

        datos_ssd = {
            "total_gb" : round(disco.total / gb_const, 2),
            "usado_gb" : round(disco.used / gb_const, 2),
            "libre_gb" : round(disco.free / gb_const, 2 ),
            "porcentaje_uso" : disco.percent

        }
        return datos_ssd
    except FileNotFoundError:
        return {"error": "La ruta especificada no existe."}

def listar_apps_ram():
    procesos = []

    for proc in psutil.process_iter(['pid', 'name', 'memory_info', 'memory_percent']):
        try:
            info = proc.info
            uso_mb = round(info['memory_info'].rss / (1024 **2), 2)
            if uso_mb > 0: #Modificar para mostrar a partir de cuantos MB se desea mostrar
                procesos.append({
                    "pid": info['pid'],
                    "app": info['name'],
                    "ram_usada_mb": uso_mb,
                    "porcentaje": round(info['memory_percent'], 2)
                })
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    procesos_ordenados = sorted(procesos, key=lambda x: x['ram_usada_mb'], reverse = True)

    return procesos_ordenados




# Para poder listar las apps dentro del SSD o disco duro se necesitan permisos de administrador para
#ciertas aplicaciones, por lo que a menos de que sea muy necesario no se extraera por el momento
def obtener_tamano_carpeta(ruta_base):
    tamano_total = 0
    # Recorremos la carpeta y subcarpetas sumando el tamaño de cada archivo
    try:
        for directorio_raiz, carpetas, archivos in os.walk(ruta_base):
            for archivo in archivos:
                ruta_archivo = os.path.join(directorio_raiz, archivo)
                # Omitimos accesos directos y archivos protegidos para evitar errores
                if not os.path.islink(ruta_archivo) and os.path.exists(ruta_archivo):
                    tamano_total += os.path.getsize(ruta_archivo)
    except (PermissionError, FileNotFoundError):
        pass # Ignoramos carpetas del sistema a las que no tenemos acceso como usuarios normales
        
    return tamano_total

def desglosar_almacenamiento_ssd(): #SE TARDA MUCHISIMOOOOO
    gb_const = 1024 ** 3
    usuario = os.getlogin() 
    
    #Sistema Operativo (Carpeta Windows)
    sistema_gb = obtener_tamano_carpeta('C:\\Windows') / gb_const
    
    #Aplicaciones Instaladas (Archivos de Programa)
    apps_gb = (obtener_tamano_carpeta('C:\\Program Files') + 
               obtener_tamano_carpeta('C:\\Program Files (x86)')) / gb_const
    
    #Multimedia (Videos, Imágenes, Música del usuario)
    rutas_multimedia = [
        f'C:\\Users\\{usuario}\\Videos',
        f'C:\\Users\\{usuario}\\Pictures',
        f'C:\\Users\\{usuario}\\Music'
    ]
    multimedia_gb = sum(obtener_tamano_carpeta(ruta) for ruta in rutas_multimedia) / gb_const
    
    return {
        "sistema_gb": round(sistema_gb, 2),
        "aplicaciones_gb": round(apps_gb, 2),
        "multimedia_gb": round(multimedia_gb, 2)
    }

#desglose = desglosar_almacenamiento_ssd()
#Se tarda mucho en buscar las aplicaciones, se buscara una mejor forma o se descartará

#print("--- DESGLOSE DEL DISCO ---")
#print(f"Sistema: {desglose['sistema_gb']} GB")
#print(f"Apps: {desglose['aplicaciones_gb']} GB")
#print(f"Multimedia: {desglose['multimedia_gb']} GB")


apps_ram = listar_apps_ram()
    


print(obtener_ram_global())
print(obtener_ssd())