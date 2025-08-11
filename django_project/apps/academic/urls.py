from django.urls import path
from . import views

app_name = 'academic'

urlpatterns = [
    # classroom
    path('classrooms/', views.ClassroomListView.as_view(), name='view_classroom'),
    path('classrooms/create/', views.ClassroomCreateView.as_view(), name='add_classroom'),
    path('classrooms/change/<int:pk>/', views.ClassroomUpdateView.as_view(), name='change_classroom'),
    path('classrooms/delete/<int:pk>/', views.ClassroomDeleteView.as_view(), name='delete_classroom'),
    # course
    path('courses/', views.CourseListView.as_view(), name='view_course'),
    path('courses/create/', views.CourseCreateView.as_view(), name='add_course'),
    path('courses/change/<int:pk>/', views.CourseUpdateView.as_view(), name='change_course'),
    path('courses/delete/<int:pk>/', views.CourseDeleteView.as_view(), name='delete_course'),
    # class
    path('classes/', views.ClassListView.as_view(), name='view_class'),
    path('classes/create/', views.ClassCreateView.as_view(), name='add_class'),
    path('classes/change/<int:pk>/', views.ClassUpdateView.as_view(), name='change_class'),
    path('classes/delete/<int:pk>/', views.ClassDeleteView.as_view(), name='delete_class'),
    # schedule
    path('schedules/', views.ScheduleListView.as_view(), name='view_schedule'),
    # score
    path('scores/<int:student_pk>', views.ScoreStudentListView.as_view(), name='view_score'),
    path('scores/add/<int:schedule_pk>/', views.ScoreScheduleCreateView.as_view(), name='add_score'),
    # evaluation
    path('evaluations/', views.EvaluationListView.as_view(), name='view_evaluation'),
    path('evaluations/add/<int:schedule_pk>/', views.EvaluationCreateView.as_view(), name='add_evaluation'),
    path('evaluations/delete/', views.EvaluationBulkDeleteView.as_view(), name='delete_evaluation')
]
