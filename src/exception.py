import sys


def error_message_detail(error: Exception, error_detail: sys) -> str:
    _, _, exc_tb = error_detail.exc_info()

    if exc_tb is None:
        return f"Error message: {error}"

    file_name = exc_tb.tb_frame.f_code.co_filename
    line_number = exc_tb.tb_lineno

    return (
        "Error occurred in python script "
        f"name [{file_name}] line number [{line_number}] "
        f"error message [{error}]"
    )


class CustomException(Exception):
    def __init__(self, error_message: Exception, error_detail: sys):
        super().__init__(error_message)
        self.error_message = error_message_detail(
            error=error_message,
            error_detail=error_detail,
        )

    def __str__(self) -> str:
        return self.error_message
