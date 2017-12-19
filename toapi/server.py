from signal import signal, SIGINT, SIGTERM
from time import time

from colorama import Fore
from flask import Flask, request, jsonify, logging

from toapi.log import logger


class Server:
    def __init__(self, api, settings):
        app = Flask(__name__)
        app.logger.setLevel(logging.ERROR)
        self.app = app
        self.api = api
        self.settings = settings

    def init_route(self):
        app = self.app
        api = self.api

        @app.route('/')
        def index():
            base_url = "{}://{}".format(request.scheme, request.host)
            basic_info = {
                "cache": "{}/{}".format(base_url, "cache"),
                "items": "{}/{}".format(base_url, "items"),
                "status": "{}/{}".format(base_url, "status"),
                "storage": "{}/{}".format(base_url, "storage")
            }
            return jsonify(basic_info)

        @app.route('/status')
        def status():
            status = {
                'cache_set': api.get_status('_status_cache_set'),
                'cache_get': api.get_status('_status_cache_get'),
                'storage_set': api.get_status('_status_storage_set'),
                'storage_get': api.get_status('_status_storage_get'),
                'sent': api.get_status('_status_sent'),
                'received': api.get_status('_status_received')
            }
            return jsonify(status)

        @app.route('/items/')
        def items():
            result = {
                item.__name__: "{}://{}/{}".format(request.scheme, request.host, item.__base_url__ + item.Meta.route)
                for item in api.item_classes
            }
            res = jsonify(result)
            return res

        @app.errorhandler(404)
        def page_not_found(error):
            start_time = time()
            path = request.full_path
            if path.endswith('?'):
                path = path[:-1]
            try:
                result = api.get_cache(path) or api.parse(path)
                if result is None:
                    logger.error('Received', '%s 404' % request.url)
                    return 'Not Found', 404
                api.set_cache(path, result)
                res = jsonify(result)
                api.update_status('_status_received')
                end_time = time()
                time_usage = end_time - start_time
                logger.info(Fore.GREEN, 'Received',
                            '%s %s 200 %.2fms' % (request.url, len(res.response), time_usage * 1000))

                return res
            except Exception as e:
                return str(e)

    def run(self, ip='127.0.0.1', port=5000, **options):
        """Runs the application"""

        for _signal in [SIGINT, SIGTERM]:
            signal(_signal, self.stop)

        self.app.run(ip, port, **options)

    def stop(self, signal, frame):
        logger.info(Fore.WHITE, 'Server', 'Server Stopped')
        exit()
