# Running Tests

Best create a virtual environment for the tests:
```
python -m venv .test_venv
source .test_venv/bin/activate
```

Install the test-runner dependencies:
```
pip install -r tests/requirements.txt
```

Then make the `ots` python module visible/importable to the tests by installing it:
```
pip install -e .
```

Run the whole test suite:
```
pytest
```

Run a specific test file:
```
pytest tests/test_this_file.py
```

Run a specific test:
```
pytest tests/test_this_file.py::test_this_specific_test
```

Exit virtual environment:
```
deactivate
```
