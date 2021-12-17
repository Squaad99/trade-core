
def get_percentage_diff(first, last):
    change_type = "positive"
    if first > last:
        change_type = "negative"
    try:
        percentage = abs(first - last) / max(first, last) * 100
    except ZeroDivisionError:
        percentage = float('inf')
    result = round(percentage, 2)
    if change_type == "negative":
        result = result * -1
    return result
