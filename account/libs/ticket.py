import base64
import time

from django.conf import settings
from ..utils.string import get_random_string


def generate_ticket(user, device):
    # create a string ticket and save in cache (redis) ttl=60s
    user_id_ascii_encoded = str(user.id).encode("ascii")
    user_id_b64_encoded = base64.b64encode(user_id_ascii_encoded)
    user_id = user_id_b64_encoded.decode("ascii").replace("=", "")

    device_id_ascii_encoded = str(device["id"]).encode("ascii")
    device_id_b64_encoded = base64.b64encode(device_id_ascii_encoded)
    device_id = device_id_b64_encoded.decode("ascii").replace("=", "")

    random_str = get_random_string(16)

    time_ascii_encoded = str(int(time.time())).encode("ascii")
    time_b64_encoded = base64.b64encode(time_ascii_encoded)
    _time = time_b64_encoded.decode("ascii").replace("=", "")

    return "%s.%s.%s.%s" % (random_str, user_id, _time, device_id)


def take_user_id_from_ticket(ticket):
    ticket_has_split = ticket.split(".")
    userID = base64.b64decode(
        ticket_has_split[1] + "=" * (-len(ticket_has_split[1]) % 4)
    )
    return userID.decode("ascii")


def take_life_time_from_ticket(ticket):
    ticket_has_split = ticket.split(".")
    lifetime = base64.b64decode(
        ticket_has_split[2] + "=" * (-len(ticket_has_split[2]) % 4)
    )
    return lifetime.decode("ascii")


def take_device_id_from_ticket(ticket):
    ticket_has_split = ticket.split(".")
    device_id = base64.b64decode(
        ticket_has_split[3] + "=" * (-len(ticket_has_split[3]) % 4)
    )
    return device_id.decode("ascii")


def ticket_is_invalid(ticket):
    if len(ticket.split(".")) % 4:  # 4 is quantity of params in ticket
        return True
    return False


def ticket_is_expired(ticket):
    lifetime = take_life_time_from_ticket(ticket)
    diff_time = (int(time.time()) - int(lifetime)) / 60  # 60 is 60 seconds of minute
    print(diff_time)
    if diff_time < int(settings.TICKET_LIFETIME):
        return False
    return True


def verify_ticket_with_otp(login_ticket, ticket, code):
    if login_ticket != f"{ticket}.{code}":
        return False
    return True
