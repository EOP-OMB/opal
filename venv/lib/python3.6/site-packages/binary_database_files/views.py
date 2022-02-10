import mimetypes

from django.conf import settings
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.cache import cache_control
from django.views.static import serve as django_serve

from binary_database_files.models import File
from binary_database_files import settings as _settings


@cache_control(max_age=86400)
def serve(request, name):
    """
    Retrieves the file from the database.
    """
    f = get_object_or_404(File, name=name)
    if _settings.DB_FILES_AUTO_EXPORT_DB_TO_FS:
        f.dump()
    mimetype = mimetypes.guess_type(name)[0] or "application/octet-stream"
    # Cast to bytes to work around https://code.djangoproject.com/ticket/30294
    response = HttpResponse(bytes(f.content), content_type=mimetype)
    response["Content-Length"] = f.size
    return response


def serve_mixed(request, *args, **kwargs):
    """
    First attempts to serve the file from the filesystem,
    then tries the database.
    """
    name = kwargs.get("name") or kwargs.get("path")
    document_root = kwargs.get("document_root")
    document_root = document_root or settings.MEDIA_ROOT
    try:
        # First attempt to serve from filesystem.
        return django_serve(request, name, document_root)
    except Http404:
        # Then try serving from database.
        return serve(request, name)
