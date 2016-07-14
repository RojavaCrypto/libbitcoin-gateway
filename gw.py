#!/usr/bin/python3
import argparse
import configparser
import sys

import gateway

class Settings:

    def __init__(self, args):
        self._args = args

    def load(self):
        config = configparser.ConfigParser()
        config.read(self._args.config)
        main = config["main"]
        self.websocket_port = int(main.get("websocket-port", 8888))
        self.broadcaster_url = main.get("broadcaster-url",
                                        "tcp://localhost:9109")
        self.bs_url = main.get("bs-url", "tcp://gateway.unsystem.net:9091")

        # Crypto2Crypto
        self.p2p_port = int(main.get("p2p-port", 8889))
        self.external_ip = main.get("external-ip", "85.25.198.211")
        self.internal_ip = main.get("internal-ip", "192.168.1.10")
        self.seeds = main.get("seeds", "tcp://85.25.198.213:8889")
        self.seeds = [seed.strip() for seed in self.seeds.split(",")]

        # Give precedence to command line over config file.
        self.port = self._args.port
        if self.port is None:
            self.port = int(main.get("port", 8888))

def main():
    # Command line arguments
    parser = argparse.ArgumentParser(prog="gw")
    parser.add_argument("--version", "-v", action="version",
                        version="%(prog)s 2.0")
    parser.add_argument("--config", "-c", dest="config",
                        help="Change default config file.",
                        default="gateway.cfg")
    parser.add_argument("--port", "-p", dest="port",
                        help="Run on the given port.",
                        default=None)
    args = parser.parse_args()

    # Load config file settings
    settings = Settings(args)
    settings.load()

    # Start the gateway
    gateway.start(settings)
    return 0

if __name__ == "__main__":
    sys.exit(main())

