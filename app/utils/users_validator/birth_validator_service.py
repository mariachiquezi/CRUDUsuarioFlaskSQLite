from datetime import datetime, date

from app.constants import MAX_AGE, MIN_AGE


class BirthDateValidator:

    @staticmethod
    def parse_birth_date(birth_date) -> date:
        """
        Verifica se a data de nascimento é um objeto datetime.date e, se não for, tenta convertê-la.

        Parâmetros:
            birth_date (str ou date): Data de nascimento no formato 'DD/MM/YYYY', 'DD-MM-YYYY' ou um objeto date.

        Retorna:
            date: Objeto datetime.date representando a data de nascimento.

        Levanta:
            ValueError: Se a data de nascimento não puder ser convertida.
        """
        if isinstance(birth_date, date):
            return birth_date

        # Lista de formatos aceitos para a data de nascimento
        formats = ["%d/%m/%Y", "%d-%m-%Y"]
        for fmt in formats:
            try:
                return datetime.strptime(birth_date, fmt).date()
            except ValueError:
                continue

        raise ValueError(
            "Data de nascimento inválida. O formato esperado é 'DD/MM/YYYY' ou 'DD-MM-YYYY'."
        )

    @staticmethod
    def validate_age(birth_date_obj: date) -> None:
        """
        Verifica se a idade calculada com base na data de nascimento está no intervalo permitido.

        Parâmetros:
            birth_date_obj (date): Objeto datetime.date representando a data de nascimento.

        Levanta:
            ValueError: Se a idade calculada estiver fora do intervalo permitido.
        """
        age = BirthDateValidator.calculate_age(birth_date_obj)
        if age < MIN_AGE or age > MAX_AGE:
            raise ValueError("Idade fora do intervalo permitido.")

    @staticmethod
    def format_date_to_db(birth_date_obj: date) -> str:
        """
        Formata a data de nascimento no formato 'YYYY-MM-DD' para armazenamento no banco de dados.

        Parâmetros:
            birth_date_obj (date): Objeto datetime.date representando a data de nascimento.

        Retorna:
            str: Data de nascimento formatada como string no formato 'YYYY-MM-DD'.
        """
        return birth_date_obj.strftime("%Y-%m-%d")

    @staticmethod
    def calculate_age(birth_date_obj: date) -> int:
        """
        Calcula a idade com base na data de nascimento.

        Parâmetros:
            birth_date_obj (date): Objeto datetime.date representando a data de nascimento.

        Retorna:
            int: Idade calculada.
        """
        today = date.today()
        age = (
            today.year
            - birth_date_obj.year
            - ((today.month, today.day) < (birth_date_obj.month, birth_date_obj.day))
        )
        return age

    @staticmethod
    def validate_and_format_birth_date(birth_date) -> str:
        """
        Valida e formata a data de nascimento.

        Parâmetros:
            birth_date (str ou date): Data de nascimento no formato 'DD/MM/YYYY', 'DD-MM-YYYY' ou um objeto date.

        Retorna:
            str: Data de nascimento validada e formatada como string no formato 'YYYY-MM-DD'.

        Levanta:
            ValueError: Se a data de nascimento for inválida ou a idade estiver fora do intervalo permitido.
        """
        birth_date_obj = BirthDateValidator.parse_birth_date(birth_date)
        BirthDateValidator.validate_age(birth_date_obj)
        return BirthDateValidator.format_date_to_db(birth_date_obj)
