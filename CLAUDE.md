# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is a utility tools repository focusing on database operations, currently containing a MySQL table export tool. The codebase is organized by programming language, with Python tools under the `python/` directory.

## Key Projects

### tab_exp (MySQL Table Export Tool)
**Location**: `python/tab_exp/`
**Purpose**: Complete MySQL table export including structure, data, indexes, constraints, and character sets
**Main file**: `python/tab_exp/tab_exp.py`

## Development Commands

### Setting up tab_exp
```bash
cd python/tab_exp
pip install -r requirements.txt
```

### Running tab_exp
```bash
# Basic export to SQL file
python tab_exp.py --source user:pass@host:port/db --source-table table_name --output output.sql

# Direct database-to-database migration
python tab_exp.py --source user:pass@host:port/sourcedb --source-table src_table \
                  --target user:pass@host:port/targetdb --target-table dst_table --execute

# With verbose logging
python tab_exp.py --source user:pass@host:port/db --source-table table_name -v --output output.sql
```

## Architecture Patterns

### tab_exp Architecture
- **DatabaseConnector Class**: Manages database connections, validates table existence, handles connection pooling
- **TableExporter Class**: Core export engine that:
  - Uses `SHOW CREATE TABLE` to capture complete DDL including all constraints
  - Generates INSERT statements with proper escaping and type handling
  - Supports both file output and direct database execution modes
- **Connection String Format**: `user:password@host:port/database` for simplified connection specification
- **Error Handling**: Comprehensive exception handling with user-friendly messages for common scenarios (connection failures, missing tables, permission issues)

### Data Model Context
The `python/tab_exp/results/` directory contains SQL exports from a power station data warehouse with:
- Fact tables: `fact_powerstation`
- Dimension tables: `dim_country`, `dim_date`, `dim_location`, `dim_region`
- Dictionary tables: `dict_coal_type`, `dict_powerstation_status`, `dict_powerstation_tech_type`
- Aggregation tables: `agg_powerstation_by_country`, `agg_powerstation_by_tech`
- Data quality tables: `dq_powerstation_metrics`

## Important Conventions

1. **Connection Parameters**: Tools support both connection string format and individual parameter format for flexibility
2. **Character Set**: Always use utf8mb4 for MySQL connections to ensure maximum compatibility
3. **Table Existence Handling**: When target table exists, provide user options: drop/recreate, insert only, or cancel
4. **SQL Export Format**: Include `SET FOREIGN_KEY_CHECKS=0/1` wrapper and `SET sql_mode` for safe imports

## Repository State

**Note**: This repository currently has no git commit history. When making changes, ensure proper git workflow is followed.

## Language-Specific Notes

### Python
- Python 3.x required
- Use virtual environments for dependency isolation
- PyMySQL is the preferred MySQL connector (not mysqlclient or MySQL-python)