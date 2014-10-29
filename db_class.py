from google.appengine.ext import db

class BaseClass(db.Model):
  name = db.StringProperty()

class DerivedClass(BaseClass):
  version = db.StringProperty()