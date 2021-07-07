# import libraries

from flask import Flask, flash, render_template, redirect, url_for, request, session
import mysql.connector as mysql
from flask import jsonify
from flask_cors import CORS
#webbrowser module helps in open default web browser of os 
import webbrowser
from mysql.connector import cursor
#requests getting the urls
import requests
# from resume_reader import email_fetcher
import resume_reader
import requests
from datetime import date
from datetime import datetime
import os


app = Flask(__name__)

# enable cross origin connection
CORS(app)

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

""" ----------------------get all the user function to call in custom_api--------------------- """
@app.route("/api/getUsersData",methods=['GET'])
def get_all_data():
    db = mysql.connect(host=db_host, user=db_user, passwd=db_password, database=db_name)
    cursor = db.cursor()
    query = """Select * from ResumeData"""
    cursor.execute(query)
    data = cursor.fetchall()
    final_json_data = []
    if data:
        for row in data:
            dic = {'id': row[0], 'name': (row[1]), 'email': (row[2]), 'phone_number': (row[3]), 'designation': (row[4]), 'education': (row[5]), 'skills': (row[6]), 'experience': (row[7]), 'country': (row[14]), 'screener_question': (row[9]), 'total_experience': (row[10]), 'resume_filepath': (row[11]), 'applied_date': (row[12]), 'job_title': (row[13])}
            final_json_data.append(dic)
        cursor.close()
        db.close()
        return jsonify({'data': final_json_data})
    else:
        dic = {'id': 'None', 'name': 'None', 'email': 'None', 'phone_number': 'None', 'designation': 'None', 'education': 'None', 'skills': 'None', 'experience': 'None', 'country': 'None', 'screener_question': 'None', 'total_experience': 'None', 'resume_filepath': 'None', 'applied_date': 'None', 'job_title': 'None'}
        final_json_data.append(dic)
        return jsonify({'data': final_json_data})

"""-------------------------------------- URL RESTRICTION --------------------------------------------------"""
# def user_logged_in():
#     if session["userName"]==True:
#         pass
#     else:
#         return redirect("http://addats.com/html/sign-in.html")

"""        --------------------------------    GET ALL USER       -----------------------------------------     """


@app.route('/api/allusers', methods=['GET'])
def select_all_data():

    # DB connection
    db = mysql.connect(host=db_host, user=db_user, passwd=db_password, database=db_name)

    # creating an instance of 'cursor' class which is used to execute the 'SQL' statements in 'Python'
    cursor = db.cursor()

    # define query
    query = """Select * from ResumeData"""

    # executing the query
    cursor.execute(query)

    # fetch all values
    data = cursor.fetchall()

    # initialize empty list
    final_json_data = []

    # if data is not empty
    if data:

        # iterate over data rows and form dictionary object
        for row in data:
            dic = {'id': row[0], 'name': (row[1]), 'email': (row[2]), 'phone_number': (row[3]), 'designation': (row[4]), 'education': (row[5]), 'skills': (row[6]), 'experience': (row[7]), 'country': (row[14]), 'screener_question': (row[9]), 'total_experience': (row[10]), 'resume_filepath': (row[11]), 'applied_date': (row[12]), 'job_title': (row[13])}

            # append the dictionary object 'dic' into final_json data array
            final_json_data.append(dic)

        # close connections
        cursor.close()
        db.close()

        # return jsonify data
        return jsonify({'data': final_json_data})

    # if data is empty return None dic
    else:
        dic = {'id': 'None', 'name': 'None', 'email': 'None', 'phone_number': 'None', 'designation': 'None', 'education': 'None', 'skills': 'None', 'experience': 'None', 'country': 'None', 'screener_question': 'None', 'total_experience': 'None', 'resume_filepath': 'None', 'applied_date': 'None', 'job_title': 'None'}
        final_json_data.append(dic)

        return jsonify({'data': final_json_data})


"""     --------------------------------  GET ALL USER  BY NAME  -----------------------------------------     """


@app.route('/api/name', methods=['POST'])
def get_by_name():

    # DB connection
    db = mysql.connect(host=db_host, user=db_user, passwd=db_password, database=db_name)

    # creating an instance of 'cursor' class which is used to execute the 'SQL' statements in 'Python'
    cursor = db.cursor()

    # getting value from form and saving it into name
    name = request.form['value']

    # define query
    query = "Select * from ResumeData where name = %(value)s"

    # define query parameter
    params = {'value': name}

    # executing the query
    cursor.execute(query, params)

    # fetch all values
    data = cursor.fetchall()

    # initialize empty list
    final_json_data = []

    # if data is not empty
    if data:

        # iterate over data rows and form dictionary object
        for row in data:
            dic = {'id': row[0], 'name': (row[1]), 'email': (row[2]), 'phone_number': (row[3]), 'designation': (row[4]), 'education': (row[5]), 'skills': (row[6]), 'experience': (row[7]), 'country': (row[14]), 'screener_question': (row[9]), 'total_experience': (row[10]), 'resume_filepath': (row[11]), 'applied_date': (row[12]), 'job_title': (row[13])}

            # append the dictionary object 'dic' into final_json data array
            final_json_data.append(dic)

        # close connections
        cursor.close()
        db.close()

        # return jsonify data
        return jsonify({'data': final_json_data})

    # if data is empty return None dic
    else:
        dic = {'id': 'None', 'name': 'None', 'email': 'None', 'phone_number': 'None', 'designation': 'None', 'education': 'None', 'skills': 'None', 'experience': 'None', 'country': 'None', 'screener_question': 'None', 'total_experience': 'None', 'resume_filepath': 'None', 'applied_date': 'None', 'job_title': 'None'}
        final_json_data.append(dic)

        return jsonify({'data': final_json_data})


"""     --------------------------------  GET ALL USER  BY EMAIL  -----------------------------------------     """


