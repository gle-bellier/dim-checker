class OutputsNumberError(Exception):
    """Exception raised when the number of outputs does not match the expected number of outputs."""

    def __init__(self, nb_outputs: int, expected: int, payload=None):
        self.nb_outputs = nb_outputs
        self.expected = expected
        self.payload = payload 


    def __str__(self):
        return f"""Got {self.nb_outputs} output(s), expected {self.expected} output(s) according to the pattern."""


