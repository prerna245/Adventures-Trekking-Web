from flask import Flask, redirect, render_template, request, url_for,session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)
app.secret_key = "my_secret_key"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

#users table 
class AdventureUser(db.Model):
    __tablename__ = "adventures_users"

    usr_ref_id = db.Column(db.Integer, primary_key=True)
    usrname = db.Column(db.String(111), nullable=False)
    rolee = db.Column(db.String(20), default="user")
    usr_mail = db.Column(db.String(160), unique=True, nullable=False)
    phone_no = db.Column(db.String(25), unique=True)
    gender = db.Column(db.String(20))       #it's optional
    any_medical_isue = db.Column(db.String(200))
    any_experince = db.Column(db.String(200))  #eg begginer or 2 year of exper. or no exper.
    pasword = db.Column(db.String(200))
    county = db.Column(db.String(100), nullable=False)
    state_of_usr = db.Column(db.String(100))
    city_of_usr = db.Column(db.String(120))
    perment_address = db.Column(db.String(350))
    emerg_contct_no =db.Column(db.Integer)
    is_it_actve = db.Column(db.Boolean, default=True)
    adventure_began = db.Column(db.DateTime, default=datetime.utcnow)

# relationship
    bokings_fr_usr = db.relationship('AdventureBooking',backref='user',lazy=True)
    staf_profil_of_usr = db.relationship('Adventure_Staff',backref='user',uselist=False)



# staff table 
class Adventure_Staff(db.Model):
    __tablename__ = "adventures_staff"
    staf_ref_id= db.Column(db.Integer, primary_key=True)
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
    verifed= db.Column(db.Boolean, default=False)
    date_joined = db.Column(db.DateTime,default=datetime.utcnow)
    #relationship
    treaking = db.relationship('Adventure_route',backref='assigned_staff',lazy=True)

#booking table 

class AdventureBooking(db.Model):
    __tablename__ = "adventure_bookings"

    boking_id = db.Column(db.Integer, primary_key=True)
    adv_usr_id = db.Column(db.Integer,db.ForeignKey("adventures_users.usr_ref_id"),nullable=False)     #usr id is use as forign key  
    adv_rout_id = db.Column(db.Integer,db.ForeignKey("adventures_route.adv_rout_id"),nullable=False)
    reserved_on = db.Column(db.DateTime,default=datetime.utcnow)
    booking_stat = db.Column(db.String(30),default="Pending")    # conform/pendig/pass/cancel
    payment_fail_or_succes = db.Column(db.String(30),default="Pending")   # fail/sucess/pending
    amount_to_pay = db.Column(db.Float)
    group_size = db.Column(db.Integer,default=1)
    paymnt_stats = db.Column(db.String(20),default='Pending')   #regarding payment 
    cancl_reason = db.Column(db.String(100))
    totl_amnt = db.Column(db.Float)
    any_specil_request = db.Column(db.Text)    
    




# table for route that we will take for tracking

class Adventure_route(db.Model):
    __tablename__ = "adventures_route"

    adv_rout_id = db.Column(db.Integer, primary_key=True)
    rout_name = db.Column(db.String(200), nullable=False)
    capcity = db.Column(db.Integer, nullable = False)
    rout_type = db.Column(db.String(60), nullable=False)
    destination = db.Column(db.String(180), nullable=False)
    total_days_are = db.Column(db.Integer)
    remening_spots = db.Column(db.Integer)
    rout_price = db.Column(db.Float)
    journey_date = db.Column(db.Date)
    strt_trck_date=db.Column(db.Date)
    end_trck_date=db.Column(db.Date)
    date_joined = db.Column(db.DateTime,default=datetime.utcnow)
    #strt_loction = db.Column(db.String(100), nullable=False)
    #end_loction = db.Column(db.String(100), nullable=False)
    difficulty_level = db.Column(db.String(20))  # Easy, Moderate, Hard
    distnce = db.Column(db.Float)
    max_altitdu = db.Column(db.Integer)  # in meter we count
    staf_fr_this_rout= db.Column(db.Integer, db.ForeignKey('adventures_staff.staf_ref_id'))
    
    #relationship
    bookings = db.relationship('AdventureBooking',backref='trek',lazy=True)


