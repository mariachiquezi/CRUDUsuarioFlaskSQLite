import re
from app.exceptions.validation_error import ValidationError
from app.utils.format_cpf import clean_point


class CPFValidator:
    def __init__(self, cpf: str):
        """Inicializa a classe com o CPF limpo e prepara os dígitos verificadores."""
        self.cpf = self.clean_cpf(cpf)
        self.digit_1 = None
        self.digit_2 = None

    @staticmethod
    def clean_cpf(cpf: str) -> str:
        """Remove caracteres não numéricos do CPF."""
        return re.sub(r"[^0-9]", "", cpf)

    def check_repetition(self) -> bool:
        """Verifica se o CPF contém todos os dígitos idênticos (CPF sequencial)."""
        return self.cpf == self.cpf[0] * len(self.cpf)

    def calculate_check_digit(self, partial_cpf: str, initial_weight: int) -> int:
        """Calcula o dígito de verificação com base no CPF parcial e peso inicial."""
        result = sum(
            int(digit) * (initial_weight - i) for i, digit in enumerate(partial_cpf)
        )
        check_digit = (result * 10) % 11
        return check_digit if check_digit <= 9 else 0

    def calculate_digits(self):
        """Calcula ambos os dígitos de verificação do CPF."""
        nine_digits = self.cpf[:9]
        self.digit_1 = self.calculate_check_digit(nine_digits, 10)
        ten_digits = nine_digits + str(self.digit_1)
        self.digit_2 = self.calculate_check_digit(ten_digits, 11)

    def validate_cpf(self) -> bool:
        """Valida o CPF completo verificando se os dígitos calculados correspondem aos fornecidos."""
        if len(self.cpf) != 11:
            raise ValueError("CPF inválido! O CPF deve ter 11 dígitos.")

        if self.check_repetition():
            raise ValueError("CPF inválido! O CPF não pode ser sequencial.")

        self.calculate_digits()
        calculated_cpf = f"{self.cpf[:9]}{self.digit_1}{self.digit_2}"
        return self.cpf == calculated_cpf

    @staticmethod
    def run(cpf_input: str):
        try:
            validator = CPFValidator(cpf_input)
            if not validator.validate_cpf():
                raise ValidationError(
                    "CPF inválido! Por favor, verifique e tente novamente."
                )
            return clean_point(cpf_input)
        except ValueError as e:
            raise ValidationError(str(e))
