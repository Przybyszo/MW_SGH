# MW_SGH
Multiagent systems  - Multiagent systems - Modification of wolf-rabbit-grass model from Netlogo

To install all the dependencies please run 'pip install -r requirements.txt' from the root folder.

To run this application, please run 'python app.py' from the 'mw' folder. The application was tested on Python2.7.

Application is supposed to simulate an environment, where on a 10x10 grid wolfs, rabbit and grass agents try
to surive. When a rabbit encounters a grass or a wolf encounters a rabbit, it eats it. Every agent has specific
parameters, which can be set in the GUI. The default parameters for those parameters and other environment variables
are taken from config.ini file.

Detailed description of the application is in the UML diagram file and in the comments included in source files.
