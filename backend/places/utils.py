def cover_image_path(instance, filename):
    return 'places/place_{0}/images/{1}'.format(instance.id, filename)


def cover_thumbnail_path(instance, filename):
    return 'places/place_{0}/thumbnails/{1}'.format(instance.id, filename)


def place_image_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/places/place_<id>/<filename>
    return 'places/place_{0}/images/{1}'.format(instance.place.id, filename)


def place_thumbnail_path(instance, filename):
    return 'places/place_{0}/thumbnails/{1}'.format(instance.place.id, filename)
