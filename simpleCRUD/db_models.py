from simpleCRUD import db, auth_manager
from flask_login import UserMixin


class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(70))
    login = db.Column(db.String(70), nullable = False, unique = True)
    email = db.Column(db.String(50), nullable = False, unique = True)
    password = db.Column(db.String(255), nullable = False)
    role = db.Column(db.Integer, db.ForeignKey('users_roles.role_id'), default = 1)

    car_relation = db.relationship('Cars', backref=db.backref('owner', lazy=True))

    request_relation = db.relationship('RepairRequests', backref=db.backref('repair_request', lazy=True))

    role_relation = db.relationship('Users_roles', backref = db.backref('Users', lazy = True))


class Cars(db.Model):
    car_id = db.Column(db.Integer, primary_key=True)
    vin_number = db.Column(db.String(70), nullable = False, unique = True)
    mark = db.Column(db.String(40), nullable = False)
    model = db.Column(db.String(60), nullable = False)
    prod_year = db.Column(db.Integer(), nullable = False)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    car_repair_req = db.relationship('RepairRequests', backref=db.backref('car_repair_request', lazy=True))


class Users_roles(db.Model):
    role_id = db.Column(db.Integer, primary_key=True)
    has_acess = db.Column(db.Boolean, nullable = False, default = 0)
    description = db.Column(db.String(50), nullable = False)


class RepairRequests(db.Model):
    req_id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(1000))
    repair_type = db.Column(db.Integer, db.ForeignKey('repairtypes.id'))
    client_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable = False)
    client_car = db.Column(db.Integer, db.ForeignKey('cars.car_id'), nullable = False)
    date = db.Column(db.Date, nullable = False)
    time = db.Column(db.Time, nullable = False)



class Repairtypes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(100))
    cost = db.Column(db.Integer)

    role_relation = db.relationship('RepairRequests', backref=db.backref('type_repair', lazy=True))



db.create_all()


@auth_manager.user_loader
def load_user(user_id):
    return Users.query.get(user_id)