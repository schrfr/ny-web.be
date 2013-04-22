from sitesettings import get_settings


def banners(request):
    """
    Injects in the context the banner paths if set.
    """
    context = {}
    
    settings = get_settings()
    if settings.big_banner and settings.show_big_banner:
        context['big_banner'] = settings.big_banner
        if settings.url_big_banner:
            context['url_big_banner'] = settings.url_big_banner
    if settings.first_small_banner and settings.show_first_small_banner:
        context['first_small_banner'] = settings.first_small_banner
        if settings.url_first_small_banner:
            context['url_first_small_banner'] = settings.url_first_small_banner
    if settings.second_small_banner and settings.show_second_small_banner:
        context['second_small_banner'] = settings.second_small_banner
        if settings.url_second_small_banner:
            context['url_second_small_banner'] = settings.url_second_small_banner
    return context
