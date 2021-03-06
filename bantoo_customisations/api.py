import frappe
import json
from frappe import _
from frappe import utils
from frappe.utils import getdate, nowdate

from urllib.parse import urlencode
from urllib.request import urlopen

@frappe.whitelist(allow_guest=True)
def verify_captcha(token, email, message):
    URL = 'https://www.google.com/recaptcha/api/siteverify'
    private_key = '6Lc2N3MgAAAAAK88fVJ4CeWnSe8oMXnoO__0vCFq'
    params = urlencode({
        'secret': private_key,
        'response': token,
    })

    # print params
    data = urlopen(URL, params.encode('utf-8')).read()
    result = json.loads(data)
    success = result.get('success', None)

    # frappe.errprint( float(result.get('score', 1)) )

    if success == True:
        # frappe.errprint('reCaptcha passed')
        return float( result.get('score', 1) )
    else:
        desc = message +"<br><br><br>Response Object: "+ str(result)
        frappe.errprint('reCaptcha failed')
        create_issue(email, 'reCaptcha failed on Homepage', desc)
        
        return False

def create_issue(email, subject, description):
    issue = frappe.new_doc("Issue")
    issue.raised_by = email
    issue.status = "Open"
    issue.subject = subject
    issue.description = description
    
    return issue.insert(
        ignore_permissions=True, # ignore write permissions during insert
        ignore_mandatory=True # insert even if mandatory fields are not set
    )

@frappe.whitelist(allow_guest=True)
def submit_appointment_request(args):
    frappe.set_user('Administrator')
    values = json.loads(args)
    
    date = values['date']
    time = values['time']
    
    if date and getdate(date) < getdate(nowdate()):
        frappe.throw(_("Date cannot be in the past"))
    
    lead = frappe.new_doc("Lead")
    lead.notes = "Package: " + (str(values['price_package']) or "Not set")
    lead.lead_name = values['first_name'] + " " + values['last_name']
    lead.status = "Open"
    lead.source = "Website"
    lead.email_id = values['email']
    lead.company_name = values['company']
    lead.country = values['country']
    lead.phone = values['phone_number']
    lead.organization_lead = '1'
    lead.contact_by = "tungati.m@gmail.com"
    lead.contact_date = date + " " + time #27-04-2021 22:28 
    
    return lead.insert(
        ignore_permissions=True, # ignore write permissions during insert
        ignore_mandatory=True # insert even if mandatory fields are not set
    )