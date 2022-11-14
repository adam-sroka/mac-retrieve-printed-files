# Retrieve Printed Files on Mac 🖨🗂

## What is this?

This script will retrieve information (e.g. name, time of printing) about all files ever printed on your Mac[^1], **and _possibly_ also the original files, even if they've been deleted**.

<!--TODO add gif:-->

## How do I do it?

Download this repository from [here](https://codeberg.org/adam/mac-retrieve-printed-files/archive/main.zip), unzip it, open up terminal in the folder with it, and run the python script as root, i.e. run:

```bash
sudo python retrieve_printed_files.py
```

This will create a new folder with all retrieved files and a csv file with information about every file ever printed, even if the file itself could not be recovered.

Root privileges are needed to access the protected directory where the print history is stored. Feel free to examine [the script](/retrieve_printed_files.py) before running it, its only about a hundred lines.

## How does this work?

<!--TODO explain, and add blog post link-->

## Acknowledgements

Thanks for [go-cups-control-files](https://github.com/ui-kreinhard/go-cups-control-files) and for [How to dissect a CUPS job control file](https://stackoverflow.com/questions/53688075/how-to-dissect-a-cups-job-control-file-var-spool-cups-cnnnnnn/53688639#53688639); this would not exist without these.

[^1]: And also on any other Linux system using [CUPS](https://www.cups.org/), Apple's open-source system for printing.