@app.route('/api/email', methods=['POST'])
def get_by_email():

    # DB connection
    db = mysql.connect(host=db_host, user=db_user, passwd=db_password, database=db_name)

    # creating an instance of 'cursor' class which is used to execute the 'SQL' statements in 'Python'
    cursor = db.cursor()

    # getting value from form and saving it into email
    email = request.form['value']

    # define query
    query = "Select * from ResumeData where email = %(value)s"

    # define query parameter
    params = {'value': email}

    # executing the query
    cursor.execute(query, params)

    # fetch all values
    data = cursor.fetchall()

    # initialize empty list
    final_json_data = []

    # if data is not empty
    if data:

        # iterate over data rows and form dictionary object
        for row in data:
            dic = {'id': row[0], 'name': (row[1]), 'email': (row[2]), 'phone_number': (row[3]), 'designation': (row[4]), 'education': (row[5]), 'skills': (row[6]), 'experience': (row[7]), 'country': (row[14]), 'screener_question': (row[9]), 'total_experience': (row[10]), 'resume_filepath': (row[11]), 'applied_date': (row[12]), 'job_title': (row[13])}

            # append the dictionary object 'dic' into final_json data array
            final_json_data.append(dic)

        # close connections
        cursor.close()
        db.close()

        # return jsonify data
        return jsonify({'data': final_json_data})

    # if data is empty return None dic
    else:
        dic = {'id': 'None', 'name': 'None', 'email': 'None', 'phone_number': 'None', 'designation': 'None', 'education': 'None', 'skills': 'None', 'experience': 'None', 'country': 'None', 'screener_question': 'None', 'total_experience': 'None', 'resume_filepath': 'None', 'applied_date': 'None' , 'job_title': 'None'}
        final_json_data.append(dic)

        return jsonify({'data': final_json_data})


"""   --------------------------------  GET ALL USER  BY PHONE NUMBER  -----------------------------------------     """


@app.route('/api/phoneNumber', methods=['POST'])
def get_by_phone_number():

    # DB connection
    db = mysql.connect(host=db_host, user=db_user, passwd=db_password, database=db_name)

    # creating an instance of 'cursor' class which is used to execute the 'SQL' statements in 'Python'
    cursor = db.cursor()

    # getting value from form and saving it into phone_number
    phone_number = request.form['value']

    # define query
    query = "Select * from ResumeData where phone_number = %(value)s"

    # define query parameter
    params = {'value': phone_number}

    # executing the query
    cursor.execute(query, params)

    # fetch all values
    data = cursor.fetchall()

    # initialize empty list
    final_json_data = []

    # if data is not empty
    if data:

        # iterate over data rows and form dictionary object
        for row in data:
            dic = {'id': row[0], 'name': (row[1]), 'email': (row[2]), 'phone_number': (row[3]), 'designation': (row[4]), 'education': (row[5]), 'skills': (row[6]), 'experience': (row[7]), 'country': (row[14]), 'screener_question': (row[9]), 'total_experience': (row[10]), 'resume_filepath': (row[11]), 'applied_date': (row[12]), 'job_title': (row[13])}

            # append the dictionary object 'dic' into final_json data array
            final_json_data.append(dic)

        # close connections
        cursor.close()
        db.close()

        # return jsonify data
        return jsonify({'data': final_json_data})

    # if data is empty return None dic
    else:
        dic = {'id': 'None', 'name': 'None', 'email': 'None', 'phone_number': 'None', 'designation': 'None', 'education': 'None', 'skills': 'None', 'experience': 'None', 'country': 'None', 'screener_question': 'None', 'total_experience': 'None', 'resume_filepath': 'None', 'applied_date': 'None', 'job_title': 'None'}
        final_json_data.append(dic)

        return jsonify({'data': final_json_data})


"""   --------------------------------  GET ALL USER  BY COUNTRY  -----------------------------------------     """


@app.route('/api/country', methods=['POST'])
def get_by_country():

    # DB connection
    db = mysql.connect(host=db_host, user=db_user, passwd=db_password, database=db_name)

    # creating an instance of 'cursor' class which is used to execute the 'SQL' statements in 'Python'
    cursor = db.cursor()

    # get parameter input from user
    country = request.form['value']

    # define query
    query = "Select * from ResumeData where country = %(value)s"

    # define query parameter
    params = {'value': country}

    # executing the query
    cursor.execute(query, params)

    # fetch all values
    data = cursor.fetchall()

    # initialize empty list
    final_json_data = []

    # if data is not empty
    if data:

        # iterate over data rows and form dictionary object
        for row in data:
            dic = {'id': row[0], 'name': (row[1]), 'email': (row[2]), 'phone_number': (row[3]), 'designation': (row[4]), 'education': (row[5]), 'skills': (row[6]), 'experience': (row[7]), 'country': (row[14]), 'screener_question': (row[9]), 'total_experience': (row[10]), 'resume_filepath': (row[11]), 'applied_date': (row[12]), 'job_title': (row[13])}

            # append the dictionary object 'dic' into final_json data array
            final_json_data.append(dic)

        # close connections
        cursor.close()
        db.close()

        # return jsonify data
        return jsonify({'data': final_json_data})

    # if data is empty return None dic
    else:
        dic = {'id': 'None', 'name': 'None', 'email': 'None', 'phone_number': 'None', 'designation': 'None', 'education': 'None', 'skills': 'None', 'experience': 'None', 'country': 'None', 'screener_question': 'None', 'total_experience': 'None', 'resume_filepath': 'None', 'applied_date': 'None', 'job_title': 'None'}
        final_json_data.append(dic)

        return jsonify({'data': final_json_data})


"""   --------------------------------  GET ALL USER  BY SKILLS  -----------------------------------------     """


