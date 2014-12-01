'''
Created on Oct 15, 2014

@author: ejiahug
'''
import django.dispatch
from django.utils.encoding import force_text, smart_text
from datetime import datetime, timedelta
import logging

TMP_MINICACHE_SECONDS = 5

class SettingSet(list):
    def __init__(self, name, title, description, weight=1000, markdown=False, can_preview=False):
        self.name = name
        self.title = title
        self.description = description
        self.weight = weight
        self.markdown = markdown
        self.can_preview = can_preview


class BaseSetting(object):
    @classmethod
    def add_to_class(cls, name):
        def wrapper(self, *args, **kwargs):
            return self.value.__getattribute__(name)(*args, **kwargs)

        setattr(cls, name, wrapper)

    def __init__(self, name, default, set=None, field_context=None):
        self.name = name
        self.default = default
        self.field_context = field_context or {}

        self._temp = None

        if set is not None:
            self.set = set
            
            if not set.name in Setting.sets:
                Setting.sets[set.name] = set

            Setting.sets[set.name].append(self)

    def __str__(self):
        return str(self.value)

    def __unicode__(self):
        return smart_text(self.value)

    @property
    def value(self):
        if self._temp:
            v, exp = self._temp
            if exp + timedelta(seconds=TMP_MINICACHE_SECONDS) > datetime.now():
                return v
        
        from questions.models.utils import KeyValue

        """
        Try to get the value of the key (i.e. the specific setting) from the KeyValue database.
        If key is not in database, it is a new key so save it in the database with default value.
        """
        try:
            kv = KeyValue.objects.get(key=self.name)
            v = kv.value
            self._temp = (v, datetime.now() + timedelta(seconds=TMP_MINICACHE_SECONDS))
            return v
        except KeyValue.DoesNotExist:
            self._temp = (self.default, datetime.now() + timedelta(seconds=TMP_MINICACHE_SECONDS))
            self.save(self.default)
        except Exception as e:
            logging.error("Error retrieving setting from database (%s): %s" % (self.name, str(e)))
            
        return self.default

    def set_value(self, new_value):
        new_value = self._parse(new_value)
        self._temp = None
        self.save(new_value)

    def save(self, value):

        from questions.models.utils import KeyValue

        try:
            kv = KeyValue.objects.get(key=self.name)
        except KeyValue.DoesNotExist:
            kv = KeyValue(key=self.name)
        except Exception as e:
            logging.error("Error saving setting to database (%s): %s" % (self.name, str(e)))
            return

        kv.value = value
        kv.save()

    def to_default(self):
        self.set_value(self.default)

    def _parse(self, value):
        if not isinstance(value, self.base_type):
            try:
                return self.base_type(value)
            except:
                pass
        return value

class AnyTypeSetting(BaseSetting):
     def _parse(self, value):
        return value


class Setting(object):
    emulators = {} # This is the sets for different classes for different settings
    sets = {} # sets for different settings, e.g. view_set, basic_set etc.

    def __new__(cls, name, default, set=None, field_context=None):
        if default is None:
            return AnyTypeSetting(name, default, set, field_context)
            
        deftype = type(default)

        if deftype in Setting.emulators:
            emul = Setting.emulators[deftype]
        else:
            """
            emul is the class inherited from BaseSetting with different type which is from the default value.
            For example, if default type is bool, emul is the new class named 'boolsetting', with a member
            named 'base_type'.
            """
            emul = type(deftype.__name__ + cls.__name__, (BaseSetting,), {'base_type': deftype})

            """
            fns is actually the list of callable functions in class of deftype while not in class Setting.
            """
            fns = [n for n, f in [(p, getattr(deftype, p)) for p in dir(deftype) if not p in dir(cls)] if callable(f)]

            for n in fns:
               emul.add_to_class(n)

            Setting.emulators[deftype] = emul

        """
        Finally return a new object from the class decided by the type of the default value.
        """
        return emul(name, default, set, field_context)
