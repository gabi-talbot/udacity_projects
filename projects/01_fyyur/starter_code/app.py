#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#
import sys
from datetime import datetime

import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for, abort
from flask_moment import Moment

import logging
from logging import Formatter, FileHandler

from forms import *
from models import db, Venue, Show, Artist

from flask_migrate import Migrate

import collections.abc

collections.Callable = collections.abc.Callable
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
app.app_context().push()
db.init_app(app)
# To allow use of flask-migrate commands
migrate = Migrate(app, db)


# COMPLETED: connect to a local postgresql database


#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
    date = dateutil.parser.parse(value)
    if format == 'full':
        format = "EEEE MMMM, d, y 'at' h:mma"
    elif format == 'medium':
        format = "EE MM, dd, y h:mma"
    return babel.dates.format_datetime(date, format, locale='en')


app.jinja_env.filters['datetime'] = format_datetime


#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
    return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
    # TODO: replace with real venues data.
    #       num_upcoming_shows should be aggregated based on number of upcoming shows per venue.
    database_venues = Venue.query.distinct('city').all()
    print(database_venues)


    data = []

    for venue in database_venues:
      datum = {"city": None, "state": None, "venues": []}
      datum["city"] = venue.city
      datum["state"] = venue.state
      data.append(datum)

    for city in data:
      # query db for venues in same city AND state
      city_venues = Venue.query.filter_by(city=city['city']).all()
      for city_venue in city_venues:
        # TODO: add in upcoming shows logic - refactor out from venue id
        venue_data = {"id": city_venue.id, "name": city_venue.name, "num_upcoming_shows": 0}
        city["venues"].append(venue_data)




    print(data)



    # data=[{
    #   "city": "San Francisco",
    #   "state": "CA",
    #   "venues": [{
    #     "id": 1,
    #     "name": "The Musical Hop",
    #     "num_upcoming_shows": 0,
    #   }, {
    #     "id": 3,
    #     "name": "Park Square Live Music & Coffee",
    #     "num_upcoming_shows": 1,
    #   }]
    # }, {
    #   "city": "New York",
    #   "state": "NY",
    #   "venues": [{
    #     "id": 2,
    #     "name": "The Dueling Pianos Bar",
    #     "num_upcoming_shows": 0,
    #   }]
    # }]
    return render_template('pages/venues.html', areas=data)


@app.route('/venues/search', methods=['POST'])
def search_venues():
    # TODO: implement search on venues with partial string search. Ensure it is case-insensitive.
    # seach for Hop should return "The Musical Hop".
    # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
    response = {
        "count": 1,
        "data": [{
            "id": 2,
            "name": "The Dueling Pianos Bar",
            "num_upcoming_shows": 0,
        }]
    }
    return render_template('pages/search_venues.html', results=response,
                           search_term=request.form.get('search_term', ''))


@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
    # COMPLETED: replace with real venue data from the venues table, using venue_id
    selected_venue = Venue.query.get(venue_id)

    if selected_venue is None:
        abort(404)
    else:
        # process genres string in to a list for view logic
        genres = selected_venue.genres.lstrip('{').rstrip('}').split(',')

        # retrieve a list of show dictionaries, including artist name and image, using supplied venue id
        shows = db.session.query(Show, Artist).join(Artist, Artist.id == Show.artist_id).filter(Show.venue_id == venue_id)
        formatted_shows = []
        for show in shows:
            formatted_show = {}
            formatted_show['artist_id'] = show.Show.artist_id
            formatted_show['artist_name'] = show.Artist.name
            formatted_show['artist_image_link'] = show.Artist.image_link
            formatted_show['start_time'] = show.Show.start_time
            formatted_shows.append(formatted_show)


        # split into past and upcoming based on today's date and time
        past_shows = []
        upcoming_shows = []
        now = datetime.now()
        for show in formatted_shows:
            datetime_object = datetime.strptime(show['start_time'], '%Y-%m-%d %H:%M:%S')
            if datetime_object < now:
                past_shows.append(show)
            else:
                upcoming_shows.append(show)

        # number of shows for past and upcoming
        past_shows_count = len(past_shows)
        upcoming_shows_count = len(upcoming_shows)

        data = {
            "id": selected_venue.id,
            "name": selected_venue.name,
            "city": selected_venue.city,
            "state": selected_venue.state,
            "address": selected_venue.address,
            "phone": selected_venue.phone,
            "image_link": selected_venue.image_link,
            "genres": genres,
            "facebook_link": selected_venue.facebook_link,
            "website": selected_venue.website_link,
            "seeking_talent": selected_venue.seeking_talent,
            "seeking_description": selected_venue.seeking_description,
            "past_shows": past_shows,
            "upcoming_shows": upcoming_shows,
            "past_shows_count": past_shows_count,
            "upcoming_shows_count": upcoming_shows_count
        }

    return render_template('pages/show_venue.html', venue=data)


