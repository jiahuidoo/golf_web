from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from datetime import datetime
from flask_login import current_user
from models.users import User
from models.golflog import Golf
from models.swinglog import Swing

swing = Blueprint('swing', __name__)

# This following functions is for GET /log and POST /process via log.html and log.js

# POST done via log.js
@swing.route('/golfclubs',methods=['POST'])
def generate():
    '''
    To generate the list of clubs in the golfer's golf set
    Golfer: define by the selected user email chosen in first dropdown
    
    the list of clubs will be used to populate the options in second dropdown
    '''
    user_email = request.get_json("type")['user_email']
    golfer_user = User.getUser(email=user_email)

    golfClubs = Golf.getAllGolfClubs(user=golfer_user)
    return jsonify({'golfClubs': golfClubs})

@swing.route('/log')
def log():
    #Retrieve the user_list to populate the first dropdown list
    #admin user view: all registered users
    if current_user.email == "admin@abc.com":
        user_list = User.objects()

    #non-admin user view: only existing user email 
    else:
        user_list = [current_user]

    return render_template('log.html', name=current_user.name, panel="SWING", user_list=user_list)

@swing.route('/process',methods= ['POST'])
def process():
    # Get the parameters posted by form in log.html
    user_email = request.form['user_email']
    label = request.form['club']
    speed  = float(request.form['speed'])
    dt = request.form['date']

    dt_obj = datetime.strptime(dt, '%Y-%m-%dT%H:%M')
    dt_obj= dt_obj.date()

    golfer_user = User.getUser(email=user_email)
    # By default, the golf club should already exist before a swing can be added
    # Create swing
    swingObject = Swing.createSwing(user=golfer_user, datetime=dt_obj, speed=speed, label=label)
    if swingObject:
        # Compute and update distance
        swingObject.distance = swingObject.computeDistance()
        swingObject.save()

    # If club does not exist in the golfer's set, swing object is None
    else:
        print('Golf club not found in golf set')
        return jsonify({'status_code':404, 'error':f'Golf club - {label} not found in golf set'})

    return redirect(url_for('swing.log'))


# This following functions is for GET /log2 and POST /process2 via club_advice.html and log2.js

@swing.route('/log2')
def log2():
    return render_template('club_advice.html', name=current_user.name, panel="Get Club Advice")

@swing.route('/process2',methods= ['POST'])
def process2():
    # Get the parameters posted by form in club_advice.html
    delta = 50
    speed  = float(request.form['speed'])
    desired_distance  = float(request.form['distance'])

    tmp = [f'Speed = {speed} mph, distance = {desired_distance} yards']

    existing_user = User.getUser(email=current_user.email)
    golfclubs = Golf.getAllGolfClubs(user=existing_user)

    # If there's no golfclub retrieved for the user
    if not golfclubs:
        tmp.append('No golset recorded yet!')

    else:
        # Find suitable golf club(s) that belong to the user, that can hit the golf ball to a desired distance
        #with a specified swing speed 
        suitable_clubs = []

        for club in golfclubs:

            # Compute the head height based on the type of clubhead
            if club.clubtype == "Wood":
                # size / 400
                club_head_height = float(club.hinfo) / 400

            elif club.clubtype == "Iron":
                club_head_height = 1 

            # if style is Blade, height is 1, else 0.5
            else:
                club_head_height = 1 if club.hinfo == "Blade" else 0.5

            club_length = club_head_height + club.slength #shaft_length
            
            # Compute the estimated swing distance
            estimated_distance = (280 - abs(48-club_length)*10 - abs(club.hloft - 10)*1.25) * speed/96
            difference = estimated_distance - desired_distance

            # Golf club is suitable to hit if the difference between the estimated distance and desired distance
            #is +- delta
            if abs(difference) < delta:
                suitable_clubs.append((club.label, club_length, club.hloft))

        # If there's suitable club for the user to hit
        if suitable_clubs:
            for c in suitable_clubs:
                tmp.append(f'{c[0]} length = {c[1]} loft = {c[2]}')
        
        else:
            tmp.append('No suitable club')  

    return jsonify({'golf' : tmp})
    