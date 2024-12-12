from datetime import datetime
import pytz


def get_current_timestamp():
    """
    Retorna o timestamp atual ajustado para o fuso horário de Brasília.
    """
    utc_now = datetime.utcnow().replace(tzinfo=pytz.utc)
    br_tz = pytz.timezone("America/Sao_Paulo")
    return utc_now.astimezone(br_tz).strftime("%Y-%m-%d %H:%M:%S")  # Formatando a data


class DateTimeUtils:
    def convert_to_timezone(dt, target_timezone="UTC"):
        """
        Converte uma data/hora para o fuso horário desejado.

        :param dt: Data/hora no formato datetime ou string.
        :param target_timezone: Fuso horário de destino (padrão é "UTC").
        :return: Data/hora convertida para o fuso horário de destino no formato 'YYYY-MM-DD HH:MM:SS'.
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

    def adjust_times_for_dict(data, target_timezone="UTC"):
        """
        Ajusta os campos de data em um dicionário para o fuso horário desejado.

        :param data: Dicionário contendo os campos de data/hora a serem ajustados.
        :param target_timezone: Fuso horário de destino (padrão é "UTC").
        :return: Dicionário com os campos de data/hora ajustados.
        """
        for key in ["time_created", "time_updated"]:
            if isinstance(
                data[key], (datetime, str)
            ):  # Se o valor for datetime ou string
                data[key] = DateTimeUtils.convert_to_timezone(
                    data[key], target_timezone
                )
        return data
