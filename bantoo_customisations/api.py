import frappe
from frappe import _
from future import unicode_literals
from frappe import utils

@frappe.whitelist()
def submit_appointment_request(values):
    
    """frappe.throw(
        title='Error',
        msg='This file does not exist',
        exc=FileNotFoundError
    )"""
    mess
    frappe.msgprint("values: " + str(values))
    frappe.errprint("values: " + str(values))
    return True