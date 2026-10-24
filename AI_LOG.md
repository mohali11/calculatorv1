# Apex Calc — AI Interaction Log

This log is grounded in the files currently in the repository: `calculator.py`, `app.py`, `test_calculator.py`, `test_app.py`, `templates/index.html`, `requirements.txt`, and `README.md`.

## Interaction 1 — Project setup and calculator functions

### Prompt
Set up the core of Apex Calc as a small Python calculator project. Keep the arithmetic in `calculator.py` and implement only the four operations needed by the app: `add`, `subtract`, `multiply`, and `divide`. Include short docstrings, and list the packages needed to run the Flask app and its pytest tests.

### Agent Output
Created `calculator.py` with four functions:

- `add(a, b)` returns `a + b`.
- `subtract(a, b)` returns `a - b`.
- `multiply(a, b)` returns `a * b`.
- `divide(a, b)` returns `a / b` for a non-zero divisor and has a separate zero-divisor behavior.

The project dependencies are recorded in `requirements.txt` as `flask` and `pytest`.

### My Review
I checked that `calculator.py` contains exactly the four imported operations and that each function returns the corresponding arithmetic expression. I also checked `requirements.txt` for both `flask` and `pytest`, rather than assuming the dependencies were present.

### Result
**accepted** — the module is small, the arithmetic is separated from the web layer, and the listed dependencies match the application and test files.

## Interaction 2 — Divide-by-zero handling

### Prompt
Handle division by zero without allowing the calculator to perform an invalid division. Keep the behavior clear in the calculator function, and make the Flask API return a client error with a helpful message when the divide operation receives `b` equal to zero.

### Agent Output
`divide(a, b)` checks `b == 0`, prints `Error: cannot divide by zero.`, and returns `None`. In `app.py`, the `/api/calculate` route checks for a zero divisor before calling the operation and returns status `400` with the JSON error `You can't divide by zero. Choose a non-zero divisor.`

### My Review
I checked the `b == 0` branch in `calculator.py` and the `capsys` assertion in `test_calculator.py::test_divide_by_zero_returns_none`. I also checked `test_app.py::test_divide_by_zero_returns_a_helpful_error` to confirm that the API response is `400`, has `ok` set to `False`, and includes the word `zero` in the error.

### Result
**accepted** — both the direct function and the API have explicit, tested zero-divisor behavior.

## Interaction 3 — Writing the calculator tests with a SCOPE prompt

### Prompt
Use this SCOPE prompt:

- **S — Specific cases listed:** In `test_calculator.py`, add pytest parameterized cases for `add`: `(2, 3) -> 5`, `(-2, -3) -> -5`, `(-2, 3) -> 1`, and `(0, 0) -> 0`; for `subtract`: `(5, 3) -> 2`, `(-5, -3) -> -2`, `(-5, 3) -> -8`, and `(0, 0) -> 0`; for `multiply`: `(2, 3) -> 6`, `(-2, 3) -> -6`, `(-2, -3) -> 6`, and `(0, 5) -> 0`; and for `divide`: `(10, 2) -> 5`, `(-10, 2) -> -5`, `(-10, -2) -> 5`, and `(0, 5) -> 0`. Also test division by zero for a `None` return and the printed error.
- **C — Constrained to one file:** Change only `test_calculator.py`; do not edit `calculator.py`, `app.py`, `test_app.py`, `README.md`, or `templates/index.html`.
- **O — Observable result:** Run `pytest test_calculator.py` and show the result, including the number of tests that passed.
- **P — Progressive steps in order:** First inspect the existing functions, then write the parameterized tests, then add the zero-divisor test, then run pytest, then report the result.
- **E — Explicit about the stack:** Use Python and pytest in this Flask project; do not introduce another testing framework.

### Agent Output
Added parameterized tests for the four functions in `test_calculator.py` and a `capsys` test for division by zero. Running `pytest test_calculator.py -q` produced `17 passed`.

### My Review
I checked the actual parameter lists in `test_calculator.py`, including negative values and zero cases, and checked that `test_divide_by_zero_returns_none` asserts both `result is None` and the printed error text. I also checked that the test file imports the functions from `calculator.py` and that no Flask route is being used for these unit tests.

