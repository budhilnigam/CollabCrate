from __main__ import app,db,login_manager,login_required,current_user,AdRequest,Campaign,sponsors
from flask import jsonify,request
@app.route('/ad_requests', methods=['GET','POST'])
@login_required
def ad_requests():
    if request.method == 'GET':
        if current_user.get_id().split(':')[0] == 'admin':
            sponsor_username=request.args.get('sponsor_username')
            if request.args.get('which')=='all':
                return jsonify(db.session.query(AdRequest).join(Campaign, AdRequest.cmpn_id==Campaign.cmpn_id).filter(Campaign.sp_username==sponsor_username).all())
            else:
                return jsonify(db.session.query(AdRequest).join(Campaign, AdRequest.cmpn_id==Campaign.cmpn_id).filter(Campaign.sp_username==sponsor_username,AdRequest.status==request.args.get('which')).all())
        elif current_user.get_id().split(':')[0] == 'sponsor':
            if request.args.get('which')=='all':
                return jsonify(db.session.query(AdRequest).join(Campaign, AdRequest.cmpn_id==Campaign.cmpn_id).filter(Campaign.sp_username==current_user.username).all())
            else:
                return jsonify(db.session.query(AdRequest).join(Campaign, AdRequest.cmpn_id==Campaign.cmpn_id).filter(Campaign.sp_username==current_user.username,AdRequest.status==request.args.get('which')).all())
        elif current_user.get_id().split(':')[0] == 'influencer':
            if request.args.get('which')=='all':
                return jsonify(db.session.query(AdRequest).join(Campaign, AdRequest.cmpn_id==Campaign.cmpn_id).filter(AdRequest.inf_id==current_user.inf_id).all())
            else:
                return jsonify(db.session.query(AdRequest).join(Campaign, AdRequest.cmpn_id==Campaign.cmpn_id).filter(AdRequest.inf_id==current_user.inf_id,AdRequest.status==request.args.get('which')).all())
    elif request.method == 'POST':
        cmpn_id = request.args.get('cmpn_id')
        inf_id = request.args.get('inf_id')
        message = request.form['message']
        payment_amt = request.form['payment_amt']
        ad_request = AdRequest(cmpn_id=cmpn_id, inf_id=inf_id, message=message, payment_amt=payment_amt,made_by=current_user.get_id().split(':')[0])
        db.session.add(ad_request)
        db.session.commit()
        return {"message":True}
    
@app.route('/ad_requests/action',methods=['PUT'])
@login_required
def ad_request_action():
    ad_id = request.args.get('ad_id')
    status = request.args.get('status')
    ad_request = db.session.query(AdRequest).filter(AdRequest.ad_id==ad_id).first()
    ad_request.status = status
    db.session.commit()
    return {"message":"Ad status changed to "+status}