#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
    form = VenueForm()
    return render_template('forms/new_venue.html', form=form)


@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
    # COMPLETED: insert form data as a new Venue record in the db, instead
    form = VenueForm(request.form)
    error = False

    try:
        name = form.name.data
        city = form.city.data
        state = form.state.data
        address = form.address.data
        phone = form.phone.data
        image_link = form.image_link.data
        genres = form.genres.data
        facebook_link = form.facebook_link.data
        website_link = form.website_link.data
        seeking_talent = form.seeking_talent.data
        seeking_description = form.seeking_description.data

        new_venue = Venue(
            name=name, city=city, state=state, address=address, phone=phone,
            image_link=image_link, genres=genres, facebook_link=facebook_link,
            website_link=website_link, seeking_talent=seeking_talent,
            seeking_description=seeking_description
        )
        # Create Venue object and commit to database
        db.session.add(new_venue)
        db.session.commit()
        # on successful db insert, flash success
        # TODO: modify data to be the data object returned from db insertion
        flash('Venue ' + form.name.data + ' was successfully listed!')
    except:
        error = True
        print(sys.exc_info())
        db.session.rollback()
    finally:
        db.session.close()
        if error:
            # COMPLETED: on unsuccessful db insert, flash an error instead.
            # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
            flash('An error occurred. Venue ' + form.name.data + ' could not be listed.')
        else:
            return render_template('pages/home.html')


@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
    # TODO: Complete this endpoint for taking a venue_id, and using
    # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.

    # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
    # clicking that button delete it from the db then redirect the user to the homepage
    return None


#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
    # COMPLETED: replace with real data returned from querying the database
    # Query db for a list of all Artist objects
    artists = Artist.query.all()
    data = []

    # Loop through query and append id and name to data
    for artist in artists:
        artist_data = {}
        artist_data["id"] = artist.id
        artist_data["name"] = artist.name
        data.append(artist_data)

    return render_template('pages/artists.html', artists=data)


@app.route('/artists/search', methods=['POST'])
def search_artists():
    # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
    # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
    # search for "band" should return "The Wild Sax Band".
    response = {
        "count": 1,
        "data": [{
            "id": 4,
            "name": "Guns N Petals",
            "num_upcoming_shows": 0,
        }]
    }
    return render_template('pages/search_artists.html', results=response,
                           search_term=request.form.get('search_term', ''))


