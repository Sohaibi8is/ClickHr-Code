# import required libraries

from tika import parser
import spacy
from spacy.matcher import Matcher
from nltk.corpus import stopwords
import pandas as pd
import json
import imaplib
import os
import email
import mysql.connector as mysql
import textract
from pyresparser import ResumeParser
import re
from bs4 import BeautifulSoup as BS
from find_job_titles import FinderAcora
import io
import dateutil.parser
from dateutil.relativedelta import relativedelta
from datetime import date, datetime
from json import dumps


# ----------------------------------------- extract_name ------------------------------------------ #
"""  This function takes text(all text from resume) as input and extract name from resume text by using 'spacy' model.
     will look for name entity in resume text and save it in 'n' variable. 
     if name 'n' is found, convert it into lower letters and return name. else return 'None'. """

def extract_name(text):
    try:
        # load spacy model
        nlp = spacy.load('en_core_web_md')
        # initialize matcher with a vocab
        matcher = Matcher(nlp.vocab, validate=False)
        # process text through nlp
        nlp_text = nlp(text)

        # First name and Last name are always Proper Nouns
        patterns = [[{'POS': 'PROPN'},{'POS': 'PROPN'},{'POS': 'PROPN'}]]
        
        # define pattern for name entity
        matcher.add("Name", patterns)

        # check/ find name in resume text
        matches = matcher(nlp_text)

        for match_id, start, end in matches:
            span = nlp_text[start:end]

            # transform into lower alphabets
            n = span.text

            # if name if found convert name into lower letters and return name
            if n:
                name = n.lower()
                return name

            else:
                return None

    except():
        print("Error. Name Not found")


# ----------------------------------------- extract_mobile_number ------------------------------------------ #
"""     This function find phone numbers in resume text. it take 'text' input and apply regex (regular expression) 
        on it. found the matching pattern in 'text' and save it 'phone' or 'phone1' variable.  """


def extract_mobile_number(text):
    # define and found regex pattern of phone number in resume text and save it in 'phone' variable
    phone = re.findall(re.compile(
        r'\(?\b[2-9][0-9]{2}\)?[-. ]?[2-9][0-9]{2}[-. ]?[0-9]{4}\b'), text)

    # if phone i.e is not equal to null.
    if phone:
        number = ''.join(phone[0])
        if len(number) > 13:
            return '+' + number
        else:
            return number

    # if phone is null. than find this pattern in resume text and save it in 'phone1' variable
    else:
        phone1 = re.findall(re.compile(
            r'(?:(?:\+?([1-9]|[0-9][0-9]|[0-9][0-9][0-9])\s*(?:[.-]\s*)?)?(?:\(\s*([2-9]1[02-9]|[2-9][02-8]1|[2-9][02-8][02-9])\s*\)|([0-9][1-9]|[0-9]1[02-9]|[2-9][02-8]1|[2-9][02-8][02-9]))\s*(?:[.-]\s*)?)?([2-9]1[02-9]|[2-9][02-9]1|[2-9][02-9]{2})\s*(?:[.-]\s*)?([0-9]{4})(?:\s*(?:#|x\.?|ext\.?|extension)\s*(\d+))?([0-9][1-9]|[0-9]1[02-9]|[2-9][02-8]1|[2-9][02-8][02-9])'),
            text)

        if phone1:
            number = ''.join(phone1[0])

            if len(number) > 13:
                return '+' + number
            else:
                return number


# ----------------------------------------- extract_email ------------------------------------------ #
"""     this function will look for email address in resume text. takes text as resume text input and look for 
        email address using regex pattern on it. if email is found than save it in email and return it. """


def extract_email(text):

    # define regular expression pattern for email fetching
    email = re.findall("([^@|\s]+@[^@]+\.[^@|\s]+)", text)

    # if email is fetch
    if email:
        try:
            # returning clean email address
            return email[0].split()[0].strip(';')
        except IndexError:
            return None



# ----------------------------------------- extract_skills ------------------------------------------ #
"""  this function takes input text (resume text) and looks for skills in it. it use defined skill keywords and 
     search for them in the text. when found save it in and array and return it. """


