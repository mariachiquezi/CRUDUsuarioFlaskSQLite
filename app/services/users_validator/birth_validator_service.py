from datetime import datetime


class BirthDateValidator:
    """
    Classe para validar datas de aniversário e verificar se a idade está no intervalo permitido.
    """

    MIN_AGE = 18
    MAX_AGE = 110

    @staticmethod
    def normalize_date_format(birth_date: str) -> str:
        """
        Normaliza o formato da data para usar '-' como separador.

        :param birth_date: Data de nascimento como string ('DD-MM-YYYY' ou 'DD/MM/YYYY').
        :return: Data com separador normalizado ('DD-MM-YYYY').
        """
        return birth_date.replace("/", "-")

    @staticmethod
    def parse_birth_date(birth_date: str) -> datetime:
        """
        Converte a data de nascimento em um objeto datetime.

        :param birth_date: Data de nascimento em formato string ('DD-MM-YYYY').
        :return: Objeto datetime representando a data de nascimento.
        :raises ValueError: Se o formato da data estiver incorreto.
        """
        try:
            print("date", birth_date)
            return datetime.strptime(birth_date, "%d-%m-%Y")
        except ValueError:
            raise ValueError(
                "Data de nascimento inválida. O formato esperado é 'DD-MM-YYYY' ou 'DD/MM/YYYY'."
            )

    @staticmethod
    def validate_age(birth_date_obj: datetime) -> None:
        """
        Verifica se a idade está no intervalo permitido.

        :param birth_date_obj: Objeto datetime representando a data de nascimento.
        :raises ValueError: Se a idade estiver fora do intervalo permitido.
        """
        age = BirthDateValidator.calculate_age(birth_date_obj)
        if age < BirthDateValidator.MIN_AGE or age > BirthDateValidator.MAX_AGE:
            raise ValueError(
                f"Idade fora do intervalo permitido ({BirthDateValidator.MIN_AGE}-{BirthDateValidator.MAX_AGE})."
            )

    @staticmethod
    def format_date_to_db(birth_date_obj: datetime) -> str:
        """
        Formata a data de nascimento no formato 'YYYY-MM-DD'.

        :param birth_date_obj: Objeto datetime representando a data de nascimento.
        :return: Data formatada como string.
        """
        return birth_date_obj.strftime("%Y-%m-%d")

    @staticmethod
    def calculate_age(birth_date_obj: datetime) -> int:
        """
        Calcula a idade com base na data de nascimento.

        :param birth_date_obj: Objeto datetime representando a data de nascimento.
        :return: Idade calculada.
        """
        today = datetime.today()
        age = (
            today.year
            - birth_date_obj.year
            - ((today.month, today.day) < (birth_date_obj.month, birth_date_obj.day))
        )
        return age

    @staticmethod
    def validate_and_format_birth_date(birth_date: str) -> str:
        """
        Valida e formata a data de nascimento.

        :param birth_date: Data de nascimento em formato string ('DD-MM-YYYY' ou 'DD/MM/YYYY').
        :return: Data formatada no formato 'YYYY-MM-DD'.
        :raises ValueError: Se a data não for válida ou a idade estiver fora do intervalo permitido.
        """
        normalized_date = BirthDateValidator.normalize_date_format(birth_date)
        birth_date_obj = BirthDateValidator.parse_birth_date(normalized_date)
        BirthDateValidator.validate_age(birth_date_obj)
        return BirthDateValidator.format_date_to_db(birth_date_obj)


