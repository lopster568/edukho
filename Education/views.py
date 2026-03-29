from datetime import date
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotFound
from django.contrib.auth import authenticate, login, logout
from .Model.contact import Contact
from .Model.interview import Interview
from django.http import JsonResponse
from .Model.job import Job
from .Model.news import News
from .models import User_Member
from .event import Event
from .Model.HomepageMainBanner import HomepageMainBanner
from .Model.Userpermission import Userpermission
from .Model.State import State
from .Model.Area import Area
from .Model.About import About
from .Model.Search_Banner import Search_Banner
from .Model.News_Banner import News_Banner
from .Model.Job_banner import Job_Banner
from .Model.Interview_Banner import Interview_Banner
from django.shortcuts import get_object_or_404
from .Model.Category import Category
from .Model.Video_Section import Video_Section
from .Model.Features import Features
from .Model.UserJobApply import UserJobApply
from .Model.Payment_table import Payment_table
import random as r
from django.core.mail import send_mail, EmailMessage
from django.template.loader import render_to_string
from django.contrib import messages
from django.db.models import Q
from django.utils.safestring import mark_safe
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.conf import settings
from django.db import OperationalError
import re

# ─────────────────────────────────────────────
# PUBLIC VIEWS
# ─────────────────────────────────────────────

def homepage(request):
    try:
        all_news       = News.objects.order_by("-id").filter(is_active=1)[0:9]
        all_intervieew = Interview.objects.all().order_by('-id')[0:16]
        all_job        = Job.objects.filter(is_active=1, end_date__gte=date.today()).order_by('-id')[0:8]
        banner         = HomepageMainBanner.objects.filter(is_active=1)
        all_state      = State.objects.all()
        all_area       = Area.objects.all()
        all_category   = Category.objects.all()
        news_qs        = News.objects.filter(is_active=1)
        rand_news      = news_qs.order_by("-id").first() if news_qs.exists() else None
        m1_banner      = banner.filter(banner_position=9).last()
        vidoe          = Video_Section.objects.filter(is_active='1', user_id=1).order_by('-id')[0:4]
    except Exception:
        all_news = all_intervieew = all_job = all_state = all_area = all_category = vidoe = []
        banner = []
        rand_news = m1_banner = None

    return render(request, 'homepage.html', {
        'news':      all_news,
        'm1_banner': m1_banner,
        'video':     vidoe,
        'interview': all_intervieew,
        'job':       all_job,
        'main':      rand_news,
        'banner':    banner,
        'state':     all_state,
        'area':      all_area,
        'cate':      all_category,
    })


def about(request):
    return render(request, "about.html")

def advertising(request):
    return render(request, "advertising.html")

def term_condition(request):
    return render(request, "term_condition.html")

def privacy(request):
    return render(request, "privacy.html")

def work_with_us(request):
    return render(request, "work_with_us.html")

def events(request):
    return render(request, 'Events.html') 

def contact(request):
    if request.method == 'POST':
        name    = request.POST.get('full_name')
        email   = request.POST.get('email')
        message = request.POST.get('message')
        try:
            Contact(name=name, email=email, message=message).save()
            Email_Send = EmailMessage(
                f'New Contact Form Submission from {name}',
                f'Name: {name}\nEmail: {email}\nMessage: {message}',
                to=['saif.ippl@gmail.com'],
            )
            Email_Send.send()
        except Exception:
            pass
        return redirect('/')
    return render(request, 'Contact.html')

def video(request):
    try:
        vidoe      = Video_Section.objects.filter(is_active=1, user_id=1)
        qs         = list(vidoe)
        rand_video = r.choice(qs) if qs else None
        recent     = Video_Section.objects.order_by('-id').filter(is_active=1, user_id=1)[0:4]
    except Exception:
        vidoe = recent = []
        rand_video = None
    return render(request, 'Video_section.html', {
        'video':      vidoe,
        'rand_video': rand_video,
        'recent':     recent,
    })


def clean_youtube_url(url):
    if not url:
        return ""
    # Extract just the 11-character video ID from any YouTube URL format
    match = re.search(r'youtu\.be/([a-zA-Z0-9_-]{11})', url)
    if match:
        return f"https://www.youtube.com/embed/{match.group(1)}"
    match = re.search(r'watch\?v=([a-zA-Z0-9_-]{11})', url)
    if match:
        return f"https://www.youtube.com/embed/{match.group(1)}"
    match = re.search(r'youtube\.com/embed/([a-zA-Z0-9_-]{11})', url)
    if match:
        return f"https://www.youtube.com/embed/{match.group(1)}"  # strips ?si= and all params
    return url

def job_data_read(request, job_id):
    try:
        items = Job.objects.filter(pk=job_id)
        serialized_data = [{
            'title':      item.job_title,
            'id':         item.id,
            'end_date':   item.end_date,
            'start_date': item.pub_date,
            'company':    item.company,
            'exp':        item.experience,
            'state':      item.state,
            'category':   item.job_category,
            'desc':       item.job_desc,
        } for item in items]
    except Exception:
        serialized_data = []
    return JsonResponse({'data': serialized_data})


def get_data(request, stateid):
    try:
        data = Area.objects.filter(State_id=stateid) if stateid != 0 else Area.objects.all()
        serialized_data = [{'Area_name': item.Area_name, 'Area_id': item.id} for item in data]
    except Exception:
        serialized_data = []
    return JsonResponse({'data': serialized_data})


def job_statewise(request, stateid):
    try:
        data = Job.objects.filter(state=stateid) if stateid is not None else Job.objects.all()
        serialized_data = [{
            'job_title': item.job_title,
            'company':   item.company,
            'state':     item.state,
            'end_date':  item.end_date,
        } for item in data]
    except Exception:
        serialized_data = []
    return JsonResponse({'data': serialized_data})


def demo_news(request):
    return render(request, 'demo_news.html')


