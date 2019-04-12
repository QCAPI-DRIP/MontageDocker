from mArchiveList import mArchiveList
import clam.clamservice
application = clam.clamservice.run_wsgi(mArchiveList)