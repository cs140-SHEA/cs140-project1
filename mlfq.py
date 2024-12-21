from typing import List

class Process:
  def __init__(self, process_name: str, arrival_time: int, burst_time: List[int], io_time: List[int]):
    ...