from erica.shared.model.base_domain_model import BasePayload
from erica.worker.request_processing.erica_input.v1.erica_input import FormDataEst, MetaDataEst


class TaxDeclarationPayload(BasePayload):
    est_data: FormDataEst
    meta_data: MetaDataEst

