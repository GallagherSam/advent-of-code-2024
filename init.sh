#!/bin/bash

# Check if a number is passed as an argument
if [ -z "$1" ]; then
  echo "Usage: $0 <number>"
  exit 1
fi

# Assign the input number to a variable
NUMBER=$1

# Create a file `private/{number}.notes.txt`
PRIVATE_DIR="private"
NOTES_FILE="$PRIVATE_DIR/$NUMBER.notes.txt"

# Create the `private` directory if it doesn't exist
mkdir -p "$PRIVATE_DIR"

# Create the notes file
touch "$NOTES_FILE"
echo "Created file: $NOTES_FILE"

# Create a directory `day_{number}`
DAY_DIR="day_$NUMBER"

mkdir -p "$DAY_DIR"
echo "Created directory: $DAY_DIR"

# Navigate to the new directory
cd "$DAY_DIR" || { echo "Failed to navigate to directory $DAY_DIR"; exit 1; }

# Create a virtual environment in the new directory
virtualenv venv
echo "Virtual environment created in $DAY_DIR/venv"
