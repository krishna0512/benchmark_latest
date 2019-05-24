from django.test import TestCase
from django.contrib.auth.models import User
import django.db.models.fields as models
import datetime

from benchmark.models import Resource, Dataset, Document, Language, Modality, Task, TaskCategory

class ProfileModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create(username='krishna',password='kkrishna', email='krishna@gmail.com')

    def setUp(self):
        self.profile = User.objects.get(id=1).profile

    def test_affiliation_name_max_length(self):
        max_length = self.profile._meta.get_field('affiliation_name').max_length
        self.assertEqual(max_length, 100)

    def test_affiliation_name_default_value(self):
        self.assertEqual(self.profile.affiliation_name, '')

    def test_dob_default_value(self):
        self.assertIsInstance(self.profile.dob, datetime.date)
        self.assertEqual(self.profile.dob, datetime.date.today())

    def test_save_user_profile_function(self):
        """Tests weather the changes in profile of a user
        is updated automatically when a user is saved
        using post_save django signals
        """
        u = User.objects.get(id=1)
        u.profile.affiliation_name = 'IIITH'
        u.save()
        self.assertEqual(User.objects.get(id=1).profile.affiliation_name, 'IIITH')


class ResourceModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Resource.objects.create(title='Test Resource')

    def setUp(self):
        self.resource = Resource.objects.get(id=1)

    def test_title_value(self):
        self.assertEqual(self.resource.title, 'Test Resource')

    def test_title_max_length(self):
        max_length = self.resource._meta.get_field('title').max_length
        self.assertEqual(max_length, 200)

    def test_authors_max_length(self):
        max_length = self.resource._meta.get_field('authors').max_length
        self.assertEqual(max_length, 400)

    def test_authors_default_value(self):
        self.assertEqual(self.resource.authors, 'N/A')

    def test_year_default_value(self):
        self.assertEqual(self.resource.year, 0)

    def test_year_instance(self):
        self.assertIsInstance(self.resource._meta.get_field('year'), models.PositiveSmallIntegerField)

    def test_year_min_value(self):
        """TODO: check if the validators contain minvaluevalidators(1900)
        """
        pass

    def test_year_max_value(self):
        """TODO: check if the validators contain maxvaluevalidators(2100)
        """
        pass

    def test_page_link_max_length(self):
        max_length = self.resource._meta.get_field('page_link').max_length
        self.assertEqual(max_length, 200)

    def test_page_link_default_value(self):
        self.assertEqual(self.resource.page_link, '')

    def test_page_link_only_accept_urls(self):
        self.assertIsInstance(self.resource._meta.get_field('page_link'), models.URLField)

    def test_pdf_link_max_length(self):
        max_length = self.resource._meta.get_field('pdf_link').max_length
        self.assertEqual(max_length, 200)

    def test_pdf_link_default_value(self):
        self.assertEqual(self.resource.pdf_link, '')

    def test_pdf_link_only_accept_urls(self):
        self.assertIsInstance(self.resource._meta.get_field('pdf_link'), models.URLField)

    def test__repr__function(self):
        self.assertEqual(self.resource.__repr__(), '<Resource: Test Resource>')
        self.resource.year = 2010
        self.assertEqual(self.resource.__repr__(), '<Resource: Test Resource (2010)>')

    def test__str__function(self):
        self.assertEqual(str(self.resource), self.resource.title)


class DocumentModelTest(TestCase):

    def _test_max_length(self, field_name, value):
        max_length = self.document._meta.get_field(field_name).max_length
        self.assertEqual(max_length, value)

    @classmethod
    def setUpTestData(cls):
        Document.objects.create(name='Printed')
        Modality.objects.create(name='mc', document=Document.objects.get(id=1))
        Modality.objects.create(name='ma', document=Document.objects.get(id=1))
        Modality.objects.create(name='mb', document=Document.objects.get(id=1))

    def setUp(self):
        self.document = Document.objects.get(id=1)

    def test_name_value(self):
        self.assertEqual(self.document.name, 'Printed')

    def test_name_max_length(self):
        self._test_max_length('name', 200)

    def test_description_max_length(self):
        self._test_max_length('description', 400)

    def test_description_default_value(self):
        self.assertEqual(self.document.description, '')

    def test_description_instance(self):
        self.assertIsInstance(self.document._meta.get_field('description'), models.TextField)

    def test__str__method(self):
        self.assertEqual(self.document.__str__(), self.document.name)

    def test__repr__method(self):
        self.assertEqual(self.document.__repr__(), '<Document: Printed>')

    def test_modality_set(self):
        self.assertEqual(self.document.modality.all().count(), Modality.objects.all().count())
        for i in range(Modality.objects.all().count()):
            self.assertTrue(self.document.modality.filter(id=Modality.objects.all()[0].id).distinct().exists())


class LanguageModelTest(TestCase):

    def _test_max_length(self, field_name, value):
        max_length = self.language._meta.get_field(field_name).max_length
        self.assertEqual(max_length, value)

    @classmethod
    def setUpTestData(cls):
        Language.objects.create(name='Hindi')

    def setUp(self):
        self.language = Language.objects.get(id=1)

    def test_name_value(self):
        self.assertEqual(self.language.name, 'Hindi')

    def test_name_max_length(self):
        self._test_max_length('name', 50)

    def test_description_max_length(self):
        self._test_max_length('description', 400)

    def test_description_default_value(self):
        self.assertEqual(self.language.description, '')

    def test__repr__method(self):
        self.assertEqual(self.language.__repr__(), '<Language: Hindi>')

    def test__str__method(self):
        self.assertEqual(self.language.__str__(), self.language.name)


