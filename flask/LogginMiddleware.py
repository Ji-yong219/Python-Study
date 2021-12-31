class LogMiddleWare(object):
    """WSGI middleware for collecting site usage"""

    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        url = environ.get("PATH_INFO", "")

        query = unquote_plus(environ.get("QUERY_STRING", ""))

        item = logging.LogRecord(
            name="logging",
            level=logging.INFO,
            pathname=url,
            lineno="",
            msg=query,
            args=None,
            exc_info=None
        )

        metrics=logger.handle(item)
        
        return self.app(environ, start_response)