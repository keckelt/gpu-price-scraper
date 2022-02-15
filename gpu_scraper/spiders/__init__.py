# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.

from datetime import datetime

with open('data/README.md', 'w') as readme:
    readme.write('Last updated on ' + datetime.now().strftime('%Y%m%d at %H:%M:%S') + '.\n')
