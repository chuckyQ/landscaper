""""
This module implements the JSON validation strategy for the various
routes. To validate the json data, the `@validate` decorator is
added to all of the POST routes with a defined schema (passed
as keyword arguments or a developer-defined class). For example:

    @app.route('/myroute')
    @validate(
        name = schema.String(),
        date = schema.String(regex='\d{4}-\d{2}-\d{2})
    )
    def myroute():
        ...
"""
