"""
Flask Documentation:     https://flask.palletsprojects.com/
Jinja2 Documentation:    https://jinja.palletsprojects.com/
Werkzeug Documentation:  https://werkzeug.palletsprojects.com/
This file contains the routes for your application.
"""
import os
from app import app, db;
from flask import render_template, request, redirect, url_for, flash, session
#from .forms import PropertyForm
from app.models import propertysite
from werkzeug.utils import secure_filename
from flask import send_from_directory


###
# Routing for your application.
###

@app.route('/')
def home():
    """Render website's home page."""
    return render_template('home.html')


@app.route('/about/')
def about():
    """Render the website's about page."""
    return render_template('about.html', name="Montacher Pierre")


@app.route('/properties/create', methods=['GET', 'POST'])
def form():
    form = PropertyForm()

    if request.method == 'POST':
        try:
            if form.validate_on_submit():
                Title = form.Title.data
                Description = form.Description.data
                No_Room = form.No_Room.data
                No_Bathrooms = form.No_Bathrooms.data
                Location = form.Location.data
                Price = form.Price.data
                Property_Type = form.Property_Type.data
                photo_file = form.photo.data
                filename = secure_filename(photo_file.filename)
                photo_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

                # Create new property object and add to database
                new_prop = propertysite(Title=Title, Description=Description, No_Room=No_Room, No_Bathrooms=No_Bathrooms, Location=Location, Price=Price, Property_Type=Property_Type, Photo=filename)
                db.session.add(new_prop)
                db.session.commit()

                flash('Property added successfully', 'success')
                return redirect(url_for('properties'))
            else:
                flash_errors(form)
        except Exception as e:
            flash({'An error occurred' : str(e)}, 400)    
    return render_template('newproperty.html',form=form)


@app.route('/properties', methods= ['GET'])
def properties():
    #try:
        return render_template('properties.html', properties=propertysite.query.all())

    #except Exception as e:
         #flash({'An error occurred' : str(e)}, 400)


@app.route('/properties/<propertyid>')
def property(propertyid):

    try:
         property = propertysite.query.filter_by(propertyid).first()
         return render_template('property.html', property=property)
    
    except Exception as e:
         flash({'An error occurred' : str(e)}, 400)


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(os.path.join(os.getcwd(), app.config['UPLOAD_FOLDER']), filename)
###
# The functions below should be applicable to all Flask apps.
###

def get_uploaded_images():
    rootdir =os.getcwd()
    file_lst=[]
    # print("root directry:",rootdir)
    for subdir, dirs, files in os.walk(rootdir + 'uploads/'):
        for file in files:
            file_lst.append(os.path.join(subdir, file))
    return file_lst


# Display Flask WTF errors as Flash messages
def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ), 'danger')

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also tell the browser not to cache the rendered page. If we wanted
    to we could change max-age to 600 seconds which would be 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404
