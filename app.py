from flask import Flask, redirect, render_template, request, url_for,session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime,date
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
    emerg_contct_no =db.Column(db.String(20))
    is_it_actve = db.Column(db.String(20), default="Pending")  #verify
    adventure_began = db.Column(db.DateTime, default=datetime.utcnow)
    staf_satus = db.Column(db.String(20), default="Pending")  #status of of staff 
    is_blacklsted = db.Column(db.Boolean, default=False)
    

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
    #treaking = db.relationship('Adventure_route',backref='assigned_staff',lazy=True)

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
    difficulty_level = db.Column(db.String(20))  # Easy, Moderate, Hard
    distnce = db.Column(db.Float)
    max_altitdu = db.Column(db.Integer)  # in meter we count
    track_status = db.Column(db.String(30), default="Upcoming")
    status_open_close = db.Column(db.String(20), default="Open")
    staf_fr_this_rout= db.Column(db.Integer, db.ForeignKey('adventures_users.usr_ref_id'))
    requested_slots = db.Column(db.Integer)
    slot_request_status = db.Column(db.String(20), default="Approved")

    #relationship
    bookings = db.relationship('AdventureBooking',backref='trek',lazy=True,cascade="all, delete")
    staff = db.relationship("AdventureUser",foreign_keys=[staf_fr_this_rout],backref="assigned_treks")

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

        adv_users = AdventureUser(usrname=name ,usr_mail=email, county=country, phone_no=ph_number,rolee=role,pasword=hashed_password,staf_satus="Pending" if role == "staff" else "Approved")
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
            session['usrname'] = regster_usr.usrname
            session['role'] = regster_usr.rolee
            return redirect(url_for("admin_dashboard"))

        # staf will login
        elif regster_usr.rolee == "staff":
            if regster_usr.staf_satus != "Approved":
                return "Your account is not approved yet."
            session['user_id'] = regster_usr.usr_ref_id
            session['usrname'] = regster_usr.usrname
            session['role'] = regster_usr.rolee
            return redirect(url_for("staff_dashboard"))
        
        # here user will login
        elif regster_usr.rolee == "user":
            session['user_id'] = regster_usr.usr_ref_id
            session['usrname'] = regster_usr.usrname
            session['role'] = regster_usr.rolee
            return redirect(url_for("user_dashboard"))
        # default
        return "Role not found"
    return render_template("login.html")
 
#see booked participants
@app.route("/participant_list/<int:trek_id>")
def participant_list(trek_id):
    admin = AdventureUser.query.get("admin_id")
    trek = Adventure_route.query.get_or_404(trek_id)

    bookings = AdventureBooking.query.filter_by(adv_rout_id=trek_id,booking_stat="Booked").all()

    return render_template("participant_list.html",admin=admin,trek=trek,bookings=bookings)
#admin dashboard
@app.route("/admin_dashboard")
def admin_dashboard():

    if not session.get("user_id"):
        return redirect(url_for("login"))

    if session.get("role") != "admin":
        return "Access Denied"

    admin = AdventureUser.query.get(session.get("user_id"))

    total_staff = AdventureUser.query.filter_by(rolee="staff").count()
    total_users = AdventureUser.query.filter_by(rolee="user").count()
    total_treks = Adventure_route.query.count()
    total_bookings = AdventureBooking.query.count()

    recent_bookings = AdventureBooking.query.order_by(
        AdventureBooking.reserved_on.desc()
    ).limit(5).all()

    return render_template(
        "admin_dashboard.html",
        admin=admin,
        total_staff=total_staff,
        total_users=total_users,
        total_treks=total_treks,
        total_bookings=total_bookings,
        recent_bookings=recent_bookings
    )

#user dashboard
@app.route("/user_dashboard")
def user_dashboard():
    #user login
    user_id = session.get("user_id")
    if not user_id:
        return redirect(url_for("login"))
    if session.get("role") !="user":
        return "acess denied"
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
    # checking exist booking 
    existing_booking = AdventureBooking.query.filter_by(adv_usr_id=user_id,adv_rout_id=trek_id).first()
    #booking
    booking = AdventureBooking(
        adv_usr_id=user_id,
        adv_rout_id=trek_id,
        booking_stat="Booked",
        payment_fail_or_succes="Pending",
        amount_to_pay=trek.rout_price,
        group_size=1,paymnt_stats="Pending",
        totl_amnt=trek.rout_price
    )
    # show left space if any
    trek.remening_spots -= 1
    db.session.add(booking)
    db.session.commit()
    return redirect(url_for("user_dashboard"))

