/**
 * Contracting IPC - Main JavaScript
 * 
 * This file is included in the desk header for global app functionality.
 * Currently no global scripts are needed as IPC-specific logic is in the doctype JS.
 */

// Namespace for Contracting IPC
frappe.provide("contracting_ipc");

contracting_ipc = {
    /**
     * Format currency value with company currency
     */
    format_currency: function (value, company) {
        return format_currency(value, null, 2);
    },

    /**
     * Show notification message
     */
    notify: function (message, indicator) {
        frappe.show_alert({
            message: message,
            indicator: indicator || "green"
        }, 5);
    }
};