class ModalityModelTest(TestCase):

    def _test_max_length(self, field_name, value):
        max_length = self.modality._meta.get_field(field_name).max_length
        self.assertEqual(max_length, value)

    @classmethod
    def setUpTestData(cls):
        Document.objects.create(name='Test Document')
        Modality.objects.create(name='Test Modality', document=Document.objects.get(id=1))

    def setUp(self):
        self.modality = Modality.objects.get(id=1)

    def test_name_value(self):
        self.assertEqual(self.modality.name, 'Test Modality')

    def test_document_value(self):
        self.assertEqual(self.modality.document, Document.objects.get(id=1))

    def test_name_max_length(self):
        self._test_max_length('name', 200)

    def test_description_max_length(self):
        self._test_max_length('description', 400)

    def test_description_default_value(self):
        self.assertEqual(self.modality.description, '')

    def test_description_instance(self):
        self.assertIsInstance(self.modality._meta.get_field('description'), models.TextField)

    def test_document_foreign_key(self):
        self.assertEqual(self.modality.document, Document.objects.get(id=1))

    def test_document_cascade_deletion(self):
        """If the parent document gets deleted then all the Successive
        child modalityies should also be deleted
        """
        Document.objects.all().delete()
        self.assertEqual(Modality.objects.all().count(), 0)

    def test__repr__method(self):
        self.assertEqual(self.modality.__repr__(), '<Modality: Test Modality (Test Document)>')

    def test__str__method(self):
        self.assertEqual(self.modality.__str__(), self.modality.name)


class TaskModelTest(TestCase):

    def _test_max_length(self, field_name, value):
        max_length = self.task._meta.get_field(field_name).max_length
        self.assertEqual(max_length, value)

    @classmethod
    def setUpTestData(cls):
        Document.objects.create(name='Test Document')
        Task.objects.create(name='Test Task', document=Document.objects.get(id=1))

    def setUp(self):
        self.task = Task.objects.get(id=1)

    def test_task_value(self):
        self.assertEqual(self.task.name, 'Test Task')

    def test_name_max_length(self):
        self._test_max_length('name', 100)

    def test_description_default_value(self):
        self.assertEqual(self.task.description, '')

    def test_description_instance(self):
        self.assertIsInstance(self.task._meta.get_field('description'), models.TextField)

    def test_document_foreign_key(self):
        self.assertEqual(self.task.document.name, Document.objects.get(id=1).name)

    def test_document_deletion_cascade(self):
        Document.objects.all().delete()
        self.assertEqual(Task.objects.all().count(), 0)

    def test__repr__method(self):
        self.assertEqual(self.task.__repr__(), '<Task: Test Task (Test Document)>')

    def test__str__method(self):
        self.assertEqual(self.task.__str__(), self.task.name)


class TaskCategoryModelTest(TestCase):

    def _test_max_length(self, field_name, value):
        max_length = self.tc._meta.get_field(field_name).max_length
        self.assertEqual(max_length, value)

    def setUp(self):
        self.tc = TaskCategory()

    def test_overview_max_length(self):
        self._test_max_length('overview',1000)

    def test_overview_default_value(self):
        self.assertEqual(self.tc.overview, '')

    def test_procedure_max_length(self):
        self._test_max_length('procedure',1000)

    def test_procedure_default_value(self):
        self.assertEqual(self.tc.procedure, '')


class DatasetModelTest(TestCase):

    def _test_max_length(self, field_name, value):
        max_length = self.dataset._meta.get_field(field_name).max_length
        self.assertEqual(max_length, value)

    @classmethod
    def setUpTestData(cls):
        Document.objects.create(name='document1')
        Language.objects.create(name='hindi')
        Modality.objects.create(
            name='modality1',
            document=Document.objects.get(id=1)
        )
        Task.objects.create(
            name='task1',
            document=Document.objects.get(id=1)
        )
        TaskCategory.objects.create(
            modality=Modality.objects.get(id=1),
            task=Task.objects.get(id=1),
            language=Language.objects.get(id=1)
        )
        Dataset.objects.create(
            name='dataset1',
            task_category=TaskCategory.objects.get(id=1),
            zipfile=None
        )

    def setUp(self):
        self.dataset = Dataset.objects.get(id=1)

    def test_name_value(self):
        self.assertEqual(self.dataset.name, 'dataset1')

    def test_name_max_length(self):
        self._test_max_length('name', 200)

    def test_description_default_value(self):
        self.assertEqual(self.dataset.description, '')

    def test_description_max_length(self):
        self._test_max_length('description', 1000)

    def test_description_instance(self):
        self.assertIsInstance(
            self.dataset._meta.get_field('description'),
            models.TextField
        )

    def test_version_default_value(self):
        self.assertEqual(self.dataset.version, 1)

    def test_version_instance(self):
        self.assertIsInstance(
            self.dataset._meta.get_field('version'),
            models.IntegerField
        )

    # def test_zipfile_instance(self):
        # self.assertIsInstance(
            # self.dataset._meta.get_field('zipfile'),
            # models.FileField
        # )

    def test_nimages_default_value(self):
        self.assertEqual(self.dataset.nimages, 0)

    def test_nimages_instance(self):
        self.assertIsInstance(
            self.dataset._meta.get_field('nimages'),
            models.PositiveIntegerField
        )

    def test__repr__method(self):
        self.assertEqual(self.dataset.__repr__(), '<Dataset: dataset1 for task_category__id = 1>')

    def test__str__method(self):
        self.assertEqual(self.dataset.__str__(), 'dataset1 (1)')
