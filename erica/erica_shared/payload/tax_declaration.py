from erica.erica_shared.model.base_domain_model import BasePayload
from erica.erica_worker.request_processing.erica_input.v1.erica_input import FormDataEst, MetaDataEst


class TaxDeclarationPayload(BasePayload):
    est_data: FormDataEst
    meta_data: MetaDataEst

