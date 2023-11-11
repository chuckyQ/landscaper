from .account import account
from .customers import customers
from .crew import crew
from .crews import crews
from .job import job
from .jobs import jobs
from .public import public
from .user import user
from .users import users

BLUEPRINTS = [
    account,
    crew,
    crews,
    customers,
    job,
    jobs,
    public,
    user,
    users,
]
