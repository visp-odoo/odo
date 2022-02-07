from odoo import models,fields,api
from odoo.exceptions import UserError, ValidationError




class MyTest(models.Model):
    _name = 'my.test'
    _description = 'My Test'
    
    
    name = fields.Char()
    address = fields.Text()
    email = fields.Char()
    pincode = fields.Integer()
    
class v1(models.Model):
    _inherit = 'my.test'
    
    country = fields.Char()
    State = fields.Char()
    city = fields.Char()
    
class v2(models.Model):
    _name = 'v2'
    _inherit = 'my.test' 
    
    pancard = fields.Char()
    aadhar = fields.Char()
    
    
class v3(models.Model):
    _name = 'v3'
    _inherit = {'my.test':'test_id',}
    
    
    test_id =fields.Many2one('my.test')   
    
     
class EstateProperty(models.Model):
    _inherit = 'estate.property'

    bankname = fields.Char()
    bankinterest = fields.Float()