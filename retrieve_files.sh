#! /bin/bash

# retrieves all files ever printed on this Mac or another system that uses CUPS
# has to be run as sudo

printed_files_directory="/var/spool/cups"

# copy the whole CUPS directory to current directory
cp -r printed_files_directory ./

# add read and write permission to copied directory
chmod 755 cups

# change directory to the copied CUPS directory
cd cups

# rename all pdf files to pdfs
find . -depth -name "d*" -exec sh -c 'f="{}"; mv -- "$f" "${f%}.pdf"' \;
