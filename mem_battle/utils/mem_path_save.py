def user_directory_path(instance, filename):
    return 'mem/{0}/{1}'.format(instance.owner.id, filename)