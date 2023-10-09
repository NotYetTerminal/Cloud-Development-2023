from statistics import mean


FOLDER: str = "ca1_textual/swimdata/"


def convert_2_hundreths(time: str) -> int:
    """Given a string which represents a time this function converts the string
    to a number (int) representing the string's hundreths of seconds value, which is
    returned.
    """
    if ":" in time:
        minutes, rest = time.split(":")
    else:
        rest = time
        minutes = 0

    seconds, hundreths = rest.split(".")
    return int(hundreths) + (int(seconds) * 100) + (int(minutes) * 60 * 100)


def build_time_string(num_time: float) -> str:
    """ """
    seconds, hundreths = f"{(num_time / 100):.2f}".split(".")
    minutes: int = int(seconds) // 60
    seconds = int(seconds) % 60
    return f"{minutes}:{seconds}.{hundreths}"


def get_swimmers_data(file_name: str) -> tuple:
    """ """
    name, age, distance, stroke = file_name.removesuffix(".txt").split("-")
    
    with open(FOLDER + file_name, "r") as f:
        data: str = f.read()
    
    times: list = data.strip().split(",")

    converts: list = []
    for t in times:
        converts.append(convert_2_hundreths(t))

    average: str = build_time_string(mean(converts))
    
    return name, age, distance, stroke, times, converts, average


def convert2range(v, f_min, f_max, t_min, t_max):
    """Given a value (v) in the range f_min-f_max, convert the value
    to its equivalent value in the range t_min-t_max.

    Based on the technique described here:
        http://james-ramsden.com/map-a-value-from-one-number-scale-to-another-formula-and-c-code/
    """
    return round(t_min + (t_max - t_min) * ((v - f_min) / (f_max - f_min)), 2)
