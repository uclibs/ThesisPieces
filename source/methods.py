import re
import datetime
from time import strftime, sleep

def f100a(text):
        try:
            creator = text.findtext('GetRecord/record/metadata/thesis/creator')
            f100a = creator.replace(', M.D.', '')
            f100a = creator.replace(' Jr.', '')
        except (IndexError, ValueError, AttributeError):
            f100a = "|"
        return f100a

def f245a(text):
    try:
        title = text.findtext('GetRecord/record/metadata/thesis/title')
        f245a = re.sub('(\w.*?)(:.*)', '\\1', title)
    except (IndexError, ValueError, AttributeError):
        f245a = "|"
    return f245a

def f245b(text):
    try: 
        title = text.findtext('GetRecord/record/metadata/thesis/title')
        f245b = re.sub('(\w.*?)(:\s)(.*)', '\\3', title)
        f245a = re.sub('(\w.*?)(:.*)', '\\1', title)
        #print('f245a +' + f245a)
        #print('f245b +' + f245b)
        if f245a == f245b:
            f245b = ''
        else: 
            f245b = ' :$b' + f245b
    except (IndexError, ValueError, AttributeError):
        f245b = "|"
    return f245b 

def f245c(text):
    try:
        creator = text.findtext('GetRecord/record/metadata/thesis/creator')
        splitname = creator.split(', ')
        if splitname.count('M.D.') > 0:
                splitname.remove('M.D.')
        if splitname.count(' Jr.'):
                splitname.remove(' Jr.')
        splitname.insert(0, splitname.pop(1))
        f245c = " ".join(splitname)
        f245c = re.sub('[\.]$', '', f245c)
    except (IndexError, ValueError, AttributeError):
        f245c = "|"     
    return f245c

def f245ind2(text):
    try:
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
    except (IndexError, ValueError, AttributeError):
        f245ind2 = "|"
    return f245ind2

def f264c(text):
    try:
        f264c = text.findtext('GetRecord/record/metadata/thesis/date')[0:4]
    except (IndexError, ValueError, AttributeError):
        f264c = "|"
    return f264c

def f300a(text):
    try:
        f300a = re.sub('p.', '', text.findall('GetRecord/record/metadata/thesis/format')[1].text)
    except (IndexError, ValueError, AttributeError):
        f300a = "|"
    return f300a

def f347c(text):
    try:
        f347c = text.findall('GetRecord/record/metadata/thesis/format')[2].text
    except (IndexError, ValueError, AttributeError):
        f347c = "|"
    return f347c

def f500a_keywords(text):
    try:
        SubjectElementsText = text.findall('GetRecord/record/metadata/thesis/subject')
        #keywords loop
        SubjectList = []
        for subject in SubjectElementsText:
                fsubx = subject.text
                SubjectList.append(fsubx)
        if len(SubjectList) > 0:
                #print(SubjectList)
                #check for empty item at end of list, remove if present
                SubjectList = filter(None, SubjectList)
                f500a_keywords = "; ".join(SubjectList)
        else:
                f500a_keywords = "|<NoKeywords_DeleteThisField>"
    except (IndexError, ValueError, AttributeError):
        f500a_keywords = "|"
    return f500a_keywords

def f500a_advisors(text):
    try:
        AdvisorElementsText = text.findall('GetRecord/record/metadata/thesis/contributor')
        #advisors loop
        AdvisorList = []
        for advisor in AdvisorElementsText:
                fadvis = re.sub('(\w*)(, )(\w.*)', '\\3 \\1', advisor.text)
                AdvisorList.append(fadvis)
        if len(AdvisorList) > 0:
                #print(SubjectList)
                #check for empty item at end of list, remove if present
                AdvisorList = filter(None, AdvisorList)
                f500a_advisors = ", ".join(AdvisorList)
        else:
                f500a_advisors = "|<NoAdvisor_DeleteThisField>"
    except (IndexError, ValueError, AttributeError):
        f500a_advisors = "|"
    return f500a_advisors
          
     
def f520a(text):
    try: 
        f520a = re.sub('\n', '', text.findtext('GetRecord/record/metadata/thesis/description'))
    except (IndexError, ValueError, AttributeError):
        f520a = "|"
    return f520a

def f856u(text):
    try: 
        f856u = text.findtext('GetRecord/record/metadata/thesis/identifier')
    except (IndexError, ValueError, AttributeError):
        f856u = "|"
    return f856u

def f502a_degree(text):
    try:
        f502a_degree = text.findtext('GetRecord/record/metadata/thesis/degree/name')
    except (IndexError, ValueError, AttributeError):
        f502a_degree = "|"
    return f502a_degree

def f588a_review_date(text):
    try:
        f588a_review_date = strftime("%b. %d, %Y").replace(' 0', ' ').replace('Jun.', 'June').replace('Jul.', 'July')
    except (IndexError, ValueError, AttributeError):
        f588a_review_date = "|"
    return f588a_review_date

def f610a_degree(text):
    try:
        f610a_degree = text.findtext('GetRecord/record/metadata/thesis/degree/name')
    except (IndexError, ValueError, AttributeError):
        f610a_degree = "|"
    return f610a_degree

def f610a_discipline(text):
    try:
        f610a_discipline = re.search ('(?<=: )\s\(\w.*', re.sub('((?<=: )\w.*)', ' (\\1)', text.findtext('GetRecord/record/metadata/thesis/degree/discipline'))).group(0)
        f610a_degree = text.findtext('GetRecord/record/metadata/thesis/degree/name')

        if f610a_discipline == ' (Community Planning)':
            f610a_discipline = ''
            
        if f610a_discipline == ' (Architecture (Master of))':
            f610a_discipline = ''

        if f610a_discipline == ' (Design)':
            f610a_discipline = ''
            
        if f610a_discipline == ' (Biostatistics (Environmental Health))':
            f610a_discipline = ' (Biostatistics)'
        if f610a_discipline == ' (Industrial Hygiene (Environmental Health))':
            f610a_discipline = ' (Industrial Hygiene)'
        if f610a_discipline == ' (Epidemiology (Environmental Health))':
            f610a_discipline = ' (Epidemiology)'
        if f610a_discipline == ' (Toxicology (Environmental Health))':
            f610a_discipline = ' (Toxicology)'
        if f610a_degree == 'Master of Architecture' and f610a_discipline == ' (Architecture)':
            f610a_discipline = ''
        if f610a_degree == 'Master of Music':
            f610a_discipline = ''
        if f610a_degree == 'Dr. of Education':
            f610a_discipline = ''
        if f610a_degree == 'Dr. of Musical Arts':
            f610a_discipline = ''
    except (IndexError, ValueError, AttributeError):
        f610a_discipline = "|"
    return f610a_discipline

def f506a_delay_date(text):
    try:
        delay = text.findtext('GetRecord/record/metadata/thesis/rights')
        if delay != 'unrestricted' and delay != 'restricted; full text not available online':
            f506a_delay_date = datetime.datetime.strptime(re.search('\d*-\d\d-\d\d', text.findtext('GetRecord/record/metadata/thesis/rights')).group(0), "%Y-%m-%d").strftime("%b. %d, %Y").replace(' 0', ' ')
        else:
            f506a_delay_date = ''
    except (IndexError, ValueError, AttributeError):
        f506a_delay_date = "|"
    return f506a_delay_date
