from strategy.lib.CRITERIA_VARS import *
from strategy.models import StrategyCriteria
from w_trade.data.data_set import DataSet


def check_all_criteria(criteria_list, data_set):
    criteria_sum = len(criteria_list)
    criteria_result_list = []

    for criteria in criteria_list:
        result = check_criteria(criteria, data_set)
        criteria_result_list.append(result)

    result_sum = criteria_result_list.count(True)
    if result_sum == criteria_sum:
        return True

    return False


def is_value_above(expected_lower, expected_higher):
    # First value should be lower to return true
    if float(expected_lower) < float(expected_higher):
        return True
    return False


def is_value_under(expected_higher, expected_lower):
    # First value should be higher to return true
    if float(expected_higher) > float(expected_lower):
        return True
    return False


def is_value_equal(expected_equal, expected_equal_2):
    # First value should be lower to return true
    if float(expected_equal) == float(expected_equal_2):
        return True
    return False


def check_value(data_set_value, criteria_value, direction):
    if DIRECTION_ABOVE == direction:
        return is_value_above(data_set_value, criteria_value)
    if DIRECTION_UNDER == direction:
        return is_value_under(data_set_value, criteria_value)
    if DIRECTION_EQUAL == direction:
        return is_value_equal(data_set_value, criteria_value)
    return False


def check_criteria(criteria: StrategyCriteria, data_set: DataSet):
    value_selection = criteria.value_selection
    value_direction = criteria.value_direction

    if CHANGE_PERCENT == criteria.data_name:
        return check_value(data_set.change_percentage, value_selection, value_direction)

    return False

