from django.forms import ModelForm
from vutman.models import EmailUser, EmailAlias
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from django.forms.models import inlineformset_factory


class CrispyForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(CrispyForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = "id-exampleForm"
        self.helper.form_class = "blueForms"
        self.helper.form_method = "post"
        self.helper.add_input(Submit("submit", "Submit"))


class EmailUserForm(CrispyForm):
    class Meta:
        model = EmailUser
        exclude = []


EmailAliasFormSet = inlineformset_factory(
    EmailUser, EmailAlias, fk_name="username", extra=1, can_delete=True, exclude=[]
)


class EmailAliasForm(CrispyForm):
    class Meta:
        model = EmailAlias
        exclude = []
