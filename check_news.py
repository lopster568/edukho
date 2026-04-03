import os, sys
sys.path.insert(0, os.path.dirname(__file__))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'education_khoj.settings')

import django
django.setup()

from django.db import connection

# Check if slug column exists
cursor = connection.cursor()
cursor.execute("SHOW COLUMNS FROM Education_news")
columns = [row[0] for row in cursor.fetchall()]
print("Columns:", columns)

if 'slug' not in columns:
    print("\nERROR: 'slug' column missing! Creating it...")
    cursor.execute("ALTER TABLE Education_news ADD COLUMN slug VARCHAR(255) DEFAULT '' NOT NULL")
    print("Column added. Now populating slugs...")

    from Education.Model.news import News
    for n in News.objects.all():
        n.slug = ''
        n.save()
    print(f"Populated slugs for {News.objects.count()} articles")
else:
    print("\nslug column exists, OK")

# Try creating a test news
from Education.Model.news import News
try:
    n = News(state='1', title='__test__', start_date='2026-04-03', end_date='2026-04-30',
             author='test', tags='test', category='3', desc='test')
    n.save()
    print(f"Test create OK, id={n.id}, slug={n.slug}")
    n.delete()
    print("Test deleted")
except Exception as e:
    import traceback
    print("CREATE ERROR:")
    traceback.print_exc()
