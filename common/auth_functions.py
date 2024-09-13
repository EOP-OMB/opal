from django.conf import settings


def prepare_request(request, idp):
    # in some cases, django will get the wrong results when deriving the server url from the request object. This
    # happens mostly if you are behind a proxy or running in a container. in these cases, you can override the
    # derived values by defining a few environment variables
    request_dict = {
        "https": "on" if request.is_secure() else "off",
        "http_host": request.get_host(),
        "script_name": request.path_info,
        "server_port": 443 if request.is_secure() else request.get_port(),
        "get_data": request.GET.copy(),
        "post_data": request.POST.copy(),
        "lowercase_urlencoding": idp.lowercase_encoding,
    }
    if hasattr(settings, "SAML_HTTPS"):
        if settings.SAML_HTTPS:
            request_dict["https"] = settings.SAML_HTTPS
    if hasattr(settings, "SAML_HTTP_HOST"):
        if settings.SAML_HTTP_HOST:
            request_dict["http_host"] = settings.SAML_HTTP_HOST
    if hasattr(settings, "SAML_SCRIPT_NAME"):
        if settings.SAML_SCRIPT_NAME:
            request_dict["script_name"] = settings.SAML_SCRIPT_NAME
    if hasattr(settings, "SAML_SERVER_PORT"):
        if settings.SAML_SERVER_PORT:
            request_dict["server_port"] = settings.SAML_SERVER_PORT
    return request_dict