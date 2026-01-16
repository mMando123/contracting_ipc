# Contracting IPC - Deployment Guide

## Prerequisites

- Frappe Bench (v15+)
- ERPNext (v15+)
- Python 3.10+
- Node.js 18+
- MariaDB 10.6+ or PostgreSQL 12+

## Installation

### Development Installation

```bash
# Navigate to your bench directory
cd ~/frappe-bench

# Get the app from git repository
bench get-app https://github.com/your-org/contracting_ipc
# OR from local path
bench get-app /path/to/contracting_ipc

# Install on your site
bench --site your-site.local install-app contracting_ipc

# Run migrations
bench --site your-site.local migrate

# Clear cache
bench --site your-site.local clear-cache

# Restart bench
bench restart
```

### Production Installation

```bash
# Get the app
cd ~/frappe-bench
bench get-app https://github.com/your-org/contracting_ipc

# Install on production site
bench --site production-site.com install-app contracting_ipc

# Run migrations
bench --site production-site.com migrate

# Build assets for production
bench build --production

# Restart supervisor
sudo supervisorctl restart all
```

## Post-Installation Setup

### 1. Assign Roles

Navigate to **User → Roles** and assign the following roles to appropriate users:

- **IPC Manager**: Can create and submit IPCs for approval
- **IPC Approver**: Can approve/reject IPCs and create invoices

### 2. Configure Workflow (Optional)

The app creates an approval workflow automatically. To customize:

1. Go to **Workflow List**
2. Find "IPC Approval Workflow"
3. Modify states and transitions as needed

### 3. Set Default Income Account

Ensure your Company has a **Default Income Account** set:
1. Go to **Company → Your Company**
2. Set the "Default Income Account" field

### 4. Custom Field on Sales Invoice

The app adds an "IPC" link field to Sales Invoice. Verify it exists:
1. Go to **Customize Form → Sales Invoice**
2. Look for the "IPC" field

## Usage

### Creating an IPC

1. Go to **Contracting IPC → IPC**
2. Click **+ Add IPC**
3. Fill in:
   - Customer
   - Project
   - Contract (optional)
   - Period dates
   - Total Work Done amount
   - Retention Percentage (default 10%)
   - Advance Deduction (if any)
4. Save the document

### Approval Workflow

1. IPC Manager creates IPC and clicks **Request Approval**
2. IPC Approver reviews and clicks **Approve** or **Reject**
3. Once approved, the IPC is submitted

### Creating Sales Invoice

1. Open an approved/submitted IPC
2. Click **Actions → Create Sales Invoice**
3. Confirm the creation
4. The Sales Invoice is automatically created and linked

## Fixtures

To export/import fixtures:

```bash
# Export fixtures
bench --site your-site.local export-fixtures --app contracting_ipc

# Import fixtures (happens automatically on install/migrate)
bench --site your-site.local import-fixture contracting_ipc
```

## Running Tests

```bash
# Run all tests for the app
bench --site test-site.local run-tests --app contracting_ipc

# Run specific test file
bench --site test-site.local run-tests \
    --module contracting_ipc.contracting_ipc.doctype.ipc.test_ipc
```

## Troubleshooting

### Workflow Not Working

1. Check if workflow is active: **Workflow → IPC Approval Workflow**
2. Verify the `workflow_state` field exists in IPC DocType
3. Check if user has required roles

### Sales Invoice Creation Fails

1. Verify Company has Default Income Account set
2. Check if user has permission to create Sales Invoices
3. Review error logs: **Error Log**

### Permission Denied

1. Check user roles in **User → Roles**
2. Verify Role Permissions for IPC DocType
3. Check if workflow state allows editing

## Uninstallation

```bash
# Uninstall from site
bench --site your-site.local uninstall-app contracting_ipc

# Remove app
bench remove-app contracting_ipc
```

## Support

For issues and feature requests, please create an issue on the GitHub repository.
