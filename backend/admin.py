# admin.py
from __main__ import app,db,login_manager,login_required,current_user,Influencer,sponsors,Campaign
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
@app.route('/admin/flag', methods=['PUT'])
@login_required
def flag_user():
    user_type,user_id=request.args.get('user').split(':')
    if user_type=='influencer':
        user = Influencer.query.filter_by(inf_id=user_id).first()
    elif user_type=='sponsor':
        user = sponsors.query.filter_by(sponsor_id=user_id).first()
    user.flagged = request.args.get('flag')
    db.session.commit()
    return {"message":"User "+user_id+"is "+("" if user.flagged else "un")+"flagged"}

@app.route('/campaigns/flag',methods=['PUT'])
@login_required
def flag_campaign():
    cmpn_id = request.args.get('cmpn_id')
    flag = request.args.get('flag')
    campaign = db.session.query(Campaign).filter(Campaign.cmpn_id==cmpn_id).first()
    campaign.flagged = flag
    db.session.commit()
    return {"message":"Campaign "+cmpn_id+"is "+("" if flag else "un")+"flagged"}



@app.route('/api/admin/statistics', methods=['GET'])
def get_statistics():
    total_campaigns = Campaign.query.count()
    total_users = Influencer.query.count() + sponsors.query.count()
    flagged_campaigns = Campaign.query.filter_by(flagged=True).count()
    flagged_users = (Influencer.query.filter_by(flagged=True).count() +
                     sponsors.query.filter_by(flagged=True).count())

    return jsonify({
        'totalCampaigns': total_campaigns,
        'totalUsers': total_users,
        'flaggedCampaigns': flagged_campaigns,
        'flaggedUsers': flagged_users
    })

@app.route('/api/admin/campaigns', methods=['GET'])
def get_campaigns():
    campaigns = Campaign.query.all()
    return jsonify([{
        'cmpn_id': c.cmpn_id,
        'cmpn_name': c.cmpn_name,
        'cmpn_description': c.cmpn_description,
        'flagged': c.flagged
    } for c in campaigns])

@app.route('/api/admin/users', methods=['GET'])
def get_users():
    influencers = Influencer.query.all()
    sponsors_data = sponsors.query.all()

    users = [
        {'id': u.inf_id, 'username': u.username, 'type': 'Influencer', 'flagged': u.flagged}
        for u in influencers
    ] + [
        {'id': u.sp_id, 'username': u.username, 'type': 'Sponsor', 'flagged': u.flagged}
        for u in sponsors_data
    ]

    return jsonify(users)

@app.route('/api/admin/flag/campaign/<int:campaign_id>', methods=['POST'])
def flag_campaign(campaign_id):
    campaign = Campaign.query.get(campaign_id)
    if not campaign:
        return jsonify({'error': 'Campaign not found'}), 404

    campaign.flagged = True
    db.session.commit()
    return jsonify({'message': 'Campaign flagged successfully'})

@app.route('/api/admin/flag/user/<int:user_id>', methods=['POST'])
def flag_user(user_id):
    user = Influencer.query.get(user_id) or sponsors.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    user.flagged = True
    db.session.commit()
    return jsonify({'message': 'User flagged successfully'})