@app.route('/api/skill', methods=['POST'])
def get_by_skill():

    # DB connection
    db = mysql.connect(host=db_host, user=db_user, passwd=db_password, database=db_name)

    # creating an instance of 'cursor' class which is used to execute the 'SQL' statements in 'Python'
    cursor = db.cursor()

    # getting value from form and saving it into skill
    skill = request.form['value']

    # format in lower letters
    skill = skill.lower()

    # get all data -> calling get_all_data function
    data = get_all_data()

    # initialize empty list
    skills = []
    d_skills = []

    # iterate over data rows
    for i in data:

        # define used_id and skills data in row
        user_id = i[0]
        skills = i[6]

        # if skills is not empty
        if skills:

            # format in lower letters
            skills = skills.lower()

            # if given skill is in skill set then fetch that user by id
            if skill in skills:

                # define query
                query = "Select * from ResumeData where id = %(value)s"

                # define query parameter
                params = {'value': user_id}

                # executing the query
                cursor.execute(query, params)

                # fetch all values
                d = cursor.fetchall()

                # append the fetch data into d_skills list
                d_skills.append(d)

    # initialize empty list
    final_json_data = []

    # if d_skill is not empty
    if d_skills:

        # iterate over every single list in list of lists
        for r in d_skills:

            # iterate over list elements/rows and form dictionary object
            for row in r:
                dic = {'id': row[0], 'name': (row[1]), 'email': (row[2]), 'phone_number': (row[3]), 'designation': (row[4]), 'education': (row[5]), 'skills': (row[6]), 'experience': (row[7]), 'country': (row[14]), 'screener_question': (row[9]), 'total_experience': (row[10]), 'resume_filepath': (row[11]), 'applied_date': (row[12]), 'job_title': (row[13])}

                # append the dictionary object 'dic' into final_json data array
                final_json_data.append(dic)

        # close connections
        cursor.close()
        db.close()

        # return jsonify data
        return jsonify({'data': final_json_data})

    # if data is empty return None dic
    else:
        dic = {'id': 'None', 'name': 'None', 'email': 'None', 'phone_number': 'None', 'designation': 'None', 'education': 'None', 'skills': 'None', 'experience': 'None', 'country': 'None', 'screener_question': 'None', 'total_experience': 'None', 'resume_filepath': 'None', 'applied_date': 'None', 'job_title': 'None'}
        final_json_data.append(dic)

        return jsonify({'data': final_json_data})


"""   --------------------------------  GET ALL USER  BY DESIGNATION  -----------------------------------------     """


@app.route('/api/designation', methods=['POST'])
def get_by_designation():

    # DB connection
    db = mysql.connect(host=db_host, user=db_user, passwd=db_password, database=db_name)

    # creating an instance of 'cursor' class which is used to execute the 'SQL' statements in 'Python'
    cursor = db.cursor()

    # getting value from form and saving it into designation
    designation = request.form['value']

    designation = designation.lower()

    # get all data -> calling get_all_data function
    data = get_all_data()

    designations = []
    d_designations = []

    # iterate over data rows
    for i in data:

        # define used_id and designations data in row
        user_id = i[0]
        designations = i[4]

        # if designations is not empty
        if designations:

            # format in lower letters
            designations = designations.lower()

            # if given designation is in designations set then fetch that user by id
            if designation in designations:

                # define query
                query = "Select * from ResumeData where id = %(value)s"

                # define query parameter
                params = {'value': user_id}

                # executing the query
                cursor.execute(query, params)

                # fetch all values
                d = cursor.fetchall()

                # append the fetch data into d_designations list
                d_designations.append(d)

    # initialize empty list
    final_json_data = []

    # if d_designations is not empty
    if d_designations:

        # iterate over every single list in list of lists
        for r in d_designations:

            # iterate over list elements/rows and form dictionary object
            for row in r:
                dic = {'id': row[0], 'name': (row[1]), 'email': (row[2]), 'phone_number': (row[3]), 'designation': (row[4]), 'education': (row[5]), 'skills': (row[6]), 'experience': (row[7]), 'country': (row[14]), 'screener_question': (row[9]), 'total_experience': (row[10]), 'resume_filepath': (row[11]), 'applied_date': (row[12]), 'job_title': (row[13])}

                # append the dictionary object 'dic' into final_json data array
                final_json_data.append(dic)

        # close connections
        cursor.close()
        db.close()

        # return jsonify data
        return jsonify({'data': final_json_data})

    # if data is empty return None dic
    else:
        dic = {'id': 'None', 'name': 'None', 'email': 'None', 'phone_number': 'None', 'designation': 'None', 'education': 'None', 'skills': 'None', 'experience': 'None', 'country': 'None', 'screener_question': 'None', 'total_experience': 'None', 'resume_filepath': 'None', 'applied_date': 'None', 'job_title': 'None'}
        final_json_data.append(dic)

        return jsonify({'data': final_json_data})


"""   --------------------------------  GET ALL USER  BY EDUCATION  -----------------------------------------     """


