from flask import Flask, redirect, render_template, request, url_for,session
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
    role = db.Column(db.String(20), default="user")
    usr_mail = db.Column(db.String(160), unique=True, nullable=False)
    phone_no = db.Column(db.String(25), unique=True)
    gender = db.Column(db.String(20))       #it's optional
    any_medical_isue = db.Column(db.String(200))
    any_experince = db.Column(db.String(200))  #eg begginer or 2 year of exper. or no exper.
    pasword = db.Column(db.String(200), nullable=False)
    county = db.Column(db.String(100),nullable = False)
    state_of_usr = db.Column(db.String(100),nullable = False)
    city_of_usr = db.Column(db.String(120),nullable = False)
    perment_address = db.Column(db.String(350),nullable = False)
    emerg_contct_no =db.Column(db.Integer,nullable =False)
    is_it_actve = db.Column(db.Boolean, default=True)
    adventure_began = db.Column(db.DateTime, default=datetime.utcnow)

# staff table 
class Adventure_Staff(db.Model):
    __tablename__ = "adventures_staff"
    staf_ref_id = db.Column(db.Integer, primary_key=True)
    staf_nam = db.Column(db.String(100), nullable=False)
    gender = db.Column(db.String(20))
    emerg_contat_no = db.Column(db.String(20))
    usr_ref_id = db.Column(db.Integer,db.ForeignKey("adventures_users.usr_ref_id"),nullable=False)
    skiil_area = db.Column(db.String(130))
    staf_dte_of_bith = db.Column(db.Date, nullable = False)
    phon_no = db.Column(db.String(15),nullable = False)
    yers_of_work = db.Column(db.Integer)
    langugs_known = db.Column(db.String(200))
    availability_status = db.Column(db.String(20))       #staf available already busy with other client or on Leave
    perment_adress = db.Column(db.Text,nullable = False)
    date_joined = db.Column(db.DateTime,default=datetime.utcnow,nullable = False)


#booking table 

class AdventureBooking(db.Model):
    __tablename__ = "adventure_bookings"

    boking_id = db.Column(db.Integer, primary_key=True)
    adv_usr_id = db.Column(db.Integer,db.ForeignKey("adventures_users.usr_ref_id"),nullable=False)     #usr id is use as forign key  
    adv_rout_id = db.Column(db.Integer,db.ForeignKey("adventures_route.adv_rout_id"),nullable=False)
    reserved_on = db.Column(db.DateTime,default=datetime.utcnow)
    booking_stage = db.Column(db.String(30),default="Pending")    # conform/pendig/pass/cancel
    payment_state = db.Column(db.String(30),default="Pending")   # fail/sucess/pending
    amount_to_pay = db.Column(db.Float)
    group_size = db.Column(db.Integer,default=1)
    paymnt_stats = db.Column(db.String(20),default='Pending')   #regarding payment 
    cancl_reason = db.Column(db.String(100))
    any_specil_reque = db.Column(db.Text)    





# table for route that we will take for tracking

class Adventure_route(db.Model):
    __tablename__ = "adventures_route"

    adv_rout_id = db.Column(db.Integer, primary_key=True)
    rout_name = db.Column(db.String(200), nullable=False)
    destination = db.Column(db.String(180), nullable=False)
    rout_price = db.Column(db.Float)
    capcity = db.Column(db.Integer, nullable = False)
    rout_type = db.Column(db.String(60), nullable=False)
    total_days_are = db.Column(db.Integer)
    remening_spots = db.Column(db.Integer)
    journey_date = db.Column(db.Date)
    strt_loction = db.Column(db.String(100), nullable=False)
    end_loction = db.Column(db.String(100), nullable=False)
    difficulty_level = db.Column(db.String(20))  # Easy, Moderate, Hard
    distnce = db.Column(db.Float)
    max_altitdu = db.Column(db.Integer)  # in meter we count
    
   


#revieww table for score
class Adventures_Review(db.Model):
    __tablename__ = "trek_reviews"

    reviw_id = db.Column(db.Integer, primary_key=True)
    traveler_id = db.Column(db.Integer,db.ForeignKey("adventures_users.usr_ref_id"),nullable=False)
    route_id = db.Column(db.Integer,db.ForeignKey("adventures_route.adv_rout_id"),nullable=False)
    reviw_score = db.Column(db.Integer)
    fedback = db.Column(db.Text)
    deficult_rate=db.Column(db.Integer)  #rate from 1 to 5
    reviw_date = db.Column(db.DateTime,default=datetime.utcnow)
    created_at = db.Column(db.DateTime,default=datetime.utcnow)



#routes are define
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        country = request.form.get("country")
        ph_number = request.form.get("ph_number")
        password = request.form.get("password")
        role = request.form["role"]     # identify user or admine
        hashed_password = generate_password_hash(password)

        adv_users = AdventureUser(usrname=name ,usr_mail=email, county=country, phone_no=ph_number,pasword=hashed_password)

        if role == "admin":
            return "Admin cannot do registration"

        regster_usr = AdventureUser.query.filter_by(usr_mail=email).first()
        if regster_usr:
            return "Email already registered"
        
        db.session.add(adv_users)  # it add new ussser 
        db.session.commit()            #save usr to db permanent

        return redirect(url_for("login"))
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password= request.form.get("password")
        regster_usr = AdventureUser.query.filter_by(usr_mail =email).first()

        if  not regster_usr:
            return "Invalid email id"
        
        if not check_password_hash(regster_usr.pasword, password):
            return "Invalid Password"
        
        return redirect(url_for("user_dashboard"))
    return render_template("login.html")

        
@app.route("/logout")
def logout():
    session.pop("user_id", None)
    return redirect(url_for("index"))



if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        existing_admin = AdventureUser.query.filter_by(
            usr_mail = "admin@Adventure.com").first()
        
        if not existing_admin:
            admin= AdventureUser(
                usrname="Admin",
                usr_mail="admin@Adventure.com",
                pasword= generate_password_hash("admin123"),
                role="admin",
                county ="india",
                state_of_usr="Bihar",
                city_of_usr="Patna",
                perment_address="Admin Address",
                emerg_contct_no=1234567890
            )
            db.session.add(admin)
            db.session.commit()

            print("Admin user created.")
        else:
            print("Admin account exist.") 

    app.run(debug=True)