// Copyright (c) 2024, Your Company and contributors
// For license information, please see license.txt

frappe.query_reports["IPC Summary"] = {
    "filters": [
        {
            "fieldname": "company",
            "label": __("Company"),
            "fieldtype": "Link",
            "options": "Company",
            "default": frappe.defaults.get_user_default("Company")
        },
        {
            "fieldname": "customer",
            "label": __("Customer"),
            "fieldtype": "Link",
            "options": "Customer"
        },
        {
            "fieldname": "project",
            "label": __("Project"),
            "fieldtype": "Link",
            "options": "Project"
        },
        {
            "fieldname": "status",
            "label": __("Status"),
            "fieldtype": "Select",
            "options": "\nDraft\nApproved\nInvoiced"
        },
        {
            "fieldname": "from_date",
            "label": __("From Date"),
            "fieldtype": "Date"
        },
        {
            "fieldname": "to_date",
            "label": __("To Date"),
            "fieldtype": "Date"
        }
    ],

    "formatter": function (value, row, column, data, default_formatter) {
        value = default_formatter(value, row, column, data);

        if (column.fieldname === "status") {
            if (data.status === "Invoiced") {
                value = `<span class="indicator-pill green">${value}</span>`;
            } else if (data.status === "Approved") {
                value = `<span class="indicator-pill blue">${value}</span>`;
            } else {
                value = `<span class="indicator-pill orange">${value}</span>`;
            }
        }

        return value;
    }
};
