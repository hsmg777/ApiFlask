# controllers/observer_pattern.py

from abc import ABC, abstractmethod
from extensions import socketio  # Importar socketio desde extensions
from flask_socketio import emit

class Observer(ABC):
    @abstractmethod
    def update(self, order_data):
        """Método que se llama cuando ocurre la notificación."""
        pass

class Subject:
    def __init__(self):
        self._observers = []

    def attach(self, observer: Observer):
        """Suscribir un nuevo observador."""
        self._observers.append(observer)

    def detach(self, observer: Observer):
        """Dar de baja a un observador."""
        self._observers.remove(observer)

    def notify(self, order_data):
        """Notificar a todos los observadores suscritos."""
        for observer in self._observers:
            observer.update(order_data)

# -----------------------
# Observador concreto
# -----------------------
class ChefObserver(Observer):
    """
    Observador que simula a un chef.
    Envía notificaciones en tiempo real a través de SocketIO.
    """
    def __init__(self):
        # No es necesario pasar la aplicación, ya que socketio está disponible globalmente
        pass

    def update(self, order_data):
        """Llega notificación de que se creó una nueva Orden."""
        mensaje = {
            "id_orden": order_data['id_orden'],
            "id_plato": order_data['id_plato'],
            "plato_nombre": order_data.get('Plato', 'N/A'),  # Asumiendo que 'Plato' está en order_data
            "cantidad": order_data.get('cantidad', 1)
        }
        # Emitir evento a todos los clientes conectados en el namespace '/chef_notifications'
        socketio.emit('new_order', mensaje, namespace='/chef_notifications')
        print(f"Chef: ¡Nueva orden enviada via SocketIO! ID Orden={mensaje['id_orden']}, Plato={mensaje['plato_nombre']}")

# Manejadores de eventos para el namespace '/chef_notifications'
@socketio.on('connect', namespace='/chef_notifications')
def handle_connect():
    print('Cliente conectado al namespace /chef_notifications')

@socketio.on('disconnect', namespace='/chef_notifications')
def handle_disconnect():
    print('Cliente desconectado del namespace /chef_notifications')
