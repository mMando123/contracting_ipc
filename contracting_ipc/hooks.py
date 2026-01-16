app_name = "contracting_ipc"
app_title = "Contracting IPC"
app_publisher = "Your Company"
app_description = "Interim Payment Certificates (IPC) Management for Construction Companies"
app_email = "info@yourcompany.com"
app_license = "MIT"
app_version = "1.0.0"

# Required Apps
required_apps = ["frappe", "erpnext"]

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
app_include_css = "/assets/contracting_ipc/css/contracting_ipc.bundle.css"
app_include_js = "/assets/contracting_ipc/js/contracting_ipc.bundle.js"

# include js, css files in header of web template
# web_include_css = "/assets/contracting_ipc/css/contracting_ipc.css"
# web_include_js = "/assets/contracting_ipc/js/contracting_ipc.js"

# include custom scss in every website theme (without signing in).
# scss: "contracting_ipc/public/scss/website"

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
doctype_js = {
    "IPC": "contracting_ipc/doctype/ipc/ipc.js"
}

# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Fixtures for exporting custom workflows, roles, etc.
fixtures = [
    {
        "dt": "Workflow",
        "filters": [["document_type", "=", "IPC"]]
    },
    {
        "dt": "Workflow State",
        "filters": [["name", "in", ["Draft", "Pending Approval", "Approved", "Invoiced", "Rejected"]]]
    },
    {
        "dt": "Workflow Action Master",
        "filters": [["name", "in", ["Approve", "Reject", "Request Approval"]]]
    },
    {
        "dt": "Role",
        "filters": [["name", "in", ["IPC Manager", "IPC Approver"]]]
    }
]

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#     "Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
#     "methods": "contracting_ipc.utils.jinja_methods",
#     "filters": "contracting_ipc.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "contracting_ipc.install.before_install"
after_install = "contracting_ipc.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "contracting_ipc.uninstall.before_uninstall"
# after_uninstall = "contracting_ipc.uninstall.after_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "contracting_ipc.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
#     "Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
#     "Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
#     "ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
    "IPC": {
        "validate": "contracting_ipc.contracting_ipc.doctype.ipc.ipc.validate_ipc",
        "on_submit": "contracting_ipc.contracting_ipc.doctype.ipc.ipc.on_submit_ipc",
    }
}

# Scheduled Tasks
# ---------------

# scheduler_events = {
#     "all": [
#         "contracting_ipc.tasks.all"
#     ],
#     "daily": [
#         "contracting_ipc.tasks.daily"
#     ],
#     "hourly": [
#         "contracting_ipc.tasks.hourly"
#     ],
#     "weekly": [
#         "contracting_ipc.tasks.weekly"
#     ],
#     "monthly": [
#         "contracting_ipc.tasks.monthly"
#     ],
# }

# Testing
# -------

# before_tests = "contracting_ipc.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
#     "frappe.desk.doctype.event.event.get_events": "contracting_ipc.event.get_events"
# }

# Override Document Class CRUD Methods
# ------------------------------
#
# override_doctype_dashboards = {
#     "Task": "contracting_ipc.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# User Data Protection
# --------------------

# user_data_fields = [
#     {
#         "doctype": "{doctype_1}",
#         "filter_by": "{filter_by}",
#         "redact_fields": ["{field_1}", "{field_2}"],
#         "partial": 1,
#     },
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
#     "contracting_ipc.auth.validate"
# ]
