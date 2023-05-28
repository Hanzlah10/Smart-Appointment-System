from validate_email import validate_email  # use to validate email proper or not
from flask import Flask, render_template, request, redirect, session, url_for, \
    jsonify  # Flask Framework for web development
from flask_sqlalchemy import SQLAlchemy  # SqlAlchemy for Database Connection and all CRUD operations
from flask_mail import Mail, Message  # import flask mail
from werkzeug.utils import \
    secure_filename  # use to identity uploaded image and save it (with image name changes if required)
from time import time  # time gives us current time or time as user required
from new_time_slot import init_slot_maker, getSlot, convertToUseAbleTime, init_slot_maker_1 # timeslot maker programmed manually
from datetime import date  # use to get current date or as user required
import secrets  # use to generate token
import json  # use to read json file
import pymysql

pymysql.install_as_MySQLdb()

# init Flask``
app = Flask(__name__)
# secret key required for flask, use to store unique session or data
app.secret_key = 'ffjnfgnjdkvngsrjkvngsjd'
# configuring database for our web application
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/Demo'
# storing or committing changed eg : database config : secret key
db = SQLAlchemy(app)

# configuring static(type of public folder which can be accessible by visitor ) folder, we store js,css,image in this folder
app.config['UPLOAD_FOLDER'] = 'static/Images'




# -------------new mail method ---------------

Jsoncredencials = open("templates/credentials/credentials.json", )
loadData = json.load(Jsoncredencials)

app.config.update(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT='465',
    MAIL_USE_SSL=True,
    MAIL_USERNAME=loadData['mail']['gmail'],
    MAIL_PASSWORD=loadData['mail']['password']
)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

mail = Mail(app)




# use to set email html
def setHtml(token, whom, email):
    if whom == 'thankyou':
        html = render_template('MailTemplates/thankyou.html', email=email, token=token)
    else:
        html = render_template('MailTemplates/forgotpassword.html', email=email, token=token,whom=whom)
    return html


def send_notification(receiver,token,whom):
    msg = Message(
        subject='changeable',
        sender=(loadData['site-information']['name'], loadData['mail']['gmail']),
        recipients=[receiver]
    )

    if whom == 'thankyou':
        msg.subject = "Thank you for Registering Account!"
    else:
        msg.subject = "Trouble Signing in? Forgot Password?"

    msg.html = setHtml(token, whom, receiver)
    mail.send(msg)


# Creating Database Model and setting up the table name with which type of value accepts and restrictions
class Doctor_information(db.Model):
    doctor_id = db.Column(db.Integer, primary_key=True)
    doctor_name = db.Column(db.String(80), nullable=False)
    doctor_password = db.Column(db.String(80), nullable=False)
    doctor_phone_number = db.Column(db.String(80), nullable=False)
    doctor_email = db.Column(db.String(80), nullable=False)
    qualification = db.Column(db.String(80), nullable=False)
    address = db.Column(db.String(80), nullable=False)
    profile_image = db.Column(db.String(200), nullable=True)
    status = db.Column(db.Boolean, nullable=False)
    start_time = db.Column(db.String(50), nullable=True)
    end_time = db.Column(db.String(50), nullable=True)
    start_time_1 = db.Column(db.String(50), nullable=True)
    end_time_1 = db.Column(db.String(50), nullable=True)
    specialization = db.Column(db.String(100), nullable=True)
    diagnose = db.Column(db.Integer, nullable=True)
    token = db.Column(db.String(100), nullable=False)


# Creating Database Model and setting up the table name with which type of value accepts and restrictions
class Patient_information(db.Model):
    p_id = db.Column(db.Integer, primary_key=True)
    patient_name = db.Column(db.String(80), nullable=False)
    patient_password = db.Column(db.String(80), nullable=False)
    phone = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), nullable=False)
    patient_profile_image = db.Column(db.String(200), nullable=False)
    patient_age = db.Column(db.Integer, nullable=False)
    patient_gender = db.Column(db.String(20), nullable=False)
    token = db.Column(db.String(100), nullable=False)