def news(request):
    try:
        state    = State.objects.all()
        cate     = Category.objects.all()
        all_nwes = News.objects.order_by('-id').filter(is_active=1)[0:9]
        news_qs  = News.objects.filter(is_active=1)
        rand_news = news_qs.order_by("-id").first() if news_qs.exists() else None

        school_obj      = Category.objects.filter(is_active=1, Category__iexact="school").first()
        play_school_obj = Category.objects.filter(is_active=1, Category__iexact="Play School").first()
        college_obj     = Category.objects.filter(is_active=1, Category__iexact="college").first()
        univercity_obj  = Category.objects.filter(is_active=1, Category__iexact="university").first()
        sports_obj      = Category.objects.filter(is_active=1, Category__iexact="sports academy").first()
        study_obj       = Category.objects.filter(is_active=1, Category__iexact="study abroad").first()

        school_id        = school_obj.id if school_obj else None
        play_school_id   = play_school_obj.id if play_school_obj else None
        college_id       = college_obj.id if college_obj else None
        univercity_id    = univercity_obj.id if univercity_obj else None
        Sports_Academy_id = sports_obj.id if sports_obj else None
        study_abroad_id  = study_obj.id if study_obj else None

        news_banner  = News_Banner.objects.filter(is_active=1)
        m1_banner    = news_banner.filter(position=7).last()
        m2_banner    = news_banner.filter(position=9).last()
        current_news = News.objects.order_by('-id').filter(is_active=1)[0:5]

        school_play_ids  = [cid for cid in [school_id, play_school_id] if cid]
        college_univ_ids = [cid for cid in [college_id, univercity_id] if cid]
        exclude_ids      = [cid for cid in [school_id, play_school_id, college_id,
                                            univercity_id, Sports_Academy_id, study_abroad_id] if cid]

        school_play_shool_news = (
            News.objects.order_by('-id').filter(category__in=school_play_ids, is_active=1)[0:9]
            if school_play_ids else News.objects.none()
        )
        college_university_news = (
            News.objects.order_by('-id').filter(category__in=college_univ_ids, is_active=1)[0:4]
            if college_univ_ids else News.objects.none()
        )
        sport = (
            News.objects.order_by('-id').filter(category=Sports_Academy_id, is_active=1)[0:8]
            if Sports_Academy_id else News.objects.none()
        )
        study = (
            News.objects.order_by('-id').filter(category=study_abroad_id, is_active=1)[0:9]
            if study_abroad_id else News.objects.none()
        )
        all_job = Job.objects.order_by('-id').all()[0:4]
        other_news = (
            News.objects.order_by('-id').exclude(category__in=exclude_ids).filter(is_active=1)[0:8]
            if exclude_ids
            else News.objects.order_by('-id').filter(is_active=1)[0:8]
        )

    except Exception:
        state = cate = all_nwes = current_news = []
        rand_news = m1_banner = m2_banner = None
        news_banner = school_play_shool_news = college_university_news = []
        sport = study = all_job = other_news = []

    return render(request, 'News.html', {
        'news':                 all_nwes,
        'job':                  all_job,
        'other':                other_news,
        'm1_banner':            m1_banner,
        'm2_banner':            m2_banner,
        'sport':                sport,
        'studyabroad':          study,
        'schoolplayshoolnews':  school_play_shool_news,
        'collegeuniversitynews': college_university_news,
        'news_banner':          news_banner,
        'cur':                  current_news,
        'state':                state,
        'cate':                 cate,
        'main':                 rand_news,
    })


def news_filter(request):
    cate    = request.GET.get('cate')
    stateid = request.GET.get('state')

    all_news   = []
    main_news  = {}
    news_banner = []
    m1_banner  = None
    m2_banner  = None

    try:
        state        = State.objects.all()
        current_news = News.objects.order_by('-id')[0:5]

        school_obj      = Category.objects.filter(is_active=1, Category__iexact="school").first()
        play_school_obj = Category.objects.filter(is_active=1, Category__iexact="Play School").first()
        college_obj     = Category.objects.filter(is_active=1, Category__iexact="college").first()
        univercity_obj  = Category.objects.filter(is_active=1, Category__iexact="university").first()
        sports_obj      = Category.objects.filter(is_active=1, Category__iexact="sports academy").first()
        study_obj       = Category.objects.filter(is_active=1, Category__iexact="study abroad").first()

        school_id        = school_obj.id if school_obj else None
        play_school_id   = play_school_obj.id if play_school_obj else None
        college_id       = college_obj.id if college_obj else None
        univercity_id    = univercity_obj.id if univercity_obj else None
        Sports_Academy_id = sports_obj.id if sports_obj else None
        study_abroad_id  = study_obj.id if study_obj else None

        if cate == 'all':
            if stateid is None:
                all_news    = News.objects.all()
                news_banner = News_Banner.objects.all()
                main_news   = all_news.order_by("-id").first() if all_news.exists() else {}
            else:
                all_news    = News.objects.filter(state=stateid, is_active=1)
                news_banner = News_Banner.objects.filter(state=stateid, is_active=1)
                main_news   = all_news.order_by("-id").first() if all_news.exists() else {}

        elif cate == 'college_university':
            if stateid is None:
                all_news    = News.objects.filter(Q(category=college_id) | Q(category=univercity_id), is_active=1)
                news_banner = News_Banner.objects.filter(Q(cate=college_id) | Q(cate=univercity_id), state=0, is_active=1)
            else:
                all_news    = News.objects.filter(Q(category=univercity_id) | Q(category=college_id), state=stateid, is_active=1)
                news_banner = News_Banner.objects.filter(Q(cate=univercity_id) | Q(cate=college_id), state=stateid, is_active=1)
            main_news = all_news.order_by("-id").first() if all_news.exists() else {}

        elif cate == 'school_play_shool_news':
            if stateid is None:
                all_news    = News.objects.filter(Q(category=school_id) | Q(category=play_school_id), is_active=1)
                news_banner = News_Banner.objects.filter(Q(cate=school_id) | Q(cate=play_school_id), state=0, is_active=1)
            else:
                all_news    = News.objects.filter(Q(category=school_id) | Q(category=play_school_id), state=stateid, is_active=1)
                news_banner = News_Banner.objects.filter(Q(cate=school_id) | Q(cate=play_school_id), state=stateid, is_active=1)
            main_news = all_news.order_by("-id").first() if all_news.exists() else {}

        elif cate == 'sports':
            if stateid is None:
                all_news    = News.objects.filter(category=Sports_Academy_id)
                news_banner = News_Banner.objects.filter(cate=Sports_Academy_id, state=0, is_active=1)
            else:
                all_news    = News.objects.filter(category=Sports_Academy_id, state=stateid, is_active=1)
                news_banner = News_Banner.objects.filter(cate=Sports_Academy_id, state=stateid, is_active=1)
            main_news = all_news.order_by("-id").first() if all_news.exists() else {}

        elif cate == 'study_abroad':
            if stateid is None:
                all_news    = News.objects.filter(category=study_abroad_id, is_active=1)
                news_banner = News_Banner.objects.filter(cate=study_abroad_id, state=0, is_active=1)
            else:
                all_news    = News.objects.filter(category=study_abroad_id, state=stateid, is_active=1)
                news_banner = News_Banner.objects.filter(cate=study_abroad_id, state=stateid, is_active=1)
            main_news = all_news.order_by("-id").first() if all_news.exists() else {}

        elif cate == 'others':
            exclude_q = Q(category=school_id) | Q(category=play_school_id) | Q(category=college_id) | \
                        Q(category=univercity_id) | Q(category=Sports_Academy_id) | Q(category=study_abroad_id)
            if stateid is None:
                all_news    = News.objects.filter(is_active=1).exclude(exclude_q)
                news_banner = News_Banner.objects.filter(cate=study_abroad_id, state=0, is_active=1)
            else:
                all_news    = News.objects.filter(is_active=1, state=stateid).exclude(exclude_q)
                news_banner = News_Banner.objects.filter(cate=study_abroad_id, state=0, is_active=1)
            main_news = all_news.order_by("-id").first() if all_news.exists() else {}

        if news_banner:
            m1_banner = news_banner.filter(position=7).last()
            m2_banner = news_banner.filter(position=9).last()

    except Exception:
        state = current_news = []
        all_news = news_banner = []
        main_news = m1_banner = m2_banner = None

    return render(request, 'News_Filter.html', {
        'news':        all_news,
        'stateid':     stateid,
        'cate':        cate,
        'm1_banner':   m1_banner,
        'm2_banner':   m2_banner,
        'cur':         current_news,
        'news_banner': news_banner,
        'state':       state,
        'main_news':   main_news,
    })


def random_news(request):
    try:
        all_nwes = News.objects.filter(is_active=1).order_by('-id')
        serialized_data = [{
            'title':   item.title,
            'desc':    mark_safe(item.desc),
            'category': item.category,
            'state':   item.state,
            'img':     item.img.url,
            'newsid':  item.id,
            'slug' : item.slug,
        } for item in all_nwes]
    except Exception:
        serialized_data = []
    return JsonResponse({'data': serialized_data})


