from rest_framework import serializers
from rest_framework.utils import model_meta

class UpdateMixin(serializers.ModelSerializer):
    def get_extra_kwargs(self):
        kwargs = super().get_extra_kwargs()
        no_update_fields = getattr(self.Meta, "no_update_fields", None)
        allow_uppdate_fields = getattr(self.Meta, "allow_update_fields", None)
        
        if self.instance and no_update_fields:
            for field in no_update_fields:
                kwargs.setdefault(field, {})
                kwargs[field]["write_only"] = True
                
        if self.instance and allow_uppdate_fields:
            field_names = self._get_field_names()
            for field in field_names:
                if field not in allow_uppdate_fields:
                        kwargs.setdefault(field, {})
                        kwargs[field]["read_only"] = True
        return kwargs
    
    def _get_field_names(self):
        field_names = []
        fields = getattr(self.Meta, 'field', None)
        exclude = getattr(self.Meta, 'exclude', None)
        
        if fields:
            if isinstance(fields, list) or isinstance(fields, tuple):
                field_names = fields
            else:
                field_names = self._get_all_field_name()
                
        if exclude:
            field_names = set(self._get_all_field_name()) - set(exclude)
        
        return field_names
            
    def _get_all_field_name(self):
        model = getattr(self.Meta, 'model', None)
        info = model_meta.get_field_info(model)
        field_names = (
            [info.pk.name] +
            list(info.fields) +
            list(info.forward_relations)
        )
        return field_names