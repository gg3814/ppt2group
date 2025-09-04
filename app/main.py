from flask import Flask
from routes import analyze 
# subject, level, explain, result, feedback

app = Flask(__name__)

app.register_blueprint(analyze.bp)
# app.register_blueprint(subject.bp)
# app.register_blueprint(level.bp)
# app.register_blueprint(explain.bp)
# app.register_blueprint(result.bp)
# app.register_blueprint(feedback.bp)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
