from re import search
from odoo import http
from odoo.http import request
  

class Realestate(http.Controller):
       
       @http.route('/hello', auth="public")
       def hello(self, **kw):
        return "Hello World"
     
     
       @http.route('/hello_user', auth="user")
       def hello_user(self, **kw):
        return "Hello %s" %(request.env.user.name)
     
       @http.route('/hello_templete')
       def hello_templet(self,**kw):
              return request.render('estate.hello_world')
           
           
       @http.route('/hello_template_user')
       def hello_template_user(self,**kw):
              property =  request.env['estate.property'].search([('state', '=', 'sold')])
              print("property  :::",property)
              return request.render('estate.hello_user', { 'user': request.env.user,'property': property })
      
     
   
    
      #  @http.route('/hello_template_user',website = True,auth = 'public')
      #   def hello_template_user(self, **kw):
        #    properties = request.env['estate.property'].search([('state', '=', 'confirm')])
    #    print ("properties ::: ", properties)
      #  return request.render("estate.proerty_user",{})
    # return "Hello world"
        
         #'real_estate.hello_user', { 'user': request.env.user, 'properties': properties }