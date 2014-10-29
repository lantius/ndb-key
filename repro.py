import webapp2

from google.appengine.ext import db  
from google.appengine.ext import ndb

from db_class import DerivedClass as OldDerivedClass
from ndb_class import BaseClass as NewBaseClass
from ndb_class import DerivedClass as NewDerivedClass


class Repro(webapp2.RequestHandler):
  def get(self):
    self.response.headers['Content-Type'] = 'text/plain'

    # Create a derived object using google.appengine.ext.db
    obj = OldDerivedClass(name='foo', version='bar')
    db_key = obj.put()
    self.response.write('%s, %d\n' % (db_key.kind(), db_key.id()))

    # Attempt to load using the converted key
    ndb_key = ndb.Key.from_old_key(db_key)
    try:
      ndb_key.get()
    except ndb.KindError:
      self.response.write('failed (KindError): %s\n' % str(ndb_key))

    # Attempt to create a new key using the ndb derived class
    derived_key = ndb.Key(NewDerivedClass, ndb_key.id())
    obj = derived_key.get()
    if not obj:
      self.response.write('failed (None): %s\n' % str(derived_key))

    # Attempt to create a new key using the ndb base class
    base_key = ndb.Key(NewBaseClass, ndb_key.id())
    obj = derived_key.get()
    if not obj:
      self.response.write('failed (None): %s\n' % str(base_key))

    # Manually create a new key using the ndb derived class name
    force_key = ndb.Key('DerivedClass', ndb_key.id())
    try:
      force_key.get()
    except ndb.KindError:
      self.response.write('failed (KindError): %s\n' % str(force_key))

application = webapp2.WSGIApplication([('/', Repro)], debug=True)
