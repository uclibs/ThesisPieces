from Tkinter import *
from tkFileDialog import askopenfilename
from xml.etree.ElementTree import ElementTree, fromstring
from time import strftime, sleep
from urllib import urlopen
import datetime, re, os, subprocess


print """
#######                                  ######                                
   #    #    # ######  ####  #  ####     #     # # ######  ####  ######  ####  
   #    #    # #      #      # #         #     # # #      #    # #      #      
   #    ###### #####   ####  #  ####     ######  # #####  #      #####   ####  
   #    #    # #           # #      #    #       # #      #      #           # 
   #    #    # #      #    # # #    #    #  1.5  # #      #    # #      #    # 
   #    #    # ######  ####  #  ####     #       # ######  ####  ######  ####  


   
  /////////////////UC Libraries--Electronic Resources Dept./////////////////


"""

from source.char_ref_dict import CharRefDict

def BrowseToFile(): #prompt user to select file; isolate ETD unique IDs
	root=Tk()
	root.withdraw()
	filename = askopenfilename(filetypes=[("textfiles","*.txt"),("allfiles","*")], title="Thesis Pieces -- Select input file")
	TargetDir = re.sub('(.*)(?<=/).*$', '\\1', filename)
	print filename
	InputFileText = open(filename).read()
	ETD_UniqueIDs = re.findall('ucin\d+', InputFileText)
	return filename, TargetDir, ETD_UniqueIDs

def CharRefReplace(x): # replace character references, fix degree types, remove garbage xml
	keys = dict.keys(CharRefDict)
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
	x = x.decode(encoding='UTF-8',errors='strict')
	for i in x:
		#print i
		if ord(i) > 128:
			#print x
			#print ord(i)
			x = x.replace(i, '|')

	return x, BoolUnrecognizedASCII

def ExtractFieldContent():
	content_dict = {
	'f245a' : re.sub('(\w.*?)(:.*)', '\\1', title),
	'f245b' : re.sub('(\w.*?)(:\s)(.*)', '\\3', title),
	'f245ind2' : f245ind2,
	'f100a' : creator,
	'f520a' : re.sub('\n', '', text.findtext('GetRecord/record/metadata/thesis/description')),
	'f245c' : f245c,
	'f260c' : text.findtext('GetRecord/record/metadata/thesis/date')[0:4],
        'f300a' : re.sub('p.', '', text.findall('GetRecord/record/metadata/thesis/format')[1].text),
        'filesize' : text.findall('GetRecord/record/metadata/thesis/format')[2].text,
	'f856u' : text.findtext('GetRecord/record/metadata/thesis/identifier'),
	'fdegree' : text.findtext('GetRecord/record/metadata/thesis/degree/name'),
	'rev_date' : strftime("%b. %d, %Y").replace(' 0', ' ').replace('Jun.', 'June').replace('Jul.', 'July'),
	'f008date' : strftime("%y%m%d"),
	'fdisc' : re.search ('(?<=: )\s\(\w.*', re.sub('((?<=: )\w.*)', ' (\\1)', text.findtext('GetRecord/record/metadata/thesis/degree/discipline'))).group(0),
	'delay' : text.findtext('GetRecord/record/metadata/thesis/rights'),
	'delaydate' : ''
	}
	return content_dict

def ExtractCreator(x):#remove honorifics and invert author name for SOR

	creator = text.findtext('GetRecord/record/metadata/thesis/creator')
	splitname = creator.split(', ')
	if splitname.count('M.D.') > 0:
		splitname.remove('M.D.')
	if splitname.count(' Jr.'):
		splitname.remove(' Jr.')
	splitname.insert(0, splitname.pop(1))
	f245c = " ".join(splitname)
	f245c = re.sub('[\.]$', '', f245c)
	creator = creator.replace(', M.D.', '')
	creator = re.sub('[\.]$', '', creator)
	return creator, f245c

def ExtractTitle(x):#set skip and detect subtitles
	title = text.findtext('GetRecord/record/metadata/thesis/title')
	#set skip (245 ind 2) for English initial articles
	if re.match('The\s', title):
		f245ind2 = '4'
	elif re.match('An\s', title):
		f245ind2 = '3'
	elif re.match('A\s', title):
		f245ind2 = '2'
	else:
		f245ind2 = '0'
	return title, f245ind2

def ExtractKeywords(x):
	SubjectElementsText = text.findall('GetRecord/record/metadata/thesis/subject')
	#keywords loop
	SubjectList = []
	for subject in SubjectElementsText:
		fsubx = subject.text
		SubjectList.append(fsubx)
	if len(SubjectList) > 0:
		#print SubjectList
		#check for empty item at end of list, remove if present
		SubjectList = filter(None, SubjectList)
		content_dict['fkeywrd'] = "; ".join(SubjectList)
	else:
		content_dict['fkeywrd'] = "|<NoKeywords_DeleteThisField>"
	return content_dict

def ExtractAdvisors(x):
	AdvisorElementsText = text.findall('GetRecord/record/metadata/thesis/contributor')
	#advisors loop
	AdvisorList = []
	for advisor in AdvisorElementsText:
		fadvis = re.sub('(\w*)(, )(\w.*)', '\\3 \\1', advisor.text)
		AdvisorList.append(fadvis)
	if len(AdvisorList) > 0:
		#print SubjectList
		#check for empty item at end of list, remove if present
		AdvisorList = filter(None, AdvisorList)
		content_dict['fadvisor'] = ", ".join(AdvisorList)
	else:
		content_dict['fadvisor'] = "|<NoAdvisor_DeleteThisField>"
	return content_dict

