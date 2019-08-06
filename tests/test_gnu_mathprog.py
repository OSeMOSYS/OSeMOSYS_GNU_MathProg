import os
from pytest import fixture

from subprocess import run

def get_folder():
    return os.path.dirname(os.path.abspath(__file__))

@fixture(scope='module')
def model_file():
    return os.path.join(get_folder(), '../src/osemosys.txt')

@fixture(scope='module')
def short_model_file():
    return os.path.join(get_folder(), '../src/osemosys_short.txt')

@fixture(scope='module')
def data_file():
    return os.path.join(get_folder(), 'utopia.txt')

class Test_RunMathProg():

    def test_mathprog_run_normal(self, model_file, data_file):

        arguments = ['glpsol', '-m', model_file, '-d', 
                     data_file, '-o', './results.csv']
        output = run(arguments, capture_output=True, text=True)
        assert 'OPTIMAL LP SOLUTION FOUND' in output.stdout
        assert 'obj =   2.944686269e+04' in output.stdout


    def test_mathprog_run_short(self, short_model_file, data_file):

        arguments = ['glpsol', '-m', short_model_file, '-d', 
                     data_file, '-o', './results_short.csv']
        output = run(arguments, capture_output=True, text=True)
        assert 'OPTIMAL LP SOLUTION FOUND' in output.stdout
        assert 'obj =   2.944686269e+04' in output.stdout