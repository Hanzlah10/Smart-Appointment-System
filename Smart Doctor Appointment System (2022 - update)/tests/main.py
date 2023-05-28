from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.secret_key = 'ffjnfgnjdkvngsrjkvngsjd'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/idp'
db = SQLAlchemy(app)


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
    specialization = db.Column(db.String(100), nullable=True)


class Appointments_information(db.Model):
    pid = db.Column(db.Integer, primary_key=True)
    doctor_email = db.Column(db.String(200), nullable=False )
    patient_email = db.Column(db.String(200), nullable=False)
    appointment_time = db.Column(db.String(50), nullable=False)
    done = db.Column(db.Integer, nullable=False)


    r = db.engine.execute("SELECT * FROM appointments_information FULL OUTER JOIN doctor_information ON "
                          "appointments_information.doctor_email = doctor_information.doctor_email ")

    SELECT *
    FROM
    doctor_information
    INNER
    JOIN
    appointments_information
    ON
    appointments_information.doctor_email = doctor_information.doctor_email
    where
    appointments_information.patient_email = 'rohanprajapati7860@gmail.com';

for re in r:
    print(re)