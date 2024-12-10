from datetime import datetime
from app.exceptions.validation_error import ValidationError

class AgeValidatorService:
    @staticmethod
    def validate_age(birth_date_obj: datetime):
        """
        Valida a idade com base na data de nascimento. A idade deve ser entre 18 e 110 anos.
        :param birth_date_obj: Objeto datetime representando a data de nascimento.
        :raises ValidationError: Se a idade não estiver entre 18 e 110 anos.
        """
        age = AgeValidatorService.calculate_age(birth_date_obj)
        if not (18 <= age <= 110):
            raise ValidationError("Idade inválida. A idade deve ser entre 18 e 110 anos.")

    @staticmethod
    def calculate_age(birth_date_obj: datetime) -> int:
        """
        Calcula a idade com base na data de nascimento.
        :param birth_date_obj: Objeto datetime representando a data de nascimento.
        :return: A idade em anos.
        """
        today = datetime.today()
        age = today.year - birth_date_obj.year
        if today.month < birth_date_obj.month or (today.month == birth_date_obj.month and today.day < birth_date_obj.day):
            age -= 1
        return age


    @staticmethod
    def format_birth_date(birth_date: str) -> str:
        """
        Formata uma data de nascimento de 'D-M-A' para 'AAAA-MM-DD'.

        :param birth_date: Data em formato string ('D-M-A').
        :return: Data formatada para 'YYYY-MM-DD'.
        :raises ValidationError: Se a data não estiver no formato esperado.
        """
        try:
            # Usando o formato correto para data
            birth_date_obj = datetime.strptime(birth_date, "%d-%m-%Y")
            
            # Retornar a data formatada para 'YYYY-MM-DD'
            return birth_date_obj.strftime("%Y-%m-%d")
        except ValueError:
            raise ValidationError(
                "Data de nascimento inválida. O formato esperado é 'DD-MM-AAAA'."
            )



