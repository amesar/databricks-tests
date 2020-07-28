import os
import sys

if __name__ == "__main__":
    import pytest
    args = [ arg.replace("dbfs:","/dbfs") for arg in sys.argv[1:] ]
    print("run_tests: args:",args)
    errcode = pytest.main(args)
    print("run_tests: errcode:",errcode)
    if errcode != 0:
        sys.exit(errcode)
    #sys.exit(0) # causes failure
