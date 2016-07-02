import logging

class BitcoinServerCallback:

    def __init__(self, client, request):
        self._client = client
        self._request = request

    def check_request(self):
        return True

    async def make_query(self):
        return response(None, [])

    async def query(self):
        if not self.check_request():
            logging.error("Bad parameters specified: %s", exc, exc_info=True)
            return None
        return await self.make_query()

    @property
    def _request_id(self):
        return self._request["id"]
    @property
    def _params(self):
        return self._request["params"]

    def response(self, ec, result):
        if ec is not None:
            result = []
        return {
            "id": self._request_id,
            "error": ec,
            "result": result
        }

class BsFetchLastHeight(BitcoinServerCallback):

    def check_request(self):
        return len(self._params) == 0

    async def make_query(self):
        ec, height = await self._client.last_height()
        return self.response(ec, [height])

class BitcoinServerModule:

    _handlers = {
        "fetch_last_height":                BsFetchLastHeight
    }

    def __init__(self, client):
        self._client = client

    @property
    def commands(self):
        return self._handlers.keys()

    async def handle(self, request):
        command = request["command"]
        assert command in self.commands

        handler = self._handlers[command](self._client, request)
        return await handler.query()

