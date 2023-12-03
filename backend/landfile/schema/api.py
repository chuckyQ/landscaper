from functools import wraps
import inspect
from inspect import Parameter

from flask import request, abort

from landfile.schema import schema

VALIDATED_FUNCTIONS = list()


def _make_signature(fields: list):

    return inspect.Signature(
        Parameter(x, Parameter.POSITIONAL_OR_KEYWORD)
        for x in fields
        )


def _build_schema(**params):

    class BlankSchema(schema.Schema):
        pass

    setattr(BlankSchema, '_fields', list(params.keys()))
    setattr(BlankSchema, '__signature__', _make_signature(params.keys()))

    for name, descriptor in params.items():
        setattr(BlankSchema, name, descriptor)

    return BlankSchema


def validate(_arg: schema.Descriptor=None, klass: schema.Schema=None, **params):
    """This is a decorator meant for checking `request.json`
    against a defined schema. If it succeeds, then the dispatch
    function executes. If not, a 401 error code is returned.

    >>> @app.route('/myroute') #doctest: +SKIP
    ... @validate(
    ...     name = schema.String(),
    ...     description = schema.String()
    ... )
    ... def upload():
    ...     pass

    A developer can also define a schema by creating a class
    that inherits from `schema.Schema` and defining the schema
    at the class level. For example:

        class Assignment(schema.Schema):

            name = schema.String(minsize=1, maxsize=50, regex=r'.*\S.*')
            description = schema.String(minsize=0, maxsize=150)

    Then to use this class as a validation mechanism, pass it to the `klass`
    argument of the `validate` decorator.

    >>> @app.route('/myroute') #doctest: +SKIP
    ... @validate(klass=Assignment)
    ... def upload():
    ...     pass


    It is also possible to validate without having a dict-like object
    (a list of strings for example).

    >>> @app.route('/myroute') #doctest: +SKIP
    ... @validate(schema.Array(type=String, minsize=5, maxsize=10))
    ... def upload():
    ...     pass
    """

    if [_arg is not None, klass is not None, len(params) > 0].count(True) != 1:
        raise ValueError('One of "arg", "klass", and **params must be passed.')


    if _arg is not None:

        def wrapper(func):
            """Validate the positional-only """

            VALIDATED_FUNCTIONS.append(
                (func.__qualname__, inspect.getfile(func),  _arg)
                )

            @wraps(func)
            def decorator(*_args, **kwargs):
                """
                Validate the argument of the request json against a schema with
                no keys in it (a list for example).
                """

                if not _arg.validate(request.json):
                    abort(401)

                return func(*_args, **kwargs)

            return decorator

        return wrapper


    if klass is None:
        klass = _build_schema(**params)


    def wrapper(func):

        VALIDATED_FUNCTIONS.append(
            (func.__qualname__, inspect.getfile(func), klass)
        )

        @wraps(func)
        def decorator(*args, **kwargs):

            if not klass.validate(request.json):
                abort(401)

            return func(*args, **kwargs)

        return decorator

    return wrapper
