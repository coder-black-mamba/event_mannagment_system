def is_admin(user):
    return user.groups.filter(name="admin").exists()


def is_organizer(user):
    return user.groups.filter(name="organizer").exists()


def is_participant(user):
    return user.groups.filter(name="participant").exists()