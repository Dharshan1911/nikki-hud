import psutil

def get_stats():
    return {
        "cpu": psutil.cpu_percent(interval=0.1),
        "ram": round(
            psutil.virtual_memory().used / (1024 ** 3),
            1
        ),
        "ram_percent": psutil.virtual_memory().percent
    }
