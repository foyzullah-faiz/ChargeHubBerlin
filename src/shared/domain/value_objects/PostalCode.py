from dataclasses import dataclass

@dataclass(frozen=True)
class PostalCode:
    """
    Value Object for a German Postal Code.
    It is immutable (frozen) and validates that the code is exactly 5 digits.
    """
    value: str

    def __post_init__(self):
        # Validation Logic: Must be 5 digits
        if not self.value.isdigit() or len(self.value) != 5:
            raise ValueError(f"Invalid postal code: {self.value}. Must be 5 digits.")

    def __str__(self):
        return self.value