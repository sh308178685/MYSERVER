from datetime import datetime
from flask import render_template, request, jsonify
from run import app
from wxcloudrun.dao import delete_counterbyid, query_counterbyid, insert_counter, update_counterbyid
from wxcloudrun.model import Counters, User, Venue, Booking
from wxcloudrun.response import make_succ_empty_response, make_succ_response, make_err_response
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from wxcloudrun import db
import requests
import config
from wxcloudrun.util import Util

admin = Admin(app, name='管理后台', template_mode='bootstrap3')
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Venue, db.session))
admin.add_view(ModelView(Booking, db.session))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    js_code = request.json.get('js_code')
    username = request.json.get('username')
    email = request.json.get('email')
    phone_number = request.json.get('phone_number')

    if not js_code or not username or not email or not phone_number:
        return jsonify({'status': 'error', 'message': '缺少必要的参数'}), 400

    url = f'https://api.weixin.qq.com/sns/jscode2session?appid={config.APP_ID}&secret={config.APP_SECRET}&js_code={js_code}&grant_type=authorization_code'

    response = requests.get(url, verify=False)
    # response = requests.get(url)

    if response.status_code == 200:
        session_data = response.json()
        openid = session_data.get('openid')
        if openid:
            user = User.query.filter_by(openid=openid).first()
            if user:
                token = Util.create_token(user.id, config.SERVER_SECRET, 3600 * 24)
                return jsonify({
                    'status': 'success',
                    'openid': openid,
                    'username': user.username,
                    'email': user.email,
                    'user_id': user.id,
                    'token': token,
                    'message': '登录成功'
                })
            else:
                try:
                    new_user = User(username=username, email=email, phone_number=phone_number, openid=openid)
                    db.session.add(new_user)
                    db.session.commit()

                    token = Util.create_token(new_user.id, config.SERVER_SECRET, 3600 * 24)
                    return jsonify({
                        'status': 'success',
                        'openid': openid,
                        'username': username,
                        'email': email,
                        'user_id': new_user.id,
                        'token': token,
                        'message': '注册并登录成功'
                    })
                except Exception as e:
                    db.session.rollback()
                    return jsonify({
                        'status': 'error',
                        'message': '注册失败: ' + str(e)
                    }), 500
        else:
            return jsonify({
                'status': 'error',
                'message': '网络请求失败'
            }), response.status_code


@app.route('/allbookings', methods=['GET'])
def get_allbookings():
    bookings = db.session.query(Booking, User, Venue).join(User, Booking.user_id == User.id).join(Venue, Booking.venue_id == Venue.id).all()

    events = []
    for booking, user, venue in bookings:
        events.append({
            'title': f"{user.username} - {venue.name} ({booking.details})",
            'start': booking.start_date.strftime('%Y-%m-%d'),
            'end' : booking.end_date.strftime('%Y-%m-%d'),
            'description': booking.details
        })

    return jsonify(events)


@app.route('/venues', methods=['GET'])
def get_venues():
    venues = Venue.query.all()
    return jsonify([{'id': v.id, 'name': v.name, 'location': v.location} for v in venues])


@app.route('/takebooking', methods=['POST'])
def create_booking():
    data = request.get_json()
    user_id = Util.get_current_user_id(request)

    if user_id is not None:
        venue_id = data.get('venue_id')
        # booking_date = datetime.strptime(data.get('booking_date'), '%Y-%m-%d').date()
        start_date = datetime.strptime(data.get('start_date'), '%Y-%m-%d %H:%M')
        end_date = datetime.strptime(data.get('end_date'), '%Y-%m-%d %H:%M')
        details = data.get('details')

        existing_booking = Booking.query.filter(
            Booking.user_id == user_id,
            Booking.venue_id == venue_id,
            # Booking.booking_date == booking_date,
            Booking.start_date <= end_date,
            Booking.end_date >= start_date
        ).first()
        if existing_booking:
            return jsonify({'message': 'This time slot is already booked.'}), 400

        if end_date <= start_date:
            return jsonify({'message': 'end time is before start time.'}), 401

        new_booking = Booking(
            user_id=user_id,
            venue_id=venue_id,
            # booking_date=booking_date,
            start_date=start_date,
            end_date=end_date,
            details=details
        )

        db.session.add(new_booking)
        db.session.commit()

        return jsonify({'message': 'Booking created successfully.'}), 201
    else:
        return jsonify({'message': 'TOKEN过期请重新登录.'}), 202


@app.route('/bookings', methods=['GET'])
def get_bookings():
    user_id = Util.get_current_user_id(request)
    bookings = Booking.query.filter_by(user_id=user_id).all()

    result = []
    for booking in bookings:
        venue = Venue.query.get(booking.venue_id)
        result.append({
            'id': booking.id,
            'venue_name': venue.name,
            'venue_location': venue.location,
            # 'booking_date': booking.booking_date.strftime('%Y-%m-%d'),
            'start_date': booking.start_date.strftime('%Y-%m-%d %H:%M'),
            'end_date': booking.end_date.strftime('%Y-%m-%d %H:%M'),
            'details': booking.details
        })

    return jsonify(result), 200

@app.route('/bookings/<int:booking_id>', methods=['DELETE'])
def cancel_booking(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    if booking.user_id != Util.get_current_user_id(request):
        return jsonify({'message': 'You do not have permission to cancel this booking.'}), 403

    db.session.delete(booking)
    db.session.commit()

    return jsonify({'message': 'Booking cancelled successfully.'}), 200
