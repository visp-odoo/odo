from email.policy import default
from odoo import models,fields,api
import datetime
from odoo.exceptions import UserError,ValidationError




class  EstatePropertyType(models.Model):
    _name="estate.property.type"
    _description="Estate Property Type"

    name = fields.Char()
    property_ids=fields.One2many('estate.property','property_type_id')
    
    
    

class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = 'Estate Property Tag'
    _sql_constraints = [('unique_property_tag_name', 'unique(name)', 'Tag cannot be duplicated')]

    name = fields.Char()
    


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property"
    
    
    
    def _get_discription(self):
        print(self.env.user.name)
        # if self.env.context.get('my_property_search'):
        return self.env.user.name + 's property'
    
    
    name = fields.Char(default = "Unknown*",required = True)
    description = fields.Text(default = _get_discription)
    postcode = fields.Char()
    date_availability = fields.Date(default = lambda self: fields.Datetime.now(), copy= False)
    expected_price = fields.Float(required = True)
    selling_price = fields.Float(copy= False, readonly = True)
    bedrooms = fields.Integer(default= 2)
    living_area = fields.Integer()
    buyer = fields.Char()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection([
    	("North", "North"),
    	("South", "South"),
    	("East", "East"),
    	("West", "West")
    	])
    active = fields.Boolean(default=True)
    image = fields.Image()
    property_type_id = fields.Many2one("estate.property.type")
    property_offer_ids = fields.One2many('estate.property.offer', 'property_id')
    best_price = fields.Float(compute="_compute_best_price", store=True)
    salesman_id = fields.Many2one('res.partner',default=lambda self: self.env.user)
    # salesman = fields.Many2one('res.partner',default=lambda self: self.env.user)
    buyer_id = fields.Many2one('res.partner')
    test_id = fields.Many2one('test')
    property_tag_ids = fields.Many2many('estate.property.tag')
    total_area = fields.Integer(compute="_compute_area" ,inverse ="_inverse_area")
    validity = fields.Integer(default = 7)
    date_deadline = fields.Date(compute= "_compute_date_deadline",inverse="_inverse_Days")
    state = fields.Selection([('new', 'New'), ('sold', 'Sold'), ('cancel', 'Cancelled')], default='new')
    
    
    
    def open_offers(self):
        view_id = self.env.ref('estate.estate_property_offer_tree').id
        return {
            "name":"Offers",
            "type":"ir.actions.act_window",
            "res_model":"estate.property.offer",
            "views":[[view_id, 'tree']],
            # "res_id": 2,
            "target":"new",
            "domain": [('property_id', '=', self.id)]
            }

    def confirm_offer(self):
        view_id = self.env.ref('estate.estate_property')
        
    def action_sold(self):
        for rec in self:
            if rec.state == 'cancel':
                raise UserError(("Canceled property cannot be sold"))
            else:
                rec.state = 'sold'

    def action_cancel(self):
        for rec in self:
            if rec.state == 'sold':
                raise UserError(("sold property cannot be cancel"))
            else:
                rec.state = 'cancel'
        
    @api.onchange('garden')
    def _gardenAre(self):
        for record in self:
            if record.garden:
                record.garden_area = 10
                record.garden_orientation = "North"
            else:
                record.garden_area = 0
                record.garden_orientation = None
                
            
                
    @api.depends('living_area','garden_area')
    def _compute_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area
            
            
    def _inverse_area(self):
        for record in self:
            record.living_area = record.garden_area = record.total_area / 2
            
            
                   
    @api.depends('property_offer_ids.price')
    def _compute_best_price(self): 
        for record in self:
            max_price = 0
            for offer in record.property_offer_ids:
                if offer.price > max_price:
                    max_price = offer.price
            record.best_price = max_price

    
    @api.depends('validity')
    def _compute_date_deadline(self):
        for record in self:
            record.date_deadline = fields.Date.add(record.date_availability,days =record.validity)
            
    def _inverse_Days(self):
        for record in self:
            a = record.date_deadline - record.date_availability
            record.validity = a.days
            
    @api.constrains('living_area', 'garden_area')
    def _check_garden_area(self):
        for record in self:
            if record.living_area < record.garden_area:
                raise ValidationError("Garden cannot be bigger than living area")   
    
    
    
class EstatePropertOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Estate Property Offer'
    _order = 'price desc'

    price = fields.Float()
    status = fields.Selection([('accepted', 'Accepted'),('refuse', 'Refused')])
    partner_id = fields.Many2one('res.partner',domain = "[('is_buyer','=',True)]")
    property_id = fields.Many2one('estate.property')
    property_type_ids = fields.Many2one(related='property_id.property_type_id', store=True)
    
    def action_accepted(self):
        for rec in self:
            rec.status = 'accepted'
            rec.property_id.selling_price = rec.price
            rec.property_id.buyer = rec.partner_id
    
    def action_rejected(self):
        for rec in self:
            rec.status = 'refuse'


    

class MyProperty(models.Model):
    _name = "estate.my.property"
    _description = "Estate My Property"
    _inherit = 'estate.property'
    
    
    