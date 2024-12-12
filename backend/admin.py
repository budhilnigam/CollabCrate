# admin.py
from __main__ import app,db,login_manager,login_required,current_user,Influencer,sponsors,Campaign,AdRequest,dbqueryconverter,queryconverter
from flask import request,jsonify

@app.route('/approve_registration', methods=['POST'])
@login_required
def approve_registration():
    if current_user.get_id().split(':')[0] != 'admin':
        return jsonify({"message": "Permission denied"}), 403

    user = request.args.get('user')
    if user.split(':')[0] == 'influencer':
        user = Influencer.query.filter_by(username=user.split(':')[1]).first()
    elif user.split(':')[0] == 'sponsor':
        user = sponsors.query.filter_by(username=user.split(':')[1]).first()
    if user:
        user.approved = True
        db.session.commit()
        return jsonify({"message": "User approved"}), 200
    return jsonify({"message": "User not found"}), 404

@app.route('/users/flag', methods=['PUT'])
@login_required
def flag_user():
    user_type=request.args.get('user_type')
    user_id=request.args.get('user_id')
    flag=request.args.get('flag')
    print(user_type,user_id,flag)
    if user_type=='influencer':
        user = Influencer.query.filter_by(inf_id=user_id).first()
    elif user_type=='sponsor':
        user = sponsors.query.filter_by(sponsor_id=user_id).first()
    user.flagged = int(flag)
    db.session.commit()
    return {"message":"User "+user_id+"is "+("" if user.flagged else "un")+"flagged"}

@app.route('/campaigns/flag',methods=['PUT'])
@login_required
def flag_campaign():
    cmpn_id = request.args.get('cmpn_id')
    flag = request.args.get('flag')
    campaign = db.session.query(Campaign).filter(Campaign.cmpn_id==cmpn_id).first()
    campaign.flagged = int(flag)
    db.session.commit()
    return {"message":"Campaign "+cmpn_id+"is "+("" if flag else "un")+"flagged"}

@app.route('/admin/campaigns', methods=['GET'])
@login_required
def admin_campaigns():
    return jsonify(queryconverter(Campaign.query.all()))

@app.route('/admin/users', methods=['GET'])
@login_required
def admin_users():
    return jsonify({"influencers":queryconverter(Influencer.query.all()),"sponsors":queryconverter(sponsors.query.all())})

@app.route('/admin/ad_requests', methods=['GET'])
@login_required
def admin_ad_requests():
    return jsonify(queryconverter(AdRequest.query.all()))