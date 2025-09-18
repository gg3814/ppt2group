from flask import Flask
from .routes.analyze import analyze_bp
from .routes.subject import subject_bp
from .routes.level import level_bp
from .routes.explain import explain_bp
from .routes.mode import mode_bp
from .routes.download import download_bp

app = Flask(__name__, static_folder="static")
app.config['JSON_AS_ASCII'] = False

app.register_blueprint(analyze_bp)
app.register_blueprint(subject_bp)
app.register_blueprint(level_bp)
app.register_blueprint(explain_bp)
app.register_blueprint(mode_bp)
app.register_blueprint(download_bp)

@app.route("/")
def index():
    return app.send_static_file("index.html")

if __name__ == "__main__":
    app.run(debug=True)
