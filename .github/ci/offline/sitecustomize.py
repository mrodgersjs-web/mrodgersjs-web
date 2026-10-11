"""Loaded by the steward-tests workflow via PYTHONPATH: makes any non-loopback
network access fail, so a test that reaches GitHub or the web fails instead of
silently depending on live data."""
import socket

_connect = socket.socket.connect
_getaddrinfo = socket.getaddrinfo


def _local(host):
    return host in (None, "localhost", "::1") or str(host).startswith("127.")


def _guarded_connect(self, address, *args, **kwargs):
    if self.family == getattr(socket, "AF_UNIX", object()) or (
        isinstance(address, tuple) and _local(address[0])
    ):
        return _connect(self, address, *args, **kwargs)
    raise OSError(f"network disabled in tests: connect to {address!r}")


def _guarded_getaddrinfo(host, *args, **kwargs):
    if _local(host):
        return _getaddrinfo(host, *args, **kwargs)
    raise OSError(f"network disabled in tests: resolve {host!r}")


socket.socket.connect = _guarded_connect
socket.getaddrinfo = _guarded_getaddrinfo
