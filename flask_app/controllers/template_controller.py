from pprint import pprint
from flask_app import app, render_template, redirect, request, session
from flask_app.models.thing_model import Thing

# display all things
@app.get('/things')
def all_things():
    things = Thing.find_all()
    print(f'**** FOUND - ALL THINGS: ****')
    pprint(things)
    return render_template('all_things.html', things = things)

# display one thing by id
@app.get('/things/<int:thing_id>')
def one_thing(thing_id):
    data = {
        'id': thing_id
    }
    thing = Thing.find_by_id(data)
    print(f'**** FOUND - THING ID: {thing.id} ****')
    return render_template('one_thing.html', thing = thing)

# display form to create a thing
@app.get('/things/new')
def new_thing():
    return render_template('new_thing.html')

# process form and create a thing
@app.post('/things')
def create_thing():
    thing_id = Thing.save(request.form)
    print(f'**** CREATED - THING ID: {thing_id} ****')
    return redirect('/things')

# display form to edit a thing by id
@app.get('/things/<int:thing_id>/edit')
def edit_thing(thing_id):
    data = {
        'id': thing_id
    }
    thing = Thing.find_by_id(data)
    print(f'**** FOUND - THING ID: {thing.id} ****')
    return render_template('edit_thing.html', thing = thing)

# process form and update a thing by id
@app.post('/things/<int:thing_id>/update')
def update_thing(thing_id):
    Thing.find_by_id_and_update(request.form)
    print(f'**** UPDATED - THING ID: {thing_id} ****')
    return redirect(f'/things/{thing_id}')

# delete one thing by id
@app.get('/things/<int:thing_id>/delete')
def delete_thing(thing_id):
    data = {
        'id': thing_id
    }
    Thing.find_by_id_and_delete(data)
    print(f'**** DELETED - THING ID: {thing_id} ****')
    return redirect('/things')