def extract_skills(resume_text):

    # load pre-trained spacy  model in nlp variable
    nlp = spacy.load('en_core_web_md')

    # process resume text through nlp
    doc = nlp(resume_text)
    noun_chunks = doc.noun_chunks

    nlp_text = nlp(resume_text)

    # removing stop words and implementing word tokenization
    tokens = [token.text for token in nlp_text if not token.is_stop]

    # reading the csv file of skill and skillset2
    data = pd.read_csv("skills.csv")
    data2 = pd.read_csv("skillsset2.csv", skiprows=1, names=['skills'])

    # extract values from data and data2
    skills = list(data.columns.values)
    skill2 = data2['skills'].tolist()

    # iterate over skill2 data and append it into skills fro one final skill dataset
    for i in skill2:
        skills.append(i)

    # initialize empty list
    skillset = []

    # check for one-grams (example: python)
    for token in tokens:

        # if token in skills , append it into skillset
        if token.lower() in skills:
            skillset.append(token)

    # check for bi-grams and tri-grams (example: machine learning)
    for token in noun_chunks:
        token = token.text.lower().strip()
        if token in skills:
            skillset.append(token)

    return [i.capitalize() for i in set([i.lower() for i in skillset])]


# ----------------------------------------- extract_education ------------------------------------------ #
"""     this function takes text (resume text) input and extract education from it.
        we define all the keywords related to education field in 'EDUCATION' and find the matching word in text. 
        if found, it will be save in education. """


def extract_education(resume_text):
    try:
        # load pre-trained model
        nlp = spacy.load('en_core_web_md')

        # Grad all general stop words
        STOPWORDS = set(stopwords.words('english'))

        # # Education Degrees keywords
        EDUCATION = ['BE', 'B.E.', 'B.E', 'BS', 'B.S', 'C.A.', 'c.a.', 'B.Com', 'B. Com', 'M. Com', 'M.Com', 'M. Com .',
                     'Business Management', 'Bachelors', "Bachelor's", 'business management', "Bachelor's Degree", 'ME',
                     "Bachelor’s Degree", 'M.E', 'M.E.', 'MS', 'M.S', ' Masters', 'Master', 'BTECH', 'B.TECH', 'M.TECH',
                     'MTECH', 'PHD', 'phd', 'Bachelor', 'ph.d', 'Ph.D.', 'MBA', 'mba', 'graduate', 'post-graduate',
                     '5 year integrated masters', 'masters', 'Master of Engineering', 'Secondary School Diploma',
                     'College',
                     'SSC', 'HSC', 'CBSE', 'ICSE', 'X', 'XII', 'Engineering in Mechanical Engineer', 'Engineering',
                     'Mechanical Engineering', 'Secondary School', 'Diploma', 'academy', 'school', 'certification',
                     'B. E', 'Materials Engineering', 'Secondary school', 'secondary school', "Secondary School"]

        # process resume  text through nlp
        nlp_text = nlp(resume_text)

        # Sentence Tokenizer
        nlp_text = [sent.string.strip() for sent in nlp_text.sents]

        edu = {}
        # Extract education degree
        for index, text in enumerate(nlp_text):
            for tex in text.split():
                # Replace all special symbols
                tex = re.sub(r'[?|$|.|!|,]', r'', tex)
                if tex in EDUCATION and tex not in STOPWORDS:
                    edu[tex] = text + nlp_text[index + 1]

        # Extract year
        education = []
        for key in edu.keys():
            year = re.search(re.compile(r'(((20|19)(\d{2})))'), edu[key])
            if year:
                education.append((key, ''.join(year[0])))
            else:
                # convert into lower case and return it
                ed = key.lower()
                education.append(ed)
        return education

    except:
        ("Error in reading education")


# ----------------------------------------- extract_experience ------------------------------------------ #
    """ this function takes text input and find experience years in it.
        it uses regex expression to look for few patterns in text. once found (any one) matching pattern. 
        it will save it in a variable."""


