"""
All of Easy Player exceptions are here.
"""

class EasyPlayerError(Exception):
    pass


class EasyPlayerWarning(Warning):
    pass


class EasyPlayerSaverError(EasyPlayerError):
    pass


class EasyPlayerModuleError(EasyPlayerError, ModuleNotFoundError):
    pass


class EasyPlayerOSError(EasyPlayerError, OSError):
    pass


class EasyPlayerHandleError(EasyPlayerOSError):
    pass


class EasyPlayerWidgetsError(EasyPlayerError):
    pass


class EasyPlayerCanvasError(EasyPlayerWidgetsError):
    pass


class EasyPlayerCameraError(EasyPlayerWidgetsError):
    pass


class EasyPlayerTextTooLongError(EasyPlayerWidgetsError):
    pass


class EasyPlayerOnlyReadError(EasyPlayerError):
    pass


class EasyPlayerCoordinateError(EasyPlayerError):
    pass


class EasyPlayerTranslateError(EasyPlayerError):
    pass


class EasyPlayerChatterError(EasyPlayerError):
    pass