# Creating Database Model and setting up the table name with which type of value accepts and restrictions
class Appointments_information(db.Model):
    pid = db.Column(db.Integer, primary_key=True)
    doctor_email = db.Column(db.String(200), nullable=False)
    patient_email = db.Column(db.String(200), nullable=False)
    appointment_time = db.Column(db.String(50), nullable=False)
    done = db.Column(db.Integer, nullable=False)
    someone_patient_name = db.Column(db.String(40), nullable=False)
    someone_patient_age = db.Column(db.Integer, nullable=False)
    someone_patient_contact_number = db.Column(db.Integer, nullable=False)
    someone_patient_gender = db.Column(db.String(20), nullable=False)

db.create_all()

# @app.route(link) is use to set on which link you have to provide content or template

@app.route("/")
def home():
    # render_template use to render html template
    return render_template("Home/index.html")


# Doctor Logout Function
@app.route("/doctor/logout")
def DoctorLogout():
    # check's if email and password of doctor is present in session
    if 'email' in session and 'password' in session:
        # pop function is use to delete data from session
        session.pop('email')
        session.pop('password')
        # redirect function will redirect user to another link
        return redirect('/doctor/login')
    else:
        return redirect('/doctor/login')


# Doctor Login Page Route
@app.route("/doctor/login",
           methods=['GET', 'POST'])  # methods use to allow the user on which method link should to open
def DoctorLogin():
    # checking method
    if request.method == "POST":
        # method post means user sent data from form
        email = request.form['email']  # accessing the data from form
        password = request.form['password']  # accessing the data from form
        # checking if the data already exists in database table or not
        exists = db.session.query(Doctor_information.doctor_email).filter_by(doctor_email=email,
                                                                             doctor_password=password).scalar() is not None

        if exists:
            # storing up data in chrome using session
            session['email'] = email
            session['password'] = password
            return render_template("Doctor/login.html", login=True)
        else:
            return render_template("Doctor/login.html", invalidDetails=True, email=email)

    else:
        # checking if parameter in url or not
        if request.args.get('success') and request.args.get('email'):
            success = request.args.get('success')  # getting parameter value from url
            email = request.args.get('email')
            return render_template("Doctor/login.html", success=success, email=email)
        else:
            # checking doctor logged in or not
            if AuthenticateDoctor():
                return redirect("/doctor/")
            else:
                return render_template("Doctor/login.html")


# fetching or retrieving or getting data doctor data from database table
def FetchDoctorInformation(search):
    if search == 'All':
        # getting all doctor data
        return Doctor_information.query.filter_by().all()
    else:
        # getting data of specific doctor using email search
        return Doctor_information.query.filter_by(doctor_email=search).first()  # first() use to get
        # the first data from dataset


# fetching or retrieving or getting data pateint data from database table
def FetchPatientInformation(search):
    if search == 'All':
        return Patient_information.query.filter_by().all()
    else:
        return Patient_information.query.filter_by(email=search).first()


# <string:doctor_email> or <int:age> : first is type of data you want from link and
# second is variable name of data to use it
# this is an api created for others pages to fetch data easily
@app.route("/api/upi/<string:doctor_email>/<string:patient_email>/<string:appointment_time>/<int:patient_age>/<string"
           ":patient_name>/<int:patient_contact_number>/<string:patient_gender>",
           methods=['POST', 'GET'])
