import os
import hashlib

from django.conf import settings
from binary_database_files import settings as _settings


def is_fresh(name, content_hash):
    """
    Returns true if the file exists on the local filesystem and matches the
    content in the database. Returns false otherwise.
    """
    if not content_hash:
        return False

    # Check that the actual file exists.
    fqfn = os.path.join(settings.MEDIA_ROOT, name)
    fqfn = os.path.normpath(fqfn)
    if not os.path.isfile(fqfn):
        return False

    # Check for cached hash file.
    hash_fn = get_hash_fn(name)
    if os.path.isfile(hash_fn):
        return open(hash_fn).read().strip() == content_hash

    # Otherwise, calculate the hash of the local file.
    fqfn = os.path.join(settings.MEDIA_ROOT, name)
    fqfn = os.path.normpath(fqfn)
    if not os.path.isfile(fqfn):
        return False
    local_content_hash = get_file_hash(fqfn)
    return local_content_hash == content_hash


def get_hash_fn(name):
    """
    Returns the filename for the hash file.
    """
    fqfn = os.path.join(settings.MEDIA_ROOT, name)
    fqfn = os.path.normpath(fqfn)
    fqfn_parts = os.path.split(fqfn)
    if not os.path.isdir(fqfn_parts[0]):
        os.makedirs(fqfn_parts[0])
    hash_fn = os.path.join(
        fqfn_parts[0], _settings.DB_FILES_DEFAULT_HASH_FN_TEMPLATE % fqfn_parts[1]
    )
    return hash_fn


def write_file(name, content, overwrite=False):
    """
    Writes the given content to the relative filename under the MEDIA_ROOT.
    """
    fqfn = os.path.join(settings.MEDIA_ROOT, name)
    fqfn = os.path.normpath(fqfn)
    if os.path.isfile(fqfn) and not overwrite:
        return
    fqfn_parts = os.path.split(fqfn)
    if not os.path.isdir(fqfn_parts[0]):
        os.makedirs(fqfn_parts[0])
    open(fqfn, "wb").write(content)

    # Cache hash.
    hash_value = get_file_hash(fqfn)
    hash_fn = get_hash_fn(name)
    try:
        value = bytes(hash_value, "utf-8")
    except TypeError:
        value = hash_value
    open(hash_fn, "wb").write(value)

    # Set ownership and permissions.
    uname = getattr(settings, "DATABASE_FILES_USER", None)
    gname = getattr(settings, "DATABASE_FILES_GROUP", None)
    if gname:
        gname = ":" + gname
    if uname:
        os.system('chown -RL %s%s "%s"' % (uname, gname, fqfn_parts[0]))

    # Set permissions.
    perms = getattr(settings, "DATABASE_FILES_PERMS", None)
    if perms:
        os.system('chmod -R %s "%s"' % (perms, fqfn_parts[0]))


def get_file_hash(fin, force_encoding=None, encoding=None, errors=None, chunk_size=128):
    """
    Iteratively builds a file hash without loading the entire file into memory.
    """

    force_encoding = force_encoding or _settings.DB_FILES_DEFAULT_ENFORCE_ENCODING

    encoding = encoding or _settings.DB_FILES_DEFAULT_ENCODING

    errors = errors or _settings.DB_FILES_DEFAULT_ERROR_METHOD

    if isinstance(fin, str):
        fin = open(fin, "rb")
    h = hashlib.sha512()
    while True:
        text = fin.read(chunk_size)
        if not text:
            break
        if force_encoding:
            if not isinstance(text, str):
                text = str(text, encoding=encoding, errors=errors)
            h.update(text.encode(encoding, errors))
        else:
            h.update(text)
    return h.hexdigest()


def get_text_hash_0004(text):
    """
    Returns the hash of the given text.
    """
    h = hashlib.sha512()
    if not isinstance(text, str):
        text = str(text, encoding="utf-8", errors="replace")
    h.update(text.encode("utf-8", "replace"))
    return h.hexdigest()


def get_text_hash(text, force_encoding=None, encoding=None, errors=None):
    """
    Returns the hash of the given text.
    """

    force_encoding = force_encoding or _settings.DB_FILES_DEFAULT_ENFORCE_ENCODING

    encoding = encoding or _settings.DB_FILES_DEFAULT_ENCODING

    errors = errors or _settings.DB_FILES_DEFAULT_ERROR_METHOD

    h = hashlib.sha512()
    if force_encoding:
        if not isinstance(text, str):
            text = str(text, encoding=encoding, errors=errors)
        h.update(text.encode(encoding, errors))
    else:
        h.update(text)
    return h.hexdigest()
