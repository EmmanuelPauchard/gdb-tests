# Template application for GDB unit tests

## Goal
Demonstrate how to use gdb to perform unit tests in an embedded program.

> Note: the Makefile provided here only generates a host application, because it is easier to set up the test. But the real point (and usefulness) of this technique is when used with embdedded software.

## Idea
This example will illustrate how to write a unit test of a simple conversion function `divide_and_round_to_nearest_int`, defined in file `gdb_test_example.c`. The function divides the input by 10 and rounds to the nearest integer (for 0.5, it rounds upward). We will test this function in particular in the high range (UINT32_MAX).

The technique relies on the following components:
* A Python test script (in this example, using pytest framework) implements a unit test the test by providing 
* gdb loads the python test script and executes the commands in the target (or on the host, it works the same)

## Usage
### Pre-requisite
* gdb with python support [optionnaly, for the example, with pytest and pytest-html packages installed in the python distribution used by gdb]
* make
* gcc

### Command line
```shell
$ make
$ gdb -q ./gdbtestapp.axf -x launch_test.py
Reading symbols from ./gdbtestapp.axf...
============================= test session starts ==============================
platform linux -- Python 3.8.10, pytest-6.2.5, py-1.10.0, pluggy-1.0.0
rootdir: /home/epauchard/projects/perso/gdb-tests
plugins: allure-pytest-2.9.43, html-3.1.1, metadata-1.11.0
collected 259 items

test_conversion.py ..................................................... [ 20%]
........................................................................ [ 48%]
........................................................................ [ 76%]
...........................................................FF.           [100%]

=================================== FAILURES ===================================
_________________ test_divide_and_round[4294967295-429496730] __________________

gdb_setup = None, input = 4294967295, expected_value = 429496730

    @pytest.mark.parametrize(
        "input, expected_value",
        [(a, divide_and_round_to_nearest_int(a, 10)) for a in range(2**8)] +
        [(2**32-1, divide_and_round_to_nearest_int(2**32-1, 10))] +
        [(2**32-5, divide_and_round_to_nearest_int(2**32-5, 10))] +
        [(2**32-10, divide_and_round_to_nearest_int(2**32-10, 10))]
    )
    def test_divide_and_round(gdb_setup, input, expected_value):
        """Unit-test: divide_and_round_to_nearest_int. Call it on the whole
        range and compare with a reference python implementation.
        """
        result = gdb.parse_and_eval("divide_and_round_to_nearest_int({}, 10)".format(input))
>       assert int(result) == expected_value
E       assert 0 == 429496730
E        +  where 0 = int(<gdb.Value object at 0x7fec2617ac30>)

test_conversion.py:40: AssertionError
_________________ test_divide_and_round[4294967291-429496729] __________________

gdb_setup = None, input = 4294967291, expected_value = 429496729

    @pytest.mark.parametrize(
        "input, expected_value",
        [(a, divide_and_round_to_nearest_int(a, 10)) for a in range(2**8)] +
        [(2**32-1, divide_and_round_to_nearest_int(2**32-1, 10))] +
        [(2**32-5, divide_and_round_to_nearest_int(2**32-5, 10))] +
        [(2**32-10, divide_and_round_to_nearest_int(2**32-10, 10))]
    )
    def test_divide_and_round(gdb_setup, input, expected_value):
        """Unit-test: divide_and_round_to_nearest_int. Call it on the whole
        range and compare with a reference python implementation.
        """
        result = gdb.parse_and_eval("divide_and_round_to_nearest_int({}, 10)".format(input))
>       assert int(result) == expected_value
E       assert 0 == 429496729
E        +  where 0 = int(<gdb.Value object at 0x7fec2617a030>)

test_conversion.py:40: AssertionError
- generated html file: file:///home/epauchard/projects/perso/gdb-tests/out.html -
=========================== short test summary info ============================
FAILED test_conversion.py::test_divide_and_round[4294967295-429496730] - asse...
FAILED test_conversion.py::test_divide_and_round[4294967291-429496729] - asse...
======================== 2 failed, 257 passed in 2.76s =========================
A debugging session is active.

	Inferior 1 [process 2176] will be killed.

Quit anyway? (y or n) [answered Y; input not from terminal]

```

## Conclusions
We have seen that we could write tests in Python and even with pytest and run the tests with gdb on a debugged target (local or remote).
This very simple test example detected the overflow that the function is inevitably causing by the rounding in this implementation.

