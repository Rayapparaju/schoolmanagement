import re
import logging
from urllib.parse import quote
from django.conf import settings

logger = logging.getLogger(__name__)


def clean_phone(phone):
    phone = re.sub(r'[^0-9]', '', str(phone))
    if phone.startswith('00'):
        phone = phone[2:]
    if phone.startswith('+'):
        phone = phone[1:]
    if not phone.startswith('91') and len(phone) == 10:
        phone = '91' + phone
    return phone


def generate_wa_link(phone, message):
    cleaned = clean_phone(phone)
    encoded = quote(message)
    return f'https://wa.me/{cleaned}?text={encoded}'


def send_via_twilio(phone, message):
    try:
        from twilio.rest import Client
        account_sid = getattr(settings, 'TWILIO_ACCOUNT_SID', None)
        auth_token = getattr(settings, 'TWILIO_AUTH_TOKEN', None)
        from_number = getattr(settings, 'TWILIO_WHATSAPP_FROM', None)

        if not all([account_sid, auth_token, from_number]):
            logger.warning('Twilio not configured. Set TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_WHATSAPP_FROM in settings.')
            return False

        client = Client(account_sid, auth_token)
        to_number = f'whatsapp:{clean_phone(phone)}'
        from_whatsapp = f'whatsapp:{from_number}'

        client.messages.create(body=message, from_=from_whatsapp, to=to_number)
        return True
    except Exception as e:
        logger.error(f'Twilio send failed: {e}')
        return False