@app.route('/api/education', methods=['POST'])
def get_by_education():

    # DB connection
    db = mysql.connect(host=db_host, user=db_user, passwd=db_password, database=db_name)

    # creating an instance of 'cursor' class which is used to execute the 'SQL' statements in 'Python'
    cursor = db.cursor()

    # getting value from form and saving it into education
    education = request.form['value']

    # converting the inputted data into lower letters
    education = education.lower()

    # get all data -> calling get_all_data function
    data = get_all_data()

    # initialize empty list
    educations = []
    d_educations = []

    # iterate over data rows
    for i in data:

        # define used_id and skills data in row
        user_id = i[0]
        educations = i[5]

        # if educations is not empty
        if educations:

            # format in lower letters
            educations = educations.lower()

            # if given skill is in skill set then fetch that user by id
            if education in educations:

                # define query
                query = "Select * from ResumeData where id = %(value)s"

                # define query parameter
                params = {'value': user_id}

                # executing the query
                cursor.execute(query, params)

                # fetch all values
                d = cursor.fetchall()

                # append fetch data into d_education
                d_educations.append(d)

    # initialize empty list
    final_json_data = []

    # if d_skill is not empty
    if d_educations:

        # iterate over every single list in list of lists
        for r in d_educations:

            # iterate over list elements/rows and form dictionary object
            for row in r:
                dic = {'id': row[0], 'name': (row[1]), 'email': (row[2]), 'phone_number': (row[3]), 'designation': (row[4]), 'education': (row[5]), 'skills': (row[6]), 'experience': (row[7]), 'country': (row[14]), 'screener_question': (row[9]), 'total_experience': (row[10]), 'resume_filepath': (row[11]), 'applied_date': (row[12]), 'job_title': (row[13])}

                # append the dictionary object 'dic' into final_json data array
                final_json_data.append(dic)

        # close connections
        cursor.close()
        db.close()

        # return jsonify data
        return jsonify({'data': final_json_data})

    # if data is empty return None dic
    else:
        dic = {'id': 'None', 'name': 'None', 'email': 'None', 'phone_number': 'None', 'designation': 'None', 'education': 'None', 'skills': 'None', 'experience': 'None', 'country': 'None', 'screener_question': 'None', 'total_experience': 'None', 'resume_filepath': 'None', 'applied_date': 'None', 'job_title': 'None'}
        final_json_data.append(dic)

        return jsonify({'data': final_json_data})


"""   --------------------------------  GET ALL USER  BY EXPERIENCE  -----------------------------------------     """


@app.route('/api/experience', methods=['POST'])
def get_by_experience():

    # DB connection
    db = mysql.connect(host=db_host, user=db_user, passwd=db_password, database=db_name)

    # creating an instance of 'cursor' class which is used to execute the 'SQL' statements in 'Python'
    cursor = db.cursor()

    # getting value from form and saving it into experience
    experience = request.form['value']

    # get all data -> calling get_all_data function
    data = get_all_data()

    # initialize empty list
    experiences = []
    d_experiences = []

    # iterate over data rows
    for i in data:

        # define used_id and exp data in row
        user_id = i[0]
        exp = i[10]

        # taking only year form exp
        experiences = exp[1]

        # if experiences is not empty
        if experiences:

            # if given experience is in experiences set then fetch that user by id
            if experience in experiences:

                # define query
                query = "Select * from ResumeData where id = %(value)s"

                # define query parameter
                params = {'value': user_id}

                # executing the query
                cursor.execute(query, params)

                # fetch all values
                d = cursor.fetchall()

                # append the fetch data into d_experiences list
                d_experiences.append(d)

    # initialize empty list
    final_json_data = []

    # if d_experiences is not empty
    if d_experiences:

        # iterate over every single list in list of lists
        for r in d_experiences:

            # iterate over list elements/rows and form dictionary object
            for row in r:
                dic = {'id': row[0], 'name': (row[1]), 'email': (row[2]), 'phone_number': (row[3]), 'designation': (row[4]), 'education': (row[5]), 'skills': (row[6]), 'experience': (row[7]), 'country': (row[14]), 'screener_question': (row[9]), 'total_experience': (row[10]), 'resume_filepath': (row[11]), 'applied_date': (row[12]), 'job_title': (row[13])}

                # append the dictionary object 'dic' into final_json data array
                final_json_data.append(dic)

        # close connection
        cursor.close()
        db.close()

        # return jsonify data
        return jsonify({'data': final_json_data})

    # if data is empty return None dic
    else:
        dic = {'id': 'None', 'name': 'None', 'email': 'None', 'phone_number': 'None', 'designation': 'None', 'education': 'None', 'skills': 'None', 'experience': 'None', 'country': 'None', 'screener_question': 'None', 'total_experience': 'None', 'resume_filepath': 'None',  'applied_date': 'None', 'job_title': 'None'}
        final_json_data.append(dic)

        return jsonify({'data': final_json_data})


"""   -------------------------------  GET ALL USER  BY SCREENER QUESTION  -------------------------------------     """


@app.route('/api/scrQues', methods=['POST'])
def get_by_scrques():

    # DB connection
    db = mysql.connect(host=db_host, user=db_user, passwd=db_password, database=db_name)

    # creating an instance of 'cursor' class which is used to execute the 'SQL' statements in 'Python'
    cursor = db.cursor()

    # getting value from form and saving it into scr_ques
    scr_ques = request.form['value']

    # get all data -> calling get_all_data function
    data = get_all_data()

    # initialize empty list
    experiences = []
    d_scrQuestions = []

    # iterate over data rows
    for i in data:

        # define used_id and scrQuestion data in row
        user_id = i[0]
        scrQuestion = i[9]

        # if scrQuestion is not empty
        if scrQuestion:

            # if given scr_ques is in scrQuestion set then fetch that user by id
            if scr_ques in scrQuestion:
                query = "Select * from ResumeData where id = %(value)s"
                params = {'value': user_id}

                # executing the query
                cursor.execute(query, params)

                # fetch all values
                d = cursor.fetchall()

                # append the fetch data into d_scrQuestions
                d_scrQuestions.append(d)

    # initialize empty list
    final_json_data = []

    # if d_scrQuestions is not empty
    if d_scrQuestions:

        # iterate over every single list in list of lists
        for r in d_scrQuestions:

            # iterate over list elements/rows and form dictionary object
            for row in r:
                dic = {'id': row[0], 'name': (row[1]), 'email': (row[2]), 'phone_number': (row[3]), 'designation': (row[4]), 'education': (row[5]), 'skills': (row[6]), 'experience': (row[7]), 'country': (row[14]), 'screener_question': (row[9]), 'total_experience': (row[10]), 'resume_filepath': (row[11]), 'applied_date': (row[12]), 'job_title': (row[13])}

                # append the dictionary object 'dic' into final_json data array
                final_json_data.append(dic)

        # close connection
        cursor.close()
        db.close()

        # return jsonify data
        return jsonify({'data': final_json_data})

    # if data is empty return None dic
    else:
        dic = {'id': 'None', 'name': 'None', 'email': 'None', 'phone_number': 'None', 'designation': 'None', 'education': 'None', 'skills': 'None', 'experience': 'None', 'country': 'None', 'screener_question': 'None', 'total_experience': 'None', 'resume_filepath': 'None',  'applied_date': 'None', 'job_title': 'None'}
        final_json_data.append(dic)

        return jsonify({'data': final_json_data})


