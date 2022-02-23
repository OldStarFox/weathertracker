import logging
from logging.handlers import QueueHandler, QueueListener
from multiprocessing import Manager
import sys


def console_logger_init(logLevel,cFilter=None):
	"""
	Initialize log handlers and queues for multiprocessing

	Args:
		logLevel - String: String with the desired log level INFO,DEBUG,WARNING,etc\n
		cFilter - Function: Filter method used to filter messages to be logged. Usefull when messages from sub-modules are getting logged\n
		
	Returns:
		logging.handlers.QueueListener, multiprocessing.Manager.Queue
	"""
	m = Manager()
	q = m.Queue()
	# this is the handler for all log records
	handler = logging.StreamHandler(sys.stdout)
	handler.setFormatter(logging.Formatter("{asctime}.{msecs:09.5f} - [{levelname:^8}] - [LN:{lineno:04d}] - [PID:{process:05d}] - [{name:^20}] - {message}",datefmt='%Y-%m-%d-%H:%M:%S',style='{'))

	if cFilter:
		handler.addFilter(cFilter)

	# ql gets records from the queue and sends them to the handler
	ql = QueueListener(q, handler)
	ql.start()

	if logLevel == 'DEBUG':
		logLevel = logging.DEBUG
	elif logLevel == 'INFO':
		logLevel = logging.INFO
	elif logLevel == 'WARNING':
		logLevel = logging.WARNING
	elif logLevel == 'ERROR':
		logLevel = logging.ERROR
	elif logLevel == 'CRITICAL':
		logLevel = logging.CRITICAL
	else:
		logLevel = 0

	logger = logging.getLogger()
	logger.setLevel(logLevel)
	# add the handler to the logger so records from this process are handled
	logger.addHandler(handler)

	return ql, q

def worker_init(q,logLevel):
	# all records from worker processes go to qh and then into q
	qh = QueueHandler(q)
	logger = logging.getLogger()
	logger.setLevel(logLevel)
	logger.addHandler(qh)