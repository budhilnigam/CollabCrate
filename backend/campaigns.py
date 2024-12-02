# campaigns.py
from __main__ import app,db,login_required,current_user,dbqueryconverter,singlequeryconverter,queryconverter
from flask import jsonify,request
from models import Campaign,AdRequest,sponsors
from sqlalchemy import or_

@app.route('/campaigns/create',methods=['POST'])
@login_required
def create_campaign():
    if current_user.get_id().split(':')[0] == 'sponsor':
        cmpn_name = request.form['cmpn_name']
        cmpn_description = request.form['cmpn_description']
        budget = request.form['budget']
        visibility = request.form['visibility']
        start_date = request.form['start_date']
        end_date = request.form['end_date']
        goals=request.form['goals']
        cmpn=Campaign(cmpn_name=cmpn_name,cmpn_description=cmpn_description,budget=budget,visibility=visibility,start_date=start_date,end_date=end_date,goals=goals,sp_username=current_user.username)
        db.session.add(cmpn)
        db.session.commit()
        return jsonify(singlequeryconverter(cmpn))        

@app.route('/campaigns/me',methods=['GET'])
@login_required
def get_campaigns_me():
    if current_user.get_id().split(':')[0] == 'sponsor':
        return jsonify(queryconverter(db.session.query(Campaign).filter(Campaign.sp_username==current_user.username).all()))
    elif current_user.get_id().split(':')[0] == 'influencer':
        return jsonify(queryconverter(db.session.query(Campaign).filter(Campaign.inf_id==current_user.inf_id).all()))

@app.route('/campaigns/all',methods=['GET'])
@login_required
def get_campaigns_all():
    if current_user.get_id().split(':')[0] == 'admin':
        return jsonify(db.session.query(Campaign).all())
    elif current_user.get_id().split(':')[0] == 'influencer':
        print((dbqueryconverter(db.session.query(Campaign, AdRequest).outerjoin(AdRequest,(Campaign.cmpn_id == AdRequest.cmpn_id) and (AdRequest.inf_id == current_user.inf_id)).filter(or_(Campaign.visibility == 'public', Campaign.sp_username == current_user.username)).all())))
        return jsonify(dbqueryconverter(db.session.query(Campaign.cmpn_id, AdRequest.ad_id, Campaign.cmpn_name, Campaign.cmpn_description, Campaign.budget, Campaign.visibility, Campaign.start_date, Campaign.end_date, Campaign.goals, Campaign.sp_username, AdRequest.message, AdRequest.payment_amt, AdRequest.made_by, AdRequest.status).outerjoin(AdRequest,(Campaign.cmpn_id == AdRequest.cmpn_id) and (AdRequest.inf_id == current_user.inf_id)).filter(or_(Campaign.visibility == 'public', Campaign.sp_username == current_user.username)).all()))
    elif current_user.get_id().split(':')[0] == 'sponsor':
        print((queryconverter(db.session.query(Campaign).filter(Campaign.visibility=='public' or Campaign.sp_username==current_user.username).all())))
        return jsonify(queryconverter(db.session.query(Campaign).filter(Campaign.visibility=='public' or Campaign.sp_username==current_user.username).all()))

@app.route('/campaigns/delete',methods=['DELETE'])
@login_required
def delete_campaign():
    cmpn_id = request.args.get('cmpn_id')
    campaign = db.session.query(Campaign).filter(Campaign.cmpn_id==cmpn_id).first()
    db.session.delete(campaign)
    db.session.commit()
    return {"message":"Campaign "+cmpn_id+"is deleted"}


@app.route('/campaigns/edit',methods=['PUT'])
@login_required
def edit_campaign():
    cmpn_id = request.args.get('cmpn_id')
    cmpn_name = request.form['cmpn_name']
    cmpn_description = request.form['cmpn_description']
    budget = request.form['budget']
    visibility = request.form['cmpn_visibility']
    start_date = request.form['start_date']
    end_date = request.form['end_date']
    goals=request.form['goals']
    campaign = db.session.query(Campaign).filter(Campaign.cmpn_id==cmpn_id).first()
    campaign.cmpn_name = cmpn_name
    campaign.cmpn_description = cmpn_description
    campaign.budget = budget
    campaign.visibility = visibility
    campaign.start_date = start_date
    campaign.end_date = end_date
    campaign.goals = goals
    db.session.commit()
    return {"message":"Campaign "+cmpn_id+" has been updated with new details"}