# function parameter coming from link : eg : <string:data> <int:data>
def UploadOtherPatientInformation(doctor_email, patient_email, appointment_time, patient_age, patient_name,
                                  patient_contact_number, patient_gender):
    # get the today date
    today = date.today()
    # get the patient_email which is stored by session in browser
    email = session['patient_email']
    # fetches count of today's appointment of patient using raw SQL query
    TodayAppointmentsCount = db.engine.execute("SELECT COUNT(*) FROM appointments_information "
                                               "WHERE patient_email = '{}' and appointed_datetime = '{}' and "
                                               "someone_patient_contact_number = {} ORDER BY "
                                               "pid "
                                               "DESC ".format(email, today, patient_contact_number))
    # count of today's appointment start from 0
    tps = 0
    for tps in TodayAppointmentsCount:
        # used pass keyword bcz we don't want data which is in loop
        # we used for loop to loop the data and store it in tps variable
        pass

    # the tsp in the form of tuple so we used here index number to get the first element of tuple
    # tsp contains total number of today appointment's of patient
    if tps[0] > 0:  # if tps is greater than 0 that means we don't allow the patient to take another appointment
        # patient already with appointment return 0 status
        result = {
            'status': 0
        }
        return jsonify(result)  # return the data in json format so that javascript can loop it

    else:
        # else part will run if the patient don't have any appointment
        # entry will set new data for appointment
        entry = Appointments_information(doctor_email=doctor_email, patient_email=patient_email,
                                         appointment_time=appointment_time, done=1, someone_patient_name=patient_name,
                                         someone_patient_age=patient_age, someone_patient_gender=patient_gender,
                                         someone_patient_contact_number=patient_contact_number)
        # add function upload the data which is set in entry
        db.session.add(entry)
        # confirms the new data entry
        db.session.commit()
        result = {
            'status': 1  # 1 means data added successfully
        }
        return jsonify(result)  # return the data in json format so that javascript can loop it


# <string:doctor_email> or <int:age> : first is type of data you want from link and
# second is variable name of data to use it
# this is an api created for others pages to fetch data easily
@app.route("/api/doctor-schedule/<string:email>", methods=['POST'])
# use to fetch doctor schedule
def FetchDoctorSchedule(email):
    # checks doctor or patient is logged in or not
    if AuthenticatePatient() or AuthenticateDoctor():
        Myprofile = FetchDoctorInformation(email)  # fetches the doctor data
        start_slot = Myprofile.start_time  # get the doctor start time
        end_slot = Myprofile.end_time  # get the doctor end time
        start_slot_1 = Myprofile.start_time_1  # get the doctor start time
        end_slot_1 = Myprofile.end_time_1  # get the doctor end time
        doctor_email = Myprofile.doctor_email  # get the doctor email
        doctor_diagnose_limit = Myprofile.diagnose  # get the doctor diagnose rate

        init_slot_maker(start_slot, end_slot)  # init slot maker
        init_slot_maker_1(start_slot_1, end_slot_1)  # init slot maker

        timeSlots = getSlot()  # getting the time slots
        print(timeSlots)
        # looping the slot to check slot if full or not
        for slot in range(0, len(timeSlots)):
            try:
                #            start slot time           end slot time
                total_slot = timeSlots[slot] + " - " + timeSlots[slot + 1]
                # counting the number of patient registered in this slot
                today = date.today()
                CountAppointments = db.engine.execute("SELECT COUNT(*) FROM appointments_information WHERE "
                                                      "appointment_time='{}' and "
                                                      "doctor_email = '{}' and appointed_datetime = '{}' ".format(total_slot, doctor_email,today))
                # slot count starts from 0
                CountResult = 0
                for CountResult in CountAppointments:
                    # we looped the data just to store count in CountResult
                    # that is why we passed the loop
                    pass
                # checks if the diagnose limit is equal to total doctor appointment or not
                # if it equals then the specific slot if full
                if doctor_diagnose_limit == CountResult[0]:
                    timeSlots[slot + 1] = timeSlots[slot + 1] + " full"
                else:
                    # slot is not full
                    pass

            except:
                # passed bcz it is the end of slot
                pass
        result = {
            'schedule': timeSlots
        }
        return jsonify(result)
    else:
        # if doctor or patient not logged in then this will return 0 schedule
        # basically that means you can not access data without login
        return {'schedule': '0'}


