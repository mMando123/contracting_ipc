"""
API module for Contracting IPC.

Contains whitelisted methods that can be called from client-side.
"""

import frappe
from frappe import _
from frappe.utils import flt


@frappe.whitelist()
def get_project_details(project: str) -> dict:
    """
    Get project details for populating IPC fields.
    
    Args:
        project: Project name
        
    Returns:
        Dictionary with project details
    """
    if not project:
        return {}
    
    project_doc = frappe.get_doc("Project", project)
    
    return {
        "customer": project_doc.customer,
        "company": project_doc.company,
        "project_name": project_doc.project_name
    }


@frappe.whitelist()
def get_contract_details(contract: str) -> dict:
    """
    Get contract details for populating IPC fields.
    
    Args:
        contract: Contract name
        
    Returns:
        Dictionary with contract details
    """
    if not contract:
        return {}
    
    contract_doc = frappe.get_doc("Contract", contract)
    
    return {
        "customer": contract_doc.party_name,
        "contract_value": flt(contract_doc.contract_value) if hasattr(contract_doc, 'contract_value') else 0
    }


@frappe.whitelist()
def get_ipc_totals_by_project(project: str) -> dict:
    """
    Get cumulative IPC totals for a project.
    
    Args:
        project: Project name
        
    Returns:
        Dictionary with cumulative totals
    """
    if not project:
        return {}
    
    totals = frappe.db.sql(
        """
        SELECT
            SUM(total_work_done) as total_work_done,
            SUM(retention_amount) as total_retention,
            SUM(advance_deduction) as total_advance,
            SUM(net_amount) as total_net,
            COUNT(*) as ipc_count
        FROM
            `tabIPC`
        WHERE
            project = %s
            AND docstatus = 1
        """,
        project,
        as_dict=1
    )
    
    if totals:
        return totals[0]
    
    return {
        "total_work_done": 0,
        "total_retention": 0,
        "total_advance": 0,
        "total_net": 0,
        "ipc_count": 0
    }


@frappe.whitelist()
def get_pending_ipcs(customer: str = None, project: str = None) -> list:
    """
    Get list of pending (approved but not invoiced) IPCs.
    
    Args:
        customer: Optional customer filter
        project: Optional project filter
        
    Returns:
        List of pending IPC documents
    """
    filters = {
        "docstatus": 1,
        "status": "Approved",
        "sales_invoice": ["is", "not set"]
    }
    
    if customer:
        filters["customer"] = customer
    
    if project:
        filters["project"] = project
    
    return frappe.get_all(
        "IPC",
        filters=filters,
        fields=["name", "customer", "project", "net_amount", "period_from", "period_to"],
        order_by="creation desc"
    )
