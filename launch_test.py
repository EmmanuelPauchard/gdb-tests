import pytest
import gdb


pytest.main(["--noconftest", "test_conversion.py", "--html=out.html"])
gdb.execute("quit")