def extract_experience(text):

    # writing the REGEX in one line will make it very UGLY
    MONTHS_RE = ['Jan(?:uary)?', 'Feb(?:ruary)', 'Mar(?:ch)', 'Apr(?:il)?', 'May', 'Jun(?:e)?', 'Jul(?:y)?', 'Aug(?:ust)?', 'Oct(?:ober)?',
                 'Sep(?:tember)?','(?:Nov|Dec)(?:ember)?']

    # to match MONTH NAME and capture it (Jan(?:uary)?|Feb(?:ruary)...|(?:Nov|Dec)(?:ember)?)
    RE_MONTH = '({})'.format('|'.join(MONTHS_RE))

    # THIS MATCHES  MONTH FOLLOWED BY YEAR{2 or 4} I will use two times in Final REGEXP
    RE_DATE = '{RE_MONTH}(?:|[\s]+)(\d{{2,4}})'.format(RE_MONTH=RE_MONTH)

    # FINAL REGEX
    RE_VALID_RANGE = re.compile('{RE_DATE}.+?(?:{RE_DATE}|(present))'.format(RE_DATE=RE_DATE), flags=re.IGNORECASE)

    # if you want to extract both valid an invalide
    valid_ranges = []
    invalid_ranges = []
    exp_years = []

    for line in text.split('\n'):
        if line:
            groups = re.findall(RE_VALID_RANGE, line)
            if groups:
                # If you want to do something with range
                # all valid ranges are here my be 1 or 2 depends on the number of valid range in one line
                # every group have 4 elements because there is 4 capturing group
                # if M2,Y2 are not empty present is empty or the inverse only one of them is there (because of (?:{RE_DATE}|(present)) )

                M1, Y1, M2, Y2, present = groups[0]  # here use loop if you want to verify the values even more
                valid_ranges.append(line)
            else:
                invalid_ranges.append(line)

    # this yields only valid ranges if there is 2 in one line will yield two valid ranges
    # if you are dealing with lines this is not what you want

    valid_ranges = []
    final_exp = []

    for match in re.finditer(RE_VALID_RANGE, text):
        # if you want to check the ranges

        M1, Y1, M2, Y2, present = match.groups()
        valid_ranges.append(match.group(0))  # the text is returned here

    # if valid range -> above matching pattern found. return it
    if valid_ranges:
        for exp in valid_ranges:
            exp = exp.replace(r'\u','')
            final_exp.append(exp)
            final_exp = list(dict.fromkeys(final_exp))
        return final_exp

    # else look for this (i.e 2000 - 2003) pattern in text
    elif not valid_ranges:
        experience = re.findall(re.compile(r'(([1|2][0-9][0-9][0-9])+(\-)+([1|2][0-9][0-9][0-9]))'), text)

        # if matching pattern found than return it
        if experience:
            for e in experience:
                if e:
                    exp_years.append(e[0])

            for exp in exp_years:
                exp = exp.replace(r'\u','')
                final_exp.append(exp)
                final_exp = list(dict.fromkeys(final_exp))
            return final_exp

        # else look for this ( i.e january - present) pattern in text
        else:
            # print("looking in month regex. ")

            month = re.findall(re.compile("(?P<fmonth>\w+.\d+)\s+(\-)\s+((?P<smonth>\w+.\d+)|['Present'])"), text)
            for e in month:
                exp = e[0]+ " "+e[1]+ " " +e[2]
                # print("\n exp === ", exp)
                if e:
                    exp_years.append(exp)

            for exp in exp_years:
                exp = exp.replace(r'\u', '')
                final_exp.append(exp)
                final_exp = list(dict.fromkeys(final_exp))
            return final_exp
            # return exp_years


#   ----------------------------------- date converter ------------------------------------------------
"""     this function is used to convert date into proper datetime object to
        perform or calculate th difference."""


