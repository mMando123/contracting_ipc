// Copyright (c) 2024, Your Company and contributors
// For license information, please see license.txt

frappe.ui.form.on("IPC", {
    /**
     * Form refresh handler - controls UI state and custom buttons
     */
    refresh: function (frm) {
        // Recalculate amounts on refresh
        frm.trigger("calculate_amounts");

        // Add Create Sales Invoice button for submitted IPCs without invoice
        if (frm.doc.docstatus === 1 && !frm.doc.sales_invoice && frm.doc.status !== "Invoiced") {
            frm.add_custom_button(__("Create Sales Invoice"), function () {
                frm.trigger("create_sales_invoice");
            }, __("Actions"));
        }

        // Add link to view Sales Invoice if exists
        if (frm.doc.sales_invoice) {
            frm.add_custom_button(__("View Sales Invoice"), function () {
                frappe.set_route("Form", "Sales Invoice", frm.doc.sales_invoice);
            }, __("View"));
        }

        // Set field indicators based on status
        frm.trigger("set_status_indicator");
    },

    /**
     * Setup handler - runs once when form is loaded
     */
    setup: function (frm) {
        // Set query filters for linked fields
        frm.set_query("project", function () {
            return {
                filters: {
                    "status": ["not in", ["Completed", "Cancelled"]],
                    "company": frm.doc.company || ""
                }
            };
        });

        frm.set_query("contract", function () {
            let filters = {};
            if (frm.doc.customer) {
                filters["party_name"] = frm.doc.customer;
            }
            return { filters: filters };
        });
    },

    /**
     * Customer field change handler
     */
    customer: function (frm) {
        // Clear project if customer changes
        if (frm.doc.customer) {
            frm.set_query("project", function () {
                return {
                    filters: {
                        "customer": frm.doc.customer,
                        "status": ["not in", ["Completed", "Cancelled"]]
                    }
                };
            });
        }
    },

    /**
     * Company field change handler
     */
    company: function (frm) {
        // Update project filter when company changes
        frm.set_query("project", function () {
            return {
                filters: {
                    "company": frm.doc.company,
                    "status": ["not in", ["Completed", "Cancelled"]]
                }
            };
        });
    },

    /**
     * Total work done change handler
     */
    total_work_done: function (frm) {
        frm.trigger("calculate_amounts");
    },

    /**
     * Retention percentage change handler
     */
    retention_percentage: function (frm) {
        frm.trigger("calculate_amounts");
    },

    /**
     * Advance deduction change handler
     */
    advance_deduction: function (frm) {
        frm.trigger("calculate_amounts");
    },

    /**
     * Calculate retention and net amounts
     */
    calculate_amounts: function (frm) {
        let total_work_done = flt(frm.doc.total_work_done) || 0;
        let retention_percentage = flt(frm.doc.retention_percentage) || 0;
        let advance_deduction = flt(frm.doc.advance_deduction) || 0;

        // Calculate retention amount
        let retention_amount = flt(total_work_done * retention_percentage / 100, precision("retention_amount"));
        frm.set_value("retention_amount", retention_amount);

        // Calculate net amount
        let net_amount = flt(total_work_done - retention_amount - advance_deduction, precision("net_amount"));
        frm.set_value("net_amount", net_amount);
    },

    /**
     * Create Sales Invoice action handler
     */
    create_sales_invoice: function (frm) {
        frappe.confirm(
            __("Are you sure you want to create a Sales Invoice for this IPC?"),
            function () {
                frappe.call({
                    method: "contracting_ipc.contracting_ipc.doctype.ipc.ipc.create_sales_invoice",
                    args: {
                        ipc_name: frm.doc.name
                    },
                    freeze: true,
                    freeze_message: __("Creating Sales Invoice..."),
                    callback: function (r) {
                        if (r.message) {
                            frm.reload_doc();
                        }
                    },
                    error: function (r) {
                        frappe.msgprint({
                            title: __("Error"),
                            indicator: "red",
                            message: __("Failed to create Sales Invoice. Please check the error log.")
                        });
                    }
                });
            }
        );
    },

    /**
     * Set status indicator based on document status
     */
    set_status_indicator: function (frm) {
        if (frm.doc.status === "Invoiced") {
            frm.page.set_indicator(__("Invoiced"), "green");
        } else if (frm.doc.status === "Approved") {
            frm.page.set_indicator(__("Approved"), "blue");
        } else {
            frm.page.set_indicator(__("Draft"), "orange");
        }
    },

    /**
     * Validate dates before save
     */
    validate: function (frm) {
        if (frm.doc.period_from && frm.doc.period_to) {
            if (frappe.datetime.str_to_obj(frm.doc.period_from) > frappe.datetime.str_to_obj(frm.doc.period_to)) {
                frappe.msgprint(__("Period From cannot be after Period To"));
                frappe.validated = false;
            }
        }

        // Validate net amount is positive
        if (flt(frm.doc.net_amount) <= 0 && frm.doc.docstatus === 0) {
            frappe.msgprint({
                title: __("Warning"),
                indicator: "orange",
                message: __("Net Amount should be greater than zero for submission.")
            });
        }
    },

    /**
     * Before submit validation
     */
    before_submit: function (frm) {
        if (flt(frm.doc.net_amount) <= 0) {
            frappe.msgprint(__("Cannot submit IPC with Net Amount less than or equal to zero."));
            frappe.validated = false;
        }
    }
});
