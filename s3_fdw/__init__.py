import logging
import multicorn.utils
from multicorn import ForeignDataWrapper

__version__ = '0.1.0'


class S3ForeignDataWrapper(ForeignDataWrapper):
    def __init__(self, options, columns):
        super().__init__(options, columns)
        try:
            self.object_name = options['object_name']
        except KeyError:
            multicorn.utils.log_to_postgres('object_name required', logging.ERROR)