def search(request):
    if request.method == "GET":
        state    = request.GET.get('state')
        area     = request.GET.get('area')
        category = request.GET.get('category')
        page_num = request.GET.get('page', 1)

        empty_ctx = {
            "data":          [],
            "paid_users":    [],
            "non_paid_user": [],
            'search_banner': [],
            'm1_banner':     None,
            'm2_banner':     None,
        }

        if not state or not area or not category:
            return render(request, 'search.html', empty_ctx)

        if state == '0' or area == '0' or category == '0':
            return redirect('/')

        try:
            from Education.Model.State import State
            from Education.Model.Area import Area
            from Education.Model.Category import Category

            def slug_to_name(slug):
                return slug.replace('-', ' ').strip()

            # Try slug first, then numeric ID
            state_obj    = State.objects.filter(State_name__iexact=slug_to_name(state)).first()
            if not state_obj and state.isdigit():
                state_obj = State.objects.filter(id=int(state)).first()

            area_obj     = Area.objects.filter(Area_name__icontains=slug_to_name(area)).first()
            if not area_obj and area.isdigit():
                area_obj = Area.objects.filter(id=int(area)).first()

            category_obj = Category.objects.filter(Category__iexact=slug_to_name(category)).first()
            if not category_obj and category.isdigit():
                category_obj = Category.objects.filter(id=int(category)).first()

            if not state_obj or not area_obj or not category_obj:
                return render(request, 'search.html', empty_ctx)

            data              = User_Member.objects.filter(state=str(state_obj.id), region=str(area_obj.id), i_am=str(category_obj.id), is_active="1")
            paid_user_ids     = Payment_table.objects.filter(is_active=1).values_list('userid', flat=True)
            paid_user_dataset = data.filter(id__in=paid_user_ids)
            non_paid_dataset  = data.exclude(id__in=paid_user_ids)

            combined = (
                [{'user': u, 'type': 'paid'} for u in paid_user_dataset] +
                [{'user': u, 'type': 'non-paid'} for u in non_paid_dataset]
            )

            paginator = Paginator(combined, 20)
            try:
                page_obj = paginator.page(page_num)
            except PageNotAnInteger:
                page_obj = paginator.page(1)
            except EmptyPage:
                page_obj = paginator.page(paginator.num_pages)

            try:
                search_banner = Search_Banner.objects.filter(state=state_obj.State_name, is_active=1, category=category_obj.Category, area=area_obj.Area_name)
                m1_banner     = search_banner.filter(position=5).last()
                m2_banner     = search_banner.filter(position=6).last()
            except Exception:
                search_banner = []
                m1_banner     = None
                m2_banner     = None

        except Exception as e:
            import traceback
            print('SEARCH ERROR:', traceback.format_exc())
            return render(request, 'search.html', {**empty_ctx, 'debug_error': str(e)})

        return render(request, 'search.html', {
            "data":          page_obj,
            "paid_users":    combined,
            "non_paid_user": non_paid_dataset,
            'search_banner': search_banner,
            'm1_banner':     m1_banner,
            'm2_banner':     m2_banner,
        })


def user_info_profile(request, userid):
    try:
        data    = User_Member.objects.filter(id=userid, is_superuser=0)
        about   = About.objects.filter(userid=userid)
        f_user  = Features.objects.filter(userid=userid)
        vidoe   = Video_Section.objects.filter(user_id=userid)
    except Exception:
        data = about = f_user = vidoe = []
    return render(request, 'user_profile.html', {
        'data':    data,
        'about':   about,
        'feature': f_user,
        'video':   vidoe,
    })


def singlenews(request, news_slug):
    try:
        all_news = News.objects.all()
        
        # Try slug first, then fall back to integer id
        single_news = News.objects.filter(slug=news_slug)
        
        if not single_news.exists():
            try:
                news_id = int(news_slug)
                single_news = News.objects.filter(id=news_id)
            except (ValueError, TypeError):
                pass

        news = all_news.order_by('-start_date')[:4]
        current = single_news.first()
        
        if current:
            next_btn = "disable" if current.id == all_news.last().id else "enable"
            prev_btn = "disable" if current.id == all_news.first().id else "enable"
        else:
            next_btn = prev_btn = "disable"

    except Exception:
        single_news = news = []
        next_btn = prev_btn = "disable"

    return render(request, 'single_news.html', {
        'singlenews': single_news,
        'btn':        next_btn,
        'prev_btn':   prev_btn,
        'news':       news,
        'media':      settings.MEDIA_URL,
    })


def single_interview(request, interview_id):
    try:
        all_interview = Interview.objects.all()
        next_btn  = "disable" if interview_id == all_interview.last().id else "enable"
        prev_btn  = "disable" if interview_id == all_interview.first().id else "enable"
        single_iv = Interview.objects.filter(id=interview_id)
        all_banner = Interview_Banner.objects.all()
    except Exception:
        single_iv = all_banner = []
        next_btn = prev_btn = "disable"
    return render(request, 'single_interview.html', {
        'single_interview': single_iv,
        'banner':           all_banner,
        'btn':              next_btn,
        'prev_btn':         prev_btn,
    })


def interview(request):
    try:
        all_intervieew   = Interview.objects.all()
        interview_banner = Interview_Banner.objects.all()
        m1_banner = interview_banner.filter(position=7).last()
        m2_banner = interview_banner.filter(position=8).last()
    except Exception:
        all_intervieew = interview_banner = []
        m1_banner = m2_banner = None
    return render(request, 'Interview.html', {
        'interview':        all_intervieew,
        'm1_banner':        m1_banner,
        'm2_banner':        m2_banner,
        'interview_banner': interview_banner,
    })


def job(request):
    state = request.GET.get('state')
    try:
        all_state = State.objects.all()
        if state == "0" or state is None:
            all_job    = Job.objects.filter(job_category=1, is_active=1, end_date__gte=date.today()).order_by('-id')
            job_banner = Job_Banner.objects.filter(job_category=1, is_active=1)
        else:
            all_job    = Job.objects.filter(state=state, job_category=1, is_active=1, end_date__gte=date.today()).order_by('-id')
            job_banner = Job_Banner.objects.filter(state=state, job_category=1, is_active=1)
        m1_banner = job_banner.filter(position=7).last()
        m2_banner = job_banner.filter(position=8).last()
    except Exception as e:
        import logging
        logging.error(f'Job view error: {e}')
        all_job = all_state = []
        m1_banner = m2_banner = None
    return render(request, 'Job.html', {
        'job':       all_job,
        'state':     all_state,
        'job_banner': m1_banner,
        'm2_banner': m2_banner,
    })


def Non_Teaching(request):
    state = request.GET.get('state')
    try:
        all_state = State.objects.all()
        if state == "0" or state is None:
            all_job    = Job.objects.filter(job_category=2, is_active=1)
            job_banner = Job_Banner.objects.filter(job_category=2)
        else:
            all_job    = Job.objects.filter(state=state, job_category=2, is_active=1)
            job_banner = Job_Banner.objects.filter(state=state, job_category=2)
    except Exception:
        all_job = all_state = job_banner = []
    return render(request, 'Non_Teaching.html', {
        'job':        all_job,
        'state':      all_state,
        'job_banner': job_banner,
    })
  

# ─────────────────────────────────────────────
# AUTH VIEWS
# ─────────────────────────────────────────────

