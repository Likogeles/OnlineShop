from flask import Flask, render_template, redirect, request, make_response, url_for
from flask_login import LoginManager, login_user

from data import db_session, products, users, loginform, registerform, addproductform


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)


@app.route('/cookie_drop', methods=['GET', 'POST'])
def cookie_drop():
    res = make_response("Вы съели печенье :-(")
    res.set_cookie("user_id", str(0), max_age=0)
    return res


@login_manager.user_loader
def load_user(user_id):
    session = db_session.create_session()
    return session.query(users.User).get(user_id)


def main():
    db_session.global_init("db/online_shop.sqlite")
    session = db_session.create_session()

    product = products.Product()
    product.seller_id = 1
    product.title = "first product"
    product.number = 15
    product.description = "description"
    product.image = "*link*"

    user1 = users.User()
    user1.name = "First user"
    user1.email = "first_user@shop.org"

    session = db_session.create_session()
    session.add(product)
    session.add(user1)
    session.commit()


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = registerform.RegisterForm()
    db_session.global_init("db/online_shop.sqlite")
    session = db_session.create_session()

    if form.validate_on_submit():
        if session.query(users.User).filter(users.User.email == form.email.data).first():
            return render_template('register.html',
                                   emailmassage="Этот email уже используется",
                                   form=form)
        if not form.password1.data == form.password2.data:
            return render_template('register.html',
                                   passwordmassage="Пароли не совпадают",
                                   form=form)
        user1 = users.User()
        user1.name = form.name.data
        user1.email = form.email.data
        user1.hashed_password = form.password1.data

        session.add(user1)
        session.commit()

        user = session.query(users.User).filter(users.User.email == form.email.data).first()
        res = make_response(redirect("/"))
        res.set_cookie("user_id", str(user.id), max_age=60 * 60)
        return res
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = loginform.LoginForm()
    db_session.global_init("db/online_shop.sqlite")
    session = db_session.create_session()
    session.commit()

    print("validate: " + str(form.validate_on_submit()))
    if form.validate_on_submit():
        user = session.query(users.User).filter(users.User.email == form.email.data).first()
        if user:
            if user.hashed_password == form.password.data:
                res = make_response(redirect("/"))
                res.set_cookie("user_id", str(user.id), max_age=60 * 60)
                return res
            return render_template('login.html',
                                   messagepass="Неправильный пароль",
                                   form=form)
        return render_template('login.html',
                               messageemail="Неправильный email",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/log_out', methods=['GET', 'POST'])
def log_out():
    res = make_response(redirect("/"))
    res.set_cookie("user_id", str(0), max_age=0)
    return res


@app.route('/add_product', methods=['GET', 'POST'])
def add_product():
    form = addproductform.AddProductForm()
    db_session.global_init("db/online_shop.sqlite")
    session = db_session.create_session()

    if form.validate_on_submit():
        if not form.number.data.isdigit():
            return render_template('addproduct.html',
                                   numbermassage="Неверно введено количество",
                                   form=form)
        if not form.price.data.isdigit():
            return render_template('addproduct.html',
                                   pricemassage="Неверно введена цена",
                                   form=form)

        product = products.Product()
        product.seller_id = request.cookies.get("user_id", 0)
        product.seller = session.query(users.User).filter(users.User.id == request.cookies.get("user_id", 0)).first().name
        product.title = form.title.data
        product.number = form.number.data
        product.price = form.price.data
        product.description = form.description.data
        product.image = "static/img/Nope.png"

        idd = session.query(products.Product)
        if idd:
            product.link = "/product_link/" + str(int(idd[-1].id) + 1)
        else:
            product.link = "1"
        session.add(product)
        session.commit()

        return redirect("/")
    username = session.query(users.User).filter(users.User.id == request.cookies.get("user_id", 0)).first().name
    return render_template('addproduct.html', title='Добавить товар', username=username, form=form)


@app.route('/product_link/<product_id>')
def product_link(product_id="product_id"):
    db_session.global_init("db/online_shop.sqlite")
    session = db_session.create_session()

    product = session.query(products.Product).filter(products.Product.id == product_id).first()

    if request.cookies.get("user_id", 0):
        username = session.query(users.User).filter(users.User.id == request.cookies.get("user_id", 0)).first().name
        return render_template('product.html', title=product.title, product=product, username=username)
    return render_template('product.html', title=product.title, product=product)


@app.route('/')
@app.route('/main_link')
def main_link():
    db_session.global_init("db/online_shop.sqlite")
    session = db_session.create_session()
    productes = session.query(products.Product)
    if request.cookies.get("user_id", 0):
        username = session.query(users.User).filter(users.User.id == request.cookies.get("user_id", 0)).first().name
        return render_template('products.html', products=productes, username=username)
    return render_template('products.html', title="АлиАкспресс", products=productes)


if __name__ == '__main__':
    # main()
    app.run(port=8080, host='127.0.0.1')
