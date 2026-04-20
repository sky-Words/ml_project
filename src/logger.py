import logging
import os
from datetime import datetime
import sys

LOG_FILE = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"
LOG_PATH = os.path.join(os.getcwd(), "logs", LOG_FILE)

os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)

logging.basicConfig(
    filename=LOG_PATH,
    format="[ %(asctime)s ] %(lineno)d %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

## just tst logging
# if __name__ == "__main__":
#     logging.info("Logging has started.")

#     try:
#         result = 10 / 0
#     except Exception as e:
#         logging.error(f"An error occurred: {e}")
#         raise ChildProcessError(e,sys)