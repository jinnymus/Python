from setuptools import setup, find_packages
from os.path import join, dirname

setup(name='nistest',
      version='0.5',
      description='NIS Test tools',
      url='https://jira.nis-glonass.ru/bitbucket/projects/DEV/repos/nis-test/browse',
      author='Kalistratov Kirill',
      author_email='kalistratovka@nis-glonass.ru',
      license='NIS',
      packages=find_packages(),
      install_requires=[
            'pytest',
      ],
      long_description=open(join(dirname(__file__), 'README.rst')).read(),
      zip_safe=False)

# ['requests', 'kafka', 'kazoo','zc.zk','pytest','pytest-allure-adaptor',
#           'psycopg2','jsondiff','lxml','xmldiff','xml_diff','PyHamcrest','pprint','avro','confluent-kafka',
#             'confluent-kafka[avro]','fastavro','numexpr','ConfigParser','SQLAlchemy'
#       ],
