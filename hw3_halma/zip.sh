#!/bin/bash

# Check if correct number of arguments is provided
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <directory> <zip_file>"
    exit 1
fi

# Assign arguments to variables
DIR="$1"
ZIP_FILE="$2"

# Check if the directory exists
if [ ! -d "$DIR" ]; then
    echo "Error: Directory '$DIR' does not exist."
    exit 1
fi

# Create the zip file
zip -r "$ZIP_FILE" "$DIR"

# Check if the zip command was successful
if [ $? -eq 0 ]; then
    echo "Successfully created $ZIP_FILE from $DIR"
else
    echo "Error: Failed to create zip file."
    exit 1
fi