#profile of user
@app.route("/view_profile_user")
def view_profile_user():
    # check login
    user_id = session.get("user_id")
    if not user_id:
        return redirect(url_for("login"))
    # current user
    user = AdventureUser.query.get(user_id)
    # all bookings of current user
    user_bookings = AdventureBooking.query.filter_by(
        adv_usr_id=user_id
    ).all()

    return render_template(
        "view_profile_user.html",
        user=user,
        user_bookings=user_bookings
    )

#user can edit profile
@app.route("/edit_user_profile", methods=["GET", "POST"])
def edit_user_profile():

    # login check
    user_id = session.get("user_id")

    if not user_id:
        return redirect(url_for("login"))

    # current user
    user = AdventureUser.query.get(user_id)

    # update profile
    if request.method == "POST":
        user.usrname = request.form.get("usrname")
        user.usr_mail = request.form.get("usr_mail")
        user.phone_no = request.form.get("phone_no")
        user.gender = request.form.get("gender")
        user.city_of_usr = request.form.get("city_of_usr")
        user.county = request.form.get("county")
        db.session.commit()
        return redirect(url_for("view_profile_user"))
    return render_template("edit_user_profile.html",user=user)


#user dashboard
@app.route("/user_treker_Dashboard")
def user_treker():
    return render_template("user_treker_Dashboard.html")


#staff dashboard
@app.route('/staff_dashboard')
def staff_dashboard():
    # login check
    staff_id = session.get("user_id")
    if not staff_id:
        return redirect(url_for("login"))
    if session.get("role") != "staff":
        return "Access Denied"

    # current logged in staff
    staff = AdventureUser.query.get(staff_id)

    # treks assigned by admin
    all_treks = Adventure_route.query.filter_by(staf_fr_this_rout=staff_id).all()
    assigned_treks = [trek for trek in all_treks if trek.track_status in ["Upcoming", "Ongoing"]]
    #close trek
    closed_tracks = [trek for trek in all_treks if trek.track_status == "Completed"]
    
    #count of each get update 
    total_assigned_treks = len(assigned_treks)
    total_participants = sum(len(trek.bookings) for trek in assigned_treks)
    total_tracks = len(all_treks)    
    closed_treks = len(closed_tracks)


    return render_template(
        "staff_dashboard.html",
        staff=staff,
        assigned_treks=assigned_treks,
        closed_tracks=closed_tracks,
        total_assigned_treks=total_assigned_treks, 
        total_participants=total_participants, 
        total_tracks=total_tracks, 
        closed_treks=closed_treks
    )

#staff can edit
@app.route("/edit_staff_profile", methods=["GET", "POST"])
def edit_staff_profile():
    user_id = session.get("user_id")
    if not user_id:
        return redirect(url_for("login"))
    staff = Adventure_Staff.query.filter_by(usr_ref_id=user_id).first()
    if request.method == "POST":
        staff.staf_nam = request.form.get("staf_nam")
        staff.gender = request.form.get("gender")
        staff.emerg_contat_no = request.form.get("emerg_contat_no")
        staff.phon_no = request.form.get("phon_no")
        staff.yers_of_work = request.form.get("yers_of_work")
        staff.langugs_known = request.form.get("langugs_known")
        staff.skiil_area = request.form.get("skiil_area")
        db.session.commit()
        return redirect(url_for("staff_dashboard"))
    return render_template("edit_staff_profile.html",staff=staff)

#staff can edit slots in manage trek
@app.route("/staff_edit_trek/<int:trek_id>", methods=["GET", "POST"])
def staff_edit_trek(trek_id):

    if session.get("role") != "staff":
        return redirect(url_for("login"))

    trek = Adventure_route.query.get_or_404(trek_id)

    # Staff can edit only their own trek
    if trek.staf_fr_this_rout != session.get("user_id"):
        return "Access Denied"

    if request.method == "POST":

        new_slots = int(request.form.get("capcity"))

        booked = len(trek.bookings)

        if new_slots < booked:
            return "Slots cannot be less than booked participants."

        trek.requested_slots = new_slots
        trek.slot_request_status = "Pending"

        db.session.commit()

        return redirect(url_for("staff_dashboard"))

    return render_template("staff_edit_trek.html", trek=trek)

