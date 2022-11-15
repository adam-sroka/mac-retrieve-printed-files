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

**Security sidenote**

Root privileges are needed to access the protected directory where the print history is stored. Feel free to examine [the python script](/retrieve_printed_files.py) before running it; it's only about a hundred lines.

Alternatively, you can also run the bare-bones [shell script](/retrieve_files.sh) from this repo, which only has four commands and just copies the whole folder with the print history and tries to rename the files to pdfs. Do so by running `sudo bash retrieve_files.sh`.

## How does this work?

MacOS uses a printing system called [CUPS](https://www.cups.org/), which is configured to save printed files by default in many cases. This means that if you print a file on your Mac and then delete it, it is likely that Mac has saved a copy of that file in an internal CUPS folder. This script just copies that file back, finds its name, renames it, and also retrieves some other information from CUPS control files. **You can read more in [my blog about this.](http://adam.sr/prints)** <!--TODO: make the link work-->

## Acknowledgements

Thanks for [go-cups-control-files](https://github.com/ui-kreinhard/go-cups-control-files) and for [How to dissect a CUPS job control file](https://stackoverflow.com/questions/53688075/how-to-dissect-a-cups-job-control-file-var-spool-cups-cnnnnnn/53688639#53688639); this would not exist without these.

[^1]: And also on any other Linux system using [CUPS](https://www.cups.org/), Apple's open-source system for printing.

## License

The scripts are licensed under the [GNU General Public License v3.0](https://www.gnu.org/licenses/gpl-3.0.en.html).
