#!/usr/bin/env python3
"""
Fix for frappe issue #37623
TableMissingError for Single DocType shortcuts in Workspaces
See: https://github.com/frappe/frappe/issues/37623

This patche reportview.py to return 1 for Single DocTypes (like System Settings,
Buying Settings, etc.) instead of trying to query their table (which doesn't exist,
since Single DocTypes store data in tabSingles).

Remove this file once Frappe releases an official fix.
"""
import os
import sys

filepath = '/home/frappe/frappe-bench/apps/frappe/frappe/desk/reportview.py'

if not os.path.exists(filepath):
    print(f'[fix-37623] ERROR: File not found: {filepath}')
    sys.exit(1)

lines = open(filepath).readlines()

# Check if fix is already applied
if any('issingle' in line for line in lines):
    print('[fix-37623] Fix already applied or integrated in this Frappe version - skipping')
    sys.exit(0)

# Find the insertion point: line after 'args = get_form_params()'
# followed by a line with 'partial_query'
out = []
i = 0
found = False

while i < len(lines):
    out.append(lines[i])
    if 'args = get_form_params()' in lines[i]:
        if i + 1 < len(lines) and 'partial_query' in lines[i + 1]:
            # Determine indentation from the partial_query line
            next_line = lines[i + 1]
            indent = next_line[:len(next_line) - len(next_line.lstrip())]
            # Insert the issingle guard before partial_query
            out.append(f'{indent}if frappe.get_meta(args.doctype).issingle:\n')
            out.append(f'{indent}    return 1\n')
            found = True
            print(f'[fix-37623] Inserted guard at line {i + 1} (indent: {repr(indent)})')
    i += 1

if found:
    open(filepath, 'w').writelines(out)
    print('[fix-37623] Fix applied successfully to reportview.py')
else:
    print('[fix-37623] WARNING: Pattern not found in reportview.py - fix may already be integrated')
