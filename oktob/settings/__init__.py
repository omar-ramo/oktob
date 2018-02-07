try:
	from .developement import *
except:	#in production you can remove developement.py or change this.
	from .production import *