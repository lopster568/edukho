import os, sys
sys.path.insert(0, os.path.dirname(__file__))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'education_khoj.settings')

import django
django.setup()

try:
    from Education.views import *
    print('All imports OK')
except Exception as e:
    import traceback
    print('IMPORT ERROR:')
    traceback.print_exc()
