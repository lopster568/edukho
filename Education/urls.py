from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

app_name = 'Education'
urlpatterns = [
    path('robots.txt', TemplateView.as_view(template_name="robots.txt", content_type="text/plain")),
    path('ads.txt', TemplateView.as_view(template_name="ads.txt", content_type="text/plain")),
    path('', views.homepage, name='homepage'),
    path('job_data_read/<int:job_id>', views.job_data_read, name='job_data_read'),
    path('get_data/<int:stateid>', views.get_data, name='get_data'),
    path('get_states', views.get_states, name='get_states'),
    path('job_statewise/<int:stateid>', views.job_statewise, name='job_statewise'),
    path('random_news', views.random_news, name='random_news'),
    path('News', views.news, name='news'),
    path('EmailVerify/<str:email>', views.verifyEmail, name='verify_email'),
    path('search', views.search, name='search'),
    path('video', views.video, name='video'),
    path('News/news_filter', views.news_filter, name='news_filter'),
    path('News/news_filter/', views.news_filter, name='news_filter_slash'),
    path('News/<slug:news_slug>', views.singlenews, name='singlenews'),
    path('Non_Teaching', views.Non_Teaching, name="non_teaching" ),
    path('Interveiw', views.interview, name='interview'),
    path('Interview/<int:interview_id>', views.single_interview, name='single_interview'),
    path('Interview_delete/<int:plan_id>', views.interview_banner_delete, name='interview_banner_delete'),
    path('Job', views.job, name='job'),
    path('Login_form', views.login_form, name='login_form'),
    path('demo_news', views.demo_news, name="demo_news"),
    path('Contact', views.contact, name='contact'),
    path('Sign_form', views.sign_form, name='sign_form'),
    path('user_info_profile/<int:userid>', views.user_info_profile, name='user_info_profile'),
    path('UserAccount', views.UserAccount, name='UserAccount'),
    path('User_job', views.User_job, name='User_job'),
    path('Event_activity', views.Event_activity, name='Event_activity'),
    path('event_management', views.event_management, name='event_management'),
    path('event_deactivate/<int:event_id>', views.event_deactivate, name='event_deactivate'),
    path('event_update/<int:event_id>', views.event_update, name='event_update'),
    path('event_gallery/<int:event_id>', views.event_gallery, name='event_gallery'),
    path('event_image_delete/<int:image_id>', views.event_image_delete, name='event_image_delete'),
    path('User_Feature', views.User_Feature, name='User_Feature'),
    path('send_email', views.send_html_email, name='send_html_email'),
    path('job_send_email', views.job_send_html_email, name='job_send_html_email'),
    path('accounts/', include('allauth.urls')),  # Include allauth's default authentication URLs
    path('accounts/', include('allauth.socialaccount.urls')),  # Include social authentication URLs
 # Your custom URL for Google login
    path('google_verify', views.google_verify, name='google_verify'),
    # path('Login_form/google/callback/', views.google_callback_view, name='google_callback'),

    # admin here

    path('admin_show', views.admin_show, name='admin_show'),

    path('homepage_banner', views.homepage_banner, name='homepage_banner'),
    path('homepage_banner/<int:home_banner_id>', views.homepage_banner_deactive, name='homepage_banner_deactive'),
    path('job_banner/<int:home_banner_id>', views.job_banner_deactive, name='job_banner_deactive'),
    path('job_banner_update/<int:job_id>', views.job_banner_update, name='job_banner_update'),

    path('video_section/<int:home_banner_id>', views.video_section_deactive, name='video_section_deactive'),
    path('homepage_banner_update/<int:home_banner_id>', views.homepage_banner_update, name='homepage_banner_update'),
    path('news_management_section', views.news_management_section, name='news_management_section'),
    path('news_management_section/<int:home_banner_id>', views.news_management_section_deactive, name='news_management_section_deactive'),
    path('news_management_section_update/<int:home_banner_id>', views.news_management_section_update, name='news_management_section_update'),
    path('news_banner_section', views.news_banner_section, name='news_banner_section'),
    path('news_banner_section/<int:home_banner_id>', views.news_banner_section_deactive, name='news_banner_section_deactive'),
    path('news_banner_section_update/<int:home_banner_id>', views.news_banner_section_update, name='news_banner_section_update'),

    path('search_content_management', views.search_content_management, name='search_content_management'),

    path('search_content_management_deactive/<int:home_banner_id>', views.search_content_management_deactive, name='search_content_management_deactive'),
    path('search_content_management_update/<int:home_banner_id>', views.search_content_management_update, name='search_content_management_update'),

    path('search_banner_section', views.search_banner_section, name='search_banner_section'),
    path('search_banner_section/<int:search_banner_id>', views.search_banner_section_deactive, name='search_banner_section_deactive'),
    path('search_banner_section_update/<int:search_banner_id>', views.search_banner_section_update, name='search_banner_section_update'),
    path('job_banner_section', views.job_banner_section, name='job_banner_section'),
    path('video_section', views.video_section, name='video_section'),
    path('about_section', views.about_section, name='about_section'),
    path('job_content_management', views.job_content_management, name='job_content_management'),
    path('job_content_management/<int:job_id>', views.job_content_management_deactive, name='job_content_management_deactive'),
    path('job_content_management_update/<int:job_id>', views.job_content_management_update, name='job_content_management_update'),

    path('interview_banner', views.interview_banner, name='interview_banner'),
    path('interview_deactive/<int:interview_id>', views.interview_deactive, name='interview_deactive'),
    path('interview_update/<int:interview_id>', views.interview_update, name='interview_update'),
    path('interview_delete/<int:interview_id>', views.interview_delete, name='interview_delete'),
    path('interview_content_managment', views.interview_content_managment, name='interview_content_managment'),
    path('category', views.category, name='category'),
    path('category/<int:category_id>', views.category_deactive, name='category_deactive'),
    path('category_update/<int:category_id>', views.category_update, name='category_update'),
    path('paid_user_is_active/<int:plan_id>', views.paid_user_is_active, name='paid_user_is_active'),
    path('paid_user_is_active_delete/<int:plan_id>', views.deleteplan, name='deleteplan'),
    path('deletehomebanner/<int:plan_id>', views.deletehomebanner, name='deletehomebanner'),
    path('deletenewsbanner/<int:plan_id>', views.deletenewsbanner, name='deletenewsbanner'),
    path('delete_job_content_managment/<int:plan_id>', views.delete_job_content_managment, name='delete_job_content_managment'),
    path('deletesearch/<int:plan_id>', views.deletesearch, name='deletesearch'),
    path('banner_search_delete/<int:plan_id>', views.banner_search_delete, name='banner_search_delete'),
    path('newdelete/<int:plan_id>', views.newdelete, name='newdelete'),
    path('delete_video/<int:plan_id>', views.delete_video, name='delete_video'),
    path('job_banner_delete/<int:plan_id>', views.job_banner_delete, name='job_banner_delete'),
    path('area', views.area, name='area'),

    path('area/<int:category_id>', views.area_deactive, name='area_deactive'),
    path('area_update/<int:category_id>', views.area_update, name='area_update'),
    path('state', views.state, name='state'),
    path('state/<int:state_id>', views.state_deactive, name='state_deactive'),
    path('state_update/<int:state_id>', views.state_update, name='state_update'),
    path('plan/<str:plan_id>', views.plan, name='plan'),

    path('logoutuser', views.logoutuser, name='logoutuser'),

    path('about', views.about, name='about'),
    path('advertising', views.advertising, name='advertising'),
    path('term_condition', views.term_condition, name='term_condition'),
    path('privacy', views.privacy, name='privacy'),
    path('work_with_us', views.work_with_us, name='work_with_us'),
    path('events', views.events, name='events'),

    path('footer_section', views.footer_section, name='footer_section'),
    path('footer_section/<int:footer_id>', views.footer_section_deactive, name='footer_section_deactive'),
    path('footer_section_update/<int:footer_id>', views.footer_section_update, name='footer_section_update'),
]