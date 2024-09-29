# TikTok Automation Script

Este es un script de automatización que utiliza Pyppeteer para interactuar con TikTok. Permite iniciar sesión en TikTok, buscar un usuario, seguirlo, dar "me gusta" a sus videos y realizar comentarios predefinidos.

## Requisitos

Antes de ejecutar el script, asegúrate de tener lo siguiente instalado:

- Python 3.x
- Pyppeteer (`pip install pyppeteer`)
- asyncio (viene preinstalado con Python 3.7+)
- Archivos JSON con la información de los usuarios y los comentarios.

## Instalación

1. Clona el repositorio:

   ```bash
   git clone https://github.com/tu_usuario/tu_repositorio.git
   ```
   ```bash
   cd tu_repositorio
   ```

2. Instala las dependencias necesarias:
```bash
pip install pyppeteer
```

3. Crea los archivos JSON de usuarios y comentarios ejecutando el script. Los archivos se generan automáticamente si no existen.

```bash
python TikTok-followers.py
```

Uso

1. Modifica el archivo tiktok_users.json con tus credenciales de usuario TikTok:

```bash
{
    "users": [
        {"username": "your_tiktok_username", "password": "your_password"}
    ]
}
```

2. Modifica el archivo comments.json con los comentarios que quieres que se publiquen:

```bash
{
    "comments": [
        "Buen video",
        "Eres el mejor",
        "Sigue así"
    ]
}
```

3. Ejecuta el script:

```bash
python script.py
```
Se te pedirá que ingreses el nombre del usuario que deseas buscar en TikTok.



# Funcionalidades

**Iniciar sesión en TikTok: Usa las credenciales proporcionadas en el archivo tiktok_users.json.**

**Buscar un usuario: Busca el nombre de usuario que ingreses cuando se te solicite.**

**Seguir al usuario: Sigue al usuario encontrado.**

**Interactuar con videos: Da "me gusta" a los videos del usuario.**

**Comentar en videos: Publica comentarios aleatorios de una lista predefinida en el archivo comments.json.**


# Archivos JSON

tiktok_users.json: Contiene las credenciales de inicio de sesión de los usuarios de TikTok.

comments.json: Contiene los comentarios que el script puede publicar en los videos de TikTok.


Ambos archivos se crean automáticamente si no existen. Asegúrate de editarlos con la información adecuada.

# Advertencia

Este script está destinado únicamente a fines educativos. El uso no autorizado de bots o scripts de automatización en plataformas como TikTok puede violar sus políticas de uso. Usa este script bajo tu propia responsabilidad.

#Contribuciones

Si tienes sugerencias o mejoras, no dudes en hacer un fork del proyecto y enviar un pull request.

# Developer

**Developer:** @Gh0stDeveloper
**Channel:** @TEAM_CHICO_CP