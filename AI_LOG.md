# Apex Calc — AI Interaction Log

## Interaction 1: Project Setup

- **Prompt:** "Create a Python file called [calculator.py](http://calculator.py) with four functions: add, subtract, multiply, and divide. Keep it simple, one file, no extra features."

- **Agent Output:** The agent created [calculator.py](http://calculator.py) with all four functions, each taking two numbers and returning the result.

- **My Review:** I read every function before running anything. The math was right, but divide had no protection against dividing by zero yet.

- **Result:** Accepted. I planned the divide fix as the next step instead of asking for everything at once.

## Interaction 2: Error Handling

- **Prompt:** "In [calculator.py](http://calculator.py), change divide so that if b is zero it prints an error message and returns None instead of crashing. Do not change the other functions."

- **Agent Output:** The agent added a zero check at the top of divide that prints "Error: cannot divide by zero." and returns None.

- **My Review:** I ran divide with zero and with normal numbers to check both paths. The normal results did not change.

- **Result:** Accepted.

## Interaction 3: Testing (SCOPE prompt)

- **Prompt:** "Specific: write pytest tests for [calculator.py](http://calculator.py) in one new file, test_[calculator.py](http://calculator.py), covering add, subtract, multiply, and divide with positive numbers, negative numbers, and zero, plus a test that divide by zero returns None and prints the error message. Constrained: create only test_[calculator.py](http://calculator.py) and change nothing else. Observable: run pytest at the end and show me the result with every test passing. Progressive: write the tests first, then run them, then fix only the tests if a test itself is wrong. Explicit: this is a Python/Flask project using pytest, and the functions live in [calculator.py](http://calculator.py)."

- **Agent Output:** The agent wrote parametrized tests, one set per function, plus a test that captures the printed error message for divide by zero.

- **My Review:** I checked that the tests assert the real return values, not just that the functions run. Weak tests that always pass would not prove anything.

- **Result:** Accepted.

## Interaction 4: Core Feature, the Flask App

- **Prompt:** "Create [app.py](http://app.py), a Flask app for this calculator. GET / serves templates/index.html. POST /api/calculate takes JSON with operation, a, and b, uses the functions from [calculator.py](http://calculator.py), and returns the result as JSON. Reject bad input with a 400 error: unknown operation, values that are not finite numbers, booleans, and divide by zero. Also write tests for the app in test_[app.py](http://app.py)."

- **Agent Output:** The agent built the app with an operations dictionary, an input check function, and JSON error responses. The tests cover valid operations, divide by zero, invalid operations, string input, a boolean input, an infinite value, and a result that overflows.

- **My Review:** I read the validation code line by line. One detail I checked on purpose was the boolean case, because True counts as a number in Python and had to be rejected on its own. I also checked that divide by zero in the API returns an error instead of the None path from [calculator.py](http://calculator.py).

- **Result:** Accepted.

## Interaction 5: Bug Found in Review, Missing Template

- **Prompt:** "Run the full test suite for the whole project and show me every failure before we push to GitHub."

- **Agent Output:** 32 tests passed and 1 failed. The failing test was the index page test, with a TemplateNotFound error for index.html.

- **My Review:** The failure was a real project bug, not a bad test. The app pointed at templates/index.html and that file had never been created. I caught it because the tests ran before the push, not after.

- **Result:** Modified. The index page was created with the Apex Calc branding and the calculator element the test checks for. I ran the full suite again and all 33 tests passed.

## Interaction 6: Documentation

- **Prompt:** "Write a [README.md](http://README.md) for Apex Calc explaining what the project does, how to install and run it, the API format with an example, and how to run the tests."

- **Agent Output:** The agent wrote a README with setup steps, a run command, a JSON example for /api/calculate, and the pytest command.

- **My Review:** I checked the details against the real project. The port in the README matches the port in [app.py](http://app.py), and the API example matches what the endpoint actually accepts.

- **Result:** Accepted.

# Submission form answers

## 1. My most effective prompt and why it worked

My most effective prompt was the SCOPE testing prompt in Interaction 3. It worked because it named the exact file, required specific test cases, limited the scope of the change, required a visible pytest result, and gave the agent a clear order of steps.

## 2. The hardest part of directing the agent, and what I would do differently next time

The hardest part was directing the agent to handle edge cases without changing unrelated files, especially division by zero and the missing template. Next time, I would run the full test suite earlier and ask the agent to verify every required file before moving on.

## 3. How my understanding of AI agents changed

At first I thought an agent was just a chatbot that returned code. Now I see it as a tool I must direct, constrain, and verify: I give it a scoped task, inspect the files and tests, run pytest, and revise anything the evidence does not support.
