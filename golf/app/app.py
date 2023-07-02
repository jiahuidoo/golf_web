# https://medium.com/@dmitryrastorguev/basic-user-authentication-login-for-flask-using-mongoengine-and-wtforms-922e64ef87fe

from flask_login import login_required, current_user
from flask import render_template, request
from app import app, db, login_manager

# Register Blueprint so we can factor routes
from controllers.auth import auth
from controllers.swing import swing
from controllers.dashboard import dashboard

# register blueprint from respective module
app.register_blueprint(auth)
app.register_blueprint(swing)
app.register_blueprint(dashboard)

from models.golflog import Golf
from models.swinglog import Swing
from models.users import User
import csv
import io
from datetime import datetime

# Load the current user if any
@login_manager.user_loader
def load_user(user_id):
    return User.objects(pk=user_id).first()

@app.route('/base')
def show_base():
    return render_template('base.html')

@app.route("/upload", methods=['GET','POST'])
@login_required
def upload():
    error = None

    # Populate all registered golfers' email in the dropdown
    all_users = User.objects()
    
    # if the user just key in the /upload in the address
    if request.method == 'GET':
        return render_template("upload.html", name=current_user.name, user_list=all_users, panel="Upload")

    elif request.method == 'POST':
        type = request.form.get('type')
        if type == 'create':
            print("No create Action yet")
        
        elif type == 'upload':
            file = request.files.get('file')
            datatype = request.form.get('datatype')
            golfer = request.form.get('golfer')

            golfer_user = User.getUserByName(name=golfer)

            data = file.read().decode('utf-8')
            rows = csv.reader(io.StringIO(data), delimiter=',', quotechar='"')
            file.close()

            if datatype == "Golf Set":
                for item in rows:
                    # only consider Putter, Wood, Iron types of club heads
                    clubtype = item[1]
                    if clubtype in ['Putter', 'Wood', 'Iron']:
                        Golf.createGolfClub(user=golfer_user, label=item[0], clubtype=clubtype, 
                        hloft=item[2], hweight=item[3], hinfo=item[4], 
                        slength=item[5], sweight=item[6], smaterial=item[7], sflex=item[8], 
                        gdiameter=item[9], gweight=item[10], gmaterial=item[11])
                    
                    else:
                        error = f'Unable to add {item[0]} into  golf set. The club type cannot be {item[1]}'

            else:
                # skip csv headers
                next(rows)
                for item in rows:
                    # remove tirple quotation mark
                    dt = item[0].replace('"', '')
                    dt_obj = datetime.strptime(dt, '%Y-%m-%dT%H:%M')
                    speed = item[1]
                    label = item[2]

                    # create swing
                    swingObject = Swing.createSwing(user=golfer_user, datetime=dt_obj, speed=speed, label=label, distance=0.0)
                    if swingObject:
                        # compute and update distance
                        swingObject.distance = swingObject.computeDistance()
                        swingObject.save()
                    
                    # unable to add swing - golf club not found in golf set
                    else:
                        error = f'Unable to add swing - {label} not found in golf set'
                    
        return render_template("upload.html", name=current_user.name, user_list=all_users, panel="Upload", error=error)
    