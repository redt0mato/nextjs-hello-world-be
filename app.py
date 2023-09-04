from flask import Flask, render_template, stream_with_context, Response
from flask_cors import CORS
import time
import random
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration
import logging

logger = logging.getLogger()


app = Flask(__name__)
CORS(app)

# TO explore SQL Alchemy integration
sentry_sdk.init(
    dsn="https://fb0dc63fe1f3f95b79cf3aefbed5577d@o4505585277206528.ingest.sentry.io/4505710071840768",
    integrations=[
        FlaskIntegration(),
    ],
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production.s
    send_default_pii=True,  # TO-DO check with Lei and Marc about sending cookie information
    environment="STAGING",
    traces_sample_rate=1.0,
)
app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/events")
def sse():
    def event_stream():
        yield "data: Start\n\n"
        time.sleep(random.randint(1, 3))

        yield "data: Processing\n\n"
        time.sleep(random.randint(1, 3))

        yield f"data: Status update: {random.randint(0, 100)}% complete\n\n"
        time.sleep(random.randint(1, 3))

        yield "data: Finished?\n\n"

        return

    return Response(event_stream(), mimetype="text/event-stream")


@app.route("/debug-sentry")
def trigger_error():
    logger.info("About to run a function...")
    division_by_zero = 1 / 0


if __name__ == "__main__":
    app.run(debug=True, threaded=True)
