# ISO 8601 or GTFO

SHORT_DATE_FORMAT = 'Y-n-j'             # '2009-1-20'
SHORT_DATETIME_FORMAT = 'Y-n-j H:i'     # '2009-1-20 15:23'

DATE_INPUT_FORMATS = [
	'%Y-%m-%d',                         # '2009-1-20'
	'%d-%m-%Y'                          # '20-01-2009'
]
TIME_INPUT_FORMATS = [
	'%H:%M:%S',                         # '15:23:35'
	'%H:%M:%S.%f',                      # '15:23:35.000200'
	'%H:%M'                             # '15:23'
]
DATETIME_INPUT_FORMATS = [
	'%Y-%m-%d %H:%M:%S',                # '2006-10-25 14:30:59'
	'%Y-%m-%d %H:%M:%S.%f',             # '2006-10-25 14:30:59.000200'
	'%Y-%m-%d %H:%M',                   # '2006-10-25 14:30'
	'%Y-%m-%d'                          # '2006-10-25'
]

THOUSAND_SEPARATOR = ' '
