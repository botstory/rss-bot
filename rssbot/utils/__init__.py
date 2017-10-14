def get_user_first_name_safe(user):
    return user['first_name'] or 'friend'


def inject_first_name(msg, user):
    return msg.replace('{{user_first_name}}', get_user_first_name_safe(user))
