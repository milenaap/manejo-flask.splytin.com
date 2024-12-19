import requests

url = "https://discord.com/api/webhooks/1319318553677004810/Yb7QE6vfM6BTjzTXs93e4LVxz4IRan2WT95yQiHBPdajkHuusZHsF6Ld047GY5hO1DWz"


def send(text, title='Title', is_error = False):


    ##title += env('APP_NAME') + ' ' + env('APP_ENV')

    embed = {
        'title': title,
        'description': text,
        'color': 0xFF0000 if is_error else 0x00FF00  ## Red: Green
    }

    payload = {
        'embeds': [embed]
    }

    try:
        response = requests.post(url, json=payload, headers={
            'Content-Type': 'application/json'
        })

        # Verificar respuesta
        if response.status_code != 204:
            print(f"Error al enviar mensaje: {response.status_code} - {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"Error: {str(e)}")



# Ejemplo de uso
send("Este es un mensaje de prueba", "Prueba", is_error=False)