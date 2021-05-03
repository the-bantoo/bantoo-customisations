import frappe
import json
from frappe import _
from frappe import utils
from frappe.utils import getdate, nowdate

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