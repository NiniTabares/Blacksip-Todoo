from odoo import api, models


class AccountMove(models.Model):
    _inherit = 'account.move'

    def _blacksip_get_invoice_dian_document(self):
        self.ensure_one()
        documentos = self.l10n_co_dian_document_ids.sorted()
        aceptados = documentos.filtered(
            lambda documento: documento.state == 'invoice_accepted'
        )
        return aceptados[:1] or documentos[:1]

    @api.depends(
        'l10n_co_dian_document_ids',
        'l10n_co_dian_document_ids.state',
        'l10n_co_dian_document_ids.attachment_id',
    )
    def _compute_l10n_co_dian_attachment(self):
        for move in self:
            documento = move._blacksip_get_invoice_dian_document()
            move.l10n_co_dian_attachment_id = (
                documento.attachment_id
                if documento.state == 'invoice_accepted'
                else False
            )

    def _l10n_co_dian_get_extra_invoice_report_values(self):
        self.ensure_one()
        valores = super()._l10n_co_dian_get_extra_invoice_report_values()
        documento = self._blacksip_get_invoice_dian_document()

        if documento.state == 'invoice_accepted':
            valores.update({
                'signing_datetime': documento.datetime.replace(
                    microsecond=0
                ),
                'identifier': documento.identifier,
            })

        return valores