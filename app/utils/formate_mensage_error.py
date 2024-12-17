def format_message_error(e):
    message_error = "; ".join(
        msg for field_errors in e.messages.values() for msg in field_errors
    )
    if "length 11" in message_error:
        message_error = "CPF deve ter 11 dígitos"
    return message_error
