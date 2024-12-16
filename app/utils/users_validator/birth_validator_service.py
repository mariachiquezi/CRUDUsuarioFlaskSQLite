from datetime import datetime, date


class BirthDateValidator:
    MIN_AGE = 18
    MAX_AGE = 110

    @staticmethod
    def parse_birth_date(birth_date) -> date:
        """Verifica se a data de nascimento já é um objeto datetime.date."""
        if isinstance(birth_date, date):
            return birth_date
        try:
            return datetime.strptime(birth_date, "%Y-%m-%d").date()
        except ValueError:
            raise ValueError(
                "Data de nascimento inválida. O formato esperado é 'YYYY-MM-DD'."
            )

    @staticmethod
    def validate_age(birth_date_obj: date) -> None:
        """Verifica se a idade está no intervalo permitido."""
        age = BirthDateValidator.calculate_age(birth_date_obj)
        if age < BirthDateValidator.MIN_AGE or age > BirthDateValidator.MAX_AGE:
            raise ValueError("Idade fora do intervalo permitido.")

    @staticmethod
    def format_date_to_db(birth_date_obj: date) -> str:
        """Formata a data de nascimento no formato 'YYYY-MM-DD'."""
        return birth_date_obj.strftime("%Y-%m-%d")

    @staticmethod
    def calculate_age(birth_date_obj: date) -> int:
        """Calcula a idade com base na data de nascimento."""
        today = date.today()
        age = (
            today.year
            - birth_date_obj.year
            - ((today.month, today.day) < (birth_date_obj.month, birth_date_obj.day))
        )
        return age

    @staticmethod
    def validate_and_format_birth_date(birth_date) -> str:
        """Valida e formata a data de nascimento."""
        birth_date_obj = BirthDateValidator.parse_birth_date(birth_date)
        BirthDateValidator.validate_age(birth_date_obj)
        return BirthDateValidator.format_date_to_db(birth_date_obj)
