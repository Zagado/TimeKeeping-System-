import datetime
import bcrypt
from app import app, db
from app.models import User, Time_Entry, Paycheck
from flask_bcrypt import Bcrypt

import csv


@app.before_first_request
def create_tables():
    db.create_all()
    with open('employees.csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                if line_count == 0:
                    pass
                else:
                    hashed_pwd = bcrypt.generate_password_hash(row[8]).decode('utf-8')
                    user = User(employee_id=row[0], lname=row[1], fname=row[2],
                                       ssn=row[3], email=row[4], address=row[5],
                                       dep_name=row[7], password=hashed_pwd)
                    # add user to the database
                    if User.query.filter_by(employee_id=row[0]).first() is None:
                        db.session.add(user)
                        db.session.commit()
                    else:
                        pass
                line_count += 1

    with open('PastPaychecks.csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                if line_count == 0:
                    pass
                else:
                    paycheck = Paycheck(Paycheck_ID=row[0], Employee_ID=row[1], Start_Date=datetime.datetime.strptime(row[2], '%m/%d/%Y').date(),
                                               End_date=datetime.datetime.strptime(row[3], '%m/%d/%Y').date(), TimeElapsed=row[4], HourlyWage=row[5], TotalPay=row[6])

                    if Paycheck.query.filter_by(Paycheck_ID=row[0]).first() is None:
                        db.session.add(paycheck)
                        db.session.commit()
                    else:
                        pass

                line_count += 1

    
@app.shell_context_processor
def make_shell_context():
   return {'db': db, 'User': User, 'Time_Entry': Time_Entry}