"""   -------------------  CUSTOM API TO FETCH DATA WITHOUT GIVING ANY FILTER/COLOUM NAME  --------------------     """


@app.route('/api/custom_api', methods=['POST'])
def custom_api():

    # DB connection
    db = mysql.connect(host=db_host, user=db_user, passwd=db_password, database=db_name)

    # creating an instance of 'cursor' class which is used to execute the 'SQL' statements in 'Python'
    cursor = db.cursor()

    # getting value from form and saving it into value
    value = request.form['value']

    # initialize empty list
    data = []
    final_json_data = []

    # define query
    query = "Select * from ResumeData WHERE %(value)s IN (name, email, phone_number, country, skills, designation, education, total_experience, screener_questions, applied_date, job_title );"

    # define query parameter
    params = {'value': value}

    # executing the query
    cursor.execute(query, params)

    # fetch all values
    d = cursor.fetchall()

    # append fetch data into data list
    data.append(d)

    # if data's first element is not empty
    if data[0]:

        # iterate over every single list in list of lists
        for r in data:

            # iterate over list elements/rows and form dictionary object
            for row in r:
                dic = {'id': row[0], 'name': (row[1]), 'email': (row[2]), 'phone_number': (row[3]), 'designation': (row[4]),'education': (row[5]), 'skills': (row[6]), 'experience': (row[7]), 'country': (row[14]),'screener_question': (row[9]), 'total_experience': (row[10]), 'resume_filepath': (row[11]), 'applied_date': (row[12]), 'job_title': (row[13])}

                # append the dictionary object 'dic' into final_json data array
                final_json_data.append(dic)

        # return jsonify data
        return jsonify({'data': final_json_data})

    # initialize empty list
    d_data = []

    # if data's first element is not empty
    if not data[0]:

        # call get_all_user function to get all users data
        d = get_all_data()
        experiences = []

        # iterate over data rows
        for i in d:

            # define used_id, designation,education, skill, exp, experiences,scr_ques,job_title and app_date data in row
            user_id = i[0]
            designation = i[4]
            education = i[5]
            skill = i[6]
            exp = i[10]
            experiences = exp[1]
            scr_ques = i[9]
            job_title = i[12]
            app_date = i[13]

            # if experience is not empty
            if experiences:

                # if given value is in experiences set then fetch that user by id
                if (value in experiences):

                    # define query
                    query = "Select * from ResumeData where id = %(value)s"

                    # define query parameter
                    params = {'value': user_id}

                    # executing the query
                    cursor.execute(query, params)

                    # fetch all values
                    d = cursor.fetchall()

                    # append fetch data into d_data
                    d_data.append(d)

                # if d_data is empty
                if not d_data:

                    # if designation is not empty
                    if designation:

                        # if given value is in designation set then fetch that user by id
                        if (value in designation):

                            # define query
                            query = "Select * from ResumeData where id = %(value)s"

                            # define query parameter
                            params = {'value': user_id}

                            # executing the query
                            cursor.execute(query, params)

                            # fetch all values
                            d = cursor.fetchall()

                            # append fetch data into d_data
                            d_data.append(d)

                # if d_data is empty
                if not d_data:

                    # if education is not empty
                    if education:

                        # if given value is in education set then fetch that user by id
                        if(value in education):

                            # define query
                            query = "Select * from ResumeData where id = %(value)s"

                            # define query parameter
                            params = {'value': user_id}

                            # executing the query
                            cursor.execute(query, params)

                            # fetch all values
                            d = cursor.fetchall()

                            # append fetch data into d_data
                            d_data.append(d)

                # if d_data is empty
                if not d_data:

                    # if skill is not empty
                    if skill:

                        # if given value is in skill set then fetch that user by id
                        if (value in skill):

                            # define query
                            query = "Select * from ResumeData where id = %(value)s"

                            # define query parameter
                            params = {'value': user_id}

                            # executing the query
                            cursor.execute(query, params)

                            # fetch all values
                            d = cursor.fetchall()

                            # append fetch data into d_data
                            d_data.append(d)

                # if d_data is empty
                if not d_data:

                    # if scr_ques is not empty
                    if scr_ques:

                        # if given value is in scr_ques set then fetch that user by id
                        if (value in scr_ques):

                            # define query
                            query = "Select * from ResumeData where id = %(value)s"

                            # define query parameter
                            params = {'value': user_id}

                            # executing the query
                            cursor.execute(query, params)

                            # fetch all values
                            d = cursor.fetchall()

                            # append fetch data into d_data
                            d_data.append(d)

                # if d_data is empty
                if not d_data:

                    # if job_title is not empty
                    if job_title:

                        # if given value is in job_title set then fetch that user by id
                        if (value in job_title):

                            # define query
                            query = "Select * from ResumeData where id = %(value)s"

                            # define query parameter
                            params = {'value': user_id}

                            # executing the query
                            cursor.execute(query, params)

                            # fetch all values
                            d = cursor.fetchall()

                            # append fetch data into d_data
                            d_data.append(d)

                # if d_data is empty
                if not d_data:

                    # if app_date is not empty
                    if app_date:

                        # if given value is in app_date set then fetch that user by id
                        if (value in app_date):

                            # define query
                            query = "Select * from ResumeData where id = %(value)s"

                            # define query parameter
                            params = {'value': user_id}

                            # executing the query
                            cursor.execute(query, params)

                            # fetch all values
                            d = cursor.fetchall()

                            # append fetch data into d_data
                            d_data.append(d)

    # if d_data is not empty
    if d_data:

        # iterate over every single list in list of lists
        for r in d_data:

            # iterate over list elements/rows and form dictionary object
            for row in r:
                dic = {'id': row[0], 'name': (row[1]), 'email': (row[2]), 'phone_number': (row[3]), 'designation': (row[4]), 'education': (row[5]), 'skills': (row[6]), 'experience': (row[7]), 'country': (row[14]), 'screener_question': (row[9]), 'total_experience': (row[10]), 'resume_filepath': (row[11]),  'applied_date': (row[12]), 'job_title': (row[13])}

                # append the dictionary object 'dic' into final_json data array
                final_json_data.append(dic)

        # close conections
        cursor.close()
        db.close()

        # return jsonify data
        return jsonify({'data': final_json_data})

    # if data is empty return None dic
    else:
        dic = {'id': 'None', 'name': 'None', 'email': 'None', 'phone_number': 'None', 'designation': 'None',
               'education': 'None', 'skills': 'None', 'experience': 'None', 'country': 'None',
               'screener_question': 'None', 'total_experience': 'None', 'resume_filepath': 'None', 'applied_date': 'None', 'job_title': 'None'}
        final_json_data.append(dic)

        return jsonify({'data': final_json_data})


