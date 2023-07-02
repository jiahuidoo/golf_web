from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
import json

from models.swinglog import Swing
from models.users import User

dashboard = Blueprint('dashboard', __name__)

def getChartDim(user_email=None):
    chartDim = {} 
    labels = []

    try:
        #admin: get all swings
        swings = Swing.getAllSwings()

        chartDim = {}

        for swing in swings:
            user_swing = chartDim.get(swing.user.name)
            if not user_swing:
                chartDim[swing.user.name]=[[swing.datetime, swing.distance]]
            else:
                user_swing.append([swing.datetime, swing.distance])
        
        # make sure the datetime line is sorted    
        for value in chartDim.values():
            value.sort(key=lambda x: x[0])
        
        print(chartDim)
        return chartDim, labels

    except:
        return None

def getChartDim2(user_email):
    chartDim = {} 
    labels = []

    try:
        #non-admin: get existing user's swings
        existing_user = User.getUser(email=user_email)
        swings = Swing.getSwings(user=existing_user)

        chartDim = {}

        for swing in swings:
            user_swing = chartDim.get(swing.label)
            
            if not user_swing:
                chartDim[swing.label]=[[swing.datetime, swing.distance]]

            else:
                user_swing.append([swing.datetime, swing.distance])
        
        # make sure the datetime line is sorted    
        for value in chartDim.values():
            value.sort(key=lambda x: x[0])
        
        print(chartDim)
        return chartDim, labels

    except:
        return None
    
# chart GET and POST act in tandum, POST done via myChart_CSV2.js
@dashboard.route('/chart', methods=['GET', 'POST'])
@login_required
def render_chart():
    if request.method == 'GET':
        #I want to get some data from the service
        return render_template('swing_chart.html', name=current_user.name, email_id=current_user.email, panel="SWING")
    
    elif request.method == 'POST':
        # Retrieve data from AJAX POST
        res = request.get_data("data")
        d_token = json.loads(res)
        email_id = d_token['email_id']
        
        # If it is Admin, all swing records are to be charted
        if email_id == "admin@abc.com":
            chartDim, labels = getChartDim()

        else: #non-admin, chart the user's swings by the various golf clubs
            chartDim, labels = getChartDim2(user_email=email_id)

        return jsonify({'chartDim': chartDim, 'labels': labels})
    