# page for setting up doctor schedule by doctor
@app.route("/doctor/schedule", methods=['GET', 'POST'])
def DoctorSchedule():
    if AuthenticateDoctor():
        email = session['email']
        Myprofile = FetchDoctorInformation(email)
        if Myprofile.profile_image is not None:
            if request.method == 'POST':
                start_time = request.form['start_time'].strip()
                end_time = request.form['end_time'].strip()
                start_time_1 = request.form['start_time_1'].strip()
                end_time_1 = request.form['end_time_1'].strip()

                Myprofile.start_time = convertToUseAbleTime(start_time)
                Myprofile.end_time = convertToUseAbleTime(end_time)
                Myprofile.start_time_1 = convertToUseAbleTime(start_time_1)
                Myprofile.end_time_1 = convertToUseAbleTime(end_time_1)
                db.session.commit()

                return render_template("Doctor/schedule.html", email=email, doctor_data=Myprofile, success=True)
            else:
                return render_template("Doctor/schedule.html", email=email, doctor_data=Myprofile)
        else:
            Myprofile = FetchDoctorInformation(email)
            return render_template("doctor/profile.html", doctor_data=Myprofile, profile=False)
    else:
        return redirect("/doctor/login")


@app.route("/doctor/")
def DoctorDashboard():
    if AuthenticateDoctor():
        email = session['email']
        # checks if the profile img is set or not
        if FetchDoctorInformation(email).profile_image is not None:

            email = session['email']
            # joining data using raw SQL
            AllAppointments = db.engine.execute("SELECT COUNT(*) FROM appointments_information a "
                                                "INNER JOIN doctor_information s ON a.doctor_email = s.doctor_email "
                                                "INNER JOIN patient_information p ON a.patient_email = p.email "
                                                "WHERE a.doctor_email = '{}' ORDER BY a.pid "
                                                "DESC ".format(email))

            today = date.today()
            TodayAppointmentsCount = db.engine.execute("SELECT COUNT(*) FROM appointments_information a "
                                                       "INNER JOIN doctor_information s ON a.doctor_email = s.doctor_email "
                                                       "INNER JOIN patient_information p ON a.patient_email = p.email "
                                                       "WHERE a.doctor_email = '{}' and a.appointed_datetime = '{}' ORDER BY a.pid "
                                                       "DESC ".format(email, today))
            # looping data to store total patients of doctor in totalpatient variable
            # we dont want to add another data or dont want to do any calculation
            # that is why passed the loop
            for totalpatient in AllAppointments:
                pass
            for todaypatientcount in TodayAppointmentsCount:
                pass

            return render_template("doctor/index.html", email=email, totalpatient=totalpatient[0],
                                   todaypatientcount=todaypatientcount[0])
        else:
            Myprofile = FetchDoctorInformation(email)
            return render_template("doctor/profile.html", doctor_data=Myprofile, profile=False)
    else:
        return redirect("/doctor/login")


@app.route("/doctor/profile", methods=['GET', 'POST'])
def DoctorProfile():
    if AuthenticateDoctor():
        email = session['email']
        Myprofile = FetchDoctorInformation(email)
        if request.method == 'POST':
            new_name = request.form['name'].strip()  # strip use to remove unwanted white spaces from data
            new_status = request.form['status'].strip()
            new_qualification = request.form['qualification'].strip()
            new_phone = request.form['phone'].strip()
            new_address = request.form['address'].strip()
            new_profile_pic = request.files['pimage']
            specialization = request.form['specialization']
            diagnose = request.form['diagnose']
            # millis = str(round(time() * 1000))  # gives the current time in milles
            # saving image with unique name is the hardest thing that is why we renamed the
            # image name to image name with current time milles which is going to be unique !
            image_name = new_profile_pic.filename

            # getting length of image name to check whether user uploaded image or not
            if len(secure_filename(new_profile_pic.filename)) > 0:
                # saving image in static folder
                new_profile_pic.save((app.config['UPLOAD_FOLDER']) + '\\' + secure_filename(image_name))
                Myprofile.profile_image = "/static/Images/" + image_name

            if new_status == 'available':
                Myprofile.status = 1  # 1 means available
            else:
                Myprofile.status = 0  # 0 means not available

            # updating doctor all data
            Myprofile.doctor_name = new_name
            Myprofile.qualification = new_qualification
            Myprofile.doctor_phone_number = new_phone
            Myprofile.address = new_address
            Myprofile.specialization = specialization
            Myprofile.diagnose = diagnose

            db.session.commit()
            # success True is parameter send to template to pupup updated data
            return render_template("Doctor/profile.html", email=email, doctor_data=Myprofile, success=True)


        else:
            return render_template("Doctor/profile.html", email=email, doctor_data=Myprofile)
    else:
        return redirect("/doctor/login")


