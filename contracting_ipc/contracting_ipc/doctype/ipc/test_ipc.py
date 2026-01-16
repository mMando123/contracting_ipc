"""
Test cases for IPC DocType.
"""

import frappe
from frappe.tests.utils import FrappeTestCase
from frappe.utils import flt, today, add_days


class TestIPC(FrappeTestCase):
    """Test cases for IPC (Interim Payment Certificate) DocType."""

    @classmethod
    def setUpClass(cls):
        """Set up test data."""
        super().setUpClass()
        cls.create_test_data()

    @classmethod
    def create_test_data(cls):
        """Create necessary test data."""
        # Create test company if not exists
        if not frappe.db.exists("Company", "_Test Company"):
            company = frappe.get_doc({
                "doctype": "Company",
                "company_name": "_Test Company",
                "default_currency": "USD",
                "country": "United States"
            })
            company.insert(ignore_permissions=True)

        # Create test customer if not exists
        if not frappe.db.exists("Customer", "_Test Customer"):
            customer = frappe.get_doc({
                "doctype": "Customer",
                "customer_name": "_Test Customer",
                "customer_type": "Company"
            })
            customer.insert(ignore_permissions=True)

        # Create test project if not exists
        if not frappe.db.exists("Project", "_Test Project"):
            project = frappe.get_doc({
                "doctype": "Project",
                "project_name": "_Test Project",
                "company": "_Test Company"
            })
            project.insert(ignore_permissions=True)

    def get_ipc_doc(self, **kwargs):
        """Create an IPC document with default values."""
        default_values = {
            "doctype": "IPC",
            "customer": "_Test Customer",
            "project": "_Test Project",
            "company": "_Test Company",
            "period_from": today(),
            "period_to": add_days(today(), 30),
            "total_work_done": 100000,
            "retention_percentage": 10,
            "advance_deduction": 5000
        }
        default_values.update(kwargs)
        return frappe.get_doc(default_values)

    def test_retention_calculation(self):
        """Test that retention amount is calculated correctly."""
        ipc = self.get_ipc_doc(
            total_work_done=100000,
            retention_percentage=10
        )
        ipc.insert()

        self.assertEqual(flt(ipc.retention_amount), 10000)

    def test_net_amount_calculation(self):
        """Test that net amount is calculated correctly."""
        ipc = self.get_ipc_doc(
            total_work_done=100000,
            retention_percentage=10,
            advance_deduction=5000
        )
        ipc.insert()

        # net = 100000 - 10000 (retention) - 5000 (advance) = 85000
        self.assertEqual(flt(ipc.net_amount), 85000)

    def test_date_validation(self):
        """Test that period_from must be before period_to."""
        ipc = self.get_ipc_doc(
            period_from=add_days(today(), 30),
            period_to=today()
        )

        with self.assertRaises(frappe.ValidationError):
            ipc.insert()

    def test_zero_retention(self):
        """Test IPC with zero retention percentage."""
        ipc = self.get_ipc_doc(
            total_work_done=100000,
            retention_percentage=0,
            advance_deduction=10000
        )
        ipc.insert()

        self.assertEqual(flt(ipc.retention_amount), 0)
        self.assertEqual(flt(ipc.net_amount), 90000)

    def test_status_default(self):
        """Test that default status is Draft."""
        ipc = self.get_ipc_doc()
        ipc.insert()

        self.assertEqual(ipc.status, "Draft")

    def test_submit_changes_status(self):
        """Test that submitting IPC changes status to Approved."""
        ipc = self.get_ipc_doc()
        ipc.insert()
        ipc.submit()

        ipc.reload()
        self.assertEqual(ipc.status, "Approved")
