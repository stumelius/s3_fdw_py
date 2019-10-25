import logging
import multicorn.utils
from multicorn import ForeignDataWrapper

__version__ = '0.1.0'


class S3ForeignDataWrapper(ForeignDataWrapper):
    def __init__(self, options: dict, columns: dict):
        super().__init__(options, columns)
        self.object_name = self._parse_required_option(
            key='object_name', options=options
        )
        self.bucket_name = self._parse_required_option(
            key='bucket_name', options=options
        )
        self.access_key = self._parse_required_option(key='access_key', options=options)
        self.secret_key = self._parse_required_option(key='secret_key', options=options)

    @classmethod
    def _parse_required_option(cls, key: str, options: dict):
        try:
            return options[key]
        except KeyError:
            multicorn.utils.log_to_postgres(
                '{key} required'.format(key=key), logging.ERROR
            )
