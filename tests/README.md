# Python unit test framework - Unittest

## How to run

### Run all tests

```bash
python3 -m unittest
```

### Run a specific test file

```bash
python3 -m unittest -v test_state.py
```

Runs the `test_state.py` test file with verbose output.4

### Run a specific test case

```bash
python3 -m unittest -v test_state.TestGameState.test_init
```

Runs the `test_init` test case in the `TestGameState` test class in the `test_state.py` test file with verbose output.
