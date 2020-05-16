import pytest
from workouts import print_workout_days


test_values = [
    ("Upper", "Mon, Thu\n"),
    ("LOWER", "Tue, Fri\n"),
    ("1", "Mon, Tue\n"),
    ("2", "Thu, Fri\n"),
    ("3", "Wed\n"),
    ("0", "Wed\n"),
    ("BoDy", "Mon, Tue, Thu, Fri\n"),
    ("o", "Mon, Tue, Wed, Thu, Fri\n"),
]


new_dict = {
    "sun": "30 minute yoga",
    "tue": "upper body #4",
    "wed": "lower body #4",
    "fri": "upper body #3",
    "sat": "lower body #3",
}


test_values_new_dict = [
    ("Upper", "Tue, Fri\n"),
    ("LOWER", "Wed, Sat\n"),
    ("1", "No matching workout\n"),
    ("2", "No matching workout\n"),
    ("3", "Sun, Fri, Sat\n"),
    ("0", "Sun\n"),
    ("BoDy", "Tue, Wed, Fri, Sat\n"),
    ("o", "Sun, Tue, Wed, Fri, Sat\n"),
]


@pytest.mark.parametrize("provided, expected", test_values)
def test_print_workout_days(capsys, provided, expected):
    print_workout_days(provided)
    assert capsys.readouterr().out == expected


@pytest.mark.parametrize("provided, expected", test_values_new_dict)
def test_print_workout_days_new_dict(capsys, provided, expected):
    print_workout_days(provided, my_workouts=new_dict)
    assert capsys.readouterr().out == expected


@pytest.mark.xfail(raises=TypeError, reason="Blank Dict Provided")
def test_blank_workout_given(capsys):
    print_workout_days("Doesn't Matter", my_workout=None)
    assert capsys.readouterr().err == "TypeError"
