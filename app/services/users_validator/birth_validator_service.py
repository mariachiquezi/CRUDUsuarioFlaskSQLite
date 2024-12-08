from datetime import datetime
from app.exceptions.validation_error import ValidationError


class BirthFormatter:
    @staticmethod
    def parse_date(birth_date: str, input_format: str = "%d-%m-%Y") -> datetime:
        """
        Converte uma string de data para um objeto `datetime`.

        :param birth_date: Data em formato string.
        :param input_format: Formato esperado para a data (padrão: '%d-%m-%Y').
        :return: Objeto datetime correspondente à data fornecida.
        :raises ValidationError: Se a data não estiver no formato esperado.
        """
        # Se ocorrer um erro de formatação, a exceção é lançada automaticamente
        return datetime.strptime(birth_date, input_format)

    @staticmethod
    def format_date_for_db(date_obj: datetime) -> str:
        """
        Formata um objeto `datetime` para o formato 'YYYY-MM-DD', adequado ao banco de dados.

        :param date_obj: Objeto datetime.
        :return: Data formatada como string no formato 'YYYY-MM-DD'.
        :raises ValueError: Se o objeto fornecido não for um datetime válido.
        """
        # Se o objeto não for válido, a exceção será automaticamente lançada
        return date_obj.strftime("%Y-%m-%d")

    @staticmethod
    def format_birth_date(birth_date: str) -> str:
        """
        Valida e formata uma data de nascimento de 'D-M-A' para 'AAAA-MM-DD'.

        :param birth_date: Data em formato string ('D-M-A').
        :return: Data formatada para 'AAAA-MM-DD'.
        :raises ValidationError: Se a data não estiver no formato esperado.
        """
        # Aqui, a exceção será lançada diretamente, sem a necessidade de um tratamento intermediário
        parsed_date = BirthFormatter.parse_date(birth_date)
        return BirthFormatter.format_date_for_db(parsed_date)
