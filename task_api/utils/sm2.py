from typing import Union
import math

def sm2(quality: int, repetitions: int, ease_factor: float, interval: int) -> Union[int, int, float]:
    """
    Generates spaced repetition intervals for the SM2 algorithm.

    Args:
        quality (int): The quality of the last repetition.
        repetitions (int): The number of repetitions.
        ease_factor (float): The ease factor.
        interval (int): The interval.

    Returns:
        Union[int, int, float]: The new interval, new repetitions, and new ease factor.
    """
    if quality >= 3: # correct response
        if repetitions == 0:
            interval = 1
        elif repetitions == 1:
            interval = 6
        else:
            interval = interval * ease_factor
        interval = math.ceil(interval)
        repetitions += 1
    else: # incorrect response
        repetitions = 0
        interval = 1
    ease_factor = ease_factor + (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02))
    ease_factor = max(ease_factor, 1.3)
    return interval, repetitions, ease_factor


