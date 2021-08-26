class RidgeplotError(Exception):
    """Base ridgeplot exception."""


class InvalidColorscaleError(RidgeplotError):
    """Invalid format or type for colorscale."""
