"""
IPC Summary Report.

Provides a summary view of all IPCs with filtering options.
"""

import frappe
from frappe import _


def execute(filters=None):
    """Execute the IPC Summary report."""
    columns = get_columns()
    data = get_data(filters)
    return columns, data


def get_columns():
    """Define report columns."""
    return [
        {
            "fieldname": "name",
            "label": _("IPC"),
            "fieldtype": "Link",
            "options": "IPC",
            "width": 120
        },
        {
            "fieldname": "customer",
            "label": _("Customer"),
            "fieldtype": "Link",
            "options": "Customer",
            "width": 150
        },
        {
            "fieldname": "project",
            "label": _("Project"),
            "fieldtype": "Link",
            "options": "Project",
            "width": 150
        },
        {
            "fieldname": "company",
            "label": _("Company"),
            "fieldtype": "Link",
            "options": "Company",
            "width": 120
        },
        {
            "fieldname": "period_from",
            "label": _("From"),
            "fieldtype": "Date",
            "width": 100
        },
        {
            "fieldname": "period_to",
            "label": _("To"),
            "fieldtype": "Date",
            "width": 100
        },
        {
            "fieldname": "total_work_done",
            "label": _("Total Work Done"),
            "fieldtype": "Currency",
            "width": 130
        },
        {
            "fieldname": "retention_amount",
            "label": _("Retention"),
            "fieldtype": "Currency",
            "width": 110
        },
        {
            "fieldname": "advance_deduction",
            "label": _("Advance Deduction"),
            "fieldtype": "Currency",
            "width": 130
        },
        {
            "fieldname": "net_amount",
            "label": _("Net Amount"),
            "fieldtype": "Currency",
            "width": 120
        },
        {
            "fieldname": "status",
            "label": _("Status"),
            "fieldtype": "Data",
            "width": 100
        },
        {
            "fieldname": "sales_invoice",
            "label": _("Sales Invoice"),
            "fieldtype": "Link",
            "options": "Sales Invoice",
            "width": 120
        }
    ]


def get_data(filters):
    """Fetch report data based on filters."""
    conditions = get_conditions(filters)

    data = frappe.db.sql(
        """
        SELECT
            name,
            customer,
            project,
            company,
            period_from,
            period_to,
            total_work_done,
            retention_amount,
            advance_deduction,
            net_amount,
            status,
            sales_invoice
        FROM
            `tabIPC`
        WHERE
            docstatus < 2
            {conditions}
        ORDER BY
            creation DESC
        """.format(conditions=conditions),
        filters,
        as_dict=1
    )

    return data


def get_conditions(filters):
    """Build SQL conditions based on filters."""
    conditions = ""

    if filters.get("company"):
        conditions += " AND company = %(company)s"

    if filters.get("customer"):
        conditions += " AND customer = %(customer)s"

    if filters.get("project"):
        conditions += " AND project = %(project)s"

    if filters.get("status"):
        conditions += " AND status = %(status)s"

    if filters.get("from_date"):
        conditions += " AND period_from >= %(from_date)s"

    if filters.get("to_date"):
        conditions += " AND period_to <= %(to_date)s"

    return conditions
