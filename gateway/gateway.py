import json
import random
import traceback
import tornado.options
import tornado.web
import tornado.websocket

import libbitcoin

# Debug stuff
import logging
logging.basicConfig(level=logging.DEBUG)

import gateway.bs_module
import gateway.subscribe_module
import gateway.brc
import gateway.legacy

def create_random_id():
    MAX_UINT32 = 4294967295
    return random.randint(0, MAX_UINT32)

class GatewayApplication(tornado.web.Application):

    def __init__(self, context, settings, loop):
        self._context = context
        self._settings = settings
        client_settings = libbitcoin.ClientSettings()
        client_settings.query_expire_time = settings.bs_query_expire_time
        self._client = self._context.Client(settings.bs_url, client_settings)
        # Setup the modules
        self.bs_module = gateway.bs_module.BitcoinServerModule(self._client)
        self.subscribe_module = gateway.subscribe_module.SubscribeModule(
            self._client, loop)
        self.brc_module = gateway.brc.Broadcaster(context, settings, loop,
                                                  self._client)
        self.legacy_module = gateway.legacy.LegacyModule(settings)

        handlers = [
            # /block/<block hash>
            #(r"/block/([^/]*)(?:/)?", rest_handlers.BlockHeaderHandler),

            # /block/<block hash>/transactions
            #(r"/block/([^/]*)/transactions(?:/)?",
            #    rest_handlers.BlockTransactionsHandler),

            # /tx/
            #(r"/tx(?:/)?", rest_handlers.TransactionPoolHandler),

            # /tx/<txid>
            #(r"/tx/([^/]*)(?:/)?", rest_handlers.TransactionHandler),

            # /address/<address>
            #(r"/address/([^/]*)(?:/)?", rest_handlers.AddressHistoryHandler),

            # /height
            #(r"/height(?:/)?", rest_handlers.HeightHandler),

            # /height
            #(r"/status(?:/)?", status.StatusHandler, {"app": self}),

            # /
            (r"/", QuerySocketHandler, {"loop": loop})
        ]

        tornado_settings = dict(debug=True)
        tornado_settings.update(tornado.options.options.as_dict())
        super().__init__(handlers, tornado_settings)

    def start_listen(self):
        print("Listening on port %s" % self._settings.port)
        self.listen(self._settings.port)

class QuerySocketHandler(tornado.websocket.WebSocketHandler):

    # Set of WebsocketHandler
    listeners = set()
    # Protects listeners
    #listen_lock = threading.Lock()

    # Accept all connections.
    def check_origin(self, origin):
        return True

    def initialize(self, loop):
        self._loop = loop
        self._bs_module = self.application.bs_module
        self._subscribe_module = self.application.subscribe_module
        self._brc_module = self.application.brc_module
        self._legacy_module = self.application.legacy_module
        #self._obelisk_handler = self.application.obelisk_handler
        #self._brc_handler = self.application.brc_handler
        #self._json_chan_handler = self.application.json_chan_handler
        #self._ticker_handler = self.application.ticker_handler
        #self._subscriptions = defaultdict(dict)
        self._connected = False
        self.connection_id = None

    def open(self):
        self.connection_id = create_random_id()
        logging.info("OPEN")
        self._connected = True
        #with QuerySocketHandler.listen_lock:
        #    self.listeners.add(self)

    def on_close(self):
        logging.info("CLOSE")
        self._connected = False
        self._loop.spawn_callback(self._close)
        #disconnect_msg = {'command': 'disconnect_client', 'id': 0, 'params': []}
        #self._obelisk_handler.handle_request(self, disconnect_msg)
        #self._json_chan_handler.handle_request(self, disconnect_msg)
        #with QuerySocketHandler.listen_lock:
        #    self.listeners.remove(self)

    async def _close(self):
        await self._subscribe_module.delete_all(self)
        self.connection_id = None

    def on_message(self, message):
        logging.info("MESSAGE")
        self._loop.spawn_callback(self._handle_message, message)

    def _check_request(self, request):
        # {
        #   "command": ...
        #   "id": ...
        #   "params": [...]
        # }
        return ("command" in request) and ("id" in request) and \
            ("params" in request and type(request["params"]) == list)

    async def _handle_message(self, message):
        try:
            request = json.loads(message)
        except:
            logging.error("Error decoding message: %s", message, exc_info=True)
            self.close()
            return

        # Check request is correctly formed.
        if not self._check_request(request):
            logging.error("Malformed request: %s", request, exc_info=True)
            self.close()
            return

        if request["command"] in self._legacy_module.commands:
            self._legacy_module.handle_request(self, request)
            return

        response = await self._handle_request(request)
        if response is None:
            self.close()
            return

        self.queue(response)

    async def _handle_request(self, request):
        if request["command"] in self._bs_module.commands:
            response = await self._bs_module.handle(request)
        elif request["command"] in self._subscribe_module.commands:
            response = await self._subscribe_module.handle(request, self)
        elif request["command"] in self._brc_module.commands:
            response = await self._brc_module.handle(request, self)
        else:
            logging.warning("Unhandled command. Dropping request: %s",
                request, exc_info=True)
            return None
        return response

    def queue(self, message):
        # Calling write_message on the socket is not thread safe
        self._loop.spawn_callback(self._send, message)

    def _send(self, message):
        try:
            self.write_message(message)
        except tornado.websocket.WebSocketClosedError:
            self._connected = False
            logging.warning("Dropping response to closed socket: %s",
                            message, exc_info=True)
        except Exception as e:
            print("Error sending:", str(e))
            traceback.print_exc()
            print("Message:", message.keys())

def start(settings):
    import zmq.asyncio
    from tornado.ioloop import IOLoop
    from tornado.platform.asyncio import AsyncIOMainLoop
    zmq.asyncio.install()
    AsyncIOMainLoop().install()
    context = libbitcoin.TornadoContext()
    loop = IOLoop.current()
    app = GatewayApplication(context, settings, loop)
    app.start_listen()
    context.start(loop)
    loop.start()

