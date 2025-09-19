from flask import Flask
from .routes.analyze import analyze_bp
from .routes.mode import mode_bp
from .routes.explain import explain_bp
from .routes.download import download_bp
import logging


app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
app.register_blueprint(analyze_bp)
app.register_blueprint(mode_bp)     
app.register_blueprint(explain_bp)
app.register_blueprint(download_bp)

logging.basicConfig(level=logging.INFO, format="[{asctime}] {levelname} in {module}: {message}", style="{")

@app.route("/")
def index():
    return app.send_static_file("index.html")

if __name__ == "__main__":
    app.run(debug=True)

