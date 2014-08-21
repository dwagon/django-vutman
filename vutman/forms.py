from django.forms import ModelForm
from vutman.models import EmailUser, EmailAlias
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout


class CrispyForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(CrispyForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-exampleForm'
        self.helper.form_class = 'blueForms'
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Submit'))


class EmailUserForm(CrispyForm):
    class Meta:
        model = EmailUser

from django.forms.models import inlineformset_factory

EmailAliasFormSet = inlineformset_factory(
    EmailUser, EmailAlias, fk_name="username",
    extra=2, can_delete=True
)

class EmailAliasForm(ModelForm):
    class Meta:
        model = EmailAlias