"""   --------------------------------  GET USER  BY ID  -----------------------------------------     """


@app.route('/api/user/<id>', methods=['POST'])
def select_user(id):

    # sava user id coming in url into user_id
    user_id = id

    # DB connection
    db = mysql.connect(host=db_host, user=db_user, passwd=db_password, database=db_name)

    # creating an instance of 'cursor' class which is used to execute the 'SQL' statements in 'Python'
    cursor = db.cursor()

    # define query
    query_resume = "Select * from ResumeData where id = %(value)s"

    # define query parameter
    params = {'value': user_id}

    # executing the query
    cursor.execute(query_resume, params)

    # fetch results
    data_resume = cursor.fetchall()

    # define fetch query from call record table
    query_callRecord = "Select * from CallRecord where ResumeData_id = %(value)s"

    # pass phone_number and queury parmertr
    cursor.execute(query_callRecord, params)

    # fetch all values
    data_callRecord = cursor.fetchall()

    # initialize empty list
    final_json_data = []

    # iterate over data rows and form dictionary object
    for row in data_resume:
        dic = {'id': row[0], 'name': (row[1]), 'email': (row[2]), 'phone_number': (row[3]), 'designation': (row[4]), 'education': (row[5]), 'skills': (row[6]), 'experience': (row[7]), 'country': (row[8]), 'screener_question': (row[9]), 'total_experience': (row[10]), 'resume_filepath': (row[11]), 'applied_date': (row[12]), 'job_title': (row[14])}

        # append the dictionary object 'dic' into final_json data array
        final_json_data.append(dic)

    # check call record data is empty or not
    if data_callRecord:

        # iterate over data_record and append in dic
        for row in data_callRecord:
            dic['status'] = row[1]
            dic['join_date'] = row[2]
            dic['agent'] = row[3]

            final_json_data.append(dic)

    # if call record data is empty return None in data
    else:
        dic['status'] = "None"
        dic['join_date'] = "None"
        dic['agent'] = "None"
        final_json_data.append(dic)

    # closing cursor
    cursor.close()
    db.close()

    # return jsonify data
    return jsonify({'data': final_json_data})


"""     --------------------------------  GET ALL USER  BY JOB TITLE  -----------------------------------------     """


@app.route('/api/jobTitle', methods=['POST'])
def get_by_jobTitle():

    # DB connection
    db = mysql.connect(host=db_host, user=db_user, passwd=db_password, database=db_name)

    # creating an instance of 'cursor' class which is used to execute the 'SQL' statements in 'Python'
    cursor = db.cursor()

    # getting value from form and saving it into job_title
    job_title = request.form['value']

    # get all data -> calling get_all_data function
    data = get_all_data()

    # initialize empty list
    experiences = []
    d_jobtitle = []

    # iterate over data rows
    for i in data:

        # define used_id and job_t data in row
        user_id = i[0]
        job_t = i[13]

        # if job_t is not empty
        if job_t:

            # if given job_title is in job_t set then fetch that user by id
            if job_title in job_t:

                # define query
                query = "Select * from ResumeData where id = %(value)s"

                # define query parameter
                params = {'value': user_id}

                # executing the query
                cursor.execute(query, params)

                # fetch all values
                d = cursor.fetchall()

                # append fetch data into d_jobtitle
                d_jobtitle.append(d)

    # initialize empty list
    final_json_data = []

    # if d_jobtitle is not empty
    if d_jobtitle:

        # iterate over every single list in list of lists
        for r in d_jobtitle:

            # iterate over list elements/rows and form dictionary object
            for row in r:
                dic = {'id': row[0], 'name': (row[1]), 'email': (row[2]), 'phone_number': (row[3]), 'designation': (row[4]), 'education': (row[5]), 'skills': (row[6]), 'experience': (row[7]), 'country': (row[14]), 'screener_question': (row[9]), 'total_experience': (row[10]), 'resume_filepath': (row[11]), 'applied_date': (row[12]), 'job_title': (row[13])}

                # append the dictionary object 'dic' into final_json data array
                final_json_data.append(dic)

        # closing connetions
        cursor.close()
        db.close()

        # return jsonify data
        return jsonify({'data': final_json_data})

    # if data is empty return None dic
    else:
        dic = {'id': 'None', 'name': 'None', 'email': 'None', 'phone_number': 'None', 'designation': 'None', 'education': 'None', 'skills': 'None', 'experience': 'None', 'country': 'None', 'screener_question': 'None', 'total_experience': 'None', 'resume_filepath': 'None',  'applied_date': 'None', 'job_title': 'None'}
        final_json_data.append(dic)

        return jsonify({'data': final_json_data})


