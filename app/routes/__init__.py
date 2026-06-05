from app.routes import auth, cart, history, main, payment


def register_routes(app):
    main.register(app)
    auth.register(app)
    cart.register(app)
    payment.register(app)
    history.register(app)
