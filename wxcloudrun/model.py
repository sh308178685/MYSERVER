from datetime import datetime
from flask_admin.contrib.sqla import ModelView
from wxcloudrun import db


# 计数表
class Counters(db.Model):
    # 设置结构体表格名称
    __tablename__ = 'Counters'

    # 设定结构体对应表格的字段
    id = db.Column(db.Integer, primary_key=True)
    count = db.Column(db.Integer, default=1)
    created_at = db.Column('createdAt', db.TIMESTAMP, nullable=False, default=datetime.now())
    updated_at = db.Column('updatedAt', db.TIMESTAMP, nullable=False, default=datetime.now())


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    email = db.Column(db.String(100))
    phone_number = db.Column(db.String(20))
    openid = db.Column(db.String(255))
    def __repr__(self):
        return self.username

class Venue(db.Model):
    __tablename__ = 'venues'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    location = db.Column(db.String(255))
    contact = db.Column(db.Boolean, default=False)  # 新增字段
    def __repr__(self):
        return self.name


class Booking(db.Model):
    __tablename__ = 'bookings'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    venue_id = db.Column(db.Integer, db.ForeignKey('venues.id'))
    # booking_date = db.Column(db.Date)
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    details = db.Column(db.Text)
    phone = db.Column(db.Text)
    user = db.relationship('User', backref=db.backref('bookings', lazy=True))
    venue = db.relationship('Venue', backref=db.backref('bookings', lazy=True))

    status = db.Column(db.String(20), default='pending')  # 'pending', 'approved', 'rejected'
    admin_feedback = db.Column(db.Text, nullable=True)


    def __repr__(self):
        return f'<Booking {self.id}>'
    


class BookingModelView(ModelView):
    column_list = ('user.username', 'venue.name', 'start_date', 'end_date', 'details', 'status', 'admin_feedback')
    form_columns = ('user', 'venue', 'start_date', 'end_date', 'details', 'status', 'admin_feedback')

    # 使用column_formatters来格式化status字段的显示
    column_formatters = {
        'status': lambda v, c, m, p: {
            'pending': '待审核',
            'approved': '已批准',
            'rejected': '已拒绝'
        }.get(m.status, '未知状态')
    }

    form_choices = {
        'status': [
            ('pending', '待审核'),
            ('approved', '已批准'),
            ('rejected', '已拒绝')
        ]
    }

    column_filters = ['status', 'start_date', 'end_date']


class PendingBookingModelView(ModelView):
    column_list = ('user.username', 'venue.name', 'start_date', 'end_date', 'details', 'status', 'admin_feedback')
    form_columns = ('user', 'venue', 'start_date', 'end_date', 'details', 'status', 'admin_feedback')

    # 使用 column_formatters 将 status 显示为中文
    column_formatters = {
        'status': lambda v, c, m, p: {
            'pending': '待审核',
            'approved': '已批准',
            'rejected': '已拒绝'
        }.get(m.status, '未知状态')
    }

    form_choices = {
        'status': [
            ('pending', '待审核'),
            ('approved', '已批准'),
            ('rejected', '已拒绝')
        ]
    }

    # 限制页面只显示status为pending的记录
    def get_query(self):
        return self.session.query(self.model).filter(self.model.status == 'pending')

    def get_count_query(self):
        return self.session.query(db.func.count('*')).filter(self.model.status == 'pending')
