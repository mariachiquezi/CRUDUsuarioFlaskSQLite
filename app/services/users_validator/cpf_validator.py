import re
from app.exceptions.validation_error import ValidationError
from app.utils.id_generator import clean_point


class CPFValidator:
    def __init__(self, cpf: str):
        # Inicializa a classe com o CPF limpo
        self.cpf = self.clean_cpf(cpf)
        self.digit_1 = None
        self.digit_2 = None

    @staticmethod
    def clean_cpf(cpf: str) -> str:
        """
        Remove caracteres não numéricos do CPF.
        """
        return re.sub(r"[^0-9]", "", cpf)

    def check_repetition(self) -> bool:
        """
        Verifica se o CPF contém todos os dígitos idênticos (CPF sequencial).
        """
        return self.cpf == self.cpf[0] * len(self.cpf)

    def calculate_check_digit(self, partial_cpf: str, initial_weight: int) -> int:
        """
        Calcula o dígito de verificação (primeiro ou segundo) com base no CPF parcial e peso inicial.
        """
        result = 0
        for i, digit in enumerate(partial_cpf):
            result += int(digit) * (initial_weight - i)
        check_digit = (result * 10) % 11
        return check_digit if check_digit <= 9 else 0

    def calculate_digits(self):
        """
        Calcula ambos os dígitos de verificação do CPF.
        """
        nine_digits = self.cpf[:9]

        # Calcula o primeiro dígito
        self.digit_1 = self.calculate_check_digit(nine_digits, 10)

        # Calcula o segundo dígito
        ten_digits = nine_digits + str(self.digit_1)
        self.digit_2 = self.calculate_check_digit(ten_digits, 11)

    def validate(self) -> bool:
        """
        Valida o CPF completo (verifica se os dígitos calculados correspondem aos fornecidos).
        """
        if len(self.cpf) != 11:
            raise ValueError("CPF inválido! O CPF deve ter 11 dígitos.")

        if self.check_repetition():
            raise ValueError("CPF inválido! O CPF não pode ser sequencial.")

        # Calcula os dígitos de verificação
        self.calculate_digits()

        # Gera o CPF com os dígitos calculados
        calculated_cpf = f"{self.cpf[:9]}{self.digit_1}{self.digit_2}"

        # Compara o CPF fornecido com o gerado
        return self.cpf == calculated_cpf

    @staticmethod
    def run(cpf_input: str):
        try:
            # Cria a instância do validador com o CPF limpo
            validator = CPFValidator(cpf_input)

            # Valida o CPF
            if not validator.validate():
                raise ValidationError(
                    "CPF inválido! Por favor, verifique e tente novamente."
                )

            # Retorna o CPF validado e formatado
            cpf_validado_formatado = clean_point(cpf_input)
            print("cpf_validado_formatado", cpf_validado_formatado)

            return cpf_validado_formatado
        except ValueError as e:
            raise ValidationError(str(e))  # Repassa o erro como ValidationError
        except ValidationError as e:
            raise e  # Propaga o erro customizado
