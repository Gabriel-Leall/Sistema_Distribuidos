from typing import List
import math
import time

class Utils:
    @staticmethod
    def calculate_standard_deviation(mrts: List[float]) -> float:
        # get the sum of array
        total_sum = sum(mrts)

        # get the mean of array
        length = len(mrts)
        mean = total_sum / length

        # calculate the standard deviation
        standard_deviation = sum((num - mean) ** 2 for num in mrts)

        return math.sqrt(standard_deviation / length)

    @staticmethod
    def register_time(received_message: str) -> str:
        # Split the message and get last timestamp
        string_splited = received_message.split(';')
        last_registered_time_stamp_string = string_splited[-1]
        
        # Get current time in milliseconds and calculate difference
        time_now = int(time.time() * 1000)
        time_diff = time_now - int(last_registered_time_stamp_string.strip())
        
        # Return updated message with new timestamps
        return f"{received_message}{time_now};{time_diff};"
