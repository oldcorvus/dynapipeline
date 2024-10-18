"""Contains decorator to measure execution time"""
import time
from functools import wraps


def measure_execution_time(func):
    """Decorator to calculate execution time"""

    @wraps(func)
    async def wrapper(self, *args, **kwargs):
        try:
            self.start_time = time.time()
            result = await func(self, *args, **kwargs)
            return result
        except Exception:
            raise
        finally:
            self.end_time = time.time()
            self.execution_time = self.end_time - self.start_time

    return wrapper