#route of current trek
@app.route("/current_tracks")
def current_tracks():
    staff_id = session.get("user_id")
    if not staff_id:
        return redirect(url_for("login"))
    staff = AdventureUser.query.get(staff_id)

    # upcoming + ongoing
    tracks = Adventure_route.query.filter(
        Adventure_route.staf_fr_this_rout == staff_id,
        Adventure_route.track_status.in_(["Upcoming", "Ongoing"])
    ).all()

    return render_template(
        "current_track.html",
        staff=staff,
        tracks=tracks
    )


# close trek
@app.route("/closed_tracks")
def closed_tracks():

    staff_id = session.get("user_id")

    if not staff_id:
        return redirect(url_for("login"))

    staff = AdventureUser.query.get(staff_id)

    tracks = Adventure_route.query.filter_by(
        staf_fr_this_rout=staff_id,
        track_status="Completed"
    ).all()

    return render_template(
        "closed_track.html",
        staff=staff,
        tracks=tracks
    )


@app.route("/add_trek", methods=["GET", "POST"])     #add or edit by admin
def add_trek():
    # get all staff users
    stafs = AdventureUser.query.filter_by(rolee="staff").all()
    admin_name = session.get("usrname")
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
        strt_trck_date = request.form.get( "strt_trck_date" )
        end_trck_date = request.form.get( "end_trck_date" )
        distnce = request.form.get("distnce")
        max_altitdu = request.form.get("max_altitdu")

        strt_trck_date = datetime.strptime(strt_trck_date, "%Y-%m-%d").date()
        end_trck_date = datetime.strptime(end_trck_date, "%Y-%m-%d").date()
        if strt_trck_date < date.today():
            return "can't register this date"

        if end_trck_date < strt_trck_date:
            return "End trek date can't before start trek"
        #one staff can go in in trek
        existing_trek = Adventure_route.query.filter(
            Adventure_route.staf_fr_this_rout == staf_ref_id,
            Adventure_route.strt_trck_date <= end_trck_date,
            Adventure_route.end_trck_date >= strt_trck_date
        ).first()

        if existing_trek:
            return "this staff is already busy with other track"
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
            distnce=distnce,
            max_altitdu=max_altitdu,
            strt_trck_date=strt_trck_date,
            end_trck_date=end_trck_date,
             # default values
            track_status="Upcoming", 
            status_open_close="Open" 
        )

        db.session.add(new_route)
        db.session.commit()
        #after save it go to table booking
        return redirect(url_for("booking_table"))
    return render_template("add_trek.html", staff=stafs,admin_name=admin_name, today_date=date.today().strftime("%Y-%m-%d"))

#user see their booking table
@app.route("/user_booking_table")
def user_booking_table():
# check login
    user_id = session.get("user_id")

    if not user_id:
        return redirect(url_for("login"))

    # get current user
    user = AdventureUser.query.get(user_id)

    # get bookings of current user
    bookings = AdventureBooking.query.filter_by(adv_usr_id=user_id).all()

    return render_template(
        "user_booking_table.html",
        user=user,
        bookings=bookings
    )





#tracking table
@app.route("/booking_table")
def booking_table():

    if not session.get("user_id"):
        return redirect(url_for("login"))

    admin = AdventureUser.query.get(session.get("user_id"))
    search = request.args.get("search", "").strip()

    if search:
        bookings = AdventureBooking.query\
            .join(AdventureBooking.user)\
            .join(AdventureBooking.trek)\
            .outerjoin(Adventure_route.staff)\
            .filter(
                (AdventureUser.usrname.ilike(f"%{search}%")) |
                (Adventure_route.rout_name.ilike(f"%{search}%")) |
                (Adventure_route.staff.has(
                    AdventureUser.usrname.ilike(f"%{search}%")
                ))
            ).all()
    else:
        bookings = AdventureBooking.query.order_by(
            AdventureBooking.reserved_on.desc()
        ).all()

    return render_template(
        "booking_table.html",
        bookings=bookings,
        admin=admin
    )

#route for status change from open to close
@app.route("/change_track_status/<int:track_id>/<string:new_status>")
def change_track_status(track_id, new_status):

    track = Adventure_route.query.get_or_404(track_id)

    track.track_status = new_status

    # if ongoing or completed then close booking
    if new_status in ["Ongoing", "Completed"]:
        track.status_open_close = "Close"

    else:
        track.status_open_close = "Open"

    db.session.commit()
    return redirect(url_for("manage_trek"))