def date_converter(date1):
    # if date have month and year i.e: Aug 2018

    start = ""

    # check the month name in the date and convert it into " 1-01-18 "
    if (date1[0] == "January") or (date1[0] == "Jan") or (date1[0] == "january")  or (date1[0] == "JANUARY") or (date1[0] == "JAN") or (date1[0] == "01") or (date1[0] == "1"):
        start = "1-" + "01" + "-" + date1[1][2:]
        # print(start)

    elif (date1[0] == "February") or (date1[0] == "Feb") or (date1[0] == "february") or (date1[0] == "FEBRUARY") or (date1[0] == "FEB") or (date1[0] == "02") or (date1[0] == "2"):
        start = "1-" + "02" + "-" + date1[1][2:]
        # print(start)

    elif (date1[0] == "March") or (date1[0] == "Mar") or (date1[0] == "march")or (date1[0] == "MARCH") or (date1[0] == "MAR")  or (date1[0] == "03") or (date1[0] == "3"):
        start = "1-" + "03" + "-" + date1[1][2:]
        # print(start)

    elif (date1[0] == "April") or (date1[0] == "Apr") or (date1[0] == "april") or (date1[0] == "APRIL") or (date1[0] == "APR") or (date1[0] == "04") or (date1[0] == "4"):
        start = "1-" + "04" + "-" + date1[1][2:]
        # print(start)/

    elif (date1[0] == "May") or (date1[0] == "may") or (date1[0] == "MAY") or (date1[0] == "05") or (date1[0] == "5"):
        start = "1-" + "05" + "-" + date1[1][2:]
        # print(start)

    elif (date1[0] == "June") or (date1[0] == "Jun") or (date1[0] == "june") or (date1[0] == "JUNE") or (date1[0] == "JUN") or (date1[0] == "06") or (date1[0] == "6"):
        start = "1-" + "06" + "-" + date1[1][2:]
        # print(start)

    elif (date1[0] == "July") or (date1[0] == "Jul") or (date1[0] == "july") or (date1[0] == "JULY") or (date1[0] == "JUL") or (date1[0] == "07") or (date1[0] == "7"):
        start = "1-" + "07" + "-" + date1[1][2:]
        # print(start)

    elif (date1[0] == "August") or (date1[0] == "Aug") or (date1[0] == "august") or (date1[0] == "AUG") or (date1[0] == "AUGUST") or (date1[0] == "08") or (date1[0] == "8"):
        start = "1-" + "08" + "-" + date1[1][2:]
        # print(start)

    elif (date1[0] == "September") or (date1[0] == "Sep") or (date1[0] == "september") or (date1[0] == "SEPTEMBER") or (date1[0] == "SEP") or (date1[0] == "09") or (date1[0] == "9"):
        start = "1-" + "09" + "-" + date1[1][2:]
        # print(start)

    elif (date1[0] == "October") or (date1[0] == "Oct") or (date1[0] == "october") or (date1[0] == "OCTOBER") or (date1[0] == "OCT") or (date1[0] == "10") or (date1[0] == "10"):
        start = "01-" + "10" + "-" + date1[1][2:]
        # print(start)/

    elif (date1[0] == "November") or (date1[0] == "Nov") or (date1[0] == "november") or (date1[0] == "NOVEMBER") or (date1[0] == "NOV") or (date1[0] == "11") or (date1[0] == "11"):
        start = "1-" + "11" + "-" + date1[1][2:]
        # print(start)

    elif (date1[0] == "December") or (date1[0] == "Dec") or (date1[0] == "december") or (date1[0] == "DECEMBER") or (date1[0] == "DEC") or (date1[0] == "12") or (date1[0] == "12"):
        start = "1-" + "12" + "-" + date1[1][2:]

    #  for patterns like  i.e 2018 - 2019 or 05/2018
    else:
        # print("in end else ->  with only year in date ", date1[0])
        string = ""
        for i in date1:
            # if the date string contains - , that means it is 2018 - 2019 patterns  than seperat string with " - "
            for j in i:
                #  if -
                if j == "-":
                    string = date1[0].split("-")

        if string:
            #  if string ("2018" "2019" => dates separated ) than save first as start year and second index as end year
            first = string[0]
            last = string[1]
            start = "1-" + "01" + "-" + first[-2:]
            end = "1-" + "01" + "-" + last[-2:]

            return start, end

        else:
            # for pattern like " 05/2018 " separate by " /" and save first index as month and second as year
            string = date1[0].split("/")
            month = string[0]
            year = string[1]
            start = "1-" + month + "-" + year[-2:]

        return start

    return start


# -------------------------- date calculator -----------------------------------------
"""     this function is used to see the date pattern, if its like ' 2009 - present ', 
        then for present it will get the today's date and   """


def date_calculator(date1, date2):

    diff = []

    # agr date2 hai. mtlb apka pattern Aug 2018 Aug 2019 ka hai.
    if date2:
        for d in date2:
            #  call date_converter method and format date as datetime pattern for startdate
            start = date_converter(date1)

            s = datetime.strptime(start, "%d-%m-%y").date()

            #  if the date contains Present than fetch current date as end date
            if (d[0] == "Present") or (d[0] == "present") or (d[0] == "PRESENT") or (d[0] == "Current") or (
                    d[0] == "current") or (d[0] == "CURRENT"):

                # get today's date
                currentdate = datetime.now().date()

                # re arrange date pattern in day-month-year pattern and save it in enddate variable
                enddate = date.strftime(currentdate, "%d-%m-%y")
                ed = datetime.strptime(enddate, "%d-%m-%y").date()

                # calculate difference between start date and end date
                difference_in_years = relativedelta(ed, s).years
                difference_in_months = relativedelta(ed, s).months

                # calcualte the difference in years and month
                diff = ([difference_in_years , difference_in_months])

                return diff


            #  if its not present than it will contain a valid date and covert start and end date from date_converter and find difference in month and year
            else:
                start = date_converter(date1)

                s = datetime.strptime(start, "%d-%m-%y").date()

                enddate = date_converter(d)

                ed = datetime.strptime(enddate, "%d-%m-%y").date()

                difference_in_years = relativedelta(ed, s).years
                difference_in_months = relativedelta(ed, s).months

                diff = ([difference_in_years , difference_in_months])
                return diff

    #  for 2018 - 2019 and 05/2019 - 05/2020 patterns
    else:
        start, end = date_converter(date1)
        s = datetime.strptime(start, "%d-%m-%y").date()
        ed = datetime.strptime(end, "%d-%m-%y").date()
        difference_in_years = relativedelta(ed, s).years
        difference_in_months = relativedelta(ed, s).months
        diff = ([difference_in_years, difference_in_months])

        return diff


