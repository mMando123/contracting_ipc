"""
Installation hooks for Contracting IPC app.
"""

import frappe
from frappe import _


def after_install():
    """Setup after app installation."""
    create_custom_roles()
    create_ipc_workflow()
    frappe.db.commit()


def create_custom_roles():
    """Create custom roles for IPC management."""
    roles = [
        {
            "role_name": "IPC Manager",
            "desk_access": 1,
            "is_custom": 1
        },
        {
            "role_name": "IPC Approver", 
            "desk_access": 1,
            "is_custom": 1
        }
    ]
    
    for role_data in roles:
        if not frappe.db.exists("Role", role_data["role_name"]):
            role = frappe.new_doc("Role")
            role.update(role_data)
            role.insert(ignore_permissions=True)
            frappe.msgprint(_("Created Role: {0}").format(role_data["role_name"]))


def create_ipc_workflow():
    """Create the IPC approval workflow."""
    workflow_name = "IPC Approval Workflow"
    
    if frappe.db.exists("Workflow", workflow_name):
        return
    
    # Create Workflow States if they don't exist
    workflow_states = [
        {"state": "Draft", "style": "Primary"},
        {"state": "Pending Approval", "style": "Warning"},
        {"state": "Approved", "style": "Success"},
        {"state": "Invoiced", "style": "Success"},
        {"state": "Rejected", "style": "Danger"}
    ]
    
    for ws in workflow_states:
        if not frappe.db.exists("Workflow State", ws["state"]):
            state_doc = frappe.new_doc("Workflow State")
            state_doc.workflow_state_name = ws["state"]
            state_doc.style = ws["style"]
            state_doc.insert(ignore_permissions=True)

    # Create Workflow Actions if they don't exist
    workflow_actions = ["Request Approval", "Approve", "Reject"]
    for action in workflow_actions:
        if not frappe.db.exists("Workflow Action Master", action):
            action_doc = frappe.new_doc("Workflow Action Master")
            action_doc.workflow_action_name = action
            action_doc.insert(ignore_permissions=True)
    
    # Create the workflow
    workflow = frappe.new_doc("Workflow")
    workflow.workflow_name = workflow_name
    workflow.document_type = "IPC"
    workflow.is_active = 1
    workflow.workflow_state_field = "workflow_state"
    workflow.send_email_alert = 0
    
    # Add states
    workflow.append("states", {
        "state": "Draft",
        "doc_status": 0,
        "allow_edit": "IPC Manager"
    })
    workflow.append("states", {
        "state": "Pending Approval",
        "doc_status": 0,
        "allow_edit": "IPC Approver"
    })
    workflow.append("states", {
        "state": "Approved",
        "doc_status": 1,
        "allow_edit": "IPC Approver"
    })
    workflow.append("states", {
        "state": "Invoiced",
        "doc_status": 1,
        "allow_edit": ""
    })
    workflow.append("states", {
        "state": "Rejected",
        "doc_status": 0,
        "allow_edit": "IPC Manager"
    })
    
    # Add transitions
    workflow.append("transitions", {
        "state": "Draft",
        "action": "Request Approval",
        "next_state": "Pending Approval",
        "allowed": "IPC Manager",
        "allow_self_approval": 1
    })
    workflow.append("transitions", {
        "state": "Pending Approval",
        "action": "Approve",
        "next_state": "Approved",
        "allowed": "IPC Approver",
        "allow_self_approval": 0
    })
    workflow.append("transitions", {
        "state": "Pending Approval",
        "action": "Reject",
        "next_state": "Rejected",
        "allowed": "IPC Approver",
        "allow_self_approval": 0
    })
    workflow.append("transitions", {
        "state": "Rejected",
        "action": "Request Approval",
        "next_state": "Pending Approval",
        "allowed": "IPC Manager",
        "allow_self_approval": 1
    })
    
    workflow.insert(ignore_permissions=True)
    frappe.msgprint(_("Created Workflow: {0}").format(workflow_name))
