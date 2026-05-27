import psutil

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


print(obtener_ram_global())