#revieww table for score
class Adventures_Review(db.Model):
    __tablename__ = "trek_reviews"

    reviw_id = db.Column(db.Integer, primary_key=True)
    adv_usr_id = db.Column(db.Integer,db.ForeignKey("adventures_users.usr_ref_id"),nullable=False)
    route_id = db.Column(db.Integer,db.ForeignKey("adventures_route.adv_rout_id"),nullable=False)
    reviw_score = db.Column(db.Integer)
    fedback = db.Column(db.Text)
    deficult_rate=db.Column(db.Integer)  #rate from 1 to 5
    date_on_crete = db.Column(db.DateTime,default=datetime.utcnow)   #created date when it was created



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
        role = request.form["role"]     # identify user or staff
        hashed_password = generate_password_hash(password)

        adv_users = AdventureUser(usrname=name ,usr_mail=email, county=country, phone_no=ph_number,rolee=role,pasword=hashed_password)
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
        password = request.form.get("password")
        regster_usr = AdventureUser.query.filter_by(usr_mail=email).first()
#all checking 
        # email check
        if not regster_usr:
            return "Invalid Email ID"

        # check password
        if not check_password_hash(regster_usr.pasword,password):
            return "Invalid Password"
        # active check
        
        # admin will register here
        if regster_usr.rolee == "admin":
            session['user_id'] = regster_usr.usr_ref_id
            return redirect(url_for("admin_dashboard"))

        # staf will login
        elif regster_usr.rolee == "staff":
            if regster_usr.is_it_actve ==False:
                return "Your account isn't verified yet! wait till approve."
            session['user_id'] = regster_usr.usr_ref_id
            return redirect(url_for("staff_dashboard"))
        
        # here user will login
        elif regster_usr.rolee == "user":
            session['user_id'] = regster_usr.usr_ref_id
            return redirect(url_for("user_dashboard"))
        # default
        return "Role not found"
    return render_template("login.html")

@app.route("/admin_dashboard")
def admin_dashboard():
    #staff ,trek, and user detail is store
    total_staf = AdventureUser.query.filter_by(rolee="staff").count()
    #total_staf = Adventure_Staff.query.count()
    total_treks = Adventure_route.query.count()
    pnding_staff = AdventureUser.query.filter_by(rolee="staff",is_it_actve= True).count()
    #staff = Adventure_Staff.query.all()
    staff = AdventureUser.query.filter_by(rolee="staff").all()
    total_users=AdventureUser.query.filter_by(rolee="user").count()
    #get admin detail
    admin_id = session.get("user_id")    #this is for login admin id
    admin = AdventureUser.query.get(admin_id)
    #get booking detail
    total_bookings = AdventureBooking.query.count()
    recent_bookings = AdventureBooking.query.order_by(AdventureBooking.reserved_on.desc()).limit(5).all()
    return render_template('admin_dashboard.html',total_staff=total_staf,total_treks=total_treks,pending_staff=pnding_staff,total_bookings=total_bookings,total_users=total_users,recent_bookings=recent_bookings,staff=staff,admin=admin)

@app.route("/user_dashboard")
def user_dashboard():
    #user login
    user_id = session.get("user_id")
    if not user_id:
        return redirect(url_for("login"))
    # user detail
    user = AdventureUser.query.get(user_id)
    # this show available trek blike if it available or not
    treks = Adventure_route.query.all()
    # here user booking 
    my_bookings = AdventureBooking.query.filter_by(adv_usr_id=user_id).all()
    return render_template("user_dashboard.html",user=user,treks=treks,my_bookings=my_bookings)

