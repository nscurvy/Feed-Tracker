import exception.FeedTrackerError


class InvalidFormSubmissionError(exception.FeedTrackerError):
    """Indicates an invalid form submission has been attempted."""
    pass
