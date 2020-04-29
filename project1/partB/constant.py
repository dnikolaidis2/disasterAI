from numpy import concatenate, array

DAY_COUNT = 14
EMPLOYEE_COUNT = 30
SHIFT_COUNT = 3

DAY_OFF = 0
MORNING = 1
EVENING = 2
NIGHT = 3

M_HOURS = 8
E_HOURS = 8
N_HOURS = 10

MAX_WORK_HOURS = 70
MAX_WORK_DAYS = 7
MAX_NIGHT_SHIFTS = 4

MAX_PENALTY = 94776
MIN_PENALTY = 46703

MIN_PENALTY_DIFFERENTIATION = 100

MINIMUM_POPULATION = 35

CROSS_TYPE = ['uniform', 'two-point']
MUT_TYPE = ['swap', 'bit-flip']

PREFERRED_SCHEDULE = array([3, 3, 3, 3, 0, 0])
EXPECTED_ELEMENTS = array([1, 2, 3])
ALLOWED_VALUES = array([0, 1, 2, 3])

REQUIRED_WORKFORCE_COVERAGE_PER_WEEK = array([[10, 10, 5, 5, 5, 5, 5],
                                              [10, 10, 10, 5, 10, 5, 5],
                                              [5, 5, 5, 5, 5, 5, 5]])

REQUIRED_COVERAGE = concatenate([REQUIRED_WORKFORCE_COVERAGE_PER_WEEK,
                                 REQUIRED_WORKFORCE_COVERAGE_PER_WEEK],
                                axis=1)
