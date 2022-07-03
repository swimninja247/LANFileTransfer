"""
Global arguments
"""

import os

# maximum filesize in megabytes
file_mb_max = 100

# encryption key
app_key = 'any_non_empty_string'

# full path destination for our upload files
upload_dest = os.path.join(os.getcwd(), 'uploads')

# list of allowed extensions
extensions = {'txt', 'pdf', 'png', 'heic'}
