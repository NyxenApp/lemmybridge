import os

from flask import Flask

from routes import bp

app = Flask(__name__)
app.register_blueprint(bp)


def main():
    host = os.environ.get("HOST", "0.0.0.0")
    port = int(os.environ.get("PORT", "8080"))
    app.run(host=host, port=port)


if __name__ == "__main__":
    main()
