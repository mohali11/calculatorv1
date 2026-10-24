# Apex Calc

A small Flask calculator web app. The math lives in calculator.py and the web app in app.py serves a calculator page and a JSON API at /api/calculate.

## Run

```
pip install -r requirements.txt
python app.py
```

The app runs on port 5001. Open http://127.0.0.1:5001 in a browser.

## API

POST /api/calculate with a JSON body:

```
{"operation": "add", "a": 12, "b": 8}
```

Operation can be add, subtract, multiply, or divide. The response is JSON with ok and result, or ok false with an error message.

## Tests

```
pytest
```
