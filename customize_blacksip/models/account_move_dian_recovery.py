from unicodedata import combining, normalize

from odoo import _, models
from odoo.exceptions import UserError


EXCLUDED_ZONE_CITIES = frozenset({
    "amazonas", "guainia", "guaviare", "vaupes", "vichada", "san andres",
})
EXCLUDED_ZONE_POSITION = "Zona excluido Amazonas, Guainía, Guaviare, Vaupés, Vichada y San Andres"
REQUIRED_ZONE_POSITIONS = {
    "out_invoice": EXCLUDED_ZONE_POSITION,
    "out_refund": f"Dev {EXCLUDED_ZONE_POSITION}",
}


class AccountMove(models.Model):
    _inherit = "account.move"

    def _post(self, soft=True):
        for move in self:
            if move.move_type not in REQUIRED_ZONE_POSITIONS or move.state != "draft":
                continue

            city = normalize("NFD", (move.partner_id.city or "").casefold())
            city = " ".join("".join(char for char in city if not combining(char)).split())

            # Compare the configured fiscal position name across user languages.
            fiscal_name = (move.fiscal_position_id.with_context(lang=None).name or "").strip()
            if city in EXCLUDED_ZONE_CITIES:
                required_position = REQUIRED_ZONE_POSITIONS[move.move_type]
                if fiscal_name != required_position:
                    raise UserError(_(
                        "Para contabilizar %(document)s con un contacto de %(city)s, "
                        "selecciona la posición fiscal «%(position)s».",
                        document=move.display_name,
                        city=move.partner_id.city,
                        position=required_position,
                    ))
            elif move.move_type == "out_refund" and not fiscal_name.casefold().startswith("dev"):
                raise UserError(_(
                    "Para contabilizar la nota crédito %(document)s, selecciona "
                    "una posición fiscal cuyo nombre empiece por «Dev».",
                    document=move.display_name,
                ))

        return super()._post(soft=soft)