def send_html_email(user):
    subject      = 'Activate your account'
    message      = 'Activate your account.'
    from_email   = 'ishaaninfomedia@gmail.com'
    recipient_list = [user['email']]
    html_message = render_to_string('email_form_demo.html', {'user': user})
    send_mail(subject, message, from_email, recipient_list, html_message=html_message)
    return HttpResponse('Verify your mail Please')


def verifyEmail(request, email):
    try:
        user = User_Member.objects.get(user_email=email)
        user.is_active = True
        user.save()
        return redirect('/Login_form')
    except User_Member.DoesNotExist:
        return HttpResponseNotFound("User not found")
    except Exception as e:
        return HttpResponseNotFound("An error occurred")


def login_form(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('pass')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('/UserAccount')
            else:
                return HttpResponse('Your account is inactive. Please verify your email.')
        else:
            return render(request, 'Login.html')
    return render(request, 'Login.html')


def sign_form(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('pass')
        Iam      = request.POST.get('iam')
        email    = request.POST.get('email')
        if User_Member.objects.filter(user_email=email).exists():
            return HttpResponse('User Already Exists, please go to login page')
        reg_member = User_Member.objects.create_user(
            username=email, password=password,
            i_am=Iam, user_email=email, name=username, is_active=True
        )
        reg_member.save()
        return HttpResponse('Please Check Email and Verify')
    all_cate = Category.objects.all()
    return render(request, 'Sign.html', {'cate': all_cate})


def logoutuser(request):
    logout(request)
    return redirect('/Login_form')


def google_verify(request):
    return redirect('/accounts')


def custom_404(request, exception):
    return render(request, '404.html', status=404)


# ─────────────────────────────────────────────
# USER ACCOUNT VIEWS
# ─────────────────────────────────────────────

def UserAccount(request):
    if request.user.is_anonymous:
        return redirect('/Login_form')
    if request.method == "POST":
        add_ban = User_Member.objects.get(pk=request.user.id)
        img = request.FILES.get('img')
        add_ban.state                    = request.POST.get('state')
        add_ban.i_am                     = request.POST.get('category')
        add_ban.username                 = request.POST.get('email')
        add_ban.contact_no               = request.POST.get('contact')
        add_ban.name                     = request.POST.get('name')
        add_ban.name_of_institution      = request.POST.get('name_of_institution')
        add_ban.address_of_institution   = request.POST.get('address_of_institution')
        add_ban.country                  = request.POST.get('country')
        add_ban.user_email               = request.POST.get('email')
        add_ban.user_web                 = request.POST.get('web_link')
        add_ban.name_of_concerned_person = request.POST.get('concerned_person')
        add_ban.year_of_establishment    = request.POST.get('year_of_establishment')
        add_ban.region                   = request.POST.get('area')
        if img:
            add_ban.add_logo_of_instituion = img
        add_ban.save()
        messages.success(request, "Update Successful")
        return redirect('/UserAccount')

    cate     = Category.objects.all()
    state    = State.objects.all()
    area     = Area.objects.all()
    data     = User_Member.objects.filter(pk=request.user.id, is_active=1)
    user_per = {}
    if Payment_table.objects.filter(userid=request.user.id).exists():
        user_per = Userpermission.objects.get(userid=request.user.id)
    return render(request, 'Admin/UserAccount.html', {
        'state':   state,
        'area':    area,
        'cate':    cate,
        'data':    data,
        'userper': user_per,
    })


@login_required
def User_Feature(request):
    cate = Category.objects.all()
    if request.user.is_superuser:
        if request.method == "POST":
            user_feature = request.POST.get('editor')
            Features(userid=request.user.id, features=user_feature).save()
        user_feature_data = Features.objects.filter(userid=request.user.id)
        return render(request, 'Admin/User_Feature.html', {'cate': cate, 'user_f': user_feature_data})
    try:
        user_payment_status = Payment_table.objects.get(userid=request.user.id).is_active
        userper = Userpermission.objects.get(userid=request.user.id)
        if user_payment_status == "1" and userper.is_active == "1" and userper.Salient_Features == "1":
            if request.method == "POST":
                Features(userid=request.user.id, features=request.POST.get('editor')).save()
            user_feature_data = Features.objects.filter(userid=request.user.id)
            return render(request, 'Admin/User_Feature.html', {
                'cate': cate, 'userper': userper, 'user_f': user_feature_data
            })
        return redirect('/UserAccount')
    except Payment_table.DoesNotExist:
        return redirect('/UserAccount')


@login_required
def User_job(request):
    all_state = State.objects.all()
    all_job   = Job.objects.all()
    is_job_add = ""
    if request.user.is_superuser:
        if request.method == "POST":
            Job(
                job_title=request.POST.get('title'),
                job_category=request.POST.get('cate'),
                company=request.POST.get('company'),
                state=request.POST.get('state'),
                job_desc=request.POST.get('editor'),
                experience=request.POST.get('experience'),
                pub_date=request.POST.get('start_date'),
                salary=request.POST.get('salary'),
                end_date=request.POST.get('end_date'),
                userid=request.user.id,
            ).save()
            is_job_add = "true"
        return render(request, 'Admin/User_job.html', {"message": is_job_add, 'job': all_job, 'state': all_state})
    try:
        user_payment_status = Payment_table.objects.get(userid=request.user.id).is_active
        userper = Userpermission.objects.get(userid=request.user.id)
        if user_payment_status == "1" and userper.is_active == "1" and userper.Job == "1":
            if request.method == "POST":
                Job(
                    job_title=request.POST.get('title'),
                    job_category=request.POST.get('cate'),
                    company=request.POST.get('company'),
                    state=request.POST.get('state'),
                    job_desc=request.POST.get('editor'),
                    experience=request.POST.get('experience'),
                    pub_date=request.POST.get('start_date'),
                    salary=request.POST.get('salary'),
                    end_date=request.POST.get('end_date'),
                    userid=request.user.id,
                ).save()
                is_job_add = "true"
            return render(request, 'Admin/User_job.html', {
                "message": is_job_add, 'job': all_job, 'state': all_state, 'userper': userper
            })
        return redirect('/UserAccount')
    except Payment_table.DoesNotExist:
        return redirect('/UserAccount')


@login_required
def Event_activity(request):
    is_banner_add = ""
    all_state = State.objects.all()
    all_cate  = Category.objects.all()
    all_news  = News.objects.all()
    if request.user.is_superuser:
        if request.method == "POST":
            News(
                state=request.POST.get('state'),
                title=request.POST.get('title'),
                start_date=request.POST.get('start_date'),
                end_date=request.POST.get('end_date'),
                author=request.POST.get('author'),
                img=request.FILES.get('news_img'),
                tags=request.POST.get('tags'),
                category=request.POST.get('category'),
                desc=request.POST.get('editor'),
                userid=request.user.id,
            ).save()
            is_banner_add = "true"
        return render(request, 'Admin/Event_Activity.html', {
            'state': all_state, 'cate': all_cate, "message": is_banner_add, 'news': all_news
        })
    try:
        user_payment_status = Payment_table.objects.get(userid=request.user.id).is_active
        userper = Userpermission.objects.get(userid=request.user.id)
        if user_payment_status == "1" and userper.is_active == "1" and userper.Event_Activity == "1":
            if request.method == "POST":
                News(
                    state=request.POST.get('state'),
                    title=request.POST.get('title'),
                    start_date=request.POST.get('start_date'),
                    end_date=request.POST.get('end_date'),
                    author=request.POST.get('author'),
                    img=request.FILES.get('news_img'),
                    tags=request.POST.get('tags'),
                    category=request.POST.get('category'),
                    desc=request.POST.get('editor'),
                    userid=request.user.id,
                ).save()
                is_banner_add = "true"
            return render(request, 'Admin/Event_Activity.html', {
                'state': all_state, 'cate': all_cate, "message": is_banner_add,
                'news': all_news, 'userper': userper,
            })
        return redirect('/UserAccount')
    except Payment_table.DoesNotExist:
        return redirect('/UserAccount')


# ─────────────────────────────────────────────
# PLAN VIEW
# ─────────────────────────────────────────────

def plan(request, plan_id):
    if request.user.is_anonymous:
        return redirect('/Login_form')
    PLAN_PRICES = {
        "monthly":    "300",
        "quartely":   "750",
        "half-yearly": "1200",
        "yearly":     "2000",
    }
    PLAN_PERMISSIONS = {
        "monthly":     dict(Salient_Features=1, Job=0, Event_Activity=0, Video_Section=0, About=1),
        "quartely":    dict(Salient_Features=1, Job=0, Event_Activity=1, Video_Section=0, About=1),
        "half-yearly": dict(Salient_Features=1, Job=1, Event_Activity=1, Video_Section=0, About=1),
        "yearly":      dict(Salient_Features=1, Job=1, Event_Activity=1, Video_Section=1, About=1),
    }
    if request.method == "POST":
        upi = request.POST.get('upi')
        img = request.FILES.get('img')
        if not upi or not img:
            return render(request, 'Admin/plan.html', {'error': 'Missing UPI or Image', 'plan': plan_id})
        userper, _ = Userpermission.objects.get_or_create(userid=request.user.id)
        perms = PLAN_PERMISSIONS.get(plan_id, {})
        for attr, val in perms.items():
            setattr(userper, attr, val)
        userper.save()
        Payment_table(upi_no=upi, slip_upload=img, package_id=plan_id, userid=request.user.id).save()
        return render(request, 'Admin/payment_succ.html')
    price = PLAN_PRICES.get(plan_id, "2000")
    return render(request, 'Admin/plan.html', {'plan': plan_id, 'price': price})


# ─────────────────────────────────────────────
# ADMIN VIEWS
# ─────────────────────────────────────────────

def admin_show(request):
    if not request.user.is_superuser:
        return redirect('/Login_form')
    all_payment = Payment_table.objects.all()
    for x in all_payment:
        x.id = User_Member.objects.get(id=x.userid).name
    return render(request, "./Admin/admin.html", {'pay_user': all_payment})


@login_required
def paid_user_is_active(request, plan_id):
    instance = Payment_table.objects.get(userid=plan_id)
    user_per = Userpermission.objects.get(userid=plan_id)
    if instance.is_active == "1" and user_per.is_active == "1":
        instance.is_active = user_per.is_active = 0
        data = "Deactivate Successful!"
    else:
        instance.is_active = user_per.is_active = 1
        data = "Activate Successful!"
    instance.save()
    user_per.save()
    return JsonResponse({'data': data})


@login_required
def deleteplan(request, plan_id):
    Payment_table.objects.filter(id=plan_id).delete()
    return JsonResponse({'data': "Delete Successful!"})


@login_required
def deletehomebanner(request, plan_id):
    HomepageMainBanner.objects.get(id=plan_id).delete()
    return JsonResponse({'data': "Delete Successful!"})


@login_required
def deletenewsbanner(request, plan_id):
    News_Banner.objects.get(id=plan_id).delete()
    return JsonResponse({'data': "Delete Successful!"})


@login_required
def delete_job_content_managment(request, plan_id):
    Job.objects.get(id=plan_id).delete()
    return JsonResponse({'data': "Delete Successful!"})


@login_required
def deletesearch(request, plan_id):
    get_object_or_404(User_Member, id=plan_id).delete()
    return JsonResponse({'data': "Delete Successful!"})


@login_required
def banner_search_delete(request, plan_id):
    Search_Banner.objects.get(id=plan_id).delete()
    return JsonResponse({'data': "Delete Successful!"})


@login_required
def newdelete(request, plan_id):
    News.objects.get(id=plan_id).delete()
    return JsonResponse({'data': "Delete Successful!"})


@login_required
def delete_video(request, plan_id):
    Video_Section.objects.get(id=plan_id).delete()
    return JsonResponse({'data': "Delete Successful!"})


@login_required
def job_banner_delete(request, plan_id):
    Job_Banner.objects.get(id=plan_id).delete()
    return JsonResponse({'data': "Delete Successful!"})


@login_required
def interview_banner_delete(request, plan_id):
    Interview_Banner.objects.get(id=plan_id).delete()
    return JsonResponse({'data': "Delete Successful!"})


@login_required
def interview_delete(request, interview_id):
    Interview.objects.get(id=interview_id).delete()
    return JsonResponse({'data': "Delete Successful!"})


# ─────────────────────────────────────────────
# EMAIL
# ─────────────────────────────────────────────

def send_html_email_view(request):
    if request.method == 'POST':
        name  = request.POST.get('full_name')
        email = request.POST.get('email')
        msg   = request.POST.get('message')
        contact = Contact(name=name, email=email, message=msg)
        contact.save()
        Email_Send = EmailMessage(
            f'New Contact Form Submission from {name}',
            f'Name: {name}\nEmail: {email}\nMessage: {msg}',
            to=['saif.ippl@gmail.com'],
        )
        Email_Send.send()
    return redirect("/")


def job_send_html_email(request):
    if request.method == 'POST':
        name   = request.POST.get('full_name')
        email  = request.POST.get('email')
        file   = request.FILES.get('file')
        job_id = request.POST.get('job_id')
        UserJobApply(name=name, email=email, job_id=job_id).save()
        Email_Send = EmailMessage(
            f'New Job Application from {name}',
            f'Name: {name}\nEmail: {email}\nJob ID: {job_id}',
            to=['saif.ippl@gmail.com'],
        )
        if file:
            Email_Send.attach(file.name, file.read(), file.content_type)
        Email_Send.send()
    return redirect("/")


# ─────────────────────────────────────────────
# BANNER / CONTENT MANAGEMENT (ADMIN)
# ─────────────────────────────────────────────

def homepage_banner(request):
    is_banner_add = ""
    if request.method == "POST":
        HomepageMainBanner(
            title=request.POST.get('title'),
            start_date=request.POST.get('start_date'),
            end_date=request.POST.get('end_date'),
            banner_link_website=request.POST.get('banner_website_link'),
            img=request.FILES.get('banner_img'),
            banner_position=request.POST.get('position'),
        ).save()
        is_banner_add = "true"
    all_banner = HomepageMainBanner.objects.all()
    return render(request, './Admin/homepage_banner.html', {"message": is_banner_add, 'banner': all_banner})


def homepage_banner_deactive(request, home_banner_id):
    item = HomepageMainBanner.objects.get(pk=home_banner_id)
    item.is_active = 0 if item.is_active == "1" else 1
    item.save()
    return JsonResponse({'data': "Deactivate Successful!" if item.is_active == 0 else "Activate Successful!"})


def homepage_banner_update(request, home_banner_id):
    if request.method == "POST":
        item = HomepageMainBanner.objects.get(pk=home_banner_id)
        item.title                = request.POST.get('title')
        item.start_date           = request.POST.get('start_date')
        item.end_date             = request.POST.get('end_date')
        item.banner_link_website  = request.POST.get('banner_website_link')
        item.banner_position      = request.POST.get('position')
        if request.FILES.get('banner_img'):
            item.img = request.FILES.get('banner_img')
        item.save()
        messages.success(request, "Update Successful")
        return redirect('/homepage_banner')
    item = HomepageMainBanner.objects.filter(pk=home_banner_id)
    data = [{'title': i.title, 'banner_link_website': i.banner_link_website,
             'position': i.banner_position, 'end_date': i.end_date, 'start_date': i.start_date} for i in item]
    return JsonResponse({'data': data})


def job_banner_deactive(request, home_banner_id):
    item = Job_Banner.objects.get(pk=home_banner_id)
    item.is_active = 0 if item.is_active == "1" else 1
    item.save()
    return JsonResponse({'data': "Deactivate Successful!" if item.is_active == 0 else "Activate Successful!"})


def video_section_deactive(request, home_banner_id):
    item = Video_Section.objects.get(pk=home_banner_id)
    item.is_active = 0 if item.is_active == "1" else 1
    item.save()
    return JsonResponse({'data': "Deactivate Successful!" if item.is_active == 0 else "Activate Successful!"})


def news_management_section(request):
    is_banner_add = ""
    if request.method == "POST":
        News(
            state=request.POST.get('state'),
            title=request.POST.get('title'),
            start_date=request.POST.get('start_date'),
            end_date=request.POST.get('end_date'),
            author=request.POST.get('author'),
            img=request.FILES.get('news_img'),
            tags=request.POST.get('tags'),
            category=request.POST.get('category'),
            desc=request.POST.get('editor'),
        ).save()
        is_banner_add = "true"
    all_state = State.objects.all()
    all_cate  = Category.objects.all()
    all_news  = News.objects.all()
    return render(request, './Admin/news_management_section.html', {
        'state': all_state, 'cate': all_cate, "message": is_banner_add, 'news': all_news
    })


def news_management_section_deactive(request, home_banner_id):
    item = News.objects.get(pk=home_banner_id)
    item.is_active = 0 if item.is_active == "1" else 1
    item.save()
    return JsonResponse({'data': "Deactivate Successful!" if item.is_active == 0 else "Activate Successful!"})


def news_management_section_update(request, home_banner_id):
    if request.method == "POST":
        item = News.objects.get(pk=home_banner_id)
        item.title      = request.POST.get('title')
        item.start_date = request.POST.get('start_date')
        item.end_date   = request.POST.get('end_date')
        item.tags       = request.POST.get('tags')
        item.author     = request.POST.get('author')
        item.state      = request.POST.get('state')
        item.category   = request.POST.get('category')
        item.desc       = request.POST.get('editor')
        if request.FILES.get('news_img'):
            item.img = request.FILES.get('news_img')
        item.save()
        messages.success(request, "Update Successful")
        return redirect('/news_management_section')
    item = News.objects.filter(pk=home_banner_id)
    data = [{'title': i.title, 'end_date': i.end_date, 'start_date': i.start_date,
             'tags': i.tags, 'author': i.author, 'state': i.state,
             'category': i.category, 'desc': i.desc} for i in item]
    return JsonResponse({'data': data})


def news_banner_section(request):
    is_banner_add = ""
    if request.method == "POST":
        News_Banner(
            state=request.POST.get('state'),
            title=request.POST.get('title'),
            cate_home=request.POST.get('category_home_page'),
            cate=request.POST.get('category'),
            start_date=request.POST.get('start_date'),
            end_date=request.POST.get('end_date'),
            page=request.POST.get('page'),
            banner_link_website=request.POST.get('banner_website_link'),
            img=request.FILES.get('banner_img'),
            position=request.POST.get('position'),
        ).save()
        is_banner_add = "true"
    all_state   = State.objects.all()
    news_banner = News_Banner.objects.all()
    all_cate    = Category.objects.all()
    return render(request, './Admin/news_banner_section.html', {
        "message": is_banner_add, 'cate': all_cate, "state": all_state, "news_banner": news_banner
    })


def news_banner_section_deactive(request, home_banner_id):
    item = News_Banner.objects.get(pk=home_banner_id)
    item.is_active = 0 if item.is_active == "1" else 1
    item.save()
    return JsonResponse({'data': "Deactivate Successful!" if item.is_active == 0 else "Activate Successful!"})


def news_banner_section_update(request, home_banner_id):
    if request.method == "POST":
        item = News_Banner.objects.get(pk=home_banner_id)
        item.title                = request.POST.get('title')
        item.start_date           = request.POST.get('start_date')
        item.end_date             = request.POST.get('end_date')
        item.banner_link_website  = request.POST.get('banner_website_link')
        item.page                 = request.POST.get('page')
        item.position             = request.POST.get('position')
        item.state                = request.POST.get('state')
        item.cate                 = request.POST.get('category')
        if request.FILES.get('banner_img'):
            item.img = request.FILES.get('banner_img')
        item.save()
        messages.success(request, "Update Successful")
        return redirect('/news_banner_section')
    item = News_Banner.objects.filter(pk=home_banner_id)
    data = [{'title': i.title, 'page': i.page, 'banner_link_website': i.banner_link_website,
             'end_date': i.end_date, 'start_date': i.start_date, 'state': i.state,
             'category': i.cate, 'position': i.position} for i in item]
    return JsonResponse({'data': data})


@login_required
def search_content_management(request):
    is_banner_add = ""
    if request.method == "POST":
        img = request.FILES.get('img')
        User_Member(
            state=request.POST.get('state'),
            username=request.POST.get('email'),
            i_am=request.POST.get('category'),
            name=request.POST.get('name'),
            add_logo_of_instituion=img,
            region=request.POST.get('area'),
            user_web=request.POST.get('web_link'),
            user_email=request.POST.get('email'),
            name_of_concerned_person=request.POST.get('concerned_person'),
            year_of_establishment=request.POST.get('year_of_establishment'),
            contact_no=request.POST.get('contact'),
            country=request.POST.get('country'),
            address_of_institution=request.POST.get('address_of_institution'),
            name_of_institution=request.POST.get('name_of_institution'),
            start_date=request.POST.get('start_date'),
            end_date=request.POST.get('end_date'),
        ).save()
        is_banner_add = "true"
    cate        = Category.objects.all()
    state       = State.objects.all()
    area        = Area.objects.all()
    all_payment = Payment_table.objects.all()
    pay_user_ids = [user.userid for user in all_payment]
    data        = User_Member.objects.filter(is_superuser=0)
    return render(request, './Admin/search_content_management.html', {
        "message": is_banner_add, 'pay_user': pay_user_ids,
        'state': state, 'area': area, 'cate': cate, 'data': data,
    })


def search_content_management_deactive(request, home_banner_id):
    item = User_Member.objects.get(pk=home_banner_id)
    item.is_active = 0 if item.is_active == 1 else 1
    item.save()
    return JsonResponse({'data': "Deactivate Successful!" if item.is_active == 0 else "Activate Successful!"})


def search_content_management_update(request, home_banner_id):
    if request.method == "POST":
        item = User_Member.objects.get(pk=home_banner_id)
        item.state                    = request.POST.get('state')
        item.i_am                     = request.POST.get('category')
        item.username                 = request.POST.get('email')
        item.contact_no               = request.POST.get('contact')
        item.name                     = request.POST.get('name')
        item.name_of_institution      = request.POST.get('name_of_institution')
        item.address_of_institution   = request.POST.get('address_of_institution')
        item.country                  = request.POST.get('country')
        item.user_email               = request.POST.get('email')
        item.user_web                 = request.POST.get('web_link')
        item.name_of_concerned_person = request.POST.get('concerned_person')
        item.year_of_establishment    = request.POST.get('year_of_establishment')
        item.region                   = request.POST.get('area')
        item.start_date               = request.POST.get('start_date')
        item.end_date                 = request.POST.get('end_date')
        if request.FILES.get('img'):
            item.add_logo_of_instituion = request.FILES.get('img')
        item.save()
        messages.success(request, "Update Successful")
        return redirect('/search_content_management')
    item = User_Member.objects.filter(pk=home_banner_id)
    data = [{'cate': i.i_am, 'state': i.state, 'contact': i.contact_no, 'name': i.name,
             'name_of_institution': i.name_of_institution, 'address_of_institution': i.address_of_institution,
             'country': i.country, 'user_email': i.user_email, 'user_web': i.user_web,
             'name_of_concerned_person': i.name_of_concerned_person,
             'year_of_establishment': i.year_of_establishment,
             'area': i.region, 'start_date': i.start_date, 'end_date': i.end_date} for i in item]
    return JsonResponse({'data': data})


def search_banner_section(request):
    is_banner_add = ""
    if request.method == "POST":
        Search_Banner(
            state=request.POST.get('state'),
            start_date=request.POST.get('start_date'),
            end_date=request.POST.get('end_date'),
            page=request.POST.get('page'),
            title=request.POST.get('title'),
            banner_link_website=request.POST.get('banner_website_link'),
            img=request.FILES.get('banner_img'),
            position=request.POST.get('position'),
            category=request.POST.get('cate'),
            area=request.POST.get('area'),
        ).save()
        is_banner_add = "true"
    all_state       = State.objects.all()
    all_cate        = Category.objects.all()
    all_area        = Area.objects.all()
    all_search_banner = Search_Banner.objects.all()
    return render(request, './Admin/search_banner_section.html', {
        'area': all_area, 'state': all_state, 'cate': all_cate,
        'search_banner': all_search_banner, "message": is_banner_add,
    })


def search_banner_section_deactive(request, search_banner_id):
    item = Search_Banner.objects.get(pk=search_banner_id)
    item.is_active = 0 if item.is_active == "1" else 1
    item.save()
    return JsonResponse({'data': "Deactivate Successful!" if item.is_active == 0 else "Activate Successful!"})


def search_banner_section_update(request, search_banner_id):
    if request.method == "POST":
        item = Search_Banner.objects.get(pk=search_banner_id)
        item.title                = request.POST.get('title')
        item.start_date           = request.POST.get('start_date')
        item.end_date             = request.POST.get('end_date')
        item.banner_link_website  = request.POST.get('banner_website_link')
        item.page                 = request.POST.get('page')
        item.position             = request.POST.get('position')
        item.state                = request.POST.get('state')
        item.area                 = request.POST.get('area')
        item.cate                 = request.POST.get('cate')
        if request.FILES.get('banner_img'):
            item.img = request.FILES.get('banner_img')
        item.save()
        messages.success(request, "Update Successful")
        return redirect('/search_banner_section')
    item = Search_Banner.objects.filter(pk=search_banner_id)
    data = [{'title': i.title, 'page': i.page, 'banner_link_website': i.banner_link_website,
             'end_date': i.end_date, 'start_date': i.start_date, 'state': i.state,
             'category': i.category, 'position': i.position, 'area': i.area} for i in item]
    return JsonResponse({'data': data})


@login_required
def job_banner_section(request):
    is_banner_add = ""
    if request.method == "POST":
        Job_Banner(
            state=request.POST.get('state'),
            start_date=request.POST.get('start_date'),
            end_date=request.POST.get('end_date'),
            page=request.POST.get('page'),
            title=request.POST.get('title'),
            banner_link_website=request.POST.get('banner_website_link'),
            img=request.FILES.get('banner_img'),
            position=request.POST.get('position'),
            job_category=request.POST.get('job_cate'),
        ).save()
        is_banner_add = "true"
    all_state  = State.objects.all()
    job_banner = Job_Banner.objects.all()
    return render(request, "./Admin/job_banner_section.html", {
        "message": is_banner_add, 'state': all_state, 'job_banner': job_banner
    })


@login_required
def job_banner_update(request, job_id):
    if request.method == "POST":
        item = Job_Banner.objects.get(pk=job_id)
        item.title               = request.POST.get('title')
        item.start_date          = request.POST.get('start_date')
        item.end_date            = request.POST.get('end_date')
        item.banner_link_website = request.POST.get('banner_link_website')
        item.page                = request.POST.get('page')
        item.position            = request.POST.get('position')
        item.state               = request.POST.get('state')
        item.job_category        = request.POST.get('job_cate')
        if request.FILES.get('banner_img'):
            item.img = request.FILES.get('banner_img')
        item.save()
        messages.success(request, "Update Successful")
        return redirect('/job_banner_section')
    item = Job_Banner.objects.filter(pk=job_id)
    data = [{'title': i.title, 'page': i.page, 'banner_link_website': i.banner_link_website,
             'end_date': i.end_date, 'start_date': i.start_date, 'state': i.state,
             'category': i.job_category, 'position': i.position} for i in item]
    return JsonResponse({'data': data})


def job_content_management(request):
    is_job_add = ""
    if request.method == "POST":
        Job(
            job_title=request.POST.get('title'),
            job_category=request.POST.get('cate'),
            company=request.POST.get('company'),
            state=request.POST.get('state'),
            job_desc=request.POST.get('editor'),
            experience=request.POST.get('experience'),
            pub_date=request.POST.get('start_date'),
            salary=request.POST.get('salary'),
            end_date=request.POST.get('end_date'),
        ).save()
        is_job_add = "true"
    all_state = State.objects.all()
    all_job   = Job.objects.all()
    return render(request, './Admin/job_content_managmenet.html', {
        "message": is_job_add, 'state': all_state, 'job': all_job
    })


def job_content_management_deactive(request, job_id):
    item = Job.objects.get(pk=job_id)
    item.is_active = 0 if item.is_active == "1" else 1
    item.save()
    return JsonResponse({'data': "Deactivate Successful!" if item.is_active == 0 else "Activate Successful!"})


def job_content_management_update(request, job_id):
    if request.method == "POST":
        item = Job.objects.get(pk=job_id)
        item.job_title    = request.POST.get('title')
        item.pub_date     = request.POST.get('start_date')
        item.end_date     = request.POST.get('end_date')
        item.state        = request.POST.get('state')
        item.salary       = request.POST.get('salary')
        item.company      = request.POST.get('company')
        item.job_category = request.POST.get('cate')
        item.experience   = request.POST.get('experience')
        item.job_desc     = request.POST.get('editor')
        item.save()
        messages.success(request, "Update Successful")
        return redirect('/job_content_management')
    item = Job.objects.filter(pk=job_id)
    data = [{'title': i.job_title, 'company': i.company, 'state': i.state, 'salary': i.salary,
             'end_date': i.end_date, 'start_date': i.pub_date, 'exp': i.experience,
             'category': i.job_category, 'desc': i.job_desc} for i in item]
    return JsonResponse({'data': data})


def interview_banner(request):
    is_banner_add = ""
    if request.method == "POST":
        Interview_Banner(
            start_date=request.POST.get('start_date'),
            end_date=request.POST.get('end_date'),
            page=request.POST.get('page'),
            title=request.POST.get('title'),
            banner_link_website=request.POST.get('banner_website_link'),
            img=request.FILES.get('banner_img'),
            position=request.POST.get('position'),
        ).save()
        is_banner_add = "true"
    all_banner = Interview_Banner.objects.all()
    return render(request, "./Admin/interview_banner.html", {"message": is_banner_add, 'banner': all_banner})


@login_required
def interview_content_managment(request):
    is_banner_add = ""
    if request.method == "POST":
        Interview(
            title=request.POST.get('title'),
            profile=request.POST.get('profile'),
            interview_name=request.POST.get('interview_name'),
            name_of_person=request.POST.get('name_of_person'),
            institution_name=request.POST.get('institution_name'),
            desc=request.POST.get('editor'),
            img=request.FILES.get('img'),
        ).save()
        is_banner_add = "true"
    data = Interview.objects.all()
    return render(request, "./Admin/interview_content_managment.html", {"message": is_banner_add, 'data': data})


@login_required
def interview_update(request, interview_id):
    if request.method == "POST":
        item = Interview.objects.get(pk=interview_id)
        item.title            = request.POST.get('title')
        item.interview_name   = request.POST.get('interview_name')
        item.name_of_person   = request.POST.get('name_of_person')
        item.institution_name = request.POST.get('institution_name')
        item.desc             = request.POST.get('desc')
        if request.FILES.get('banner_img'):
            item.img = request.FILES.get('banner_img')
        item.save()
        messages.success(request, "Update Successful")
        return redirect('/interview_content_managment')
    item = Interview.objects.filter(pk=interview_id)
    data = [{'title': i.title, 'interview_name': i.interview_name, 'name_of_person': i.name_of_person,
             'institution_name': i.institution_name, 'desc': i.desc} for i in item]
    return JsonResponse({'data': data})


@login_required
def interview_deactive(request, interview_id):
    item = Interview.objects.get(pk=interview_id)
    item.is_active = 0 if item.is_active == "1" else 1
    item.save()
    return JsonResponse({'data': "Deactivate Successful!" if item.is_active == 0 else "Activate Successful!"})


def category(request):
    is_banner_add = ""
    if request.method == "POST":
        Category(Category=request.POST.get('category')).save()
        is_banner_add = "true"
    all_category = Category.objects.all()
    return render(request, "./Admin/Category_Add.html", {"message": is_banner_add, "categroy": all_category})


def category_deactive(request, category_id):
    item = Category.objects.get(pk=category_id)
    item.is_active = 0 if item.is_active == "1" else 1
    item.save()
    return JsonResponse({'data': "Deactivate Successful!" if item.is_active == 0 else "Activate Successful!"})


def category_update(request, category_id):
    if request.method == "POST":
        item = Category.objects.get(pk=category_id)
        item.Category = request.POST.get('category')
        item.save()
        messages.success(request, "Update Successful")
        return redirect('/category')
    item = Category.objects.filter(pk=category_id)
    data = [{'cate': i.Category} for i in item]
    return JsonResponse({'data': data})


def area(request):
    is_banner_add = ""
    if request.method == "POST":
        Area(Area_name=request.POST.get('area'), State_id=request.POST.get('state')).save()
        is_banner_add = "true"
    all_state    = State.objects.all()
    all_category = Area.objects.all()
    return render(request, "./Admin/Area.html", {"message": is_banner_add, "area": all_category, 'state': all_state})


def area_deactive(request, category_id):
    item = Area.objects.get(pk=category_id)
    item.is_active = 0 if item.is_active == "1" else 1
    item.save()
    return JsonResponse({'data': "Deactivate Successful!" if item.is_active == 0 else "Activate Successful!"})


def area_update(request, category_id):
    if request.method == "POST":
        item = Area.objects.get(pk=category_id)
        item.Area_name = request.POST.get('area')
        item.State_id  = request.POST.get('state')
        item.save()
        messages.success(request, "Update Successful")
        return redirect('/area')
    item = Area.objects.filter(pk=category_id)
    data = [{'state_id': i.State_id, 'area_name': i.Area_name} for i in item]
    return JsonResponse({'data': data})


def state(request):
    is_banner_add = ""
    if request.method == "POST":
        State(State_name=request.POST.get('state')).save()
        is_banner_add = "true"
    all_category = State.objects.all()
    return render(request, "./Admin/State.html", {"message": is_banner_add, "state": all_category})


def state_deactive(request, state_id):
    item = State.objects.get(pk=state_id)
    item.is_active = 0 if item.is_active == "1" else 1
    item.save()
    return JsonResponse({'data': "Deactivate Successful!" if item.is_active == 0 else "Activate Successful!"})


def state_update(request, state_id):
    if request.method == "POST":
        item = State.objects.get(pk=state_id)
        item.State_name = request.POST.get('state')
        item.save()
        messages.success(request, "Update Successful")
        return redirect('/state')
    item = State.objects.filter(pk=state_id)
    data = [{'state': i.State_name} for i in item]
    return JsonResponse({'data': data})


@login_required
def video_section(request):
    is_banner_add = ""
    if request.user.is_superuser:
        if request.method == "POST":
            Video_Section(
                video=clean_youtube_url(request.POST.get('youtube_video', '')),
                title=request.POST.get('title'),
                user_id=request.user.id,
            ).save()
            is_banner_add = "true"
        all_banner = Video_Section.objects.filter(user_id=request.user.id)
        return render(request, './Admin/Video_Feature.html', {"message": is_banner_add, 'banner': all_banner})
    try:
        user_payment_status = Payment_table.objects.get(userid=request.user.id).is_active
        userper = Userpermission.objects.get(userid=request.user.id)
        if user_payment_status == "1" and userper.is_active == "1" and userper.Video_Section == "1":
            if request.method == "POST":
                Video_Section(video=clean_youtube_url(request.POST.get('youtube_video', '')), title=request.POST.get('title', ''), user_id=request.user.id).save()
                is_banner_add = "true"
            all_banner = Video_Section.objects.filter(user_id=request.user.id)
            return render(request, './Admin/Video_Feature.html', {
                "message": is_banner_add, 'banner': all_banner, 'userper': userper
            })
        return redirect('/UserAccount')
    except Payment_table.DoesNotExist:
        return redirect('/UserAccount')


@login_required
def about_section(request):
    is_banner_add = ""
    if request.user.is_superuser:
        if request.method == "POST":
            About(userid=request.user.id, about=request.POST.get('editor')).save()
            is_banner_add = "true"
        all_banner = HomepageMainBanner.objects.all()
        return render(request, './Admin/Image_Feature.html', {"message": is_banner_add, 'banner': all_banner})
    try:
        user_payment_status = Payment_table.objects.get(userid=request.user.id).is_active
        userper = Userpermission.objects.get(userid=request.user.id)
        if user_payment_status == "1" and userper.is_active == "1" and userper.About == "1":
            if request.method == "POST":
                About(userid=request.user.id, about=request.POST.get('editor')).save()
                is_banner_add = "true"
            all_banner = HomepageMainBanner.objects.all()
            return render(request, './Admin/Image_Feature.html', {
                "message": is_banner_add, 'banner': all_banner, 'userper': userper
            })
        return redirect('/UserAccount')
    except Payment_table.DoesNotExist:
        return redirect('/UserAccount')
# MARKER Sat Mar 14 08:21:21 UTC 2026
