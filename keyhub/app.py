import argparse
import logging


def setup_options(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--daemon', dest='daemon', action='store_true',
                        help='run keyhub in daemon mode')
    parser.add_argument('-p', '--port', dest='port', default=5000,
                        metavar='int', type=int)
    parser.add_argument('-H', '--host', dest='host', default='127.0.0.1')
    parser.add_argument('--debug', dest='debug', action='store_true')

    return parser.parse_args(argv)


def run_daemon(opts):
    log = logging.getLogger("daemon")
    log.info("Loading db...")
    from keyhub.rest.models import db
    log.info("done")

    log.info("Loading REST API...")
    from keyhub.rest.controller import api
    log.info("done")

    log.info("Loading WSGI app...")
    from keyhub.wsgi import app
    log.info("done")
    app.run(port=opts.port, host=opts.host, debug=opts.debug)


def main(argv=None):
    opts = setup_options()
    if opts.daemon:
        run_daemon(opts)
