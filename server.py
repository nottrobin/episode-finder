#!/usr/bin/env python

import subprocess
import os
import re
from werkzeug.wrappers import Request, Response

def application(environ, start_response):
    request = Request(environ)
    query = request.args.get('q', '')

    rss_response = subprocess.check_output(
        ['./episode-finder.py', query]
    )

    response = Response(rss_response, mimetype='application/rss+xml')
    return response(environ, start_response)

if __name__ == '__main__':
    from werkzeug.serving import run_simple
    run_simple('0.0.0.0', 8111, application, use_debugger=True, use_reloader=True)

