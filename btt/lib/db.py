"""DB and Django ORM utilities and extensions."""

from django.contrib.contenttypes.models import ContentType, ContentTypeManager

try:
    # temporal backward compatibility layer for Django < r7216
    from django.contrib.contenttypes.models import CONTENT_TYPE_CACHE
    ContentTypeManager._cache = CONTENT_TYPE_CACHE
except ImportError:
    pass

def get_without_app(model):
    for key in ContentTypeManager._cache:
        app_name, model_name = key
        if model_name == model:
            return key
    return None


def ctm_get(self, **kwargs):
    if 'model' in kwargs:
        if 'app_label' in kwargs:
            key = (kwargs['app_label'], kwargs['model'])
        else:
            key = get_without_app(kwargs['model'])
        if key:
            try:
                return ContentTypeManager._cache[key]
            except KeyError:
                pass
        ctype = self.get_query_set().get(**kwargs)
        ContentTypeManager._cache[(ctype.app_label, ctype.model)] = ctype
        return ctype
    return self.get_query_set().get(**kwargs)


def get_ranges(keys):
    """Get less possible number of inclusive ranges of integers keys."""
    if not keys:
        return []
    keys.sort()
    ranges = []
    last_key, range_begin = keys[0], keys[0]
    for key in keys[1:]:
        if key - last_key != 1:         # new range
            ranges.append((range_begin, last_key))
            range_begin = key
            last_key = key
        else:
            last_key = key
    ranges.append((range_begin, last_key))
    return ranges


def get_ranges_sql(field, ranges):
    """Return WHERE statement for the ranges"""
    def sql(range):
        diff = range[1] - range[0]
        if diff > 1:
            return "(%s>=%d AND %s<=%d)" % (field, range[0], field, range[1])
        elif diff == 1:
            return "%s=%d OR %s=%d" % (field, range[0], field, range[1])
        else:
            return "%s=%d" % (field, range[0])
    return "(" + " OR ".join([sql(r) for r in ranges]) + ")"


def load_generic_related(object_list, related_qs, cache_field, field='object_id', ct_field='content_type'):
    if object_list:
        ct = ContentType.objects.get_for_model(object_list[0])
        return load_related(object_list, related_qs.filter(**{ct_field: ct.id}), cache_field, field)
    return object_list


def load_related(object_list, related_qs, cache_field=None, field=None):
    """
    Load related objects for a list of objects.
    Function will do only 1 SQL query instead of len(object_list) queries.

    Parameters::

        - object_list - list of objects to attach related objects.
        - related_qs - queryset (or a manager) from where to fetch related objects.
        - cache_field - name for attaching related objects, optional
                        (determined by the name of object_list model).
        - field - relation field, by which related_qs is related to object_list, optional
                  (determined by the name of related_qs model).
    """
    if not object_list:
        return object_list
    if not field:
        field = object_list[0]._meta.object_name.lower()
    field = related_qs.model._meta.get_field(field)
    if not cache_field:
        cache_field = related_qs.model.__name__.lower() + "_cache"
    pks = list(set([field.to_python(obj.pk) for obj in object_list]))
    # get related queryset
    if isinstance(pks[0], int):
        ranges = get_ranges(pks)
        related_qs = related_qs.extra(where = (get_ranges_sql(field.column, ranges),))
    else:
        related_qs = related_qs.filter(**{"%s__in" % field.name: pks})
    # generate list of related objects
    related_list = {}
    for rel_obj in related_qs:
        related_list.setdefault(getattr(rel_obj, field.attname), []).append(rel_obj)
    # append related objects to cache field
    for obj in object_list:
        setattr(obj, cache_field, related_list.get(obj.pk, []))
    return object_list


def load_content_objects(object_list, cache_field='content_object', field='object_id', ct_field='content_type', select_related=1):
    """Load content objects for a generic relation.
    Number of sql queries is equals not to number of objects but number of unique
    content types. For example we have article and project models that can be tagged and we
    want to load all objects tagged with a tag, then we always will spent 2 SQL queries
    instead of number of tagged objects SQL queries.
    """
    if not object_list:
        return object_list
    field = object_list[0]._meta.get_field(field)
    ct_field = object_list[0]._meta.get_field(ct_field)
    ctypes = {}
    for obj in object_list:         # group objects by ctype
        ct_id = getattr(obj, ct_field.column)
        try:
            ctypes[ct_id].append(obj)
        except KeyError:
            ctypes[ct_id] = [obj]
    for ct_id, objects in ctypes.items(): # fetch each ctype by 1 SQL query
        ctype = ContentType.objects.get_for_id(ct_id)
        model = ctype.model_class()
        pk_field = model._meta.pk
        pk_object_map = {}
        for obj in objects:
            pk_value = pk_field.to_python(getattr(obj, field.column))
            try:
                pk_object_map[pk_value].append(obj)
            except KeyError:
                pk_object_map[pk_value] = [obj]
        keys = pk_object_map.keys()
        qs = model.objects.filter(pk__in=keys)
        if select_related:
            qs = qs.select_related(depth=select_related)
        for model_obj in qs:
            for obj in pk_object_map[model_obj.pk]:
                setattr(obj, cache_field, model_obj)
    return object_list