## How to perform this test on an embedded device?
* Set the variable `GDB` to "remote" in file `test_conversion.py`
* Start a gdb-server connected to your target debug interface, and update `target remote localhost:2331` in file `test_conversion.py` to match your configuration
* Make sure the symbol is not inlined or pruned in your executable (in the example, I am using gcc attributes `used` and `noinline`.
* Load the executable on your target
* Start gdb with the same command line as detailed in the previous section; Make sure the gdb program you use matches your target architecture, or use `gdb-multiarch`
* You will notice the test is longer:
```shell
$ gdb-multiarch -q ./empty.axf -x launch_test.py 
Reading symbols from ./empty.axf...
============================= test session starts ==============================
platform linux -- Python 3.8.10, pytest-6.2.5, py-1.10.0, pluggy-1.0.0
rootdir: /home/epauchard/projects/perso/gdb-tests
plugins: allure-pytest-2.9.43, html-3.1.1, metadata-1.11.0
collected 259 items

test_conversion.py ..................................................... [ 20%]
........................................................................ [ 48%]
........................................................................ [ 76%]
...........................................................FFF           [100%]

=================================== FAILURES ===================================
_________________ test_divide_and_round[4294967295-429496730] __________________

gdb_setup = None, input = 4294967295, expected_value = 429496730

    @pytest.mark.parametrize(
        "input, expected_value",
        [(a, divide_and_round_to_nearest_int(a, 10)) for a in range(2**8)] +
        [(2**32-1, divide_and_round_to_nearest_int(2**32-1, 10))] +
        [(2**32-5, divide_and_round_to_nearest_int(2**32-5, 10))] +
        [(2**32-10, divide_and_round_to_nearest_int(2**32-10, 10))]
    )
    def test_divide_and_round(gdb_setup, input, expected_value):
        """Unit-test: divide_and_round_to_nearest_int. Call it on the whole
        range and compare with a reference python implementation.
        """
        result = gdb.parse_and_eval("divide_and_round_to_nearest_int({}, 10)".format(input))
>       assert int(result) == expected_value
E       assert 0 == 429496730
E        +  where 0 = int(<gdb.Value object at 0x7f5f04b8ecf0>)

test_conversion.py:40: AssertionError
_________________ test_divide_and_round[4294967291-429496729] __________________

gdb_setup = None, input = 4294967291, expected_value = 429496729

    @pytest.mark.parametrize(
        "input, expected_value",
        [(a, divide_and_round_to_nearest_int(a, 10)) for a in range(2**8)] +
        [(2**32-1, divide_and_round_to_nearest_int(2**32-1, 10))] +
        [(2**32-5, divide_and_round_to_nearest_int(2**32-5, 10))] +
        [(2**32-10, divide_and_round_to_nearest_int(2**32-10, 10))]
    )
    def test_divide_and_round(gdb_setup, input, expected_value):
        """Unit-test: divide_and_round_to_nearest_int. Call it on the whole
        range and compare with a reference python implementation.
        """
        result = gdb.parse_and_eval("divide_and_round_to_nearest_int({}, 10)".format(input))
>       assert int(result) == expected_value
E       assert 0 == 429496729
E        +  where 0 = int(<gdb.Value object at 0x7f5f04b8e8b0>)

test_conversion.py:40: AssertionError
_________________ test_divide_and_round[4294967286-429496729] __________________

gdb_setup = None, input = 4294967286, expected_value = 429496729

    @pytest.mark.parametrize(
        "input, expected_value",
        [(a, divide_and_round_to_nearest_int(a, 10)) for a in range(2**8)] +
        [(2**32-1, divide_and_round_to_nearest_int(2**32-1, 10))] +
        [(2**32-5, divide_and_round_to_nearest_int(2**32-5, 10))] +
        [(2**32-10, divide_and_round_to_nearest_int(2**32-10, 10))]
    )
    def test_divide_and_round(gdb_setup, input, expected_value):
        """Unit-test: divide_and_round_to_nearest_int. Call it on the whole
        range and compare with a reference python implementation.
        """
        result = gdb.parse_and_eval("divide_and_round_to_nearest_int({}, 10)".format(input))
>       assert int(result) == expected_value
E       assert 0 == 429496729
E        +  where 0 = int(<gdb.Value object at 0x7f5f04bb9970>)

test_conversion.py:40: AssertionError
- generated html file: file:///home/epauchard/projects/perso/gdb-tests/out.html -
=========================== short test summary info ============================
FAILED test_conversion.py::test_divide_and_round[4294967295-429496730] - asse...
FAILED test_conversion.py::test_divide_and_round[4294967291-429496729] - asse...
FAILED test_conversion.py::test_divide_and_round[4294967286-429496729] - asse...
======================== 3 failed, 256 passed in 15.90s ========================
A debugging session is active.

	Inferior 1 [Remote target] will be killed.

Quit anyway? (y or n) [answered Y; input not from terminal]
```
