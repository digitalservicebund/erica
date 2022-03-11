from erica.erica_legacy.elster_xml.transfer_header_fields import TransferHeaderFields
from erica.erica_legacy.pyeric.eric import get_eric_wrapper


def add_transfer_header(base_xml: str, th_fields: TransferHeaderFields):
    """ Lets ERiC add a <TransferHeader> field with the according th_fields for xml_top.

    :param base_xml: the xml to add the transfer header to
    :param th_fields: the transfer header fields to include
    """
    with get_eric_wrapper() as eric_wrapper:
        xml_string_with_th = eric_wrapper.create_th(
            base_xml,
            datenart=th_fields.datenart, testmerker=th_fields.testmerker,
            herstellerId=th_fields.herstellerId, verfahren=th_fields.verfahren,
            datenLieferant=th_fields.datenLieferant)

        return xml_string_with_th.decode()