# Doctor Register Route
@app.route("/doctor/register", methods=['POST', 'GET'])
def DoctorRegister():
    if request.method == "POST":
        name = request.form['name']
        email = request.form["email"]
        password = request.form["password"]
        phone = request.form["phone"]
        qualification = request.form["qualification"]
        address = request.form["address"]

        exists = db.session.query(Doctor_information.doctor_email).filter_by(doctor_email=email).scalar() is not None

        if exists:
            error = 'Email id Already Registered'

            return render_template("/Doctor/register.html", error=error, name=name, email=email, phone=phone,
                                   qualification=qualification, address=address)

        else:

            is_valid = validate_email(email)

            if is_valid:
                # sending thank you mail to new registered user
                # send_notification(email, "safdssfefwefwfwfwefcwf45tg45g4", "thankyou")
                entry = Doctor_information(doctor_name=name, doctor_email=email, doctor_password=password,
                                           doctor_phone_number=phone, qualification=qualification, address=address)

                db.session.add(entry)
                db.session.commit()

                return redirect(url_for('DoctorLogin', success=True, email=email))

            else:
                error = 'Invalid Email id'

                return render_template("/Doctor/register.html", error=error, name=name, email=email, phone=phone,
                                       qualification=qualification, address=address)



    else:
        return render_template("/Doctor/register.html")


@app.route("/doctor/appointments", methods=['GET'])
def todayDoctorAppointments():
    if AuthenticateDoctor():
        email = session['email']
        today = date.today()
        TodayAppointments = db.engine.execute("SELECT * FROM appointments_information a "
                                              "INNER JOIN doctor_information s ON a.doctor_email = s.doctor_email "
                                              "INNER JOIN patient_information p ON a.patient_email = p.email "
                                              "WHERE a.doctor_email = '{}' and a.appointed_datetime = '{}' ORDER BY a.pid "
                                              "DESC ".format(email, today))
        return render_template("Doctor/appointments.html", email=email, TodayAppointments=TodayAppointments)
    else:
        return render_template("/Doctor/login.html")


@app.route("/doctor/patients", methods=['GET'])
def AllDoctorAppointments():
    if AuthenticateDoctor():
        email = session['email']
        # fetching doctor today appointment
        TodayAppointments = db.engine.execute("SELECT * FROM appointments_information a "
                                              "INNER JOIN doctor_information s ON a.doctor_email = s.doctor_email "
                                              "INNER JOIN patient_information p ON a.patient_email = p.email "
                                              "WHERE a.doctor_email = '{}' ORDER BY a.pid "
                                              "DESC ".format(email))
        return render_template("Doctor/appointments.html", email=email, TodayAppointments=TodayAppointments)
    else:
        return render_template("/Doctor/login.html")


