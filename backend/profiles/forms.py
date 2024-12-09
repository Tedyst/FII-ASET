from django import forms
from .models import User
import uuid
import os


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

    def rename_file(self, filename):
        ext = filename.split(".")[-1]
        new_filename = f"{uuid.uuid4()}.{ext}"
        return new_filename

    def delete_old_file(self, file_path):
        """Delete old file from file system."""
        print("Deleting old file:", file_path)
        if os.path.exists(file_path) and os.path.isfile(file_path):
            os.remove(file_path)
        else:
            print("File not found:", file_path)

    def save(self, commit=True):
        user = super().save(commit=False)
        # Delete old files
        # old_identity_card_image = user.identity_card_image.path
        # old_bank_statement_image = user.bank_statement_image.path
        # self.delete_old_file(old_identity_card_image)
        # self.delete_old_file(old_bank_statement_image)
        # Rename files
        user.identity_card_image.name = self.rename_file(user.identity_card_image.name)
        user.bank_statement_image.name = self.rename_file(
            user.bank_statement_image.name
        )
        if commit:
            user.save()
        return user
