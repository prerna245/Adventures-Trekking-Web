from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI' ] = "sqlite:///site.db"

db = SQLAlchemy(app)

#users table 
class AdventureUser(db.Model):
    __tablename__ = "adventures_users"

    usr_ref_id = db.Column(db.Integer, primary_key=True)
    usrname = db.Column(db.String(111), nullable=False)
    usr_mail = db.Column(db.String(160), unique=True, nullable=False)
    phone_no = db.Column(db.String(25), unique=True)
    county = db.Column(db.String(100))
    state_of_usr = db.Column(db.String(100))
    city_of_usr = db.Column(db.String(120))
    perment_address = db.Column(db.String(350))
    is_it_actve = db.Column(db.Boolean, default=True)
    adventure_began = db.Column(db.DateTime, default=datetime.utcnow)

#booking table 

class AdventureBooking(db.Model):
    __tablename__ = "adventure_bookings"

    boking_id = db.Column(db.Integer, primary_key=True)
    traveler_id = db.Column(db.Integer,db.ForeignKey("adventures_users.id"),nullable=False)
    route_id = db.Column(db.Integer,db.ForeignKey("adventure_routes.route_id"),nullable=False)
    reserved_on = db.Column(db.DateTime,default=datetime.utcnow)
    booking_stage = db.Column(db.String(30),default="Pending")    # conform/pendig/pass/cancel
    payment_state = db.Column(db.String(30),default="Pending")   # fail/sucess/pending
    amount_to_pay = db.Column(db.Float)
    group_size = db.Column(db.Integer,default=1)




# table for route that we will take for tracking

class Adventure_route(db.Model):
    __tablename__ = "adventures_rout"

    rout_id = db.Column(db.Integer, primary_key=True)
    rout_name = db.Column(db.String(200), nullable=False)
    destination = db.Column(db.String(180), nullable=False)
    rout_price = db.Column(db.Float)
    capacity = db.Column(db.Integer)
    rout_type = db.Column(db.String(60), nullable=False)
    total_days_are = db.Column(db.Integer)
    remening_spots = db.Column(db.Integer)
    journey_date = db.Column(db.Date)
    __tablename__ = "adventures_staff_members"

    staff_id = db.Column(db.Integer, primary_key=True)
    usr_ref_id = db.Column(db.Integer,db.ForeignKey("adventures_users.id"),nullable=False)
    skill_area = db.Column(db.String(130))
    phone_no = db.Column(db.String(15))
    years_of_work = db.Column(db.Integer)
    perment_address = db.Column(db.Text)
    date_joined = db.Column(db.DateTime,default=datetime.utcnow)

#revieww table for score
class Adventures_Review(db.Model):
    __tablename__ = "trek_reviews"

    reviw_id = db.Column(db.Integer, primary_key=True)
    traveler_id = db.Column(db.Integer,db.ForeignKey("adventures_users.id"),nullable=False)
    route_id = db.Column(db.Integer,db.ForeignKey("adventure_routes.route_id"),nullable=False)
    reviw_score = db.Column(db.Integer)
    fedback = db.Column(db.Text)
    reviw_date = db.Column(db.DateTime,default=datetime.utcnow)






if __name__ == "__main__":
    with app.app_context:
        db.create_all()
        existing_admin = AdventureUser.query.filter_by(
            email = "admin@Adventure.com").first()
        
        if not existing_admin:
            admin= AdventureUser(
                name="Admin",
                email="admin@Adventure.com",
                password= "admin123",
                role="admin"
            )
            db.session.add(admin)
            db.session.commit()

            print("Admin user created.")
        else:
            print("Admin account exist.") 
    app.run(debug=True)