@app.route('/manage_staff')
def manage_staff():
    # admin login check
    admin_id = session.get("user_id")
    if not admin_id:
        return redirect(url_for("login"))
    admin = AdventureUser.query.get(admin_id)
    # active tab
    active_tab = request.args.get("tab", "pending")
    # pending staff
    pending_staff = AdventureUser.query.filter_by(rolee="staff",staf_satus="Pending").all()
    # approved staff
    approved_staff = AdventureUser.query.filter_by(rolee="staff",staf_satus="Approved").all()
    # blacklisted staff
    blacklisted_staff = AdventureUser.query.filter_by(
        rolee="staff",
        staf_satus="Blacklisted"
    ).all()

    return render_template(
        'manage_staff.html',
        pending_staff=pending_staff,
        approved_staff=approved_staff,
        blacklisted_staff=blacklisted_staff,
        active_tab=active_tab,
        admin=admin
    )

#staf get reject by admin
@app.route("/reject_staff/<int:staff_id>")
def reject_staff(staff_id):

    # get staff
    staff = AdventureUser.query.get_or_404(staff_id)

    #check is there any trek assign to 
    assigned_trek = Adventure_route.query.filter_by(staf_fr_this_rout=staff.usr_ref_id).first()

    if assigned_trek:
        return "can't delete this staff directly first delete trek assigned to this staff"

    # Blacklist the staff
    staff.staf_satus = "Blacklisted"
    staff.is_blacklsted = True

    db.session.commit()

    return redirect(url_for("manage_staff", tab="blacklisted"))

# manage user by admin
@app.route("/manage_users")
def manage_users():
    # admin login check
    admin_id = session.get("user_id")
    if not admin_id:
        return redirect(url_for("login"))
    admin = AdventureUser.query.get(admin_id)
    # active tab
    active_tab = request.args.get("tab", "active")
    # active users
    active_users = AdventureUser.query.filter_by(rolee="user",is_blacklsted=False).all()
    # blacklisted users
    blacklisted_users = AdventureUser.query.filter_by(rolee="user",is_blacklsted=True).all()

    return render_template(
        "manage_users.html",
        active_users=active_users,
        blacklisted_users=blacklisted_users,
        active_tab=active_tab,
        admin=admin,
        active_page="manage_users"
    )


#blacklist user
@app.route("/blacklist_user/<int:user_id>")
def blacklist_user(user_id):

    user = AdventureUser.query.get_or_404(user_id)
    # Check if this staff is assigned to any trek
    if user.rolee == "staff":
        assigned_trek = Adventure_route.query.filter_by(staf_fr_this_rout=user.usr_ref_id).first()
        if assigned_trek:
            return "trek is assigned to this staff first delete trek then u can block this staff"

    user.is_blacklsted = True
    db.session.commit()
    return redirect(url_for("manage_users",tab="blacklisted"))



# REMOVE BLACKLIST

@app.route("/unblacklist_user/<int:user_id>")
def unblacklist_user(user_id):
    user = AdventureUser.query.get_or_404(user_id)
    user.is_blacklsted = False
    db.session.commit()
    return redirect(url_for("manage_users",tab="active"))

#user profile 
@app.route("/user_profile/<int:user_id>")
def user_profile(user_id):
    # admin login check
    admin_id = session.get("user_id")
    if not admin_id:
        return redirect(url_for("login"))
    admin = AdventureUser.query.get(admin_id)
    # selected user
    user = AdventureUser.query.get_or_404(user_id)
    # bookings of user
    user_bookings = AdventureBooking.query.filter_by(
        adv_usr_id=user_id
    ).all()

    return render_template(
        "user_profile.html",
        user=user,
        user_bookings=user_bookings,
        admin=admin,
        active_page="manage_users"
    )




#staff profile 
@app.route("/staff_profile/<int:staff_id>")
def staff_profile(staff_id):
    admin_id = session.get("user_id")

    if not admin_id:
        return redirect(url_for("login"))

    admin = AdventureUser.query.get(admin_id)

    # selected staff user
    staff = AdventureUser.query.get_or_404(staff_id)

    # extra staff profile info
    staff_profile = Adventure_Staff.query.filter_by(
        usr_ref_id=staff_id
    ).first()

    # assigned tracks
    staff_tracks = Adventure_route.query.filter_by(
        staf_fr_this_rout=staff.usr_ref_id
    ).all()

    return render_template(
        "staff_profile.html",
        staff=staff,
        admin=admin,
        staff_tracks=staff_tracks,
        staff_profile=staff_profile
    )


