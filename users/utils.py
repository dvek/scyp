
def get_full_url(image_field, request):
    if image_field:
        try:
            return request.build_absolute_uri(image_field.url)
        except:
            return None
    return None
