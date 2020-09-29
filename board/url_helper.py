import urllib.request as request
import urllib.error


def is_valid_url(url):
    """Checks if the given `url` is valid and reachable or not."""
    try:
        request.urlopen(url, timeout=5)
        return True
    except urllib.error.HTTPError as error:
        # some websites do not allow access from scripts
        return error.code == 403
    except urllib.error.URLError:
        return False
