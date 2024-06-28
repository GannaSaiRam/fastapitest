import boto3
import json


def parse_get_params():
	config = boto3.client('ssm', region_name='us-west-2')
	response = config.get_parameter(
		Name='arn:aws:ssm:us-west-2:884690463752:parameter/config/batch-logging/config_stg',
		WithDecryption=True | False
	)
	return json.loads(response["Parameter"]["Value"])


ssm_value = parse_get_params()
# PostgresDB
DB_NAME = ssm_value['DB_NAME']
DB_USERNAME = ssm_value['DB_USERNAME']
DB_PASSWORD = ssm_value['DB_PASSWORD']
DB_SERVER = ssm_value['DB_SERVER']
DATABASE_URL = f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_SERVER}:5432/{DB_NAME}"
DATABASE_URL_ASYNC = f"postgresql+asyncpg://{DB_USERNAME}:{DB_PASSWORD}@{DB_SERVER}:5432/{DB_NAME}"
PORT = 8001
# Redis DB
REDIS_HOST = ssm_value.get('REDIS_SERVER') or 'localhost'
REDIS_PORT = ssm_value.get('REDIS_PORT') or '26379'
PREFIX = "iw_batch_logging"

FILTER_API_PAGE_LIMIT = 1000

# noinspection SpellCheckingInspection
TABLE_NAMES = {
	"SCHEMAS": 4 * ["application"],
	"TABLES": ["batch_group", "batch_job", "batch_job_events", "batch_job_event_details",],
	"SEQUENCES": ["iwlogseq_group", "iwlogseq_job", "iwlogseq_event", "iwlogseq_event_detail"]
}

logging_config = {
	"version": 1,
	"disable_existing_loggers": False,
	"formatters": {
		"default": {
			"()": "uvicorn.logging.DefaultFormatter",
			"fmt": "%(levelprefix)s %(message)s",
			"use_colors": None,
		},
	},
	"handlers": {
		"default": {
			"formatter": "default",
			"class": "logging.StreamHandler",
			"stream": "ext://sys.stdout",
		},
	},
	"loggers": {
		"uvicorn": {
			"handlers": ["default"],
			"level": "WARNING",  # Change this to WARNING to suppress INFO logs
		},
		"uvicorn.error": {
			"level": "ERROR",
			"handlers": ["default"],
			"propagate": False,
		},
		"uvicorn.access": {
			"level": "WARNING",
			"handlers": ["default"],
			"propagate": False,
		},
		"sqlalchemy": {
			"level": "WARNING",
			"handlers": ["default"],
			"propagate": False,
		},
		"crud_base": {
			"level": "WARNING",
			"handlers": ["default"],
			"propagate": False,
		},
	},
}