@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
    # shows the artist page with the given artist_id
    # COMPLETED: replace with real artist data from the artist table, using artist_id
    selected_artist = Artist.query.get(artist_id)

    if selected_artist is None:
        abort(404)

    else:
        # process genres string in to a list for view logic
        genres = selected_artist.genres.lstrip('{').rstrip('}').split(',')

        # join Show and Venue on venue_id, filtered by artist_id parameter
        shows = db.session.query(Show, Venue).join(Venue, Venue.id == Show.venue_id).filter(
            Show.artist_id == artist_id)

        formatted_shows = []
        for show in shows:
            formatted_show = {}
            formatted_show['venue_id'] = show.Show.venue_id
            formatted_show['venue_name'] = show.Venue.name
            formatted_show['venue_image_link'] = show.Venue.image_link
            formatted_show['start_time'] = show.Show.start_time
            formatted_shows.append(formatted_show)

        # split into past shows and upcoming based on today's date and time
        past_shows = []
        upcoming_shows = []
        now = datetime.now()

        for show in formatted_shows:
            datetime_object = datetime.strptime(show['start_time'], '%Y-%m-%d %H:%M:%S')
            if datetime_object < now:
                past_shows.append(show)
            else:
                upcoming_shows.append(show)

        # no of shows in each category
        past_shows_count = len(past_shows)
        upcoming_shows_count = len(upcoming_shows)

        data = {
            "id": selected_artist.id,
            "name": selected_artist.name,
            "city": selected_artist.city,
            "state": selected_artist.state,
            "phone": selected_artist.phone,
            "image_link": selected_artist.image_link,
            "genres": genres,
            "facebook_link": selected_artist.facebook_link,
            "website": selected_artist.website_link,
            "seeking_venue": selected_artist.seeking_venue,
            "seeking_description": selected_artist.seeking_description,
            "past_shows": past_shows,
            "upcoming_shows": upcoming_shows,
            "past_shows_count": past_shows_count,
            "upcoming_shows_count": upcoming_shows_count
        }

    # data1 = {
    #     "id": 4,
    #     "name": "Guns N Petals",
    #     "genres": ["Rock n Roll"],
    #     "city": "San Francisco",
    #     "state": "CA",
    #     "phone": "326-123-5000",
    #     "website": "https://www.gunsnpetalsband.com",
    #     "facebook_link": "https://www.facebook.com/GunsNPetals",
    #     "seeking_venue": True,
    #     "seeking_description": "Looking for shows to perform at in the San Francisco Bay Area!",
    #     "image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
    #     "past_shows": [{
    #         "venue_id": 1,
    #         "venue_name": "The Musical Hop",
    #         "venue_image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60",
    #         "start_time": "2019-05-21T21:30:00.000Z"
    #     }],
    #     "upcoming_shows": [],
    #     "past_shows_count": 1,
    #     "upcoming_shows_count": 0,
    # }
    # data2 = {
    #     "id": 5,
    #     "name": "Matt Quevedo",
    #     "genres": ["Jazz"],
    #     "city": "New York",
    #     "state": "NY",
    #     "phone": "300-400-5000",
    #     "facebook_link": "https://www.facebook.com/mattquevedo923251523",
    #     "seeking_venue": False,
    #     "image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
    #     "past_shows": [{
    #         "venue_id": 3,
    #         "venue_name": "Park Square Live Music & Coffee",
    #         "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
    #         "start_time": "2019-06-15T23:00:00.000Z"
    #     }],
    #     "upcoming_shows": [],
    #     "past_shows_count": 1,
    #     "upcoming_shows_count": 0,
    # }
    # data3 = {
    #     "id": 6,
    #     "name": "The Wild Sax Band",
    #     "genres": ["Jazz", "Classical"],
    #     "city": "San Francisco",
    #     "state": "CA",
    #     "phone": "432-325-5432",
    #     "seeking_venue": False,
    #     "image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
    #     "past_shows": [],
    #     "upcoming_shows": [{
    #         "venue_id": 3,
    #         "venue_name": "Park Square Live Music & Coffee",
    #         "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
    #         "start_time": "2035-04-01T20:00:00.000Z"
    #     }, {
    #         "venue_id": 3,
    #         "venue_name": "Park Square Live Music & Coffee",
    #         "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
    #         "start_time": "2035-04-08T20:00:00.000Z"
    #     }, {
    #         "venue_id": 3,
    #         "venue_name": "Park Square Live Music & Coffee",
    #         "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
    #         "start_time": "2035-04-15T20:00:00.000Z"
    #     }],
    #     "past_shows_count": 0,
    #     "upcoming_shows_count": 3,
    # }
    # data = list(filter(lambda d: d['id'] == artist_id, [data1, data2, data3]))[0]
    return render_template('pages/show_artist.html', artist=data)


#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
    form = ArtistForm()
    artist = {
        "id": 4,
        "name": "Guns N Petals",
        "genres": ["Rock n Roll"],
        "city": "San Francisco",
        "state": "CA",
        "phone": "326-123-5000",
        "website": "https://www.gunsnpetalsband.com",
        "facebook_link": "https://www.facebook.com/GunsNPetals",
        "seeking_venue": True,
        "seeking_description": "Looking for shows to perform at in the San Francisco Bay Area!",
        "image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80"
    }
    # TODO: populate form with fields from artist with ID <artist_id>
    return render_template('forms/edit_artist.html', form=form, artist=artist)


