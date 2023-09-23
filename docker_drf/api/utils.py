import os


def get_image_path(instance, filename):
    return os.path.join('images', '%s' % str(instance.id), filename)


def get_image_thumb_path(instance, filename):
    return os.path.join('images', '%s' % str(instance.id), 'thumbnail', filename)
