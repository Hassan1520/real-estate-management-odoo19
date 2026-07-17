# Real State

Real State is a production-oriented Odoo 19 module for managing real-estate properties, owners, buildings, tags, history tracking, and related sales workflows. It is designed as a practical, open-source example of a clean custom module structure for ERP teams and developers.

## Why this project exists
This repository demonstrates how to build a maintainable Odoo custom module using modern conventions: clear model design, secure access control, workflow logic, XML views, reporting

## Features
- Property lifecycle management through draft, pending, sold, and closed states
- Ownership and building record management
- Tagging and property line detail tracking
- State history for auditing and traceability
- Sale order integration with related properties
- Excel export and PDF report support
- Security groups and access rules for real-world usage

## Tech Stack
- Odoo 19
- Python 3
- XML views and QWeb reports
- CSV-based ACL configuration

## Installation
1. Clone or copy the module into your Odoo custom addons path.
2. Update your apps list.
3. Install the module from the Odoo Apps menu.
4. Grant the appropriate security group access to users.

## Project Structure
- models/: ORM models and business logic
- views/: list, form, search, and menu definitions
- security/: groups, ACLs, and record rules
- wizard/: transient state-change wizard
- reports/: QWeb and Excel report definitions
- data/: sequences and initialization data

## Module Architecture
- Core models: property, owner, tag, building, property.history
- Extended models: sale.order and res.partner
- Interfaces: list/form/search views and menus
- Security: group-based permissions and record rules

## Roadmap
- Add richer workflow rules and approvals
- Introduce advanced dashboards and analytics
- Expand reporting and export capabilities
- Add more automated test coverage for inheritance logic

