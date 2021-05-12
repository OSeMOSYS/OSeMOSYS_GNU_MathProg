"""Tests the pre-processing script which adds mode x subsets

"""
from . preprocess_data import main
from io import StringIO


def test_add_emission_sets():

    fixture = \
"""
param default 0.0 : EmissionActivityRatio :=
REGION NENG00ILGX NECO2 1 2019 0.0503006546999384
;

set TECHNOLOGY :=
NENG00ILGX
;

set YEAR :=
2019
;

end;"""

    expected = \
"""
param default 0.0 : EmissionActivityRatio :=
REGION NENG00ILGX NECO2 1 2019 0.0503006546999384
;

set TECHNOLOGY :=
NENG00ILGX
;

set YEAR :=
2019
;

set MODEperTECHNOLOGY[NENG00ILGX]:= 1;
end;"""

    actual = StringIO()

    main('otoole', StringIO(fixture), actual)
    print(actual.getvalue())
    assert actual.getvalue() == expected
