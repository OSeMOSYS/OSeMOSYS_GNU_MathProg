# Scripts

A collection of useful scripts for running the GNU MathProg implementation of
OSeMOSYS

## cplex_batchRun.bat

This batch script is for running multiple runs in Windows using GNU MathProg
and CPLEX. Place all files together with the batch file, and make sure to change
the naming to your text files and OSeMOSyS version.

To run: just double click the batch file and it will execute.

## kth_hpc_cplex_batchrun.sh

Acknowledgment to Jing Gong at PDC center @ KTH for rewriting the script for Tegner.
This batch script is for running one run for GNU MathProg and CPLEX on High Performance Comupter using SLURM commands
and Linux operating system (such as Tegner @ KTH).
Place all files together with the batch file, and make sure to change the naming
to your text files and OSeMOSyS version.
To run on HPC Tegner @ KTH write: `sbatch kth_hpc_cplex_batchrun.sh`
and it will queue the file and run it.

## convert_cplex_to_cbc.py

This script converts the solution file output of a OSeMOSYS run with the CPLEX
solver into the same format of that produced by CBC.

This removes the zeros, and moves closer to a tidy format that is generally
preferable (sparser and more transferable).

To run use the command `python convert_cplex_to_cbc.py cplex_file output_file`

Use the `-h` or `--help` flag to get the full set of options:

```python
$ python convert_cplex_to_cbc.py --help
usage: convert_cplex_to_cbc.py [-h] [-s START_YEAR] [-e END_YEAR]
                               [--csv | --cbc]
                               cplex_file output_file

Convert OSeMOSYS CPLEX files into different formats

positional arguments:
  cplex_file            The filepath of the OSeMOSYS cplex output file
  output_file           The filepath of the converted file that will be
                        written

optional arguments:
  -h, --help            show this help message and exit
  -s START_YEAR, --start_year START_YEAR
                        Output only the results from this year onwards
  -e END_YEAR, --end_year END_YEAR
                        Output only the results upto and including this year
  --csv                 Output file in comma-separated-values format
  --cbc                 Output file in CBC format, (default option)
```
