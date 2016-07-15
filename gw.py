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

        # [main]
        main = config["main"]
        # Give precedence to command line over config file.
        self.port = self._args.port
        if self.port is None:
            self.port = int(main.get("port", 8888))

        # [bs]
        bs = config["bs"]
        self.bs_url = bs.get("url", "tcp://gateway.unsystem.net:9091")
        self.bs_query_expire_time = int(bs.get("query-expire-time", 200))

        # [txradar]
        txradar = config["txradar"]
        self.txradar_url = txradar.get("url", "tcp://localhost:7678")
        self.txradar_watch_expire_time = \
            int(txradar.get("watch-expire-time", 200))
        self.txradar_cleanup_timeout = int(txradar.get("cleanup-timeout", 200))

        # [p2p]
        p2p = config["p2p"]
        self.p2p_port = int(p2p.get("p2p-port", 8889))
        self.external_ip = p2p.get("external-ip", "85.25.198.211")
        self.internal_ip = p2p.get("internal-ip", "192.168.1.10")
        self.seeds = p2p.get("seeds", "tcp://85.25.198.213:8889")
        self.seeds = [seed.strip() for seed in self.seeds.split(",")]

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