def CleanupProgramNames(x):
	if content_dict['fdisc'] == ' (Community Planning)':
		content_dict['fdisc'] = ''
	if content_dict['fdisc'] == ' (Architecture (Master of))':
		content_dict['fdisc'] = ''
	if content_dict['fdisc'] == ' (Design)':
		content_dict['fdisc'] = ''
	if content_dict['fdisc'] == ' (Biostatistics (Environmental Health))':
		content_dict['fdisc'] = ' (Biostatistics)'
	if content_dict['fdisc'] == ' (Industrial Hygiene (Environmental Health))':
		content_dict['fdisc'] = ' (Industrial Hygiene)'
	if content_dict['fdisc'] == ' (Epidemiology (Environmental Health))':
		content_dict['fdisc'] = ' (Epidemiology)'
	if content_dict['fdisc'] == ' (Toxicology (Environmental Health))':
		content_dict['fdisc'] = ' (Toxicology)'
	if content_dict['fdegree'] == 'Master of Architecture' and content_dict['fdisc'] == ' (Architecture)':
		content_dict['fdisc'] = ''
	if content_dict['fdegree'] == 'Master of Music':
		content_dict['fdisc'] = ''
	if content_dict['fdegree'] == 'Dr. of Education':
		content_dict['fdisc'] = ''
	if content_dict['fdegree'] == 'Dr. of Musical Arts':
		content_dict['fdisc'] = ''
	return content_dict

#read and compile identifiers from input file, get XML recs fro OAI harvester
fullcount = 0
embcount = 0


filename, TargetDir, ETD_UniqueIDs = BrowseToFile()

ETD_UniqueIDs = dict.fromkeys(ETD_UniqueIDs).keys()
print 'Downloading ' + str(len(ETD_UniqueIDs)) + ' ETDs'
ETD_UniqueIDs = sorted(ETD_UniqueIDs)

print "Processing...\n"

#loop pulls XML recs from Olink and writes to tempfile
for ucin in ETD_UniqueIDs:
	sleep(1)
	page = urlopen("https://etd.ohiolink.edu/!etd_search_oai?verb=GetRecord&metadataPrefix=oai_etdms&identifier=oai:etd.ohiolink.edu:" + ucin)
	page = page.read()
	#replace character references
	page, BoolUnrecognizedASCII = CharRefReplace(page)
	
	#traverse XML tree and capture element text
	text = fromstring(page)
	print page
	#invert author name and strip M.D. for 100a
	creator, f245c = ExtractCreator(text)
	#get full title, cleanup, detect skip
	title, f245ind2 = ExtractTitle(text)
	#initialize dictionary; pull values for
	content_dict = ExtractFieldContent()

	#check for presense of subtitle, clear variable if absent
	if content_dict['f245a'] ==  content_dict['f245b']:
		content_dict['f245b'] = ''
	#if present, add preceding subfield and punct
	else:
		content_dict['f245b'] = ' :$b' + content_dict['f245b']
		

	#edit or remove degree discriptions based on ETD standard
	content_dict = CleanupProgramNames(content_dict)
	
	#capture and convert embargo release date
	if content_dict['delay'] != 'unrestricted':
		#added if to Check for fully restricted, grandfathered content; should not occur in new recs
		if content_dict['delay'] != 'restricted; full text not available online':
			try:
				content_dict['delaydate'] = datetime.datetime.strptime(re.search('\d*-\d\d-\d\d', text.findtext('GetRecord/record/metadata/thesis/rights')).group(0), "%Y-%m-%d").strftime("%b. %d, %Y").replace(' 0', ' ')
			except AttributeError:
				content_dict['delaydate'] = '|'
	#gather keywords from repeated elements
	content_dict = ExtractKeywords(content_dict)

	content_dict = ExtractAdvisors(content_dict)
	
	#ETD full-text template
	full_etd = open('source/RDA_fulltext_template.txt').read() % content_dict
	#ETD embargo template
	brief_etd = open('source/RDA_embrief_template.txt').read() % content_dict
	#choose between brief and full templates based on rights element
	if content_dict['delay'] == 'unrestricted':
		rec_output = full_etd
		outputfile = TargetDir + strftime("%Y%m%d") + '_fulltextETD.mrk'
		fullcount = fullcount + 1
	else:
		rec_output = brief_etd
		outputfile = TargetDir + strftime("%Y%m%d") + '_embargoETD.mrk'
		embcount = embcount + 1

	#write to file
	print rec_output
	f = open(outputfile, 'a')
	f.write(rec_output)
	f.close()

EmbargoFileName_mrk = strftime("%Y%m%d") + '_embargoETD.mrk'
FullFileName_mrk = strftime("%Y%m%d") + '_fulltextETD.mrk'
EmbargoFileName_mrc = strftime("%Y%m%d") + '_embargoETD.mrc'
FullFileName_mrc = strftime("%Y%m%d") + '_fulltextETD.mrc'

if fullcount > 0:
	subprocess.call(['C:\\Program Files\\MarcEdit 6\\cmarcedit.exe', '-s', TargetDir + FullFileName_mrk, '-d', TargetDir + FullFileName_mrc, '-make'])
if embcount > 0:
	subprocess.call(['C:\\Program Files\\MarcEdit 6\\cmarcedit.exe', '-s', TargetDir + EmbargoFileName_mrk, '-d', TargetDir + EmbargoFileName_mrc, '-make'])
if BoolUnrecognizedASCII > 0: 
	AsciiReport = open(TargetDir + strftime("%Y%m%d") + '_UnrecognizedAsciiReport.txt', 'r').read()
	print '\n\n***Script found unrecognized diacritic html character code(s)***\n'
	print AsciiReport
	print 'See ' + TargetDir + strftime("%Y%m%d") + '_UnrecognizedAsciiReport.txt'' for details\n'
#print full_etd
#print brief_etd
raw_input('\nProcess finished, press Enter')