@app.route("/book_trek/<int:trek_id>")
def book_trek(trek_id):
    user_id = session.get("user_id")
    if not user_id:
        return redirect(url_for("login"))
    trek = Adventure_route.query.get_or_404(trek_id)
    # booking willn't availble when spot become 0 
    if trek.remening_spots <= 0:
        return "No spots available"
    # booking 
    booking = AdventureBooking(adv_usr_id=user_id,adv_rout_id=trek_id,booking_stat="Booked",payment_fail_or_succes="Pending",amount_to_pay=trek.rout_price,
                               group_size=1,paymnt_stats="Pending",totl_amnt=trek.rout_price)
    # show left space if any
    trek.remening_spots -= 1
    db.session.add(booking)
    db.session.commit()
    return redirect(url_for("user_dashboard"))

@app.route("/user_treker")
def user_treker():
    return render_template("user_treker.html")


@app.route('/staff_dashboard')
def staff_dashboard():
    stafs = AdventureUser.query.filter_by(rolee="staff").all()
    return render_template("staff_dashboard.html",stafs=stafs)

@app.route('/approve_staff/<int:staf_ref_id>')
def verrify_stafs(staf_ref_id):
    stafs =AdventureUser.query.get_or_404(staf_ref_id)
    stafs.is_it_actve=True
    db.session.commit()
    return redirect(url_for("admin_dashboard"))


@app.route("/add_route", methods=["GET", "POST"])
def add_routes():

    # get all staff users
    stafs = AdventureUser.query.filter_by(rolee="staff").all()

    if request.method == "POST":
        rout_name = request.form.get("rout_name")
        staf_ref_id= request.form.get("staf_ref_id")
        destination = request.form.get("destination")
        rout_type = request.form.get("rout_type")
        difficulty_level = request.form.get("difficulty_level")
        total_days_are = request.form.get("total_days_are")
        rout_price = request.form.get("rout_price")
        capcity = request.form.get("capcity")
        remening_spots = request.form.get("remening_spots")
        journey_date = request.form.get("journey_date")
        distnce = request.form.get("distnce")
        max_altitdu = request.form.get("max_altitdu")

        new_route = Adventure_route(
            rout_name=rout_name,
            staf_fr_this_rout=staf_ref_id,
            destination=destination,
            rout_type=rout_type,
            difficulty_level=difficulty_level,
            total_days_are=total_days_are,
            rout_price=rout_price,
            capcity=capcity,
            remening_spots=remening_spots,
            journey_date=journey_date,
            distnce=distnce,
            max_altitdu=max_altitdu
        )

        db.session.add(new_route)
        db.session.commit()

        return redirect(url_for("admin_dashboard"))

    return render_template("add_route.html", staff=stafs)

@app.route('/manage_staff')
def manage_staff():
    mng_stafs=AdventureUser.query.filter_by(rolee="staff").all()
    return render_template('manage_staff.html', staff=mng_stafs)

@app.route('/manage_trek')
def manage_routes():
    return render_template('manage_trek.html')

@app.route("/manage_users")
def manage_users():
    users = AdventureUser.query.filter_by(rolee="user").all()
    return render_template("manage_users.html",users=users)
  

@app.route("/browse_treks")
def browse_treks():
    user_id = session.get("user_id")
    if not user_id:
        return redirect(url_for("login"))
    # here id of current user
    user = AdventureUser.query.get(user_id)
    #all trek will here
    treks = Adventure_route.query.all()
    return render_template("browse_treks.html",user=user,treks=treks)
        

@app.route("/logout")
def logout():
    session.clear()             #.pop("user_id", None)
    return redirect('/login')



if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        existing_admin = AdventureUser.query.filter_by(usr_mail = "admin@Adventure.com").first()
        
        if not existing_admin:
            admin= AdventureUser(
                usrname="Admin",
                usr_mail="admin@Adventure.com",
                pasword= generate_password_hash("admin123"),
                rolee="admin",
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