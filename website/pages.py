from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from . import db
from .models import School
import json
import random

pages = Blueprint('pages', __name__)


@pages.route('/', methods=['GET', 'POST'])
@login_required
def home():
    incomplete_schools = School.query.filter_by(completed=False).all()
    if len(incomplete_schools) > 0:
        random_school = random.choice(incomplete_schools)
    else:
        random_school = None

    return render_template("add.html", user=current_user, curr_school=random_school)
