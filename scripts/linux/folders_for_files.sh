#!/bin/bash

if [[ "$1" == "-h" || "$1" == "--h" || "$1" == "-help" || "$1" == "--help" ]]; then
  echo "Usage: \"./folders_for_files.sh PATH\""
  exit 0
fi

if [ $# -eq 0 ]; then
    echo "No arguments supplied"
    exit 1
fi

if [ ! -d "$1" ]; then
  echo "Folder \"$1\" does not exist."
  exit 1
fi

echo "Working folder: \"$1\""

# https://unix.stackexchange.com/a/9499
OIFS="$IFS"
IFS=$'\n'

VIDEO_FILES=$(find "$1" -maxdepth 1 -type f)
# echo "Found ${#VIDEO_FILES[@]} files" # does not work!!

count=0
success=0
for FILE_PATH in $VIDEO_FILES; do
    let count++
    echo "=============================================="
    echo "Processing file \"$FILE_PATH\""

    file_name=$(basename $FILE_PATH)
    echo "File name: \"$file_name\""

    folder_name=${file_name%.*}
    echo "Creating folder \"$folder_name\""
    mkdir $1/$folder_name
    if [ $? -ne 0 ]; then
      continue
    fi

    echo "Moving file to folder"
    mv $FILE_PATH $1/$folder_name
    if [ $? -ne 0 ]; then
      continue
    fi

    echo "Success"
    let success++
done

echo "=============================================="
if [ $count -eq 0 ]; then
  echo "No files found"
else
  echo "$success/$count files processed successfully"
fi

IFS="$OIFS"