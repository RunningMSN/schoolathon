from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from . import db
from .models import School, Advisor, User
import json
import random
import pandas as pd

pages = Blueprint('pages', __name__)


@pages.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        school_id = request.form.get('school_id')
        school = School.query.filter_by(school_id=school_id).first()

        no_advisors_check = False
        if request.form.get('noAdvisorsCheck'):
            no_advisors_check = True
        found_advisors = False
        for item in request.form:
            if str(item).startswith("advisorRow"):
                num = str(item).split("-")[1]
                name = request.form.get(f"name-{num}")
                email = request.form.get(f"email-{num}")
                advisor_type = request.form.get(f"advisorType-{num}")

                if len(email) > 0:
                    found_advisors = True

                    new_advisor = Advisor(school_id=school_id, advisor_name=name, email=email, type=advisor_type, user_id=current_user.id)
                    db.session.add(new_advisor)
                    db.session.commit()
        
        if found_advisors or no_advisors_check:
            # Check Boxes
            if request.form.get('ccCheck'):
                school.community_college = True
            if request.form.get('hbcuCheck'):
                school.hbcu = True
            if request.form.get('msiCheck'):
                school.msi = True
            # Notes
            if len(request.form.get('notes')):
                school.notes = request.form.get('notes')

            school.completed = True
            school.user_id = current_user.id

            # Add contribution count
            current_user.contributions += 1

            db.session.commit()
        else:
            flash('You must either enter an advisor, or check that no advisors were found.', category='error')

    incomplete_schools = School.query.filter_by(completed=False).all()
    if len(incomplete_schools) > 0:
        random_school = random.choice(incomplete_schools)
    else:
        random_school = None

    return render_template("add.html", user=current_user, curr_school=random_school)


@pages.route('/leaderboard', methods=['GET', 'POST'])
@login_required
def leaderboard():
    users_query = pd.read_sql("SELECT name,contributions,team FROM user", db.engine)
    top_users = users_query[users_query['contributions'] > 0]
    top_users = top_users.sort_values('contributions', ascending=False)[0:20]
    
    
    top_teams = users_query.groupby('team', as_index=False).sum(numeric_only=True)

    top_teams = top_teams[top_teams['team'].notna() & (top_teams['team'] != "")]

    top_teams = top_teams.sort_values('contributions', ascending=False).head(20)


    return render_template("leaderboard.html", user=current_user, top_users=top_users, top_teams=top_teams)