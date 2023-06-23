import tkinter as tk
from tkinter.filedialog import askopenfilename
from xml.etree.ElementTree import ElementTree, fromstring
from time import strftime, sleep
from urllib.request import urlopen
import datetime, re, os, subprocess
from source.char_ref_dict import *
from source.methods import *

MARC_EDIT_PATH = "C:\\Program Files\\Terry Reese\\MarcEdit 7.6\\cmarcedit.exe"
OAI_PREFIX = "https://etd.ohiolink.edu/apexprod/!etd_search_oai?verb=GetRecord&metadataPrefix=oai_etdms&identifier=oai:etd.ohiolink.edu:"

EmbargoFileName_mrk = f"{strftime('%Y%m%d')}_embargoETD.mrk"
FullFileName_mrk    = f"{strftime('%Y%m%d')}_fulltextETD.mrk"
EmbargoFileName_mrc = f"{strftime('%Y%m%d')}_embargoETD.mrc"
FullFileName_mrc    = f"{strftime('%Y%m%d')}_fulltextETD.mrc"


print("""
#######                                  ######                                
   #    #    # ######  ####  #  ####     #     # # ######  ####  ######  ####  
   #    #    # #      #      # #         #     # # #      #    # #      #      
   #    ###### #####   ####  #  ####     ######  # #####  #      #####   ####  
   #    #    # #           # #      #    #       # #      #      #           # 
   #    #    # #      #    # # #    #    #  2.0  # #      #    # #      #    # 
   #    #    # ######  ####  #  ####     #       # ######  ####  ######  ####  


   
  /////////////////UC Libraries--Electronic Resources Dept./////////////////

ech
""")


def BrowseToFile(): #prompt user to select file; isolate ETD unique IDs
	root = tk.Tk()
	root.withdraw()
	filename = askopenfilename(filetypes=[("textfiles","*.txt"),("allfiles","*")], title="Thesis Pieces -- Select input file")
	TargetDir = re.sub('(.*)(?<=/).*$', '\\1', filename)
	print(filename)
	InputFileText = open(filename).read()
	ETD_UniqueIDs = re.findall('ucin\d+', InputFileText)
	return filename, TargetDir, ETD_UniqueIDs

def CharRefReplace(x): # replace character references, fix degree types, remove garbage xml
	keys = dict.keys(CharRefDict)
	keys = list(CharRefDict.keys())
	for key in range(len(keys)):
		x = re.sub(CharRefDict[keys[key]][0], CharRefDict[keys[key]][1], x)
	#find and output file with unknown ascii chars
	UnrecognizedASCII = re.findall('&#\d*?;', x)
	#replace unkown ascii chars
	BoolUnrecognizedASCII = 0
	if UnrecognizedASCII:
		BoolUnrecognizedASCII = 1
		asciif = open(TargetDir + strftime("%Y%m%d") + '_UnrecognizedAsciiReport.txt', 'a')
		asciif.write(ucin + ' ' + str(UnrecognizedASCII) + '\n')
		asciif.close()
	x = re.sub('\$#.*?;', '|', x)
	x = re.sub('&#\d*?;', '|', x)
	#x = x.decode(encoding='UTF-8',errors='strict')
	for i in x:
		#print i
		if ord(i) > 128:
			#print x
			#print ord(i)
			x = x.replace(i, '|')

	return x, BoolUnrecognizedASCII

def ExtractFieldContent():
	content_dict = {
	'f245a' : f245a(text),
	'f245b' : f245b(text),
	'f245ind2' : f245ind2(text),
	'f100a' : f100a(text),
	'f245c' : f245c(text),
	'f520a' : f520a(text),
	'f245c' : f245c(text),
	'f264c' : f264c(text),
        'f300a' : f300a(text),
        'f347c' : f347c(text),
        'f500a_keywords' : f500a_keywords(text),
        'f500a_advisors' : f500a_advisors(text),
        'f502a_degree' : f502a_degree(text),
        'f610a_degree' : f610a_degree(text),
        'f610a_discipline' : f610a_discipline(text),
	'f856u' : f856u(text),
	'f502a_degree' : f502a_degree(text),
	'f588a_review_date' : f588a_review_date(text),
	'f008date' : strftime("%y%m%d"),
	'f506a_delay_date' : f506a_delay_date(text)
	}
	return content_dict

#read and compile identifiers from input file, get XML recs fro OAI harvester
fullcount = 0
embcount = 0

filename, TargetDir, ETD_UniqueIDs = BrowseToFile()

ETD_UniqueIDs = dict.fromkeys(ETD_UniqueIDs).keys()

print('Downloading ' + str(len(ETD_UniqueIDs)) + ' ETDs')

ETD_UniqueIDs = sorted(ETD_UniqueIDs)

print("Processing...\n")

#loop pulls XML recs from Olink and writes to tempfile
for ucin in ETD_UniqueIDs:
	print(ucin)
	sleep(1)
	page = urlopen(f"{OAI_PREFIX}{ucin}")
	page = page.read().decode('utf-8')
	#replace character references
	page, BoolUnrecognizedASCII = CharRefReplace(page)
	
	#traverse XML tree and capture element text
	text = fromstring(page)

        #print page
	
        #initialize dictionary; pull values for
	content_dict = ExtractFieldContent()

	#ETD full-text template
	full_etd = open('source/RDA_fulltext_template.txt').read() % content_dict
	
        #ETD embargo template
	brief_etd = open('source/RDA_embrief_template.txt').read() % content_dict

#choose between brief and full templates based on rights element
	if  text.findtext('GetRecord/record/metadata/thesis/rights') == 'unrestricted':
		rec_output = full_etd
		outputfile = TargetDir + strftime("%Y%m%d") + '_fulltextETD.mrk'
		fullcount = fullcount + 1
	else:
		rec_output = brief_etd
		outputfile = TargetDir + strftime("%Y%m%d") + '_embargoETD.mrk'
		embcount = embcount + 1

	#write to file
	#print(rec_output)
	f = open(outputfile, 'a')
	f.write(rec_output)
	f.close()

try:
    if fullcount > 0:
        subprocess.call([MARC_EDIT_PATH, '-s', TargetDir + FullFileName_mrk, '-d', TargetDir + FullFileName_mrc, '-make'])
    if embcount > 0:
        subprocess.call([MARC_EDIT_PATH, '-s', TargetDir + EmbargoFileName_mrk, '-d', TargetDir + EmbargoFileName_mrc, '-make'])
    if BoolUnrecognizedASCII > 0: 
        AsciiReport = open(TargetDir + strftime("%Y%m%d") + '_UnrecognizedAsciiReport.txt', 'r').read()
        print('\n\n***Script found unrecognized diacritic html character code(s)***\n')
        print(AsciiReport)
        print('See ' + TargetDir + strftime("%Y%m%d") + '_UnrecognizedAsciiReport.txt'' for details\n')
except OSError:
    print("MARCedit could not be found - output MRK files only")
    #print full_etd
    #print brief_etd
input('\nProcess finished, press Enter')
