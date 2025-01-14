def normalize_time(hours, minutes, seconds):
    minutes += seconds // 60
    seconds = seconds % 60
    hours += minutes // 60
    minutes = minutes % 60
    return hours, minutes, seconds