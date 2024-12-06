import re

from app.exceptions.user_exceptions import ValidationError


class CPFValidator:
    def __init__(self, cpf: str):
        # Initialize the class with the cleaned CPF
        self.cpf = self.clean_cpf(cpf)
        self.digit_1 = None
        self.digit_2 = None

    @staticmethod
    def clean_cpf(cpf: str) -> str:
        """
        Removes non-numeric characters from the CPF.
        """
        return re.sub(r"[^0-9]", "", cpf)

    def check_repetition(self) -> bool:
        """
        Checks if the CPF contains all identical digits (sequential CPF).
        """
        return self.cpf == self.cpf[0] * len(self.cpf)

    def calculate_check_digit(self, partial_cpf: str, initial_weight: int) -> int:
        """
        Calculates the check digit (first or second) based on the partial CPF and initial weight.
        """
        result = 0
        for i, digit in enumerate(partial_cpf):
            result += int(digit) * (initial_weight - i)
        check_digit = (result * 10) % 11
        return check_digit if check_digit <= 9 else 0

    def calculate_digits(self):
        """
        Calculates both check digits for the CPF.
        """
        nine_digits = self.cpf[:9]

        # Calculate the first digit
        self.digit_1 = self.calculate_check_digit(nine_digits, 10)

        # Calculate the second digit
        ten_digits = nine_digits + str(self.digit_1)
        self.digit_2 = self.calculate_check_digit(ten_digits, 11)

    def validate(self) -> bool:
        """
        Validates the complete CPF (checks if the generated digits match the provided ones).
        """
        if len(self.cpf) != 11:
            raise ValueError("Invalid CPF! The CPF must have 11 digits.")

        if self.check_repetition():
            raise ValueError("Invalid CPF! The CPF cannot be sequential.")

        # Calculate the check digits
        self.calculate_digits()

        # Generate the CPF with the calculated digits
        calculated_cpf = f"{self.cpf[:9]}{self.digit_1}{self.digit_2}"

        # Compare the provided CPF with the generated one
        return self.cpf == calculated_cpf

    def run(cpf_input: str):
        try:
            # Create the CPF validator instance
            validator = CPFValidator(cpf_input)

            # Validate the CPF
            if not validator.validate():
                raise ValidationError(
                    "CPF inválido! Por favor, verifique e tente novamente"
                )

        except ValueError as e:
            print(e)
