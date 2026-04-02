import os, sys, django
sys.path.insert(0, os.path.dirname(__file__))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'education_khoj.settings')
django.setup()

from Education.Model.Footer_section import Footer_Section

# Clear existing and re-seed with correct slug URLs
Footer_Section.objects.all().delete()

links = [
    (1, 'About Us', '/about'),
    (1, 'Contact Us', '/Contact'),
    (1, 'Advertise With Us', '/advertising'),
    (1, 'Terms and Conditions', '/term_condition'),
    (1, 'Privacy Policy', '/privacy'),
    (1, 'Work with Us', '/work_with_us'),
    (2, 'Best Play School in Najafgarh', '/search?category=play-school&state=new-delhi&area=najafgarh'),
    (2, 'Best Play School in Dwarka', '/search?category=play-school&state=new-delhi&area=dwarka'),
    (2, 'Best Play School in Vikaspuri', '/search?category=play-school&state=new-delhi&area=vikaspuri'),
    (2, 'Best Pre School in Rohini', '/search?category=play-school&state=new-delhi&area=rohini'),
    (2, 'Best Play School in Gurugram', '/search?category=play-school&state=haryana&area=gurugram'),
    (2, 'Best Play School in Dehradun', '/search?category=play-school&state=uttrakhand&area=dehradun'),
    (2, 'Best Pre School in Chandigarh', '/search?category=play-school&state=chandigarh&area=chandigarh'),
    (2, 'Top School in Chandigarh', '/search?category=school&state=chandigarh&area=chandigarh'),
    (2, 'Top School in Dehradun', '/search?category=school&state=uttrakhand&area=dehradun'),
    (2, 'Best School in Noida', '/search?category=school&state=uttar-pradesh&area=noida'),
    (3, 'Top School in Gurugram', '/search?category=school&state=haryana&area=gurugram'),
    (3, 'Top School in Palam Vihar Gurugram', '/search?category=school&state=haryana&area=palam-vihar-gurugram'),
    (3, 'Best School in Bahadurgarh', '/search?category=school&state=haryana&area=bahadurgarh'),
    (3, 'Top School in Faridabad', '/search?category=school&state=haryana&area=faridabad'),
    (3, 'Best School in Najafgarh', '/search?category=school&state=new-delhi&area=najafgarh'),
    (3, 'Top Schools in Vikaspuri', '/search?category=school&state=new-delhi&area=vikaspuri'),
    (3, 'Top Schools in Rohini', '/search?category=school&state=new-delhi&area=rohini'),
    (3, 'Top School in Paschim Vihar', '/search?category=school&state=new-delhi&area=paschim-vihar'),
    (3, 'Best School in Dwarka', '/search?category=school&state=new-delhi&area=dwarka'),
    (3, 'Best Coaching Institute in Dwarka', '/search?category=coaching-institute&state=new-delhi&area=dwarka'),
    (4, 'Best Coaching Institute in Janakpuri', '/search?category=coaching-institute&state=new-delhi&area=janak-puri'),
    (4, 'Best Coaching Institute in Rohini', '/search?category=coaching-institute&state=new-delhi&area=rohini'),
    (4, 'Top Coaching Institute in Gurugram', '/search?category=coaching-institute&state=haryana&area=gurugram'),
    (4, 'Top Coaching Institute in Noida', '/search?category=coaching-institute&state=uttar-pradesh&area=noida'),
    (4, 'Best Coaching Institute in Vasundhra Gaziabad', '/search?category=coaching-institute&state=uttar-pradesh&area=vasundhra-ghaziabad'),
    (4, 'Top Coaching Institute in Dehradun', '/search?category=coaching-institute&state=uttrakhand&area=dehradun'),
    (4, 'Best Coaching Institute in Chandigarh', '/search?category=coaching-institute&state=chandigarh&area=chandigarh'),
    (4, 'Best Coaching Institute in Faridabad', '/search?category=coaching-institute&state=haryana&area=faridabad'),
    (4, 'Best Coaching Institute in Greater Noida', '/search?category=coaching-institute&state=uttar-pradesh&area=greater-noida'),
    (4, 'Best Music Academy in Dwarka', '/search?category=music-academy&state=new-delhi&area=dwarka'),
    (5, 'Best Dance Academy in Dwarka', '/search?category=dance-academy&state=new-delhi&area=dwarka'),
    (5, 'Best College in Dwarka', '/search?category=college&state=new-delhi&area=dwarka'),
    (5, 'Best College in Dehradun', '/search?category=college&state=uttrakhand&area=dehradun'),
    (5, 'Top Universities in Dehradun', '/search?category=university&state=uttrakhand&area=dehradun'),
    (5, 'Computer Institute in Chandigarh', '/search?category=professional-institute&state=chandigarh&area=chandigarh'),
    (5, 'Computer Institute in Dehradun', '/search?category=professional-institute&state=uttrakhand&area=dehradun'),
    (5, 'Jobs in Education', '/Job'),
]

for col, title, link in links:
    Footer_Section.objects.create(user_id='1', title=title, footer_link=link, column_number=col)

print(f'Seeded {len(links)} links with slug URLs')
