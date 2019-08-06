import os
import pytest

from subprocess import run

def get_folder():
    return os.path.dirname(os.path.abspath(__file__))

class Test_RunMathProg():

    def test_mathprog_run_normal(self):

        model_file = os.path.join(get_folder(), '../src/osemosys.txt')
        data_file = os.path.join(get_folder(), 'utopia.txt')

        arguments = ['glpsol', '-m', model_file, '-d', 
                     data_file, '-o', './results.csv']
        output = run(arguments, capture_output=True, text=True)
        assert 'OPTIMAL LP SOLUTION FOUND' in output.stdout
        assert 'obj =   2.944686269e+04' in output.stdout


    def test_mathprog_run_short(self):

        model_file = os.path.join(get_folder(), '../src/osemosys_short.txt')
        data_file = os.path.join(get_folder(), 'utopia.txt')

        arguments = ['glpsol', '-m', model_file, '-d', 
                     data_file, '-o', './results_short.csv']
        output = run(arguments, capture_output=True, text=True)
        assert 'OPTIMAL LP SOLUTION FOUND' in output.stdout
        assert 'obj =   2.944686269e+04' in output.stdout