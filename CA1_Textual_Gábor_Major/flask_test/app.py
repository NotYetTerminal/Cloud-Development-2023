from flask import Flask


app: Flask = Flask(__name__)


@app.get("/")
@app.get("/hello")
def hello() -> str:
    return "Hello from my first app!"


if __name__ == "__main__":
    app.run()
