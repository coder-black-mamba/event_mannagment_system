from django import forms
from .models import Event,Category,Participant

# phitron code provided by instructor as it is hard i copied it
class StyledFormMixin:
    default_classes = "block px-4 py-2 border border-gray-300 rounded w-full"

    def apply_styled_widgets(self):
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.TextInput):
                field.widget.attrs.update({
                    'class': self.default_classes,
                    'placeholder': f"Enter {field.label.lower()}"
                })
            elif isinstance(field.widget, forms.Textarea):
                field.widget.attrs.update({
                    'class': f"{self.default_classes} resize-none",
                    'placeholder': f"Enter {field.label.lower()}",
                    'rows': 4
                })
            elif isinstance(field.widget, forms.EmailInput):
                field.widget.attrs.update({
                    'class': f"{self.default_classes} resize-none",
                    'type': 'email',
                    'placeholder': f"Enter {field.label.lower()}",
                })
            elif isinstance(field.widget, forms.SelectDateWidget):
                field.widget.attrs.update({
                    'class': f"{self.default_classes} resize-none",
                    'type': 'date',
                    'placeholder': f"Enter {field.label.lower()}",
                })
            elif isinstance(field.widget, forms.TimeInput):
                field.widget.attrs.update({
                    'class': f"{self.default_classes} resize-none",
                    'type': 'time',
                    'placeholder': f"Enter {field.label.lower()}",
                })
            elif isinstance(field.widget, forms.SelectMultiple):
                field.widget.attrs.update({
                    'class': f"{self.default_classes}",
                })
            
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_styled_widgets()

#  name = CharField(max_length=255)
#     description = TextField()
#     image_link = CharField(max_length=255)
#     date = DateField()
#     time = TimeField()
#     location = CharField(max_length=255)
#     category = ForeignKey(Category,on_delete=DO_NOTHING)




class EventForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = Event
        fields = ['name', 'description', 'date', 'time', 'location','event_img', 'category']
        widgets = {
            'date': forms.SelectDateWidget,
            'time':forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'event_img': forms.FileInput(attrs={'class': 'px-4 py-2 border border-gray-300 rounded w-full','placeholder': 'Upload Image'}),
            'category': forms.Select(attrs={'class': StyledFormMixin.default_classes,'placeholder': 'Select Category'}),
        }


class CategoryForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name','description']


class ParticipantForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = Participant
        fields = '__all__'




    