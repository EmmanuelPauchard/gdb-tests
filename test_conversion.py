import pytest
import gdb
import decimal

decimal.getcontext().rounding = decimal.ROUND_HALF_UP

GDB = "local"
#GDB = "remote"


def divide_and_round_to_nearest_int(number, divisor):
    """Reference implementation of the tested function
    """
    return int((decimal.Decimal(number) / decimal.Decimal(divisor)).to_integral())


@pytest.fixture(scope="session")
def gdb_setup():
    global GDB
    gdb.Breakpoint("main")
    if GDB == "remote":
        gdb.execute("target remote localhost:2331")
        gdb.execute("monitor reset")
    else:
        gdb.execute("run")


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
    assert int(result) == expected_value
