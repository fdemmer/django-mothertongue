# -*- coding: utf-8 -*-
# import stuff we need from django
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.utils import translation

# import package specific stuff
from django.conf import settings

# class to handle translated models
class TranslatedModelBase(models.Model):
    """
    Models that extend this class will have the ability to define:
    - translation_set, e.g: 'contenttranslation_set', the many to many
      manager name for the translation models for this model.
    - translated_fields = e.g: ['content',] - the fields that may be
      translated. A match is found if a translation exists with a 'language'
      the same as the current language, e.g: 'es' and a matching name.
    """
    _translation_cache = None

    class Meta(object):
        abstract = True

    def __init__(self, *args, **kwargs):
        super(TranslatedModelBase, self).__init__(*args, **kwargs)
        self._translation_cache = {}

    @property
    def translations_query(self):
        """
        Property to quickly get the queryset for the translations.
        """
        get = lambda p: super(TranslatedModelBase, self).__getattribute__(p)
        translation_set_name = get('translation_set')
        return get(translation_set_name)

    def has_translation(self, language):
        """
        Returns True if this model has a translation in `language`.
        Always returns True if `language` is the default language (settings
        .LANGUAGE_CODE).
        """
        if language == settings.LANGUAGE_CODE:
            return True
        return self.translations_query.filter(obj_lang=language).count() > 0

    def __getattribute__(self, name):
        """
        Specialise to look for translated content, note we use super's
        __getattribute__ within this function to avoid a recursion error.
        """
        get = lambda p:super(TranslatedModelBase, self).__getattribute__(p)
        translated_fields = get('translated_fields')
        if name in translated_fields:
            try:
                translation_set = get('translation_set')
                code = translation.get_language()
                translated_manager = get(translation_set)
                translated_object = None
                try:
                    translated_object = self._translation_cache[code]
                except KeyError:
                    translated_object = translated_manager.get(obj_lang=code)
                finally:
                    self._translation_cache[code] = translated_object
                if translated_object:
                    return getattr(translated_object, name)
            except (ObjectDoesNotExist, AttributeError):
                pass
        return get(name)