#   --------------------------------- calculate total experience ----------------------------------------------
"""     Calculate the total experience years in 'experience'. 
        it loop over the experience and calculate total moths and years of 
        experience and gives total year and total months in the form of """


def total_experience(experience):

    difference = []
    try:
        for exp in experience:
            exp = exp.split()
            date1 = []
            date2 = []
            index = 0
            date3 = ""
            for i in exp:
                #  separate date1(start date) and date2(end date)
                # agr " to " " - " wagaira  ajae toh os k agy ki string date2 (end date ) may save krdo wrna date1 may save krty jao
                if (i == "to") or (i == "—") or (i == "-") or (i == "–") or (i == "\ufffd"):
                    date2.append(exp[index+1:])
                    break
                date1.append(i)
                index += 1

            diff = date_calculator(date1, date2)
            # if difference:
            difference.append(diff)
            # return difference

    except:
        try:

            # if running this block then remove any previous element for list
            for d in difference:
                difference.remove(d)

            # iterate over experience
            for exp in experience:

                exp = exp.split()

                date1 = []
                date2 = []
                index = 0
                date3 = ""
                dte1 = []

                print("exception occured")

                for i in exp:
                    for ii in i:
                        #  seperate date1(start date) and date2(end date)
                        # agr " to " " - " wagaira  ajae toh os k agy ki string date2 (end date ) may save krdo wrna date1 may save krty jao
                        if (ii == "—") or (ii == "-") or (ii == "-") or (ii == "–") or (i == "\ufffd"):
                            e_d = i.split("-")
                            date2.append(e_d[-1:])
                            break
                        # date1.append(i)
                        index += 1

                    date3 = date3 + i
                    date3 = date3 + " "

                    dte1 = str(date3).split("-")

                    dte1 = dte1[:-1]
                    for i in dte1:
                        dte1 = i.split()

                date1.append(dte1[0])
                date1.append(dte1[-1])

                diff = date_calculator(date1, date2)
                difference.append(diff)

        except:
            try:

                # if running this block then remove any previous element for list

                for d in difference:
                    difference.remove(d)

                for exp in experience:
                    exp = exp.split()
                    date1 = []
                    date2 = []
                    index = 0
                    dte1 = []
                    date3 = ""
                    for i in exp:
                        for ii in i:
                            #  seperate date1(start date) and date2(end date)
                            # agr " to " " - " wagaira  ajae toh os k agy ki string date2 (end date ) may save krdo wrna date1 may save krty jao
                            if (ii == "to") or (ii == "—") or (ii == "-") or (ii == "–") or (i == "\ufffd"):
                                date2.append(exp[index + 1:])
                                break
                        dte1.append(i)
                        index += 1

                    ind = 0
                    count = 0
                    for d in dte1:

                        for dd in d:
                            if dd == "-":
                                ind = count
                            # print("dd =>",dd)
                                break
                                # dte1.remove[index:]
                        count +=1

                    d1 = dte1[ind]

                    split = d1.split("-")
                    c = 0
                    for i in date2:
                        c+=1
                        date2.remove(i)
                    if c > 0:
                        d = date2.append([ split[-1], dte1[-1]])
                    diff = date_calculator(date1, date2)
                    difference.append(diff)

            except:
                print("NO GIVEN OR VALID PATTERN FOUND")
                pass

    return difference


# -------------------------------- calculator -------------------------------------
"""     this function calculate the difference using total_experience   """


def calculator(exp):

    # save total experience in 'dif'
    dif = total_experience(exp)

    # initialize empty array
    total = [0, 0]

    # iterate over dif item
    for i in dif:
        # experience in year
        total[0]+= i[0]

        # experience in month
        total[1]+= i[1]

        # if total month is == 12 or greater than 12 but less than 24
        if (total[1] == 12) or (total[1] > 12 and total[1] < 24):

            # add 1 year in total year count and subtract 12 months from months count
            total[0] += 1
            total[1] -= 12

    # return total
    return total


# ----------------------------------------- extract_country ------------------------------------------ #
"""     this function use spacy model to process resume text and extract country name and return it    """


def extract_country(data):

    # load spacy model
    nlp = spacy.load('en_core_web_md')

    # process text through nlp
    doc = nlp(data)

    for ent in doc.ents:
        # find if country is present in text
        if ent.label_ in ['GPE', 'LOC']:
            country = ent.text.lower()
            return (country)


