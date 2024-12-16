from marshmallow import fields
from datetime import date, datetime
import pytz


class CustomDateField(fields.Field):
    default_error_messages = {
        "invalid": "Formato de data inválido. Os formatos esperados são DD/MM/YYYY ou DD-MM-YYYY.",
    }

    def _decode(self, value, attr, data, **kwargs):
        """
        Transforma uma data fornecida nos formatos DD/MM/YYYY ou DD-MM-YYYY para um objeto date.

        Parâmetros:
            value (str ou date): Valor da data a ser mudado.
            attr (str): Atributo que está sendo mudado.
            data (dict): Dicionário de dados que contém o valor.

        Retorna:
            date: Objeto date representando a data deserializada.
        """
        if isinstance(value, date):
            return value  # Já é um objeto date, retorna como está
        for fmt in ("%d/%m/%Y", "%d-%m-%Y"):
            try:
                return datetime.strptime(value, fmt).date()
            except ValueError:
                continue
        self.fail("invalid", input=value)

    def _serialize(self, value, attr, obj, **kwargs):
        """
        Serializa uma data para o formato YYYY-MM-DD.

        Parâmetros:
            value (date): Objeto date a ser serializado.
            attr (str): Atributo que está sendo serializado.
            obj (object): Objeto que contém o valor.

        Retorna:
            str: String representando a data no formato YYYY-MM-DD.
        """
        if value is None:
            return ""
        if isinstance(value, (datetime, date)):
            return value.strftime("%Y-%m-%d")  # Converte para o formato yyyy-mm-dd
        return value


class DateTimeUtils:
    @staticmethod
    def convert_to_timezone(dt, target_timezone="UTC"):
        """
        Converte uma data/hora para o fuso horário desejado.

        Parâmetros:
            dt (datetime ou str): Data/hora no formato datetime ou string.
            target_timezone (str): Fuso horário de destino (padrão é "UTC").

        Retorna:
            str: Data/hora convertida para o fuso horário de destino no formato 'YYYY-MM-DD HH:MM:SS'.

        Levanta:
            ValueError: Se a string não estiver no formato esperado.
            TypeError: Se dt não for datetime ou string.
        """
        # Se for uma string, tenta convertê-la para datetime
        if isinstance(dt, str):
            try:
                dt = datetime.strptime(dt, "%Y-%m-%d %H:%M:%S")
            except ValueError:
                raise ValueError(
                    f"A string '{dt}' não tem o formato esperado '%Y-%m-%d %H:%M:%S'."
                )

        # Verifica se o objeto é datetime
        if isinstance(dt, datetime):
            # Se não tiver um fuso horário (tzinfo), assume-se que é UTC
            if dt.tzinfo is None:
                dt = pytz.utc.localize(dt)  # Assume que está em UTC
        else:
            raise TypeError(f"Esperado datetime ou string, mas foi passado: {type(dt)}")

        # Converte para o fuso horário de destino
        target_tz = pytz.timezone(target_timezone)
        converted_time = dt.astimezone(target_tz)

        return converted_time.strftime("%Y-%m-%d %H:%M:%S")

    @staticmethod
    def adjust_times_for_dict(data, target_timezone="UTC"):
        """
        Ajusta os campos de data em um dicionário para o fuso horário desejado.

        Parâmetros:
            data (dict): Dicionário contendo os campos de data/hora a serem ajustados.
            target_timezone (str): Fuso horário de destino (padrão é "UTC").

        Retorna:
            dict: Dicionário com os campos de data/hora ajustados.
        """
        for key in ["time_created", "time_updated"]:
            if isinstance(
                data[key], (datetime, str)
            ):  # Se o valor for datetime ou string
                data[key] = DateTimeUtils.convert_to_timezone(
                    data[key], target_timezone
                )
        return data