### Result
**accepted** — the prompt limited the work to one file, the cases are observable, and the unit-test command passes.

## Interaction 4 — Flask app and the `/api/calculate` endpoint

### Prompt
Build the Flask layer around the existing calculator functions. Serve the existing calculator page at `/`, and add `POST /api/calculate` that accepts JSON with `operation`, `a`, and `b`. Use the four existing operations, return JSON with `ok` and `result` for valid input, and return status `400` with `ok: false` for invalid input, division by zero, or a result that cannot be displayed as a finite number.

### Agent Output
`app.py` creates a Flask app, maps the four operation names to the functions from `calculator.py`, renders `templates/index.html` at `/`, and implements `POST /api/calculate`. The endpoint rejects missing or non-object JSON, unknown operations, booleans and non-numeric values, non-finite numbers, division by zero, and non-finite results. Successful responses use `{"ok": true, "result": ...}`; errors use `{"ok": false, "error": ...}` and status `400`.

### My Review
I checked the `OPERATIONS` mapping in `app.py` against the four options in `templates/index.html`. I also checked the parametrized success cases and the invalid-request cases in `test_app.py`, plus `test_index_serves_the_calculator_ui`, which verifies that `/` returns `200` and contains `Apex` and `id="calculator"`.

### Result
**accepted** — the route, response shapes, validation, and page serving are all represented in the repository tests.

## Interaction 5 — Review caught an incomplete numeric validation case

### Prompt
Review the API validation against the edge-case tests before treating it as complete. In particular, verify that a very large Python integer does not crash `math.isfinite`, that boolean values are not accepted as numbers, and that an arithmetic overflow is returned as a `400` JSON error. Fix the implementation if it handles only a floating-point infinity case.

### Agent Output
The review identified that `math.isfinite(10**400)` can raise `OverflowError` instead of returning `False`. The numeric helper in `app.py` now rejects booleans and non-number types, calls `math.isfinite` inside a `try` block, and returns `False` on `OverflowError`. The endpoint also checks the operation result so multiplication such as `1e308 * 1e308` produces the existing “too large to display” error instead of an infinite JSON result.

### My Review
I checked `test_rejects_a_number_too_large_for_a_float` and `test_rejects_a_result_that_overflows` in `test_app.py`, not just the ordinary success cases. I also checked the `except OverflowError` branch and the `is_finite_number(result)` check in `app.py`; these checks show that the fix covers both an oversized input and an oversized result.

### Result
**modified** — the first validation approach was incomplete for a huge integer; after the review fix, the implementation matches the edge-case tests.

## Interaction 6 — Documentation and README

### Prompt
Write documentation for only the behavior present in the repository. Explain how to install the dependencies, run the Flask app, open it, call `POST /api/calculate`, and run the tests. List only the four supported operation names and the actual port used by `app.py`.

### Agent Output
`README.md` documents Apex Calc as a Flask calculator, identifies `calculator.py` and `app.py`, gives the `pip install -r requirements.txt`, `python app.py`, and `pytest` commands, records port `5001`, and shows a JSON example for `POST /api/calculate`. It lists `add`, `subtract`, `multiply`, and `divide`, and describes the success and error response shapes.

### My Review
I checked the README commands against `requirements.txt` and `app.py`, including the `app.run(port=5001)` setting. I also compared the API example and the four operation names with the `calculate` route and the operation selector in `templates/index.html`.

### Result
**accepted** — the README describes the checked-in setup, endpoints, operations, and test command without adding unsupported features.

# Submission form answers

## 1. My most effective prompt and why it worked

My most effective prompt was the SCOPE test prompt in Interaction 3. It worked because it listed exact cases, limited the change to one file, required a visible pytest result, gave the steps in order, and named the Python, Flask, and pytest stack.

## 2. The hardest part of directing the agent, and what I would do differently next time

The hardest part was directing the agent to handle edge cases without changing unrelated files, especially division by zero and very large numeric inputs. Next time, I would state the file boundary and exact test command earlier and ask for a failure-path review before accepting the implementation.

## 3. How my understanding of AI agents changed

At first I thought an agent was just a chatbot that returned code. Now I see it as a tool I must direct, constrain, and verify: I give it a scoped task, inspect the files and tests, run pytest, and revise anything the evidence does not support.
