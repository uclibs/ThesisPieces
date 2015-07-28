###Thesis Pieces

Harvest and process Electronic Thesis and Dissertation records from the OhioLINK ETD Center. Convert from ETDMS xml to MARC, customized for University of Cincinnati Libraries.

####Requirements

* Windows 7
* Python 2.7
* MarcEdit 6

####Notes on usage

Create .txt file containing ETD email notifications (in Outlook, select all the messages and save as .txt). The script yanks all *ucin* identifiers from the notifications file and searches each in the OhioLINK ETD center. 

1. Execute script by double-clicking icon or invoking from command line.
2. Select text file of *ucin* indentifiers in pop-up dialog.
3. Monitor script while records are downloaded and processed. 

The script separates embargo and full text records and outputs a file for each in the same folder where the input text file is stored.
