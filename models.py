from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()



class User(db.Model):
    """User model with signup/login"""

    __tablename__ = 'users'

    def __repr__(self):
        """returns basic info"""
        return f"<User(id: {self.id}): {self.username}>"

    id = db.Column(
        db.Integer,
        primary_key=True,
        nullable=False,
        autoincrement=True
    )

    username = db.Column(
        db.Text,
        nullable=False,
        unique=True
    )

    password = db.Column(
        db.Text,
        nullable=False
    )

    @classmethod
    def signup(cls, username, password):
        """Adds user to db with encrypted password"""

        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = User(
            username = username,
            password = hashed_pwd
        )

        db.session.add(user)
        return user
    
    @classmethod
    def changePassword(cls, user_id, password):
        """Updates password in db"""

        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = User.query.get_or_404(user_id)
        user.password = hashed_pwd
        db.session.commit()

    
    @classmethod
    def authenticateUser(cls, username, password):
        """Allows user to log in with password"""

        user = cls.query.filter_by(username=username).first()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user

        return False
    
class PokemonTeam(db.Model):
    """model for a team of six pokemon"""

    __tablename__ = 'pokemonteams'

    id = db.Column(
        db.Integer,
        primary_key=True,
        nullable=False,
        autoincrement=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete='CASCADE'),
        nullable=False
    )

    pokemon1 = db.Column(
        db.Text
    )

    pokemon1URL = db.Column(
        db.Text
    )

    pokemon2 = db.Column(
        db.Text
    )

    pokemon2URL = db.Column(
        db.Text
    )


    pokemon3 = db.Column(
        db.Text
    )

    pokemon3URL = db.Column(
        db.Text
    )


    pokemon4 = db.Column(
        db.Text
    )

    pokemon4URL = db.Column(
        db.Text
    )


    pokemon5 = db.Column(
        db.Text
    )

    pokemon5URL = db.Column(
        db.Text
    )


    pokemon6 = db.Column(
        db.Text
    )

    pokemon6URL = db.Column(
        db.Text
    )

    user = db.relationship('User')

def connect_db(app):
    app.app_context().push()
    db.app = app
    db.init_app(app)