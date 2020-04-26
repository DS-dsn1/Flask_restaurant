from flask import render_template, request, flash, redirect, url_for, abort
from models import Chef, Dish, Customer, restaurant, db


@restaurant.route('/')
def index():
    return render_template('index.html')


@restaurant.route('/chefs')
def show_chef():
    chefs = Chef.query.all()
    return render_template('chefs.html', chefs=chefs)


@restaurant.route('/dish')
def show_dish():
    all_dishes = Dish.query.all()
    return render_template('dish.html', all_dishes=all_dishes)


@restaurant.route('/customer')
def show_customer():
    customers = Customer.query.all()
    return render_template('customer.html', customers=customers)


@restaurant.route('/dish/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        name = request.form['name']
        recipe = request.form['recipe']
        ingredients = request.form['ingredients']
        cost = request.form['cost']
        error = None

        if not name:
            error = 'Name is required.'

        if not cost:
            error = 'Cost is required.'

        if error is not None:
            flash(error)
        else:
            db.session.add(Dish(name, recipe, ingredients, cost))
            db.session.commit()
            return redirect(url_for('show_dish'))
    return render_template('create.html')


def get_dish(id):
    dish = Dish.query.get(id)

    if dish is None:
        abort(404, f"Dish id {id} doesn't exist.")

    return dish


@restaurant.route('/dish/<int:id>/update', methods=('POST', 'GET'))
def update(id):
    dish = get_dish(id)

    if request.method == 'POST':
        name = request.form['name']
        recipe = request.form['recipe']
        ingredients = request.form['ingredients']
        cost = request.form['cost']
        error = None

        if not name:
            error = 'Name is required.'

        if not cost:
            error = 'Cost is required.'

        if error is not None:
            flash(error)
        else:
            dish.name = name
            dish.recipe = recipe
            dish.ingredients = ingredients
            dish.cost = cost
            db.session.commit()
            return redirect(url_for('show_dish'))
    return render_template('update.html', dish=dish)


@restaurant.route('/dish/<int:id>/delete', methods=('POST',))
def delete(id):
    dish = get_dish(id)

    db.session.delete(dish)
    db.session.commit()
    return redirect(url_for('show_dish'))


if __name__ == '__main__':
    restaurant.run()
