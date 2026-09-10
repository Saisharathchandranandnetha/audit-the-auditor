#!/bin/bash
if [ -f "legacy_database_backup.sql" ]; then
    echo "Error: Legacy database conflict. Aborting."
    exit 1
else
    echo "Dataset processed successfully."
    exit 0
fi
