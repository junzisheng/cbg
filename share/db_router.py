from cbg_backup import settings


def route_db(app_label , def_val = 'default'):
    return settings.MAP_LOGICAL_DB_BY_APP.get(app_label , def_val)


class DB_Router(object):
    """
    A router to control all database operations on models in the
    oms application.
    """

    def db_for_read(self, model, **hints):
        """
        Attempts to read oms_local models go to oms_local_db.
        """
        return settings.MAP_LOGICAL_DB_BY_APP.get(model._meta.app_label)

    def db_for_write(self, model, **hints):
        """
        Attempts to write oms_local models go to oms_local_db.
        """
        return settings.MAP_LOGICAL_DB_BY_APP.get(model._meta.app_label)


    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if a model in the oms_local app is involved.
        """
        return None


    def allow_migrate(self, db, app_label, model=None, **hints):
        """
        Make sure the oms_local app only appears in the 'auth_db'
        database.
        """
        return None
