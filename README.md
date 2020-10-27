Mars Rover
===========

The requirements can be found at [Google Code](https://code.google.com/archive/p/marsrovertechchallenge/)

Those requirements mention some sample test input, that is placed in the file "test_input.txt".

To run the Mars Rover program
-----------------------------
Pass the rover commands to standard input:

    python3 rover.py < test_input.txt

The program writes the output to standard output.

Tests
-----

There are some unit tests that use pytest, you can run them like this:

    python3 -m pytest

There are some component tests written with TextTest on the branch 'with_texttests'
