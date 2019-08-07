import os
from pytest import fixture

from subprocess import run

def get_folder():
    return os.path.dirname(os.path.abspath(__file__))

@fixture(scope='session')
def model_file():
    return os.path.join(get_folder(), '../src/osemosys.txt')

@fixture(scope='session')
def short_model_file():
    return os.path.join(get_folder(), '../src/osemosys_short.txt')

@fixture(scope='session')
def data_file():
    return os.path.join(get_folder(), 'utopia.txt')

@fixture(scope="session")
def results_folder(tmp_path_factory):
    path = tmp_path_factory.mktemp("results")
    fn = os.path.join(str(path),'results.csv')
    return fn

@fixture(scope="session")
def lp_folder(tmp_path_factory):
    path = tmp_path_factory.mktemp("model")
    fn = os.path.join(str(path),'model.lp')
    return fn

def check_results(path, variable):
    """Extracts a variable name from the GLPK results output

    Arguments
    ---------
    path : str
        File path to the results file
    variable : str
        Row name for which to extract information

    Returns
    -------
    dict
        A dictionary with the header names as keys and extracted row values
    """
    value = None

    header = ["No.", "Row name", "St", "Activity", 
              "Lower bound", "Upper bound", "Marginal"]

    with open(path, 'r') as results_file:
        for line in results_file:
            if variable in line:
                value = line + next(results_file)

    if value:
        return dict(zip(header, value.split()))
    else:
        raise ValueError("No row found with variable name {}".format(variable))

class TestNormalWithCBC():

    @fixture(scope='function')
    def run_model_cbc(self, model_file, data_file, lp_folder, results_folder):
        arguments = ['glpsol', '-m', model_file, '-d', 
                     data_file, '--wlp', lp_folder, '--check']
        run(arguments)
        arguments = ['cbc', lp_folder, 'solve', '-solu', results_folder]
        output = run(arguments)      
        return output, results_folder   

    def test_run_model_with_cbc(self, run_model_cbc):
        _, results_folder = run_model_cbc
        assert os.path.exists(results_folder)
        with open(results_folder, 'r') as solution_file:
            line = next(solution_file)
            assert 'Optimal - objective value 29446.86269434' in line

class TestNormal():

    @fixture(scope='function')
    def run_model(self, model_file, data_file, results_folder):
        arguments = ['glpsol', '-m', model_file, '-d', 
                     data_file, '-o', results_folder]
        output = run(arguments, capture_output=True, text=True)
        return output, results_folder

    def test_mathprog_run_normal(self, run_model):

        output, results_folder = run_model
        assert 'OPTIMAL LP SOLUTION FOUND' in output.stdout
        assert 'obj =   2.944686269e+04' in output.stdout

    def test_results_exist(self, run_model):
        _, results_folder = run_model
        assert os.path.exists(results_folder)

    def test_results_read(self, run_model):
        _, results_folder = run_model

        actual = check_results(results_folder, 'CAa1_TotalNewCapacity[UTOPIA,E01,1990]')
        assert actual['Activity'] == '0'
        assert actual['Marginal'] == '39.036'


class TestShort():

    def test_mathprog_run_short(self, short_model_file, data_file, results_folder):

        arguments = ['glpsol', '-m', short_model_file, '-d', 
                     data_file, '-o', results_folder]
        output = run(arguments, capture_output=True, text=True)
        assert 'OPTIMAL LP SOLUTION FOUND' in output.stdout
        assert 'obj =   2.944686269e+04' in output.stdout