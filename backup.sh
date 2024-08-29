#!/bin/bash

# YOU MUST HAVE THE MYSQL CONFIGURATIONS PRESENT IN config.yaml IN ORDER
# FOR THIS SCRIPT TO WORK.

# Path to the YAML file
YAML_FILE="properties.yaml"

# Extracting values from the YAML file
USER=$(grep 'user:' $YAML_FILE | awk '{print $2}')
PASSWORD=$(grep 'password:' $YAML_FILE | awk '{print $2}')
HOST=$(grep 'host:' $YAML_FILE | awk '{print $2}')
DB_NAME=$(grep 'database:' $YAML_FILE | awk '{print $2}')

# Other options
BACKUP_PATH="$(pwd)/backups"
DATE=$(date +"%Y-%m-%d_%H-%M-%S")
BACKUP_NAME="${DB_NAME}_backup_${DATE}.sql"

# Create backup
mysqldump -u $USER -p$PASSWORD -h $HOST $DB_NAME > $BACKUP_PATH/$BACKUP_NAME

# Print completion message
echo "Backup completed: $BACKUP_PATH/$BACKUP_NAME"