# ----------------------------------------- extract_designation ------------------------------------------ #
"""     this function is extracting designation. it uses 'FinderAcora' to extract designations from resume.
        it takes file and resume text data and return designation array """


def extract_designation(fn, data):
    # initialize empty list
    designations = []

    finder = FinderAcora()

    # give 'FinderAcora' function resume data
    print(data)

    try:
        f = finder.findall(data)
    except Exception:
        return

    # iterate over 'f'
    for match in f:
        # if match is not equal to CTO than convert the word into lower letters and append it into designation list
        if match[2] != "CTO":

            des = match[2]
            des = des.lower()
            designations.append(des)
    designations = list(dict.fromkeys(designations))

    # if designation
    if designations:
        return designations

    elif fn:
        extracted_data = ResumeParser(fn).get_extracted_data()
        if extracted_data:
            de = extracted_data['designation']
            if de == None:
                designation = extracted_data['experience']
                if designation:
                    design = designation[0].lower()
                    return design
            elif de:
                design = de[0].lower()
                return design
            else:
                return None


# ----------------------------------------- fine data ------------------------------------------ #
"""      this function is use to fine/ clean the extracted data before dumping it into db.  """


def finer(data):
    strng = data
    strng = strng.replace('"', "")
    strng = strng.replace('[', "")
    strng = strng.replace(']', "")
    return strng


# ----------------------------------------- fine phone number ------------------------------------------ #
"""      this function is use to fine/ clean the extracted phone number before dumping it into db.  """


def number_cleaner(ph_number):
    ph_number = ph_number.replace("-", "")
    ph_number = ph_number.replace(")", "")
    ph_number = ph_number.replace("(", "")
    ph_number = ph_number.replace("+", "")
    ph_number = ph_number.replace(".", "")

    return ph_number


# local database config
db_name = "clickhr"
db_password = "sohaib1998"
db_user = "root"
db_host = "127.0.0.1"

# server database config
# db_name = "addatsco_resume_database"
# db_password = "marYami8is!!!"
# db_user = "addatsco_maryam"
# db_host = "162.214.195.234"

# ----------------------------------------- extraction ------------------------------------------ #
"""      this function call all the other extraction function and pass the required data to these function. 
         the extracted value that is returned are save in variables. 
         """
def extraction(data, fn, scr_ques, fp, email_date, email_subject):

    # DB connection
    db = mysql.connect(host=db_host, user=db_user, password=db_password, database=db_name)
    
    cursor = db.cursor()

    # getting file name and file extension
    file_name, extension = os.path.splitext(fn)

    # if fn != "./resumes/Weekly report.pdf":
    # if file name
    if fn:
        n = extract_name(str(data))
        phone_number = extract_mobile_number(data)
        email = extract_email(data)
        skills = extract_skills(data)
        education = extract_education(data)
        experience = extract_experience(data)
        country = extract_country(data)
        address=extract_address(fn,country)  #Muhammad Sohaib
        designation = extract_designation(fn,data)
        screener_question = scr_ques
        e_date = email_date
        e_subject = email_subject
        resume_filePath = str(fp)
        total_exp = calculator(experience)

        if n:
            name = n
        # adding ' to email address
        if email:
            em_add = "'" + email + "'"

            # Selecting user by email ID (If exist)
            qry = (" SELECT * from resumeData WHERE email ={}".format(em_add))
            cursor.execute(qry)  # execute query
            find_user = cursor.fetchone()  # fetch result

            # print("\n\n\n find_user =>", find_user)

            #extract only Job title from e_subject
            e_sub = e_subject.split("-")
            e_sub2 = e_sub[0].split(":")

            job_title = ""

            if (e_sub2[0] == "Fw") or (e_sub2[0] == "Fwd"):
                # print("\n\n\n in esub_2")
                f = e_sub2[1]
                f = f.replace("candidate", "")
                # print("\n\n\n\n f after replacement  = > \t", f)

                job_title = f.lower()
                # print("\n\n job title = > \t", job_title)

            else:
                f = e_sub2[0]
                f = f.replace("candidate", "")

                job_title = f.lower()


            # extract only date from e_date
            dt = dateutil.parser.parse(e_date)
            applied_date = dt.strftime('%b %d, %Y')
            applied_date = applied_date.replace(",", "")
            applied_date = applied_date.lower()

            if phone_number:

                phone_number = number_cleaner(phone_number)



            # If there is no result => as there is no record of that user in DB => save the records in DB
            if find_user==None:

                # print("\n\n\n user not exist \n entering data into table")

                # converting skills and degree list [array] into json object so that it can be save in DB
                skl = json.dumps(skills)
                skill = finer(skl)

                educa = json.dumps(education)
                edu = finer(educa)

                exper = json.dumps(experience)
                exp = finer(exper)

                te = json.dumps(total_exp)
                t_e = finer(te)

                scr_que = json.dumps(screener_question)
                screener_que = finer(scr_que)

                # desig = json.dumps(designation)
                if designation:
                    # d = np.unique(designation)

                    des = json.dumps(designation)
                    desig = finer(des)
                    # print("\n\nfinal desig: {} \n\n".format(desig))
                    # desig = d[0]
                else:
                    desig = None

                # url = 'http://clickhrdb.8tkt.com/api/create'
                # myobj = {'name': name,
                #          'email': email ,
                #          'phone_number': phone_number ,
                #          'designation': desig ,
                #          'education': edu,
                #          'skills': skill,
                #          'experience': exp,
                #          'country': country,
                #          'screener_questions': screener_que,
                #          'resume_filePath': resume_filePath,
                #          'total_experience': total_experience }
                # x = requests.post(url, data=myobj)

                try:
                    # define Insert data query
                    query = "INSERT INTO resumeData(name, email , phone_number ,designation ,education, skills, experience, country, screener_questions, resume_filePath ,total_experience, applied_date, job_title, address) VALUES (%s, %s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                    ## define query parameters
                    values = (name, email, phone_number,desig, edu, skill, exp, country, screener_que, resume_filePath, t_e, applied_date, job_title, address)
                    # executing the query with values
                    cursor.execute(query, values)
                    # to make final output we have to run the 'commit()' method of the database object
                    db.commit()
                # if any error occure
                except:
                    ("\n\n\n \t\t Error occured while dumping data into Database \n\n\n")
        # if record aleady exist than skip and countinue
        else:
            print("\n Record already exist \n")
    else:
        print("\n wrong file")