"""     ------------------------------  GET ALL USER  BY APPLIED DATE  -----------------------------------------     """


@app.route('/api/appliedDate', methods=['POST'])
def get_by_appliedDate():

    # DB connection
    db = mysql.connect(host=db_host, user=db_user, passwd=db_password, database=db_name)

    # creating an instance of 'cursor' class which is used to execute the 'SQL' statements in 'Python'
    cursor = db.cursor()

    # getting value from form and saving it into applied_date
    applied_date = request.form['value']

    # define query
    query = "Select * from ResumeData where applied_date = %(value)s"

    # define query parameter
    params = {'value': applied_date}

    # executing the query
    cursor.execute(query, params)

    # fetch all values
    data = cursor.fetchall()

    # initialize empty list
    final_json_data = []

    # if data is not empty
    if data:

        # iterate over data rows and form dictionary object
        for row in data:
            dic = {'id': row[0], 'name': (row[1]), 'email': (row[2]), 'phone_number': (row[3]), 'designation': (row[4]), 'education': (row[5]), 'skills': (row[6]), 'experience': (row[7]), 'country': (row[14]), 'screener_question': (row[9]), 'total_experience': (row[10]), 'resume_filepath': (row[11]), 'applied_date': (row[12]), 'job_title': (row[13])}

            # append the dictionary object 'dic' into final_json data array
            final_json_data.append(dic)

        # close connections
        cursor.close()
        db.close()

        # return jsonify data
        return jsonify({'data': final_json_data})

    # if data is empty return None dic
    else:
        dic = {'id': 'None', 'name': 'None', 'email':'None', 'phone_number': 'None', 'designation': 'None', 'education': 'None', 'skills': 'None', 'experience': 'None', 'country': 'None', 'screener_question': 'None', 'total_experience': 'None', 'resume_filepath': 'None', 'applied_date': 'None', 'job_title': 'None'}
        final_json_data.append(dic)
        return jsonify({'data': final_json_data})


"""    -------------------------------  READ EMAIL AND FETCH NEW DATA  -----------------------------------------     """


@app.route('/api/refresh_page', methods=['GET'])
def fetch_emails():

    # call email reader function
    resume_reader.email_fetcher()
    # when emails are read, redirect to all users database page
    return redirect("/api/allusers")

"""--------------------------- GET THE LOCATION AND SHOW ON GOOGLE MAP----------------------------Muhammad Sohaib    """ 

@app.route('/api/location/<user_address>',methods=["GET","POST"]) #Muhammad Sohaib
def get_location_on_gmap(user_address):
    # get parameter input from user
    address = user_address
    url=requests.get("http://www.google.com/maps/place/"+str(address)) 
    return redirect(url.url)

"""---------------------------------USER LOGIN--------------------------- Muhammad Sohaib """  

def setSession():
    session['userLoggedin']=1
    return "success"


@app.route('/api/userLogin/<userData>',methods=["GET","POST"])  #Muhammad Sohaib
def userLogin(userData):
    db = mysql.connect(host=db_host,user=db_user,passwd=db_password,database=db_name)
	# creating an instance of 'cursor' class which is used to execute the 'SQL' statements in 'Python'
    cursor = db.cursor()
    userData=userData.split(",")
    # define query
    query = "Select username,email,password from usersData where username = %(value)s OR email = %(value)s"
    # define query parameter
    params = {'value': userData[0]}
    # executing the query
    cursor.execute(query, params)
    # fetch all values
    data = cursor.fetchall()
    print(data)
    status="none"
    if data:
        for row in data:
            if(row[0]==userData[0] or row[1]==userData[0]):
                if(row[2]==userData[1]):
                    print(session)
                    status=setSession()
                    break
                else:
                    status="Invalid Password"
                    break
            else:
                status="Invalid Username"
    if status=="success":return jsonify({"result":"success"})
        #return redirect("http://addats.com/html/dashboard-3.html")
    else:return jsonify({"result":status})


