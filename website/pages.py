from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from . import db
from .models import School, Advisor
import json
import random

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

                    new_advisor = Advisor(school_id=school_id, advisor_name=name, email=email, type=advisor_type)
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

            # Add contribution count
            current_user.contributions += 1

            db.session.commit()

    incomplete_schools = School.query.filter_by(completed=False).all()
    if len(incomplete_schools) > 0:
        random_school = random.choice(incomplete_schools)
    else:
        random_school = None

    return render_template("add.html", user=current_user, curr_school=random_school)
