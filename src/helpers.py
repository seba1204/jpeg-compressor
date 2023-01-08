import os


def replace_extension(path: str, new_extension: str) -> str:
    """Replace the extension of a file"""
    return os.path.splitext(path)[0] + new_extension


def is_image(path: str) -> bool:
    """Check if the file is an image"""
    return path.endswith((".jpg", ".jpeg", ".png", ".bmp", ".tiff", ".gif", ".webp", ".CR2"))


def join(iterator, seperator):
    """Join an iterator with a seperator"""
    it = map(str, iterator)
    seperator = str(seperator)
    string = next(it, '')
    for s in it:
        string += seperator + s
    return string


def fn_without_ext(path: str) -> str:
    """Get the file name without extension"""
    return os.path.splitext(os.path.basename(path))[0]
