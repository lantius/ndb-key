from google.appengine.ext import ndb
from google.appengine.ext.ndb import polymodel

class BaseClass(polymodel.PolyModel):
  name = ndb.StringProperty()

class DerivedClass(BaseClass):
  version = ndb.StringProperty()