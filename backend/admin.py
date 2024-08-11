from __main__ import app,db,login_manager,login_required,Influencer,sponsor
from flask import request

@app.route('/admin/flag', methods=['PUT'])
@login_required
def flag_user():
    user_type,user_id=request.args.get('user').split(':')
    if user_type=='influencer':
        user = Influencer.query.filter_by(inf_id=user_id).first()
    elif user_type=='sponsor':
        user = sponsor.query.filter_by(sponsor_id=user_id).first()
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