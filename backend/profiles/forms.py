from django import forms
from .models import User


class DocumentUploadForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["identity_card_image", "bank_statement_image", "iban", "personal_uid"]
        labels = {
            "iban": "IBAN",
            "personal_uid": "National Identifier",
        }

    def clean(self):
        cleaned_data = super().clean()
        identity_card_image = cleaned_data.get("identity_card_image")
        bank_statement_image = cleaned_data.get("bank_statement_image")
        iban = cleaned_data.get("iban")
        personal_uid = cleaned_data.get("personal_uid")

        # if not identity_card_image:
        #     self.add_error('identity_card_image', 'This field is required.')
        # if not bank_statement_image:
        #     self.add_error('bank_statement_image', 'This field is required.')
        if not iban:
            self.add_error("iban", "This field is required.")
        if not personal_uid:
            self.add_error("personal_uid", "This field is required.")

        return cleaned_data