# staf get approve by admin
@app.route('/approve_staff/<int:staff_id>')
def approve_staff(staff_id):
    staff = AdventureUser.query.get_or_404(staff_id)
    staff.staf_satus = "Approved"
    staff.is_it_actve = "Approved"
    staff.is_blacklsted=False
     # check if profile already exists
    existing_staff = Adventure_Staff.query.filter_by(usr_ref_id=staff.usr_ref_id).first()
    # create staff profile if not exists
    if not existing_staff:
        new_staff = Adventure_Staff(
            staf_nam=staff.usrname,
            usr_ref_id=staff.usr_ref_id,
            gender="Not Added",
            emerg_contat_no="0000000000",
            skiil_area="Not Added",
            staf_dte_of_bith=datetime.utcnow().date(),
            phon_no=staff.phone_no,
            yers_of_work=0,
            langugs_known="Not Added",
            availability_status="Available",
            perment_adress="Not Added"
        )
        db.session.add(new_staff)
    db.session.commit()
    return redirect(url_for('manage_staff'))


# trek manage by admin 
@app.route('/manage_trek')
def manage_trek():
    #admin
    admin_id = session.get("user_id")
    admin = AdventureUser.query.get(admin_id)
    # get all treks from database
    search = request.args.get("search", "").strip()
    if search:
        treks = Adventure_route.query.filter(
                (Adventure_route.rout_name.ilike(f"%{search}%")) |
                (Adventure_route.destination.ilike(f"%{search}%")) |
                (AdventureUser.usrname.ilike(f"%{search}%"))
        ).all()
    else:
        treks = Adventure_route.query.all()
    
    pending_requests = Adventure_route.query.filter_by(slot_request_status="Pending").all()
        
    return render_template('manage_trek.html',treks=treks,admin=admin,pending_requests=pending_requests)



#admin edit/ add trek
@app.route("/edit_trek/<int:trek_id>", methods=["GET", "POST"])
def edit_trek(trek_id):

    trek = Adventure_route.query.get_or_404(trek_id)

    if request.method == "POST":

        trek.rout_name = request.form.get("rout_name")
        trek.destination = request.form.get("destination")
        trek.difficulty_level = request.form.get("difficulty_level")

        trek.capcity = int(request.form.get("capcity"))

        trek.remening_spots = int(
            request.form.get("remening_spots")
        )

        db.session.commit()
        return redirect(url_for("manage_trek"))
    return render_template(
        "edit_trek.html",
        trek=trek
    )

#aprove route if staff edit trek slot
@app.route("/approve_slot_request/<int:trek_id>")
def approve_slot_request(trek_id):
    trek = Adventure_route.query.get_or_404(trek_id)
    trek.capcity = trek.requested_slots
    booked = len(trek.bookings)
    trek.remening_spots = trek.capcity - booked
    trek.slot_request_status = "Approved"
    trek.requested_slots = None
    db.session.commit()
    return redirect(url_for("manage_trek"))


#reject route if staff edit trek slot
@app.route("/reject_slot_request/<int:trek_id>")
def reject_slot_request(trek_id):
    trek = Adventure_route.query.get_or_404(trek_id)
    trek.slot_request_status = "Rejected"
    trek.requested_slots = None
    db.session.commit()
    return redirect(url_for("manage_trek"))

#deleted trek by admin 
@app.route("/delete_trek/<int:trek_id>")
def delete_trek(trek_id):
    trek = Adventure_route.query.get_or_404(trek_id)
    db.session.delete(trek)
    db.session.commit()
    return redirect(url_for("manage_trek"))

#user can browese/search trek 
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

#user can see or book trek here
@app.route("/trek_details/<int:trek_id>")
def trek_details(trek_id):
    user_id = session.get("user_id")
    if not user_id:
        return redirect(url_for("login"))
    trek = Adventure_route.query.get_or_404(trek_id)
    #trek assign to staff
    assigned_staff = AdventureUser.query.get( trek.staf_fr_this_rout )
    #booking show here all
    bookings = AdventureBooking.query.filter_by( adv_rout_id=trek_id ).all()
    return render_template("trek_details.html", trek=trek,assigned_staff=assigned_staff, bookings=bookings )
        
#user can see which trek on which days and that trek i complete or what
@app.route("/trek_history")
def trek_history():

    user_id = session.get("user_id")

    if not user_id:
        return redirect(url_for("login"))

    # current user
    user = AdventureUser.query.get(user_id)

    # completed bookings only
    history = AdventureBooking.query.filter_by(
        adv_usr_id=user_id
    ).all()

    return render_template(
        "trek_history.html",
        user=user,
        history=history
    )

#logout get to login page
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
                pasword= generate_password_hash("a123"),
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
