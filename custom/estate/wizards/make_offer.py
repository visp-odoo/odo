from odoo import _,fields,models,api


class Makeoffer(models.TransientModel):
    _name = 'make.offer'
    _description = 'Make offer'
    
    price = fields.Float()
    partner_id = fields.Many2one('res.partner')
    
    def Make_Offer(self):
        self.ensure_one()
        activeIds = self.env.context.get('active_ids')
        data = {
            'price': self.price,
            'partner_id': self.partner_id.id,
            #'status': self.status
        }

        for pr in self.env['estate.property'].browse(activeIds):
            pr.write({'property_offer_ids': [(0, 0, data)]})

        