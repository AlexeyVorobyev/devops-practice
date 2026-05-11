def build_numbers():
    return [3, 7, 11, 19, 23]


def calculate_sum(numbers):
    return sum(numbers)


def calculate_average(numbers):
    return calculate_sum(numbers) / len(numbers)


def calculate_maximum(numbers):
    return max(numbers)


def build_report(numbers, total, average, maximum):
    return {
        "numbers": numbers,
        "count": len(numbers),
        "sum": total,
        "average": average,
        "max": maximum,
    }
