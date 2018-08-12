import common.config

# Get the application instance
connex_app = common.config.connex_app

# Read the swagger.yml file to configure the endpoints
connex_app.add_api('swagger.yml', arguments={'title': 'User API'})

if __name__ == '__main__':
    connex_app.run(debug=True)