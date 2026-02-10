import socket
import threading
from settings import UDP_TRANSMIT_PORT, UDP_RECEIVE_PORT, UDP_BROADCAST_ADDRESS, UDP_BUFFER_SIZE


class NetworkManager:
    def __init__(self, root):
        self.root = root
        self._broadcast_addr = UDP_BROADCAST_ADDRESS
        self._callback = None
        self._running = False
        self._thread = None

        # Transmit socket — sends to equipment/traffic generator on port 7500
        self._tx_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # Receive socket — binds to port 7501 to get events from equipment
        self._rx_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._rx_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._rx_sock.settimeout(1.0)
        self._rx_sock.bind(("0.0.0.0", UDP_RECEIVE_PORT))

    def set_broadcast_address(self, addr):
        self._broadcast_addr = addr

    def transmit(self, code):
        try:
            message = str(code).encode("utf-8")
            self._tx_sock.sendto(message, (self._broadcast_addr, UDP_TRANSMIT_PORT))
        except Exception as e:
            print(f"Transmit error: {e}")

    def start_receiving(self, callback):
        self._callback = callback
        self._running = True
        self._thread = threading.Thread(target=self._receive_loop, daemon=True)
        self._thread.start()

    def stop_receiving(self):
        self._running = False
        if self._thread:
            self._thread.join(timeout=2)
            self._thread = None

    def _receive_loop(self):
        while self._running:
            try:
                data, addr = self._rx_sock.recvfrom(UDP_BUFFER_SIZE)
                message = data.decode("utf-8").strip()
                if ":" in message:
                    parts = message.split(":")
                    tx_id = int(parts[0])
                    hit_id = int(parts[1])
                    if self._callback:
                        self.root.after(0, self._callback, tx_id, hit_id)
            except socket.timeout:
                continue
            except Exception as e:
                if self._running:
                    print(f"Receive error: {e}")

    def shutdown(self):
        self.stop_receiving()
        try:
            self._tx_sock.close()
        except Exception:
            pass
        try:
            self._rx_sock.close()
        except Exception:
            pass
