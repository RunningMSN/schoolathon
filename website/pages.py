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
    # Get total contributions
    total_contributions = sum(top_users['contributions'])

    # Pick top 20 users
    top_users = top_users.sort_values('contributions', ascending=False)[0:20]
    
    # Pick top 20 teams
    top_teams = users_query.groupby('team', as_index=False).sum(numeric_only=True)
    top_teams = top_teams[top_teams['team'].notna() & (top_teams['team'] != "")]
    top_teams = top_teams.sort_values('contributions', ascending=False).head(20)

    # Number of schools left
    incomplete_schools_count = len(School.query.filter_by(completed=False).all())

    # Number of schools that we already have
    complete_schools_count = len(School.query.filter_by(completed=True).all())
    current_advisors_count = len(Advisor.query.all())

    return render_template("leaderboard.html", user=current_user, top_users=top_users, 
                           top_teams=top_teams, total_contributions=total_contributions, 
                           incomplete_schools_count=incomplete_schools_count, 
                           complete_schools_count=complete_schools_count,
                           current_advisors_count=current_advisors_count)

# @pages.route('/merge', methods=['GET', 'POST'])
# def merge_integration():
#     integration_sheet = pd.read_csv("/Users/daniel/Documents/schoolathon/other/NAAHP_Integration_Sheet.tsv", sep="\t")
#     new_schools_count = 0
#     updated_schools_count = 0
#     new_advisor_count = 0
#     # Iterate through sheet to update school information
#     for idx, row in integration_sheet.iterrows():
#         # If have an advisor 1, then need to integrate
#         if not pd.isna(row["advisor_1"]):
#             school_id = row["school_id"]
#             school = School.query.filter_by(school_id=school_id).first()
            
#             wiki_link = ""
#             if not pd.isna(row["wiki"]):
#                 wiki_link=row["wiki"]

#             # If no school, need to add in a new school
#             if not school:
#                 new_schools_count += 1
#                 new_school = School(school_id=school_id,region=row["region"],state=row["state"],school_name=row["school_name"],wiki=wiki_link,community_college=row["community_college"],hbcu=row["hbcu"],msi=row["msi"],completed=1)
#                 db.session.add(new_school)
#                 db.session.commit()
#             # Otherwise can add information to existing school entry
#             else:
#                 updated_schools_count += 1
#                 school.completed = 1
#                 school.community_college = row["community_college"]
#                 school.hbcu = row["hbcu"]
#                 school.msi = row["msi"]
#                 if not school.notes == row["notes"]:
#                     if not pd.isna(school.notes):
#                         school.notes = f"{school.notes}; {row["notes"]}"
#                     else:
#                         school.notes = row["notes"]
#                 db.session.commit()

#     # Process advisors
#     ## Start by subsetting and pivoting the dataframe
#     advisor_cols = integration_sheet.filter(regex=r'^(school_id|advisor_|email_)').columns
#     advisors_df = integration_sheet[advisor_cols]
#     advisors_df = advisors_df[advisors_df["advisor_1"].str.len() > 0]
#     advisors_df_long = (
#         pd.wide_to_long(
#             advisors_df,
#             stubnames=["advisor", "email"],
#             i="school_id",
#             j="x",
#             sep="_"
#         ).reset_index()
#     )
#     advisors_df_long = advisors_df_long[advisors_df_long["advisor"].notna()]
    
#     # Iterate through to get new advisors
#     for idx, row in advisors_df_long.iterrows():
#         if not Advisor.query.filter_by(email=row["email"]).first():
#             new_advisor_count += 1
#             new_advisor = Advisor(school_id=row["school_id"], advisor_name=row["advisor"], email=row["email"], type="Pre-Health Advisor")
#             db.session.add(new_advisor)
#             db.session.commit()

#     print("Final NAAHP Merge Statistics:")
#     print(f"New Schools Added: {new_schools_count}")
#     print(f"Total Schools Updated: {updated_schools_count}")
#     print(f"New Advisors Added: {new_advisor_count}")

#     return render_template("login.html", user=current_user)