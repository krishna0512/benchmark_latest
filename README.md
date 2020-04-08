Thoughts regarding the design of database around the dataset and task_category
-> 		task_category will have a ManyToManyField dataset that links to Dataset.
		this field will be ManyToManyField because each TC can have multiple dataset having different versions
		and furthermore each dataset will be unique only for tasks and language and same for all the modalities of the document.

-> 		Dataset will have the fields 
		name (string)
		task_category (ManyToManyField)
		version (int)
		

Each dataset will have a name that is mildly descriptive to the user downloading that dataset.
Each dataset will be connected to unique (Document ; Language ; Task) e.g. (Printed ; Hindi ; Line Recognition)
Each dataset will be having a link a a zip folder that user can directly download
	This zip folder is ideally stored in media folder in django and this dataset will have different number of images in zip.
	for e.g. Printed->Hindi->PageRecognition will have 20 complete Page Images
	and 	 Printed->Hindi->LineRecognition will have 20 X 15 Images of line (where 20 = Page number and 15 = number of lines in each page)
	etc....
Each dataset will also have a version number and a unique (Document ; Language ; Task) can have 2 dataset but thier version should be diff.
Each dataset will also have some Meta stats like
	number of images in zip folder

To visualize the models present in the database.
Install django extensions
$ pip install django-extensions
$ python manage.py graph_models -a -o benchmark_models.png

Installation Instruction:
-> Create and activate a virtualenv using command inside the home folder of Django (where there is manage.py)

$ virtualenv benchmark_venv

$ source benchmark_venv/bin/activate

-> Install the requirements.txt

$ pip install -r requirements.txt

-> Check for any new migrations and migrate the database.

$ python manage.py makemigrations

$ python manage.py migrate

-> Run the django server

$ python manage.py runserver
