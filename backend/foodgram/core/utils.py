ADMIN_GROUP_NAME = 'admins'

def isInAdminGroup(user):
    return user.groups.filter(name=ADMIN_GROUP_NAME).exists()