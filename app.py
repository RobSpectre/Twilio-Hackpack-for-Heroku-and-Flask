import os
import signal

from hackpack.app import app


def graceful_shutdown(signum, frame):
    exit()

# Restarts Dyno gracefully so there is no error on shutdown.
signal.signal(signal.SIGTERM, graceful_shutdown)

# If PORT not specified by environment, assume development config.
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    if port == 5000:
        app.debug = True
    app.run(host='0.0.0.0', port=port)
