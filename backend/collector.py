import os
from wsgiref.simple_server import WSGIServer, make_server

import prometheus_client
import prometheus_client.multiprocess
from prometheus_client import make_wsgi_app, multiprocess, start_http_server

if os.getenv("PROMETHEUS_MULTIPROC_DIR") and not os.path.exists(
    os.getenv("PROMETHEUS_MULTIPROC_DIR", "")
):
    os.makedirs(os.getenv("PROMETHEUS_MULTIPROC_DIR", ""))

registry = prometheus_client.CollectorRegistry()
multiprocess.MultiProcessCollector(registry)

app = make_wsgi_app(registry)
httpd = make_server("0.0.0.0", 7999, app, WSGIServer)

httpd.serve_forever()
