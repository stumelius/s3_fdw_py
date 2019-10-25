import logging
import boto3
import multicorn.utils
import csv
from typing import List
from multicorn import ForeignDataWrapper
from io import BytesIO, StringIO

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
        self.endpoint_url = self._parse_optional_option(
            key='endpoint_url', options=options
        )
        self.columns = columns

    @classmethod
    def _parse_required_option(cls, key: str, options: List[str]):
        try:
            return options[key]
        except KeyError:
            multicorn.utils.log_to_postgres(
                '{key} required'.format(key=key), logging.ERROR
            )

    @classmethod
    def _parse_optional_option(cls, key: str, options: dict):
        try:
            return options[key]
        except KeyError:
            return None

    def execute(self, quals, columns):
        s3 = boto3.resource(
            's3',
            endpoint_url=self.endpoint_url,
            aws_access_key_id=self.access_key,
            aws_secret_access_key=self.secret_key,
        )
        s3_bucket = s3.Bucket(name=self.bucket_name)
        # TODO: Raise error if object not found
        s3_object = s3_bucket.Object(key=self.object_name)

        byte_stream = BytesIO()
        s3_object.download_fileobj(byte_stream)
        byte_stream.seek(0)
        stream = StringIO(byte_stream.read().decode())
        for i, row in enumerate(csv.reader(stream)):
            if i == 0:
                header = row
            else:
                row_dict = {key: value for key, value in zip(header, row)}
                yield [row_dict[col] for col in self.columns]