@app.route("/doctor/forgot-password", methods=['GET', 'POST'])
def ForgotDoctorPassword():
    if request.method == 'POST':
        email = request.form['email']
        exists = db.session.query(Doctor_information.doctor_email).filter_by(doctor_email=email).scalar() is not None

        if exists:
            # generating token
            token = secrets.token_hex(32)
            DoctorProfile = FetchDoctorInformation(email)
            DoctorProfile.token = token
            db.session.commit()
            # send_notification(email, token, "doctor")

            return render_template("/Doctor/forgot-password.html", exists=1, email=email)
        else:
            return render_template("/Doctor/forgot-password.html", exists=0)

    else:
        return render_template("/Doctor/forgot-password.html", exists=3)


@app.route("/doctor/forgot-password/<string:email>/<string:token>", methods=['GET', 'POST'])
def setNewDoctorPassword(email, token):
    # checking token in link
    if len(token) > 10:
        # checking that email with this token exists or not
        exists = db.session.query(Doctor_information.doctor_email).filter_by(doctor_email=email,
                                                                             token=token).scalar() is not None

        if exists:
            if request.method == 'POST':
                DoctorInfomation = FetchDoctorInformation(email)
                DoctorInfomation.token = 'empty'
                DoctorInfomation.doctor_password = request.form['password']
                db.session.commit()
                return render_template("Doctor/NewPassword.html", passwordChanged=1)

            return render_template("Doctor/NewPassword.html")
        else:
            return redirect("/doctor/login")
    else:
        return redirect("doctor/login")


# authenticating patient exists or not
def AuthenticatePatient():
    if 'patient_email' in session and 'patient_password' in session:
        email = session['patient_email']
        password = session['patient_password']
        exists = db.session.query(Patient_information.email).filter_by(email=email,
                                                                       patient_password=password).scalar() is not None
        if exists:
            return True
        else:
            session.pop('patient_email')
            session.pop('patient_password')
            return False
    else:
        return False


# authenticating doctor exists or not
def AuthenticateDoctor():
    if 'email' in session and 'password' in session:
        email = session['email']
        password = session['password']
        exists = db.session.query(Doctor_information.doctor_email).filter_by(doctor_email=email,
                                                                             doctor_password=password).scalar() is not None
        if exists:
            return True
        else:
            session.pop('email')
            session.pop('password')
            return False
    else:
        return False


# showing patient appointments
@app.route("/patient/appointment", methods=['GET'])
def PatientAppointment():
    if AuthenticatePatient():
        email = session['patient_email']
        MyAppointment = db.engine.execute("SELECT * "
                                          " FROM doctor_information INNER JOIN appointments_information ON "
                                          "appointments_information.doctor_email = doctor_information.doctor_email "
                                          "where appointments_information.patient_email = '{}' ORDER BY pid DESC ".format(
            email))



        return render_template("Home/appointment.html", email=email, MyAppointment=MyAppointment)
    else:
        return redirect("/patient/login")


@app.route("/patient/")
def PatientDashboard():
    if AuthenticatePatient():
        email = session['patient_email']
        AllDoctors = FetchDoctorInformation("All")
        MyProfile = FetchPatientInformation(email)
        return render_template("/Home/dashboard.html", MyProfile=MyProfile, email=email, AllDoctors=AllDoctors,
                               )
    else:
        return redirect("/patient/login")


@app.route("/patient/profile", methods=['GET', 'POST'])
def PatientProfile():
    if AuthenticatePatient():
        email = session['patient_email']
        Myprofile = FetchPatientInformation(email)
        if request.method == 'POST':
            new_name = request.form['name'].strip()
            new_phone = request.form['phone'].strip()
            new_profile_pic = request.files['pimage']
            new_gender_patient = request.form['gender']
            new_patient_age = request.form['age']
            millis = str(round(time() * 1000))
            image_name = millis + new_profile_pic.filename

            if len(secure_filename(new_profile_pic.filename)) > 0:
                new_profile_pic.save((app.config['UPLOAD_FOLDER']) + '\\' + secure_filename(image_name))
                Myprofile.patient_profile_image = "/static/Images/" + image_name

            Myprofile.patient_name = new_name
            Myprofile.phone = new_phone
            Myprofile.patient_age = new_patient_age
            Myprofile.patient_gender = new_gender_patient

            db.session.commit()

            return render_template("Home/profile.html", email=email, patient_data=Myprofile, success=True)

        else:
            return render_template("Home/profile.html", email=email, patient_data=Myprofile)
    else:
        return redirect("/patient/login")