# ----------------------------------------- extract_text_from_doc ------------------------------------------ #
"""      this function reads doc/docx files and return the text     """


def extract_text_from_doc(doc_path):
    # read and process doc file and save text in 'text'
    text = textract.process(doc_path)

    # decode and return text
    text = text.decode("utf-8")
    return text


# ----------------------------------------- extract_from_text_file ------------------------------------------ #
"""      this function reads text files and return the text     """


def extract_from_text_file(fn):
    # open the txt file and read and save the file line by line. return text
    with io.open(fn, 'r', encoding='utf8', errors='replace') as f:
        text = f.read()
    return text


# ----------------------------------------- extract_screener_question ------------------------------------------ #
"""     this function is used to read email html file and extract screener question from it.
        read the html file and process it through beautiful soup (BS) 
        extract the screener question part. clean and return it     """


def extract_screener_question_ionos(fn):
    # initialize empty list
    text = []
    txt = []

    # open and read file. save it in 'text' list
    with open(fn, "r") as f:
        text.append(f.read())

    # process through beautiful soup
    soup = BS(''.join(text))

    # remove = or \n (next line) character from test
    for my_str in text:
        my_str = my_str.replace("=", "")
        my_str = my_str.replace("\n", "")
        txt.append(my_str)

    # remove the file in which email html is saved after reading it
    os.remove(fn)

    # will give text only
    keywords = []

    # iterate over soup text
    for link in soup.find_all(text=True):
        line = link

        # stop appending keywords when Message word comes -> it indicate the ending of screener questions.
        end = "Message=\n"
        if line == end:
            break
        keywords.append(line)

        # save keywords in ques
        ques = keywords
        # initialize empty list
        screener_question = []

        # if link is not empty than remove it from 'ques' -> it is removing anything before the start of screener question
        if link:
            ques.remove(link)

            link = link.replace("=", "")
            link = link.replace("\n", "")

            # if link == "Screener questions" break the loop -> indicates that screener questions are starting
            if (link == "Screener questions"):
                break

    # if ques is not empty -> remove characters from it
    if ques:
        screener_question = []
        for i in ques:
            # print("\n\n i", i[0])
            if (i[0] == "<"):
                ques.remove(i)

        for i in ques:
            if (i[0] == "="):
                ques.remove(i)

        for i in ques:
            if i == "Message":
                break
            screener_question.append(i)

        for i in ques:
            if i == ' spacer line':
                break
            screener_question.append(i)

        scr = []
        final_ques = []

        for my_str in screener_question:
            my_str = my_str.replace("=", "")
            my_str = my_str.replace("\n", "")
            my_str = my_str.replace("\xa0", "")
            my_str = my_str.replace("</span>", "")
            my_str = my_str.replace("tr>", "")
            my_str = my_str.replace("C2A0", "")
            my_str = my_str.replace("</p>", "")
            my_str = my_str.replace("&nbsp;", "")
            scr.append(my_str)

        for i in scr:
            if i :
                if i == "Message":
                    break
                s = i.lower()
                final_ques.append(s)


