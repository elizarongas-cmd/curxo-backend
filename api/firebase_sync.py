import json
import urllib.request
from datetime import datetime


FIREBASE_CONFIG = {
    "project_id": "academia-curxo-26-47c4e",
    "api_key": "AIzaSyDummy-REEMPLAZA_CON_TU_API_KEY"
}


def sync_to_firestore(collection_name, data):
    """
    Sincroniza datos de Django a Firebase Firestore
    """
    try:
        url = f"https://firestore.googleapis.com/v1/projects/{FIREBASE_CONFIG['project_id']}/databases/(default)/documents/{collection_name}"
        
        payload = json.dumps({
            "fields": {k: {"stringValue": str(v)} for k, v in data.items()}
        }).encode('utf-8')
        
        req = urllib.request.Request(
            url,
            data=payload,
            headers={
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {get_firebase_token()}'
            }
        )
        
        with urllib.request.urlopen(req, timeout=10) as response:
            return json.loads(response.read().decode())
            
    except Exception as e:
        print(f"Firebase sync error: {e}")
        return None


def get_firebase_token():
    """
    Obtiene token de autenticacion de Firebase
    En produccion, usar service account credentials
    """
    return "placeholder-token-replace-with-service-account"


def sync_alumnos_to_firestore(alumnos):
    """
    Sincroniza la lista de alumnos a Firestore
    """
    for alumno in alumnos:
        data = {
            'nombre': alumno.get('nombre', ''),
            'grupo': alumno.get('grupo', ''),
            'estado': alumno.get('estado', ''),
            'fecha_registro': str(datetime.now()),
            'sincronizado_desde': 'django-local'
        }
        sync_to_firestore('alumnos_backup', data)


def sync_mensajes_to_firestore(mensajes):
    """
    Sincroniza mensajes del chat a Firestore
    """
    for mensaje in mensajes:
        data = {
            'autor': mensaje.get('autor', ''),
            'contenido': mensaje.get('contenido', ''),
            'tipo': mensaje.get('tipo', ''),
            'timestamp': str(datetime.now()),
            'sincronizado_desde': 'django-local'
        }
        sync_to_firestore('mensajes_backup', data)


def backup_all_to_firestore():
    """
    Funcion principal de backup completo
    """
    from api.models import Alumno, MensajeChat
    
    alumnos = list(Alumno.objects.all().values())
    mensajes = list(MensajeChat.objects.all().values())
    
    sync_alumnos_to_firestore(alumnos)
    sync_mensajes_to_firestore(mensajes)
    
    return {
        'alumnos_sync': len(alumnos),
        'mensajes_sync': len(mensajes),
        'timestamp': str(datetime.now())
    }
