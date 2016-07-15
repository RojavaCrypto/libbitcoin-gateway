import logging
import time
import zmq
import libbitcoin

def hash_transaction(raw_tx):
    return libbitcoin.bitcoin_hash(raw_tx)[::-1]

class RadarInterface:

    def __init__(self, context, settings, loop):
        self._monitored = {}

        # Create socket
        self._socket = context.zmq_context.socket(zmq.SUB)
        self._socket.connect(settings.txradar_url)
        self._socket.setsockopt(zmq.SUBSCRIBE, b"")
        loop.spawn_callback(self._listen)

        self._loop = loop
        self._expire_time = settings.txradar_expire_time
        self._cleanup_timeout = settings.txradar_cleanup_timeout
        self._schedule_cleanup()

    def _schedule_cleanup(self):
        self._loop.add_timeout(self._cleanup_timeout, self._clean_old)

    async def _listen(self):
        while True:
            _, tx_hash = await self._socket.recv_multipart()
            if tx_hash in self._monitored:
                self._monitored[tx_hash].notify()

    async def _clean_old(self):
        time_now = time.time()
        is_expired = lambda notify: \
            notify.timestamp + self._expire_time < time_now
        # Delete expired items.
        self._monitored = {tx_hash: notify for tx_hash, notify in
                           self._monitored.items() if not is_expired(notify)}
        self._schedule_cleanup()

    def monitor(self, tx_hash, notify):
        self._monitored[tx_hash] = notify

class NotifyCallback:

    def __init__(self, connection, request_id):
        self._connection = connection
        self._request_id = request_id
        self.timestamp = time.time()
        self._count = 0

    def notify(self):
        response = {
            "id": self._request_id,
            "error": None,
            "result": [self._count, "radar"]
        }
        self._connection.queue(response)
        self._count += 1

class Broadcaster:

    commands = [
        "broadcast_transaction"
    ]

    def __init__(self, context, settings, loop, client):
        self._client = client
        self._radar = RadarInterface(context, settings, loop)

    @staticmethod
    def parse_params(request):
        if not request["params"]:
            logging.error("No param for broadcast specified.")
            return None
        try:
            raw_tx = bytes.fromhex(request["params"][0])
        except ValueError:
            logging.error("Bad parameter supplied for broadcast.")
            return None
        return raw_tx

    async def handle(self, request, connection):
        assert request["command"] in self.commands
        raw_tx = self.parse_params(request)
        if raw_tx is None:
            return None
        request_id = request["id"]
        # Prepare notifier object
        tx_hash = hash_transaction(raw_tx)
        notify = NotifyCallback(connection, request_id)
        self._radar.monitor(tx_hash, notify)
        # Add to txradar
        ec = await self._client.broadcast(raw_tx)
        # Response
        return {
            "id": request_id,
            "error": ec,
            "result": [
            ]
        }

