"""
IPC (Interim Payment Certificate) DocType Controller.

This module handles the server-side logic for IPC documents including:
- Automatic calculation of retention and net amounts
- Validation of document data
- Sales Invoice creation
"""

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import flt, getdate


class IPC(Document):
    """Controller class for Interim Payment Certificate (IPC) DocType."""

    def validate(self):
        """Validate the IPC document before saving."""
        self.validate_dates()
        self.calculate_amounts()

    def validate_dates(self):
        """Ensure period_from is before or equal to period_to."""
        if self.period_from and self.period_to:
            if getdate(self.period_from) > getdate(self.period_to):
                frappe.throw(
                    _("Period From date cannot be after Period To date."),
                    title=_("Invalid Date Range")
                )

    def calculate_amounts(self):
        """Calculate retention_amount and net_amount based on inputs."""
        # Calculate retention amount
        total_work_done = flt(self.total_work_done)
        retention_percentage = flt(self.retention_percentage)
        advance_deduction = flt(self.advance_deduction)

        self.retention_amount = flt(
            total_work_done * retention_percentage / 100.0,
            self.precision("retention_amount")
        )

        # Calculate net amount
        self.net_amount = flt(
            total_work_done - self.retention_amount - advance_deduction,
            self.precision("net_amount")
        )

    def on_submit(self):
        """Actions to perform when IPC is submitted."""
        self.db_set("status", "Approved")

    def on_cancel(self):
        """Actions to perform when IPC is cancelled."""
        self.db_set("status", "Draft")

    def before_submit(self):
        """Validate before submission."""
        if flt(self.net_amount) <= 0:
            frappe.throw(
                _("Net Amount must be greater than zero to submit the IPC."),
                title=_("Invalid Amount")
            )


def validate_ipc(doc, method=None):
    """Hook function for IPC validation."""
    doc.validate_dates()
    doc.calculate_amounts()


def on_submit_ipc(doc, method=None):
    """Hook function for IPC submission."""
    pass  # Additional submit logic can be added here


@frappe.whitelist()
def create_sales_invoice(ipc_name: str) -> str:
    """
    Create and submit a Sales Invoice from an IPC document.

    Args:
        ipc_name: Name of the IPC document

    Returns:
        Name of the created Sales Invoice
    """
    # Get the IPC document
    ipc = frappe.get_doc("IPC", ipc_name)

    # Validate IPC state
    if ipc.docstatus != 1:
        frappe.throw(
            _("IPC must be submitted before creating a Sales Invoice."),
            title=_("Invalid Operation")
        )

    if ipc.sales_invoice:
        frappe.throw(
            _("A Sales Invoice ({0}) already exists for this IPC.").format(ipc.sales_invoice),
            title=_("Duplicate Invoice")
        )

    if ipc.status == "Invoiced":
        frappe.throw(
            _("This IPC has already been invoiced."),
            title=_("Already Invoiced")
        )

    # Get company settings for income account
    company = frappe.get_doc("Company", ipc.company)
    default_income_account = company.default_income_account

    if not default_income_account:
        frappe.throw(
            _("Please set Default Income Account in Company {0}").format(ipc.company),
            title=_("Missing Configuration")
        )

    # Get customer default currency or company currency
    customer = frappe.get_doc("Customer", ipc.customer)
    currency = customer.default_currency or company.default_currency

    # Create Sales Invoice
    sales_invoice = frappe.new_doc("Sales Invoice")
    sales_invoice.customer = ipc.customer
    sales_invoice.company = ipc.company
    sales_invoice.currency = currency
    sales_invoice.project = ipc.project
    sales_invoice.ipc = ipc_name  # Custom link field

    # Set posting date
    sales_invoice.posting_date = frappe.utils.today()
    sales_invoice.due_date = frappe.utils.add_days(frappe.utils.today(), 30)

    # Add item for IPC work done
    description = _("Interim Payment Certificate: {0}\nPeriod: {1} to {2}").format(
        ipc_name,
        frappe.format_value(ipc.period_from, {"fieldtype": "Date"}),
        frappe.format_value(ipc.period_to, {"fieldtype": "Date"})
    )

    sales_invoice.append("items", {
        "item_name": _("IPC - Work Done"),
        "description": description,
        "qty": 1,
        "rate": flt(ipc.net_amount),
        "amount": flt(ipc.net_amount),
        "income_account": default_income_account,
        "project": ipc.project,
        "cost_center": company.cost_center
    })

    # Set taxes and charges if available
    # This can be customized based on customer/company tax settings

    # Insert and submit the invoice
    sales_invoice.flags.ignore_permissions = True
    sales_invoice.insert()
    sales_invoice.submit()

    # Update IPC with Sales Invoice reference and status
    frappe.db.set_value("IPC", ipc_name, {
        "sales_invoice": sales_invoice.name,
        "status": "Invoiced"
    })

    # Update workflow state if workflow is active
    if frappe.db.exists("Workflow", {"document_type": "IPC", "is_active": 1}):
        frappe.db.set_value("IPC", ipc_name, "workflow_state", "Invoiced")

    frappe.db.commit()

    frappe.msgprint(
        _("Sales Invoice {0} created successfully.").format(
            frappe.utils.get_link_to_form("Sales Invoice", sales_invoice.name)
        ),
        title=_("Invoice Created"),
        indicator="green"
    )

    return sales_invoice.name


@frappe.whitelist()
def get_ipc_dashboard_data(ipc_name: str) -> dict:
    """
    Get dashboard data for an IPC document.

    Args:
        ipc_name: Name of the IPC document

    Returns:
        Dictionary containing dashboard data
    """
    ipc = frappe.get_doc("IPC", ipc_name)

    data = {
        "total_work_done": flt(ipc.total_work_done),
        "retention_amount": flt(ipc.retention_amount),
        "advance_deduction": flt(ipc.advance_deduction),
        "net_amount": flt(ipc.net_amount),
        "status": ipc.status,
        "has_invoice": bool(ipc.sales_invoice),
        "invoice_name": ipc.sales_invoice
    }

    return data