# --------------------------------------------------- email reading ----------------------------------#
"""     if function read email from email account and save the email body into a file.
        extract attachments and check if attachment is pdf or doc or txt file and call function accordingly. """

def email_fetcher():
    # define your email address and your password
    user = 'jobs@y8hr.com'
    password = "Infiniti123?"

    # define email reading protocol
    mail = imaplib.IMAP4_SSL("imap.ionos.com", 993)

    # login to gmail account
    mail.login(user, password)

    # select inbox and read all messages
    mail.select('Inbox')

    # give 'ALL' if you want to read all emails from email account
    type, data = mail.search(None, 'ALL')

    # give 'UNSEEN' if ypu want to read only unseen or unread emails from email account
    # type, data = mail.search(None, 'UNSEEN')
    mail_ids = data[0]
    id_list = mail_ids.split()

    txt = []
    # fetching and downloading attachments
    for num in data[0].split():

        typ, data = mail.fetch(num, '(RFC822)')

        # converts byte literal to string removing b''
        raw_email = data[0][1]
        raw_email_string = raw_email.decode('utf-8')

        # downloading attachment
        email_message = email.message_from_string(raw_email_string)
        file_counter = 1

        # iterate over email data
        for part in email_message.walk():
            # this part comes from the snipped I don't understand yet...
            if part.get_content_maintype() == 'multipart':
                continue
            if part.get('Content-Disposition') is None:
                continue 

            fileName = part.get_filename()
            if bool(fileName):

                # read email for email body
                for response_part in data:
                    if isinstance(response_part, tuple):
                        msg = email.message_from_string(response_part[1].decode('utf-8'))

                        # extract email_date
                        email_date = email_message['Date']

                        # extract email_Subject
                        email_Subject = email_message['Subject']
 
                        # email_from = msg['from']

                        # extract the body and save it in file
                        txt = (msg.get_payload()[0])

                        # define file name and save email body into file
                        file = "xyz" + str(file_counter)
                        with open(file, 'w') as myfile:
                            myfile.write(str(txt))

                        file_counter += 1

                        # pass the file to extract_screener_question function to extract and return screener question
                        scr_que = extract_screener_question_ionos(file)

                filePath = os.path.join('./resumes', fileName)
                fp = os.path.abspath(filePath)


                if not os.path.isfile(filePath):
                    try:
                        fp = open(filePath, 'wb')
                        fp.write(part.get_payload(decode=True))
                        fp.close()
                    except Exception:
                        return

                subject = str(email_message).split("Subject: ", 1)[1].split("\nTo:", 1)[0]

                # file path
                fn = "./resumes/" + fileName

                # check file type => pdf, word, txt
                name, extension = os.path.splitext(fn)

                # Extract Data from resume according to file format


                # if file is in pdf format:
                if extension == '.pdf':
                    data = raw = parser.from_file(fn)
                    data = str(raw['content'])
                    extraction(data,fn, scr_que,fp, email_date, email_Subject)

                # if file is in docx/doc format:
                elif (extension =='.docx' or extension =='.doc'):
                    data = extract_text_from_doc(fn)
                    (data,fn, scr_que,fp, email_date, email_Subject)

                # if file is in txt format:
                elif extension == '.txt':
                    data = extract_from_text_file(fn)
                    extraction(data,fn, scr_que,fp, email_date, email_Subject)

                # if file is in any other formats then return format not found
                else:
                    print("\n Resume format not found \n")

    # close and logout from mail account
    mail.close()
    mail.logout()

# ------------------------------------- extract_address ------------------------------------------------# By: Muhammad Sohaib
def extract_address(fn,country):
    # opening pdf file
    parsed_pdf = parser.from_file(fn)
    address="" 
    # parsed_pdf['content'] returns string
    data = parsed_pdf['content'] 
    # saving content of pdf
    new_data=parsed_pdf.values()
    data=list(new_data)
    data=data[1]
    try:
        loc=data.find("Address:")
        if loc>0:
            i=int(loc+9)
            while(1):
                if data[i]=="\n":
                    break
                else:
                    i=i+1
        elif str(country)!="":
            address=country
        else:
            print("NO GIVEN OR VALID PATTERN FOUND")
            address=""
    except:
        print("NO GIVEN OR VALID PATTERN FOUND")
        address=country
    print(address)
    return address
