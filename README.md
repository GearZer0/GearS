# AutomateFileDownloader tool

AutomateFileDownloader tool automatically compare the hash of the file and download the file if it the hash matches.

## Break down of the automation steps
````
1. locate the filename in the url
2. Check the file hash against the website's
3. If hash doesn't match. it will display "hash mistach" and stop the script
4. If hash match, download the file if the the latest update is previous day
5. Move file into network drive
````

## Configuration
Fill in the following in auto.py :
````
self.download_folder = ""   download file location
dest = ""                   network folder location
````

# Command to run this tool
python SEP.py

# Create the Batch File
Create a Notepad file and input the following into the notepad :
```
cd "Path where your script is"
python SEP.py
pause
```
Save the Notepad as name.bat
