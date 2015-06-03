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


CharRefDict = {
	'oai' : ['xmlns="http://www.openarchives.org/OAI/2.0/"\s*xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"\s*xsi:schemaLocation="http://www.openarchives.org/OAI/2.0/\s*http://www.openarchives.org/OAI/2.0/OAI-PMH.xsd"', ''],
	'thesis' : ['xmlns="http://www.ndltd.org/standards/metadata/etdms/1.0/"\s*schemaLocation="http://www.ndltd.org/standards/metadata/etdms/1.0/\s*http://www.ndltd.org/standards/metadata/etdms/1.0/etdms.xsd"', ''],
	'dash' : ['&#8211;', '-'],
	'doubdash' : ['&#8212;', '--'],
	'horizbar' : ['&#8213;', '--'],
	'apos' : ['&#8216;', '&apos;'],
	'apos1' : ['&#8217;', '&apos;'],
	'apos2' : ['&#39;', '&apos;'],
	'slash' : ['&#47;', '/'],
	'fractSlash' : ['&#8260;', '/'],
	'apos3' : ['&#039;', '&apos;'],
	'quo' : ['&#8220;', '&quot;'],
	'quo1' : ['&#8221;', '&quot;'],
	'aster' : ['&#8727;', '*'],
	'doubsp' : ['&#160;', ' '],
	'amp' : ['&#38;', '&amp;'],
	'backsl' : ['&#34;', '&quot;'],
	#Diacritics and spec characters
	'less' : ['&#60;', '&lt;'],
	'greater' : ['&#62;' , '&gt;'],
	'AO' : ['&#160;', '{A0}'],
	'iexcl' : ['&#161;', '{iexcl}'],
	'pound' : ['&#163;', '{pound}'],
	'uml' : ['&#168;', '{uml}'],
	'copy' : ['&#169;', '{copy}'],
	'softhyphen' : ['&#173;', '-'],
	'reg' : ['&#174;', '{reg}'],
	'deg' : ['&#176;', '{deg}'],
	'micro' : ['&#181;', '[micro]'],
	'middot' : ['&#183;', '{middot}'],
	'plusminus' : ['&#177;', '{plusmin}'],
	'graveA' : ['&#192;', '{grave}A'],
	'acuteA' : ['&#193;', '{acute}A'],
	'circA' : ['&#194;', '{circ}A'],
	'tildeA' : ['&#195;', '{tilde}A'],
	'umlA' : ['&#196;', '{uml}A'],
	'ringA' : ['&#197;', '{ring}A'],
	'AElig' : ['&#198;', '{AElig}'],
	'ostroke' : ['&#248;', '{ostrok}'],
	'Ostroke' : ['&#216;', '{Ostrok}'],
	'ZCaron' : ['&#381;', '{caron}Z'],
	'zCaron' : ['&#382;', '{caron}z'],
	'cedilC' : ['&#199;', '{cedil}C'],
	'graveE' : ['&#200;', '{grave}E'],
	'acuteE' : ['&#201;', '{acute}E'],
	'circE' : ['&#202;', '{circ}E'],
	'umlE' : ['&#203;', '{uml}E'],
	'graveO' : ['&#204;', '{grave}I'],
	'acuteI' : ['&#205;', '{acute}I'],
	'circI' : ['&#206;', '{circ}I'],
	'umlI' : ['&#207;', '{uml}I'],
	'tildeN' : ['&#209;', '{tilde}N'],
	'graveO' : ['&#210;', '{grave}O'],
	'acuteO' : ['&#211;', '{acute}O'],
	'circO' : ['&#212;', '{circ}O'],
	'tildeO' : ['&#213;', '{tilde}O'],
	'umlO' : ['&#214;', '{uml}O'],
	'multi' : ['&#215;', 'x'],
	'graveU' : ['&#217;', '{grave}U'],
	'acuteU' : ['&#218;', '{acute}U'],
	'circU' : ['&#219;', '{circ}U'],
	'umlU' : ['&#220;', '{uml}U'],
	'acuteY' : ['&#221;', '{acute}Y'],
	'THORN' : ['&#222;', '{THORN}'],
	'eszett' : ['&#223', 'ss'],
	'gravea' : ['&#224;', '{grave}a'],
	'acutea' : ['&#225;', '{acute}a'],
	'circa' : ['&#226;', '{circ}a'],
	'tildea' : ['&#227;', '{tilde}a'],
	'tilde' : ['&#126;', '{tilde}'],
	'umla' : ['&#228;', '{uml}a'],
	'ringa' : ['&#229;', '{ring}a'],
	'aelig' : ['&#230;', '{aelig}'],
	'cedilc' : ['&#231;', '{cedil}c'],
	'gravee' : ['&#232;', '{grave}e'],
	'acutee' : ['&#233;', '{acute}e'],
	'circe' : ['&#234;', '{circ}e'],
	'umle' : ['&#235;', '{uml}e'],
	'gravei' : ['&#236;', '{grave}i'],
	'acutei' : ['&#237;', '{acute}i'],
	'circi' : ['&#238;', '{circ}i'],
	'umli' : ['&#239;', '{uml}i'],
	'eth' : ['&#240;', '{eth}'],
	'tilden' : ['&#241;', '{tilde}n'],
	'graveo' : ['&#242;', '{grave}o'],
	'acuteo' : ['&#243;', '{acute}o'],
	'circo' : ['&#244;', '{circ}o'],
	'tildeo' : ['&#245;', '{tilde}o'],
	'umlo' : ['&#246;','{uml}o'],
	'graveu' : ['&#249;', '{grave}u'],
	'acuteu' : ['&#250;', '{acute}u'],
	'circu' : ['&#251;', '{circ}u'],
	'umlu' : ['&#252;', '{uml}u'],
	'acutey' : ['&#253;', '{acute}y'],
	'thorn' : ['&#254;', '{thorn}'],
	'umly' : ['&#255;', '{uml}y'],
	'combMacron' : ['&#772;', '{macr}'],
	'Alpha' : ['&#913;', '[Alpha]'],
	'Beta' : ['&#914;', '[Beta]'],
	'Gamma' : ['&#915;', '[Gamma]'],
	'Delta' : ['&#916;', '[Delta]'],
	'Epsilon' : ['&#917;', '[Epsilon]'],
	'Zeta' : ['&#918;', '[Zeta]'],
	'Eta' : ['&#919;', '[Eta]'],
	'Theta' : ['&#920;', '[Theta]'],
	'Iota' : ['&#921;', '[Iota]'],
	'Kappa' : ['&#922;', '[Kappa]'],
	'Lambda' : ['&#923;', '[Lambda]'],
	'Mu' : ['&#924;', '[Mu]'],
	'Nu' : ['&#925;', '[Nu]'],
	'Xi' : ['&#926;', '[Xi]'],
	'Omicron' : ['&#927;', '[Omicron]'],
	'Pi' : ['&#928;', '[Pi]'],
	'Rho' : ['&#929;', '[Rho]'],
	'Sigma' : ['&#931;', '[Sigma]'],
	'Tau' : ['&#932;', '[Tau]'],
	'Upsilon' : ['&#933;', '[Upsilon]'],
	'Phi' : ['&#934;', '[Phi]'],
	'Chi' : ['&#935;', '[Chi]'],
	'Psi' : ['&#936;', '[Psi]'],
	'Omega' : ['&#937;', '[Omega]'],
	'alpha' : ['&#945;', '[alpha]'],
	'beta' : ['&#946;', '[beta]'],
	'gamma' : ['&#947;', '[gamma]'],
	'gamma#' : ['&#947;', '[gamma]'],
	'delta' : ['&#948;', '[delta]'],
	'epsilon' : ['&#949;', '[epsilon]'],
	'zeta' : ['&#950;', '[zeta]'],
	'eta' : ['&#951;', '[eta]'],
	'theta' : ['&#952;', '[theta]'],
	'iota' : ['&#953;', '[iota]'],
	'kappa' : ['&#954;', '[kappa]'],
	'lambda' : ['&#955;', '[lambda]'],
	'mu' : ['&#956;', '[mu]'],
	'nu' : ['&#957;', '[nu]'],
	'xi' : ['&#958;', '[xi]'],
	'omicron' : ['&#959;', '[omicron]'],
	'pi' : ['&#960;', '[pi]'],
	'rho' : ['&#961;', '[rho]'],
	'sigma' : ['&#963;', '[sigma]'],
	'tau' : ['&#964;', '[tau]'],
	'upsilon' : ['&#965;', '[upsilon]'],
	'phi' : ['&#966;', '[phi]'],
	'chi' : ['&#967;', '[chi]'],
	'psi' : ['&#968;', '[psi]'],
	'omega' : ['&#969;', '[omega]'],
	'emspace' : ['&#8195;', '  '],
	'bullet' : ['&#8226;', '{middot}'],
	'elips' : ['&#8230;', ' ... '],
	'tradem' : ['&#8482;', '[TM]'],
	'leftarrow' : ['&#8592;', '<-'],
	'rightarrow' : ['&#8594;', '->'],
	'tilde' : ['&#8764;', '~'],
	'almostEqual' : ['&#8776;', '[almost equal to]'],
	'prime' : ['&#8242;', '{softsign}'],
	'minus' : ['&#8722;', '-'],
	'lesseq' : ['&#8804;', '{under}&lt;'],
	'greateq' : ['&#8805;', '{under}&gt;'],
	'doubgreat' : ['&#8811;', '>>'],
	'dollar' : ['\$', '{dollar}'],
	#numbers
	'sup2' : ['&#178;', '{esc}p2{esc}'],
	'sup3' : ['&#179;', '{esc}p3{esc}'],
	'sub2' : ['&#8322;', '{esc}b2{esc}'],

	#degree punctuation/title fixes
	'MS' : ['<name>MS</name>', '<name>M.S.</name>'],
	'MA' : ['<name>MA</name>', '<name>M.A.</name>'],
	'MCP' : ['<name>MCP</name>', '<name>Master of Community Planning</name>'],
	'PhD' : ['<name>PhD</name>', '<name>Ph.D.</name>'],
	'MARCH' : ['<name>MARCH</name>', '<name>Master of Architecture</name>'],
	'MSARCH' : ['<name>MSARCH</name>', '<name>M.S.</name>'],
	'MDES' : ['<name>MDES</name>', '<name>Master of Design</name>'],
	'MDes' : ['<name>MDes</name>', '<name>Master of Design</name>'],
	'MM' : ['<name>MM</name>', '<name>Master of Music</name>'],
	'EdD' : ['<name>EdD</name>', '<name>Dr. of Education</name>'],
	'DMA' : ['<name>DMA</name>', '<name>Dr. of Musical Arts</name>'],
	'MEd' : ['<name>MEd</name>', '<name>Master of Education</name>'],
	}

def BrowseToFile():#prompt user to select file; isolate ETD unique IDs
	root=Tk()
	root.withdraw()
	filename = askopenfilename(filetypes=[("textfiles","*.txt"),("allfiles","*")], title="Thesis Pieces -- Select input file")
	TargetDir = re.sub('(.*)(?<=/).*$', '\\1', filename)
	print filename
	InputFileText = open(filename).read()
	ETD_UniqueIDs = re.findall('ucin\d+', InputFileText)
	return filename, TargetDir, ETD_UniqueIDs

def CharRefReplace(x):#replace character references, fix degree types, remove garbage xml
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
	title = text.findtext('GetRecord/record/metadata/thesis/title')[0] + text.findtext('GetRecord/record/metadata/thesis/title')[1:].lower()
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
	full_etd = open('source\\RDA_fulltext_template.txt').read() % content_dict
	#ETD embargo template
	brief_etd = open('source\\RDA_embrief_template.txt').read() % content_dict
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
