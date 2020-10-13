# OSeMOSYS GNU MathProg

Thanks for using OSeMOSYS and welcome to the OSeMOSYS community.

To run OSeMOSYS, enter the following line into your command prompt and
data file name:

    glpsol -m osemosys.txt -d  ../Training_Case_Studies/utopia.txt -o results.csv

Alternatively, install GUSEK (http://gusek.sourceforge.net/gusek.html)
and run the model within this integrated development environment (IDE).
To do so, open the datafile (e.g. `utopia.txt`) and
select "Use External .dat file" from the Options menu.
Then change to the model file and select the "Go" icon or press F5.

## Developers - Testing

This repository uses Travis CI to run regression tests and
harmonisation tests across each of the OSeMOSYS GNU MathProg normal and short
implementations.

Each push to a branch on the repository, or submission of a pull
request triggers a build on Travis CI, with the corresponding status reported
back in the pull request comments.

The tests must pass before a pull request may be merged into the main
repository.

Tests are defined using the Python package ``pytest`` and the runs are
configured within the Travis CI configuration file ``.travis.yml``.

The tests are stored in the ``tests`` folder.

### Running the tests

To run the tests on your local computer, you need a Python 3.7 installation.
The easiest way to install this is using
[miniconda](https://docs.conda.io/en/latest/miniconda.html).

Then you need to install pytest `conda install pytest pandas` and can then run the tests
using the command `pytest`.

Each of the tests in the `tests` folder runs an OSeMOSYS model file and checks that
the output matches a given value.