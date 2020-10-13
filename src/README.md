# OSeMOSYS GNU MathProg

Thanks for using OSeMOSYS and welcome to the OSeMOSYS community.

## Installation

To use OSeMOSYS, you'll need to install the 
[GNU Linear Programming Kit](https://www.gnu.org/software/glpk/).

The easiest way to do this is to use Anaconda or Miniconda.

### 1. Install conda package manager

First, install [miniconda](https://docs.conda.io/en/latest/miniconda.html#) by following
the instructions [here](https://conda.io/projects/conda/en/latest/user-guide/install/#).

### 2. Create a new environment

Run the following commands to create and activate a new environment containing the `glpk` library:

    conda create -n osemosys python=3.8 glpk
    conda activate osemosys

### 3. Optional - install **otoole** for pre- and post- processing

First, activate the conda environment and then install otoole::

    conda activate osemosys
    pip install otoole

### 4. Optional - install CBC or CLP open-source solvers

On Linux or OSX you can also install the more powerful CBC or CLP
open-source solvers using conda:

    conda install -c conda-forge coincbc coin-or-clp

## Running OSeMOSYS

If you've followed the instructions above using conda, before running OSeMOSYS you'll
need to activate your conda environment:

    conda activate osemosys

To run OSeMOSYS, first navigate to the folder containing your OSeMOSYS files, and enter the following line into your command prompt:

    glpsol -m osemosys.txt -d  simplicity.txt

The results from the model run should be available in the `results` folder.

## Where to get help

### Forum

The [Google Groups OSeMOSYS forum](https://groups.google.com/u/1/g/osemosys) 
contains a large number of questions and answers and is useful and active
source of information for how to use OSeMOSYS and tackle all sorts of
OSeMOSYS modelling issues.

### Github Issues

The OSeMOSYS source code and issue tracker are located on [Github](https://github.com/OSeMOSYS/OSeMOSYS_GNU_MathProg).

If you think you have identified a bug, or want to suggest an enhancement, please log an issue 
[here](https://github.com/OSeMOSYS/OSeMOSYS_GNU_MathProg/issues/new/choose).

### Training materials

- [Understanding the Energy System Lecture Slides](http://www.osemosys.org/understanding-the-energy-system.html) 
by OSeMOSYS Team
- [OSeMOSYS Video Lectures](https://www.youtube.com/watch?v=U9Z4GE_l9mQ&list=PLY5NLA2BTufKU_wDSp-JzP6dhpzwsg1Xx) by OSeMOSYS Team

### OSeMOSYS website

The OSeMOSYS website at [osemosys.org](http://osemosys.org) contains a lot of useful information.

### Newsletter

Sign up for a monthly OSeMOSYS [newsletter](http://www.osemosys.org/news-and-events.html).
