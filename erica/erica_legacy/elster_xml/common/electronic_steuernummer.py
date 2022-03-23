from erica.erica_legacy.pyeric.eric import get_eric_wrapper


def generate_electronic_aktenzeichen(aktenzeichen, bundesland):
    with get_eric_wrapper() as eric_wrapper:
        return eric_wrapper.get_electronic_aktenzeichen(aktenzeichen, bundesland)
