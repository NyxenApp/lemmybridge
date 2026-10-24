import argparse
import asyncio
import os
import shutil
import subprocess
import sys

from mitmproxy import http
from mitmproxy.options import Options
from mitmproxy.tools.dump import DumpMaster


class BridgeAddon:
    def __init__(self, bridge_host, bridge_port):
        self.bridge_host = bridge_host
        self.bridge_port = bridge_port

    def request(self, flow):
        host = flow.request.pretty_host
        path = flow.request.path
        should_redirect = (
            "reddit.com" in host
            and (
                path.startswith("/subreddits/popular")
                or path in ("/", "/.json", "/hot", "/hot.json")
                or path.startswith("/r/all")
                or path.startswith("/r/popular")
            )
        )
        if should_redirect:
            flow.request.scheme = "http"
            flow.request.host = self.bridge_host
            flow.request.port = self.bridge_port
            print(f"Redirected {host}{path} -> {self.bridge_host}:{self.bridge_port}{path}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--process", default=None)
    parser.add_argument("--bridge-host", default="127.0.0.1")
    parser.add_argument("--bridge-port", type=int, default=8080)
    parser.add_argument("--proxy-port", type=int, default=8081)
    args = parser.parse_args()

    proxy_url = f"http://127.0.0.1:{args.proxy_port}"

    if args.process:
        executable = shutil.which(args.process)
        if executable is None:
            print(f"Could not find executable for {args.process}")
            print("Launch it manually and set HTTP_PROXY/HTTPS_PROXY to " + proxy_url)
        else:
            env = os.environ.copy()
            env["HTTP_PROXY"] = proxy_url
            env["HTTPS_PROXY"] = proxy_url
            env["http_proxy"] = proxy_url
            env["https_proxy"] = proxy_url
            subprocess.Popen([executable], env=env)
            print(f"Launched {args.process} with proxy {proxy_url}")

    print(f"Starting mitmproxy on {proxy_url}")
    print("Install the mitmproxy CA certificate if HTTPS interception is needed")

    options = Options(listen_host="127.0.0.1", listen_port=args.proxy_port)
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    master = DumpMaster(options, loop=loop, with_termlog=True)
    master.addons.add(BridgeAddon(args.bridge_host, args.bridge_port))

    try:
        loop.run_until_complete(master.run())
    except KeyboardInterrupt:
        pass
    except Exception as exc:
        print(f"mitmproxy error: {exc}")
        sys.exit(1)
    finally:
        loop.close()


if __name__ == "__main__":
    main()
