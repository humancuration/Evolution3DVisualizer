# In any module
from util_helpers import setup_logger

logger = setup_logger('data_loader', 'data_loader.log')

def some_function():
    try:
        # Your code here
        pass
    except Exception as e:
        logger.error(f"An error occurred: {e}")