@app.route("/patient/logout")
def PatientLogout():
    if 'patient_email' in session and 'patient_password' in session:
        session.pop('patient_email')
        session.pop('patient_password')
        return redirect('/patient/login')
    else:
        return redirect('/patient/login')


@app.route("/patient/login", methods=['GET', 'POST'])
def PatientLogin():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']
        exists = db.session.query(Patient_information.email).filter_by(email=email,
                                                                       patient_password=password).scalar() is not None

        if exists:
            session['patient_email'] = email
            session['patient_password'] = password
            return render_template("Home/login.html", login=True)
        else:
            return render_template("Home/login.html", invalidDetails=True, email=email)

    else:
        if request.args.get('success') and request.args.get('email'):
            success = request.args.get('success')
            email = request.args.get('email')
            return render_template("Home/login.html", success=success, email=email)
        else:
            if AuthenticatePatient():
                return redirect("/patient/")
            else:
                return render_template("Home/login.html")


@app.route("/patient/register", methods=['GET', 'POST'])
def PatientRegister():
    if request.method == "POST":
        name = request.form['name'];
        email = request.form["email"]
        password = request.form["password"]
        phone = request.form["phone"]
        age = request.form['age']
        gender = request.form['gender']

        exists = db.session.query(Patient_information.email).filter_by(
            email=email).scalar() is not None

        if exists:
            error = 'Email id Already Registered'

            return render_template("/Home/register.html", error=error, name=name, email=email, phone=phone)

        else:

            is_valid = validate_email(email)

            if is_valid:
                # send_notification(email, "safdssfefwefwfwfwefcwf45tg45g4", "thankyou")
                entry = Patient_information(patient_name=name, email=email, patient_password=password,
                                            phone=phone, patient_age=age, patient_gender=gender)

                db.session.add(entry)
                db.session.commit()

                return redirect(url_for('PatientLogin', success=True, email=email))

            else:
                error = 'Invalid Email id'

                return render_template("/Home/register.html", error=error, name=name, email=email, phone=phone)



    else:
        return render_template("/Home/register.html")


@app.route("/patient/forgot-password/<string:email>/<string:token>", methods=['GET', 'POST'])
def setNewPatientPassword(email, token):
    # checking token is in link or not
    if len(token) > 10:
        exists = db.session.query(Patient_information.email).filter_by(email=email,
                                                                       token=token).scalar() is not None

        if exists:
            # checking method
            if request.method == 'POST':
                PatientInfomation = FetchPatientInformation(email)
                PatientInfomation.token = 'empty'
                PatientInfomation.patient_password = request.form['password']
                db.session.commit()
                return render_template("Home/NewPassword.html", passwordChanged=1)

            return render_template("Home/NewPassword.html")
        else:
            # redirecting user
            return redirect("/patient/login")
    else:
        # redirecting user
        return redirect("/patient/login")


@app.route("/patient/forgot-password", methods=['GET', 'POST'])
def ForgotPatientPassword():
    if request.method == 'POST':
        email = request.form['email']
        exists = db.session.query(Patient_information.email).filter_by(email=email).scalar() is not None

        if exists:
            # generating token
            token = secrets.token_hex(32)
            PatientProfile = FetchPatientInformation(email)
            PatientProfile.token = token
            db.session.commit()
            # sends new password link to mail
            # send_notification(email, token, "patient")

            return render_template("/Home/forgot-password.html", exists=1, email=email)
        else:
            # if not exists return 0
            return render_template("/Home/forgot-password.html", exists=0)

    else:
        return render_template("/Home/forgot-password.html", exists=3)


# starting server
if __name__ == '__main__':
    app.run(debug=True)
