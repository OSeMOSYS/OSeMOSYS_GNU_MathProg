import os
from pytest import fixture
import pandas as pd

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

@fixture(scope='session')
def results_folder(tmp_path_factory):
    path = tmp_path_factory.mktemp("test")
    os.mkdir(os.path.join(str(path), 'results'))
    return os.path.join(str(path))

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
        arguments = ['cbc', lp_folder, '-sec', '15', 'solve', '-solu', results_folder]
        output = run(arguments)
        return output, results_folder

    def test_run_model_with_cbc(self, run_model_cbc):
        _, results_folder = run_model_cbc
        assert os.path.exists(results_folder)
        with open(results_folder, 'r') as solution_file:
            line = next(solution_file)
            assert 'Optimal - objective value 29446.86269434' in line

class TestNormal():

    @fixture(scope='session')
    def run_model(self, model_file, data_file, results_folder):
        arguments = ['glpsol', '-m', model_file, '-d',
                     data_file]
        os.chdir(os.path.join(results_folder))
        output = run(arguments, capture_output=True, text=True)
        return output, os.path.join(results_folder, 'results')

    def test_mathprog_run_normal(self, run_model):

        output, results_folder = run_model
        assert 'OPTIMAL LP SOLUTION FOUND' in output.stdout
        assert 'obj =   2.944686269e+04' in output.stdout

    def test_results_exist(self, run_model):
        _, results_folder = run_model
        assert os.path.exists(str(results_folder))

    def test_results_read_accumulated_new_capacity(self, run_model):
        """
        """
        _, results_folder = run_model
        result_file = os.path.join(str(results_folder), 'AccumulatedNewCapacity.csv')
        actual = pd.read_csv(result_file)
        actual = actual[actual.YEAR == 2010].reset_index(drop=True)

        expected = pd.DataFrame(columns=['REGION','TECHNOLOGY','YEAR','VALUE'],
                                data=[['UTOPIA',        'E01',  2010,    2.279801],
                                      ['UTOPIA',        'E31',  2010,    0.110000],
                                      ['UTOPIA',    'IMPDSL1',  2010,   77.597496],
                                      ['UTOPIA',    'IMPHCO1',  2010,  191.565506],
                                      ['UTOPIA',        'RHE',  2010,   46.867723],
                                      ['UTOPIA',        'RHO',  2010,   46.135248],
                                      ['UTOPIA',        'RL1',  2010,   18.901890],
                                      ['UTOPIA',        'SRE',  2010,    0.100000],
                                      ['UTOPIA',        'TXD',  2010,   11.690000],
                                      ['UTOPIA',        'RIV',  2010,    5.587785]])

        pd.testing.assert_frame_equal(actual, expected)


    def test_results_read_new_capacity(self, run_model):
        """
        """
        _, results_folder = run_model

        result_file = os.path.join(str(results_folder), 'NewCapacity.csv')
        actual = pd.read_csv(result_file)
        actual = actual.groupby(by=['REGION', 'TECHNOLOGY'],
                                as_index=False).sum().drop(columns='YEAR')

        expected = pd.DataFrame(columns=['REGION','TECHNOLOGY','VALUE'],
                                data=[
                                    ['UTOPIA',        'E01',     2.279801],
                                    ['UTOPIA',        'E31',     0.110000],
                                    ['UTOPIA',    'IMPDSL1',  1717.805326],
                                    ['UTOPIA',    'IMPHCO1',  1451.847478],
                                    ['UTOPIA',        'RHE',    46.867723],
                                    ['UTOPIA',        'RHO',    46.135248],
                                    ['UTOPIA',        'RIV',    97.919280],
                                    ['UTOPIA',        'RL1',    34.303990],
                                    ['UTOPIA',        'SRE',     0.100000],
                                    ['UTOPIA',        'TXD',    17.790000],
                                      ])

        pd.testing.assert_frame_equal(actual, expected)


class TestShort():

    def test_mathprog_run_short(self, short_model_file, data_file, results_folder):

        arguments = ['glpsol', '-m', short_model_file, '-d',
                     data_file, '-o', results_folder]
        output = run(arguments, capture_output=True, text=True)
        assert 'OPTIMAL LP SOLUTION FOUND' in output.stdout
        assert 'obj =   2.944686269e+04' in output.stdout