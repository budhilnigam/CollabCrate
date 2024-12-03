from __main__ import app,db,login_manager,login_required,current_user,singlequeryconverter,queryconverter,dbqueryconverter
from models import Influencer, Campaign, AdRequest, sponsors, Admin
from flask import jsonify,request
from sqlalchemy import or_,and_,func

@app.route('/user/info', methods=['GET'])
@login_required
def sponsor_info():
    user_type=current_user.get_id().split(':')[0]
    username = current_user.username

    if user_type == 'influencer':
        # Fetch the influencer's data
        influencer = Influencer.query.filter_by(username=username).first()
        if not influencer:
            return jsonify({"error": "Influencer not found"}), 404

        # Calculate stats for the influencer
        inf_id = influencer.inf_id
        ad_requests = db.session.query(AdRequest.ad_id, AdRequest.cmpn_id, AdRequest.status, AdRequest.message, AdRequest.payment_amt, AdRequest.made_by, Campaign.cmpn_name, Campaign.cmpn_description, Campaign.sp_username, Campaign.budget, Campaign.visibility, Campaign.start_date, Campaign.end_date, Campaign.goals).join(Campaign).filter(
            and_(
                AdRequest.inf_id == inf_id,
                AdRequest.cmpn_id == Campaign.cmpn_id
            )
        ).all()
        pending_requests = AdRequest.query.filter_by(inf_id=inf_id, status='pending').count()
        completed_requests = AdRequest.query.filter_by(inf_id=inf_id, status='completed').count()
        
        ongoing_campaigns = db.session.query(Campaign).join(AdRequest).filter(
            and_(
                AdRequest.inf_id == inf_id,
                AdRequest.status == 'accepted',
                Campaign.start_date <= func.current_date(),
                Campaign.end_date >= func.current_date()
            )
        ).count()

        previous_campaigns = db.session.query(Campaign).join(AdRequest).filter(
            and_(
                AdRequest.inf_id == inf_id,
                AdRequest.status == 'accepted',
                Campaign.end_date < func.current_date()
            )
        ).count()

        stats = {
            "user_type": "influencer",
            "username": username,
            "ad_requests": dbqueryconverter(ad_requests),
            "pending_requests": pending_requests,
            "completed_requests": completed_requests,
            "ongoing_campaigns": ongoing_campaigns,
            "previous_campaigns": previous_campaigns
        }

    elif user_type == 'sponsor':
        # Fetch the sponsor's data
        sponsor = sponsors.query.filter_by(username=username).first()
        if not sponsor:
            return jsonify({"error": "Sponsor not found"}), 404

        # Calculate stats for the sponsor
        sp_username = sponsor.username
        campaigns = Campaign.query.filter_by(sp_username=sp_username).all()

        active_campaigns = Campaign.query.filter(
            and_(
                Campaign.sp_username == sp_username,
                Campaign.start_date <= func.current_date(),
                Campaign.end_date >= func.current_date()
            )
        ).count()

        completed_campaigns = Campaign.query.filter(
            and_(
                Campaign.sp_username == sp_username,
                Campaign.end_date < func.current_date()
            )
        ).count()

        ad_requests = db.session.query(AdRequest.ad_id, AdRequest.cmpn_id, AdRequest.status, AdRequest.message, AdRequest.payment_amt, AdRequest.made_by,Influencer.username, Campaign.cmpn_name, Campaign.cmpn_description, Campaign.budget, Campaign.visibility, Campaign.start_date, Campaign.end_date, Campaign.goals).join(Campaign, AdRequest.cmpn_id == Campaign.cmpn_id).join(Influencer, AdRequest.inf_id == Influencer.inf_id).filter(
            and_(
                Campaign.sp_username == sp_username,
                AdRequest.cmpn_id == Campaign.cmpn_id,
                AdRequest.inf_id == Influencer.inf_id,
            )
        ).all()
        pending_requests = AdRequest.query.filter(
            and_(
                AdRequest.status == 'pending',
                AdRequest.cmpn_id == Campaign.cmpn_id,
                Campaign.sp_username == sp_username
            )
        ).count()

        completed_requests = AdRequest.query.filter(
            and_(
                AdRequest.status == 'completed'
            )
        ).count()

        stats = {
            "user_type": "sponsor",
            "username": username,
            "campaigns": queryconverter(campaigns),
            "active_campaigns": active_campaigns,
            "completed_campaigns": completed_campaigns,
            "ad_requests": dbqueryconverter(ad_requests),
            "pending_requests": pending_requests,
            "completed_requests": completed_requests
        }

    else:
        return jsonify({"error": "Invalid user type"}), 400

    return jsonify(stats), 200


@app.route('/api/influencers', methods=['GET'])
def search_influencers():
    query = request.args.get('query', '')
    influencers = Influencer.query.all()
    results = [
        {
            "inf_id": inf.inf_id,
            "username": inf.username,
            "inf_category": inf.inf_category,
            "inf_niche": inf.inf_niche,
            "inf_reach": inf.inf_reach,
        }
        for inf in influencers
    ]
    return jsonify(queryconverter(influencers))

@app.route('/api/campaigns', methods=['GET'])
@login_required
def get_campaigns():
    sponsor_username = current_user.username
    campaigns = Campaign.query.filter_by(sp_username=sponsor_username).all()
    return jsonify(queryconverter(campaigns))

@app.route('/api/ad-requests', methods=['POST'])
def create_ad_request():
    data = request.json
    ad_request = AdRequest(
        cmpn_id=data['cmpn_id'],
        inf_id=data['inf_id'],
        message=data['message'],
        payment_amt=data['payment_amt'],
    )
    db.session.add(ad_request)
    db.session.commit()
    return jsonify({"message": "Ad request created successfully!"}), 201