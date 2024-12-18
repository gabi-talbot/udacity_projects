#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#
from flask_sqlalchemy import SQLAlchemy

from sqlalchemy import PrimaryKeyConstraint

db=SQLAlchemy()


class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(128), nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    genres = db.Column(db.String(120))
    facebook_link = db.Column(db.String(120))
    website_link = db.Column(db.String(120))
    seeking_venue = db.Column(db.Boolean, nullable=False, default=False)
    seeking_description = db.Column(db.String(500))
    artists = db.relationship('Artist', secondary='Show', backref=db.backref('shows', lazy='True'))

    # COMPLETED implement any missing fields, as a database migration using Flask-Migrate

class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(120), nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website_link = db.Column(db.String(120))
    seeking_venue = db.Column(db.Boolean, nullable=False, default=False)
    seeking_description = db.Column(db.String(500))

    # COMPLETED: implement any missing fields, as a database migration using Flask-Migrate
class Show(db.Model):
    __tablename__ = 'Show'
    __table_args__ = (
      PrimaryKeyConstraint('venue_id', 'artist_id'),
    )
    venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id'), primary_key=True)
    artist_id = db.Column( db.Integer, db.ForeignKey('Artist.id'), primary_key=True)
    start_time = db.Column(db.DateTime, nullable=False)

# COMPLETED Implement Show and Artist models, and complete all model relationships and properties, as a database migration.
