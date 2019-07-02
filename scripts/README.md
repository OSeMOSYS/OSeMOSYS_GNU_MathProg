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
