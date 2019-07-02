"""Converts a CPLEX solution file into the same format produced by CBC

"""
import sys
from typing import List, Union, Tuple


class ConvertLine(object):
    """Abstract class which defines the interface to the family of convertors

    Inherit this class and implement the ``_do_it()`` method to produce the
    data to be written out into a new format

    Example
    -------
    >>> cplex_line = "AnnualCost	REGION	CDBACKSTOP	1.0	0.0	137958.8400384134"
    >>> convertor = RegionTechnology()
    >>> convertor.convert()
    VariableName(REGION,TECHCODE01,2015)       42.69         0\n
    VariableName(REGION,TECHCODE01,2017)       137958.84         0\n
    """

    def __init__(self, data: List, start_year: int, end_year: int):
        self.data = data
        self.start_year = start_year
        self.end_year = end_year

    def _do_it(self) -> Tuple:
        raise NotImplementedError()

    def convert(self) -> List[str]:
        """Perform the conversion
        """
        cbc_data = []
        variable, dimensions, values = self._do_it()

        for index, value in enumerate(values):

            year = self.start_year + index
            if (value not in ["0.0", "0", ""]) and (year <= self.end_year):

                try:
                    value = float(value)
                except ValueError:
                    value = 0

                full_dims = ",".join(dimensions + (str(year),))

                formatted_data = "0 {0}({1}) {2} 0\n".format(
                    variable,
                    full_dims,
                    value
                    )

                cbc_data.append(formatted_data)

        return cbc_data


class RegionTimeSliceTechnologyMode(ConvertLine):

    def _do_it(self) -> Tuple:
        """Produces output indexed by Region, Timeslice, Tech and Mode

        ``0 VariableName(REGION,SD1D,TECHCODE01,2,2015) 42.69 0\n``

        """
        variable = self.data[0]
        region = self.data[1]
        timeslice = self.data[2]
        technology = self.data[3]
        mode = self.data[4]
        values = self.data[5:]

        dimensions = (region, timeslice, technology, mode)

        return (variable, dimensions, values)


class RegionTechnology(ConvertLine):

    def _do_it(self) -> Tuple:
        """Produces output indexed by dimensions Region and Technology

        ``0 VariableName(REGION,TECHCODE01,2015) 42.69 0\n``

        """
        variable = self.data[0]
        region = self.data[1]
        technology = self.data[2]

        dimensions = (region, technology)

        values = self.data[3:]

        return (variable, dimensions, values)


def process_line(line: str, start_year, end_year) -> List[str]:
    """Processes an individual line in a CPLEX file

    A different ConvertLine implementation is chosen depending upon the
    variable name

    Arguments
    ---------
    line : str
    """
    row_as_list = line.split('\t')
    variable = row_as_list[0]
    if variable in ['NewCapacity',
                    'TotalCapacityAnnual',
                    'CapitalInvestment',
                    'AnnualFixedOperatingCost',
                    'AnnualVariableOperatingCost']:
        convertor = RegionTechnology(row_as_list, start_year, end_year).convert()
    elif variable in ['RateOfActivity']:
        convertor = RegionTimeSliceTechnologyMode(row_as_list, start_year, end_year).convert()
    else:
        convertor = []

    return convertor


def convert_cplex_file(cplex_filename, output_filename, start_year=2015, end_year=2070):
    """Converts a CPLEX solution file into that of the CBC solution file

    Arguments
    ---------
    cplex_filename : str
        Path to the transformed CPLEX solution file
    output_filename : str
        Path for the processed data to be written to
    """

    with open(output_filename, 'w') as cbc_file:
        with open(cplex_filename, 'r') as cplex_file:
            for linenum, line in enumerate(cplex_file):
                convertor = process_line(line)
                try:
                    if convertor:
                        cbc_file.writelines(data)
                except ValueError:
                    msg = "Error caused at line {}: {}"
                    raise ValueError(msg.format(linenum, line))


