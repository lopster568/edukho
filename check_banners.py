import os, sys
sys.path.insert(0, os.path.dirname(__file__))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'education_khoj.settings')

import django
django.setup()

from Education.Model.HomepageMainBanner import HomepageMainBanner
from Education.Model.News_Banner import News_Banner
from Education.Model.Search_Banner import Search_Banner
from Education.Model.Category import Category
from Education.Model.State import State
from Education.Model.Area import Area


def header(text):
    print()
    print('=' * 80)
    print(text)
    print('=' * 80)


header('HOMEPAGE BANNERS')
print(f'{"id":<4} {"pos":<5} {"active":<7} {"title":<40} {"link"}')
print('-' * 100)
for b in HomepageMainBanner.objects.all().order_by('banner_position', 'id'):
    print(f'{b.id:<4} {str(b.banner_position):<5} {str(b.is_active):<7} {(b.title or "")[:40]:<40} {(b.banner_link_website or "")[:50]}')


header('NEWS BANNERS')
print(f'{"id":<4} {"pos":<5} {"page":<6} {"cate":<6} {"cate_home":<10} {"state":<6} {"active":<7} {"title":<40}')
print('-' * 100)
for b in News_Banner.objects.all().order_by('cate_home', 'position', 'id'):
    print(f'{b.id:<4} {str(b.position):<5} {str(b.page):<6} {str(b.cate):<6} {str(b.cate_home):<10} {str(b.state):<6} {str(b.is_active):<7} {(b.title or "")[:40]:<40}')


header('SEARCH BANNERS')
print(f'{"id":<4} {"pos":<5} {"cate":<6} {"state":<6} {"area":<6} {"active":<7} {"title":<40}')
print('-' * 100)
for b in Search_Banner.objects.all().order_by('position', 'id'):
    print(f'{b.id:<4} {str(b.position):<5} {str(b.category):<6} {str(b.state):<6} {str(b.area):<6} {str(b.is_active):<7} {(b.title or "")[:40]:<40}')


header('REFERENCE: CATEGORIES')
for c in Category.objects.all().order_by('id'):
    print(f'  id={c.id:<3} {c.Category}')


header('REFERENCE: STATES')
for s in State.objects.all().order_by('id'):
    print(f'  id={s.id:<3} {s.State_name}')


header('REFERENCE: AREAS (Delhi only, id 1-30)')
for a in Area.objects.filter(id__lte=30).order_by('id'):
    print(f'  id={a.id:<3} {a.Area_name}')


header('SIMULATED QUERIES — Does Search Banner query match?')
# Simulate user visiting /search?category=coaching-institute&state=new-delhi&area=dwarka
coaching = Category.objects.filter(Category__iexact='coaching institute').first()
delhi = State.objects.filter(State_name__iexact='new delhi').first()
dwarka = Area.objects.filter(Area_name__iexact='dwarka').first()
if coaching and delhi and dwarka:
    print(f'  Looking for: category="{coaching.Category}" state="{delhi.State_name}" area="{dwarka.Area_name}"')
    print(f'  Category ID: {coaching.id}, State ID: {delhi.id}, Area ID: {dwarka.id}')

    # Current buggy query (by name)
    buggy = Search_Banner.objects.filter(
        state=delhi.State_name,
        is_active=1,
        category=coaching.Category,
        area=dwarka.Area_name,
    )
    print(f'  Buggy (by name): {buggy.count()} matches')

    # Correct query (by ID)
    correct = Search_Banner.objects.filter(
        state=delhi.id,
        is_active=1,
        category=str(coaching.id),
        area=dwarka.id,
    )
    print(f'  Correct (by ID): {correct.count()} matches')
    for b in correct:
        print(f'    -> id={b.id}, pos={b.position}, title={b.title}')
else:
    print('  Could not find Coaching/Delhi/Dwarka reference records')


header('SIMULATED: News m2_banner (position=9)')
m2 = News_Banner.objects.filter(position=9, is_active=1).last()
print(f'  position=9, is_active=1: {"FOUND" if m2 else "NONE"} {(m2.title if m2 else "")}')

header('SIMULATED: News m1_banner (position=7)')
m1 = News_Banner.objects.filter(position=7, is_active=1).last()
print(f'  position=7, is_active=1: {"FOUND" if m1 else "NONE"} {(m1.title if m1 else "")}')
