import os

ENV = os.environ.get('ENV', 'local').lower()

if ENV == 'prod':
    from .prod import *
elif ENV == 'dev':
    from .dev import *
elif ENV == 'local':
    from .local import *
else:
    raise Exception(f"Invalid environment: {ENV}")