"""----------------------------------------------- FILTERS ---------------------------------------------------------------"""
@app.route("/api/searchObject/<searchDataId>",methods=["GET","POST"])
def searchObject(searchDataId):
    # response = requests.get('http://162.214.195.234:8081/api/getUsersData')
    response = requests.get('http://127.0.0.1:8081/api/getUsersData')
    searchedData=searchDataId.split(',')
    searchData={"search":searchedData}
    data=response.json()
    data=data["data"]
    result = []
    print(type(searchData["search"]))
    if searchData["search"][0]!="":
        print(data)
        for i in data:
            try:
                temp1 = i["name"].find(searchData["search"][0])
            except:
                temp1 = ""
            try:
                temp2 = i["email"].find(searchData["search"][0])
            except:
                temp2 = ""
            try:
                temp3 = i['total_experience'].find(searchData["search"][0])
            except:
                temp3 = ""
            try:
                temp4 = i['skills'].find(searchData["search"][0])
            except:
                temp4 = ""
            try:
                temp5 = str(i['phone_number']).find(searchData["search"][0])
            except:
                temp5 = ""
            try:
                temp6= i['screener_question'].find(searchData["search"][0])
            except:
                temp6= ""
            try:
                temp7 = i['applied_date'].find(searchData["search"][0])
            except:
                temp7= ""
            try:
                temp8 = i['country'].find(searchData["search"][0])
            except:
                temp8= ""
            try:
                temp9 = str(i['country']).find(searchData["search"][0])
            except:
                temp9= ""
            try:
                temp10 = i['education'].find(searchData["search"][0])
            except:
                temp10 = ""
            try:
                temp11 = i['experience'].find(searchData["search"][0])
            except:
                temp11 = ""
            try:
                temp12 = i['job_title'].find(searchData["search"][0])
            except:
                temp12 = ""
            if searchData["search"][1]=="all":
                if temp1!=-1:
                    result.append(i)
                elif temp2!=-1:
                    result.append(i)
                elif temp3!=-1:
                    result.append(i)
                elif temp4!=-1:
                    result.append(i)
                elif temp5!=-1:
                    result.append(i)
                elif temp6!=-1:
                    result.append(i)
                elif temp7!=-1:
                    result.append(i)
                elif temp8!=-1:
                    result.append(i)
                elif temp9!=-1:
                    result.append(i)
                elif temp10!=-1:
                    result.append(i)
                elif temp11!=-1:
                    result.append(i)
                elif temp12!=-1:
                    result.append(i)
            elif searchData["search"][1]=="name":
                if temp1!=-1:
                    result.append(i)
            elif searchData["search"][1]=="email":
                if temp2!=-1:
                    result.append(i)
            elif searchData["search"][1]=="skill":
                if temp4!=-1:
                    result.append(i)
            elif searchData["search"][1]=="phoneNumber":
                if temp5!=-1:
                    result.append(i)
            elif searchData["search"][1]=="scrQues":
                if temp6!=-1:
                    result.append(i)
            elif searchData["search"][1]=="appliedDate":
                if temp7!=-1:
                    result.append(i)
            elif searchData["search"][1]=="country":
                if temp8!=-1:
                    result.append(i)
            elif searchData["search"][1]=="designation":
                if temp9!=-1:
                    result.append(i)
            elif searchData["search"][1]=="education":
                if temp10!=-1:
                    result.append(i)
            elif searchData["search"][1]=="experience":
                if temp11!=-1 or temp3!=-1:
                    result.append(i)
            elif searchData["search"][1]=="jobTitle":
                if temp12!=-1:
                    result.append(i)
    else:
        result=data 
    return jsonify({'data': result})

@app.route("/api/insertComment/<data>",methods=["GET","POST"])
def insertComment(data):
    db = mysql.connect(host=db_host, user=db_user, passwd=db_password, database=db_name)
    cursor = db.cursor()
    today = date.today()
    data=data.split(",")
    d1 = today.strftime("%d/%m/%Y")
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    query="insert into comments(userId,applicant,comment,time,date) VALUES (%s,%s,%s,%s,%s)"
    values=(data[0],data[1],data[2],current_time,d1)
    cursor.execute(query, values)
    db.commit()
    return jsonify({'status':"commented"})

@app.route("/api/fetchComments/<data>",methods=["GET","POST"])
def fetchComments(data):
    db = mysql.connect(host=db_host, user=db_user, passwd=db_password, database=db_name)
    cursor = db.cursor()
    print(data)
    query = "select * from comments where applicant='"+str(data)+"'"
    cursor.execute(query)
    result = cursor.fetchall()
    print(result)
    if result:
        print(result)
        return jsonify({"result":result})
    else:
        return jsonify({"result":"No data found"})

@app.route("/api/addApplicantManually/<data>",methods=["GET","POST"])
def addApplicantManually(data):
    data = data.split(",")
    db = mysql.connect(host=db_host, user=db_user, passwd=db_password, database=db_name)
    today = date.today()
    d1 = today.strftime("%d/%m/%Y")
    db = mysql.connect(host=db_host, user=db_user, password=db_password, database=db_name)
    cursor = db.cursor()
    query = "INSERT INTO resumeData(name, email , phone_number ,designation ,education, skills, experience, country, screener_questions, resume_filePath ,total_experience, applied_date, job_title, address) VALUES (%s, %s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    values = (data[0], data[1], data[2],data[3], data[4], data[5], data[6], data[7], data[11], data[12], data[8], d1, data[10], data[9])
    cursor.execute(query, values)
    db.commit()
    # file=request.json['file']
    # file.save(os.path.join(app.root_path, data[10]))
    return jsonify({'upload':"done"})

@app.route("/api/editApplicantDetails/",methods=["GET","POST","UPDATE"])
def editApplicantProfile():
    if request.method=="POST":
        data=request.get_data().decode('big5')
        data=data.split(",$")
        print(data)
        db = mysql.connect(host=db_host, user=db_user, passwd=db_password, database=db_name)
        cursor=db.cursor()
        query="UPDATE resumeData set name=%s,phone_number=%s,designation=%s,education=%s,skills=%s,experience=%s,address=%s,country=%s,screener_questions=%s,total_experience=%s,job_titles=%s where email=%s;"
        values=(data[0],data[2],data[3],data[4],data[5],data[6],data[7],data[7],data[10],data[8],data[9],data[1])
        cursor.execute(query,values)
        db.commit()
        return jsonify({"update":"done"})
    else:
        return jsonify({"error":"Unable to update info server error"})

@app.route("/api/deleteApplicantInfo/<data>",methods=["GET","POST","DELETE"])
def deleteApplicantInfo(data):
    db = mysql.connect(host=db_host, user=db_user, passwd=db_password, database=db_name)
    cursor=db.cursor()
    query="DELETE FROM ResumeData WHERE email=%s;"
    value=(data,)
    cursor.execute(query,value)
    db.commit()
    return jsonify({"update":"done"})

# run app on 'host = localhost' and 'port = 8081'
if __name__ == '__main__':
    secret_key="clickHr123654789"
    app.secret_key = secret_key
    app.run(port=8081, debug=True)
#, host='162.214.195.234'