class TestCplexRead:

    def test_different_format(self):

        fixture = "AnnualFixedOperatingCost	REGION	AOBACKSTOP	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0		"

        expected = []

        actual = process_line(fixture, 2015, 2070)
        assert actual == expected

    def test_read_in_line(self):

        fixture = "AnnualFixedOperatingCost	REGION	CDBACKSTOP	0.0	0.0	137958.8400384134	305945.38410619126	626159.9611543404	0.0	0.0	0.0	0.0	0.0	0.0	0.0	0.0	0.0	0.0	0.0	0.0	0.0	0.0	0.0	0.0	0.0	0.0	0.0	0.0	0.0	0.0	0.0	0.0	0.0	0.0	0.0	0.0	0.0	0.0	0.0	0.0	0.0	0.0	0.0	0.0	0.0	0.0	0.0	0.0	0.0	0.0	0.0	0.0	0.0	0.0	0.0	0.0	0.0	0.0	0.0"

        expected = [
                    "0 AnnualFixedOperatingCost(REGION,CDBACKSTOP,2017) 137958.8400384134 0\n",
                    "0 AnnualFixedOperatingCost(REGION,CDBACKSTOP,2018) 305945.3841061913 0\n",
                    "0 AnnualFixedOperatingCost(REGION,CDBACKSTOP,2019) 626159.9611543404 0\n"]

        actual = process_line(fixture, 2015, 2070)
        assert actual == expected


    def test_rate_of_activity(self):

        fixture = """RateOfActivity	REGION	S1D1	CGLFRCFURX	1	0.0	0.0	0.0	0.0	0.0	0.3284446367303371	0.3451714779880536	0.3366163200621617	0.3394945166233896	0.3137488154250392	0.28605725055560716	0.2572505015401749	0.06757558148965725	0.0558936625751148	0.04330608461292407	0.0	0.0	0.0	0.0	0.0	0.0	0.0	0.0	0.0	0.0	0.0	0.0	0.0	0.0	0.0	0.0	0.0	0.0	0.0	0.0	0.0	0.0	0.0	0.0	0.0	0.0	0.0	0.0	0.0	0.0	0.0	0.0	0.0	0.0	0.0	0.0	0.0	0.0	0.0	0.0	0.0"""

        expected = [
            "0 RateOfActivity(REGION,S1D1,CGLFRCFURX,1,2020) 0.3284446367303371 0\n",
            "0 RateOfActivity(REGION,S1D1,CGLFRCFURX,1,2021) 0.3451714779880536 0\n",
            "0 RateOfActivity(REGION,S1D1,CGLFRCFURX,1,2022) 0.3366163200621617 0\n",
            "0 RateOfActivity(REGION,S1D1,CGLFRCFURX,1,2023) 0.3394945166233896 0\n",
            "0 RateOfActivity(REGION,S1D1,CGLFRCFURX,1,2024) 0.3137488154250392 0\n",
            "0 RateOfActivity(REGION,S1D1,CGLFRCFURX,1,2025) 0.28605725055560716 0\n",
            "0 RateOfActivity(REGION,S1D1,CGLFRCFURX,1,2026) 0.2572505015401749 0\n",
            "0 RateOfActivity(REGION,S1D1,CGLFRCFURX,1,2027) 0.06757558148965725 0\n",
            "0 RateOfActivity(REGION,S1D1,CGLFRCFURX,1,2028) 0.0558936625751148 0\n",
            "0 RateOfActivity(REGION,S1D1,CGLFRCFURX,1,2029) 0.04330608461292407 0\n"]

        actual = process_line(fixture, 2015, 2070)
        assert actual == expected


if __name__ == '__main__':

    if len(sys.argv) != 3:
        msg = "Usage:\npython {} <cplex_file> <output_file>\n"
        print(msg.format(sys.argv[0]))
        sys.exit(1)

    cplex_file = sys.argv[1]
    cbc_file = sys.argv[2]

    convert_cplex_file(cplex_file, cbc_file)
