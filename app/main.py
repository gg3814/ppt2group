from flask import Flask
from .routes.analyze_ppt import analyze_bp
from .routes.guess_subject import guess_bp
from .routes.evalutate_level import evaluate_bp
from .routes.generate_question import generate_bp
from .routes.explain_keyword import explain_bp
import logging


app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
app.register_blueprint(analyze_bp)
app.register_blueprint(guess_bp)
app.register_blueprint(evaluate_bp)     
app.register_blueprint(generate_bp)     
app.register_blueprint(explain_bp)

logging.basicConfig(level=logging.INFO, format="[{asctime}] {levelname} in {module}: {message}", style="{")

@app.route("/")
def index():
    return app.send_static_file("index.html")

if __name__ == "__main__":
    app.run(debug=True)

