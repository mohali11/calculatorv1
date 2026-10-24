import math

from flask import Flask, jsonify, render_template, request

from calculator import add, divide, multiply, subtract

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True

OPERATIONS = {
    "add": add,
    "subtract": subtract,
    "multiply": multiply,
    "divide": divide,
}


def is_finite_number(value):
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return False
    try:
        return math.isfinite(value)
    except OverflowError:
        return False


@app.get("/")
def index():
    return render_template("index.html")


@app.post("/api/calculate")
def calculate():
    payload = request.get_json(silent=True)
    if not isinstance(payload, dict):
        return jsonify(ok=False, error="Send a JSON body with operation, a, and b."), 400

    operation = payload.get("operation")
    a = payload.get("a")
    b = payload.get("b")

    if operation not in OPERATIONS:
        return jsonify(ok=False, error="Choose add, subtract, multiply, or divide."), 400
    if not is_finite_number(a) or not is_finite_number(b):
        return jsonify(ok=False, error="Both values must be finite numbers."), 400
    if operation == "divide" and b == 0:
        return (
            jsonify(ok=False, error="You can't divide by zero. Choose a non-zero divisor."),
            400,
        )

    result = OPERATIONS[operation](a, b)
    if not is_finite_number(result):
        return jsonify(ok=False, error="That result is too large to display."), 400
    return jsonify(ok=True, result=result)


if __name__ == "__main__":
    app.run(port=5001)
