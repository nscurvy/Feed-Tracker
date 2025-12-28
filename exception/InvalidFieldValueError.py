from typing import Any, Optional

from InvalidFormSubmissionError import InvalidFormSubmissionError


class InvalidFieldValueError(InvalidFormSubmissionError):
    """Indicates a form submission contains an invalid field value."""

    def __init__(self, field_name: str, field_value: Any, additional: str = '') -> None:
        super().__init__(f'Error submitting form with field {field_name}: {field_value}. {additional}')
        self.field_name = field_name
        self.field_value = field_value
