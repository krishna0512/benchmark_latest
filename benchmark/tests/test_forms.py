import datetime

from django.test import TestCase

from benchmark.forms import UserRegistrationForm

class UserRegistrationFormTest(TestCase):
    def setUp(self):
        self.form = UserRegistrationForm()
        self.data = {
                'username':'krishna',
                'email':'kt.krishna.tulsyan@gmail.com',
                'password':'kkrishna',
                'confirm_password':'kkrishna',
                'first_name':'Krishna',
                'last_name':'Tulsyan',
                'affiliation_name':'IIIT Hyderabad',
                'dob':datetime.date.today()
                }
                

    def test_number_of_fields(self):
        self.assertEqual(len(self.form.fields), 8)

    def test_username_required(self):
        self.assertTrue(self.form.fields['username'].required)
    def test_username_max_length(self):
        self.assertEqual(self.form.fields['username'].max_length, 32)

    def test_email_required(self):
        self.assertTrue(self.form.fields['email'].required)
    def test_email_max_length(self):
        self.assertEqual(self.form.fields['email'].max_length, 32)

    def test_password_required(self):
        self.assertTrue(self.form.fields['password'].required)
    def test_password_max_length(self):
        self.assertEqual(self.form.fields['password'].max_length, 32)

    def test_confirm_password_required(self):
        self.assertTrue(self.form.fields['confirm_password'].required)
    def test_confirm_password_max_length(self):
        self.assertEqual(self.form.fields['confirm_password'].max_length, 32)

    def test_first_name_required(self):
        self.assertTrue(self.form.fields['first_name'].required)
    def test_first_name_max_length(self):
        self.assertEqual(self.form.fields['first_name'].max_length, 32)

    def test_last_name_required(self):
        self.assertTrue(self.form.fields['last_name'].required)
    def test_last_name_max_length(self):
        self.assertEqual(self.form.fields['last_name'].max_length, 32)

    def test_affiliation_name_required(self):
        self.assertFalse(self.form.fields['affiliation_name'].required)
    def test_affiliation_name_max_length(self):
        self.assertEqual(self.form.fields['affiliation_name'].max_length, 64)

    def test_dob_required(self):
        self.assertFalse(self.form.fields['dob'].required)
    def test_dob_label(self):
        self.assertEqual(self.form.fields['dob'].label, 'Birth date (dd/mm/YYYY)')
