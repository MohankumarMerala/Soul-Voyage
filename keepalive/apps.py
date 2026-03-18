
from django.apps import AppConfig

class KeepaliveConfig(AppConfig):
    name = "keepalive"

    def ready(self):
        import threading
        from .pinger import start_pinger
        t = threading.Thread(target=start_pinger, daemon=True)
        t.start()
        print("[keepalive] Self-ping started.")