@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
    # TODO: take values from the form submitted, and update existing
    # artist record with ID <artist_id> using the new attributes

    return redirect(url_for('show_artist', artist_id=artist_id))


@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
    form = VenueForm()
    venue = {
        "id": 1,
        "name": "The Musical Hop",
        "genres": ["Jazz", "Reggae", "Swing", "Classical", "Folk"],
        "address": "1015 Folsom Street",
        "city": "San Francisco",
        "state": "CA",
        "phone": "123-123-1234",
        "website": "https://www.themusicalhop.com",
        "facebook_link": "https://www.facebook.com/TheMusicalHop",
        "seeking_talent": True,
        "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.",
        "image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60"
    }
    # TODO: populate form with values from venue with ID <venue_id>
    return render_template('forms/edit_venue.html', form=form, venue=venue)


@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
    # TODO: take values from the form submitted, and update existing
    # venue record with ID <venue_id> using the new attributes
    return redirect(url_for('show_venue', venue_id=venue_id))


#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
    form = ArtistForm()

    return render_template('forms/new_artist.html', form=form)


@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
    # called upon submitting the new artist listing form
    # COMPLETED: insert form data as a new Venue record in the db, instead
    form = ArtistForm(request.form)
    error = False

    try:
        name = form.name.data
        city = form.city.data
        state = form.state.data
        phone = form.phone.data
        genres = form.genres.data
        facebook_link = form.facebook_link.data
        image_link = form.image_link.data
        website_link = form.website_link.data
        seeking_venue = form.seeking_venue.data
        seeking_description = form.seeking_description.data

        new_artist = Artist(
            name=name, city=city, state=state, phone=phone,
            image_link=image_link, genres=genres, facebook_link=facebook_link,
            website_link=website_link, seeking_venue=seeking_venue,
            seeking_description=seeking_description
        )
        # Create Artist object and commit to database
        db.session.add(new_artist)
        db.session.commit()
        # on successful db insert, flash success
        # TODO: modify data to be the data object returned from db insertion
        flash('Artist ' + form.name.data + ' was successfully listed!')
    except:
        error = True
        print(sys.exc_info())
        db.session.rollback()
    finally:
        db.session.close()
        if error:
            # COMPLETED: on unsuccessful db insert, flash an error instead.
            # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
            flash('An error occurred. Artist ' + form.name.data + ' could not be listed.')
        else:
            return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
    # displays list of shows at /shows
    # COMPLETED: replace with real venues data.

    # join query
    queried_shows = db.session.query(Show, Venue, Artist).join(Venue, Venue.id == Show.venue_id).join(Artist, Artist.id == Show.artist_id)
    print(queried_shows)

    # format data for return
    data = []
    for show in queried_shows:
        formatted_show = {"venue_id": show.Show.venue_id, "venue_name": show.Venue.name,
                          "artist_id": show.Show.artist_id, "artist_name": show.Artist.name,
                          "artist_image_link": show.Artist.image_link, "start_time": show.Show.start_time}
        data.append(formatted_show)

    return render_template('pages/shows.html', shows=data)


@app.route('/shows/create')
def create_shows():
    # renders form. do not touch.
    form = ShowForm()
    return render_template('forms/new_show.html', form=form)


@app.route('/shows/create', methods=['POST'])
def create_show_submission():
    # called to create new shows in the db, upon submitting new show listing form
    # COMPLETED: insert form data as a new Show record in the db, instead
    form = ShowForm(request.form)

    try:
        venue_id = form.venue_id.data
        artist_id = form.artist_id.data
        start_time = form.start_time.data
        print(type(start_time))

        new_show = Show(venue_id=venue_id, artist_id=artist_id, start_time=start_time)

        db.session.add(new_show)
        db.session.commit()

        # on successful db insert, flash success
        flash('Show was successfully listed!')
    except:
        print(sys.exc_info())
        db.session.rollback()
        # COMPLETED: on unsuccessful db insert, flash an error instead.
        flash('An error occurred. Show could not be listed.')
    finally:
        db.session.close()
    # e.g., flash('An error occurred. Show could not be listed.')
    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
    return render_template('pages/home.html')


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404


@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
