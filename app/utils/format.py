from datetime import datetime
import pytz


@staticmethod
def clean_point(value):
    return value.replace(".", "").replace("-", "")

@staticmethod
def get_current_timestamp():
    """
    Retorna o timestamp atual ajustado para o fuso horário de Brasília.
    """
    utc_now = datetime.utcnow().replace(tzinfo=pytz.utc)
    br_tz = pytz.timezone("America/Sao_Paulo")
    return utc_now.astimezone(br_tz)

@staticmethod
def adjust_times_for_brasilia(data):
    """
    Ajusta os campos time_created e time_updated para o fuso horário de Brasília.
    Se o campo não tiver um fuso horário (tzinfo), assume-se que está em UTC.
    """
    br_tz = pytz.timezone("America/Sao_Paulo")

    for key in ["time_created", "time_updated"]:
        if key in data:
            data[key] = convert_to_brasilia_time(data[key], br_tz)

    return data

@staticmethod
def convert_to_brasilia_time(dt, br_tz):
    """
    Converte um datetime para o fuso horário de Brasília (UTC-3).
    Se o datetime não tiver timezone, assume-se que é UTC.
    """
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=pytz.utc)  # Assume que está em UTC
    return dt.astimezone(br_tz)

@staticmethod
def format_cpf(cpf):
    formatted_cpf = f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"

    return formatted_cpf
