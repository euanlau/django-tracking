from django.conf import settings
import re

# this is not intended to be an all-knowing IP address regex
IP_RE = re.compile('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}')

def get_ip(request):
    """
    Retrieves the remote IP address from the request data.  If the user is
    behind a proxy, they may have a comma-separated list of IP addresses, so
    we need to account for that.  In such a case, only the first IP in the
    list will be retrieved.  Also, some hosts that use a proxy will put the
    REMOTE_ADDR into HTTP_X_FORWARDED_FOR.  This will handle pulling back the
    IP from the proper place.
    """

    # if neither header contain a value, just use local loopback
    ip_address = request.META.get('HTTP_X_FORWARDED_FOR',
                                  request.META.get('REMOTE_ADDR', '127.0.0.1'))
    if ip_address:
        # make sure we have one and only one IP
        try:
            ip_address = IP_RE.match(ip_address).group(0)
        except IndexError:
            pass

    return ip_address

def get_timeout():
    """
    gets any specified timeout from the settings file, or use 10 minutes by
    default
    """
    return getattr(settings, 'TRACKING_TIMEOUT', 10)

def get_cleanup_timeout():
    """
    gets any specified visitor clean-up timeout from the settings file, or
    use 24 hours by default
    """
    return getattr(settings, 'TRACKING_CLEANUP_TIMEOUT', 24)

def get_untracked_prefixes():
    """
    gets a list of prefixes that shouldn't be tracked
    """
    return getattr(settings, 'NO_TRACKING_PREFIXES', [])