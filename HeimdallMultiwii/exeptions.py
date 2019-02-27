#!/usr/bin/env python3


class HeimdallError(Exception):
    """Base class for other exceptions"""
    pass


class WrongPortError(HeimdallError):
    """Raised when a wrong port is used por establish connection"""
    pass


class ClosedConnectionError(HeimdallError):
    """Raised when try get or send a message when the connection is closed"""
    pass


class MissingCodeError(HeimdallError):
    """Raised when no MSP code was especified"""
    pass
