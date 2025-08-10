from django.contrib.auth.models import Group
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse, NoReverseMatch
from django.apps import apps
from apps.organization.models import Program

def home_view(request):
    user = request.user
    if not user.is_authenticated:
        return redirect('account_login')
    
    s = request.session
    s['permissions'] = s.get('permissions', [])

    accessible_models_by_app = {}

    excluded_app_labels = [
        'admin',       # Django Admin
        'auth',        # Django Authentication (User, Group, Permission models)
        'contenttypes',# Django ContentTypes
        'sessions',    # Django Sessions
        'static', # Django static
    ]

    # Iterate through all installed apps
    for app_config in apps.get_app_configs():
        if app_config.label in excluded_app_labels:
            continue # Skip this app

        for model_class in app_config.get_models():
            # Skip abstract models, proxy models, or models without list views
            if model_class._meta.abstract or model_class._meta.proxy:
                continue

            app_label = model_class._meta.app_label
            model_name = model_class._meta.model_name
            verbose_name_plural = model_class._meta.verbose_name_plural or f"{model_name}s"
            verbose_name_plural = verbose_name_plural.title()

            has_rud_access = False
            if any(perm in s['permissions'] for perm in [f'change_{model_name}', f'delete_{model_name}', f'view_{model_name}']):
                has_rud_access = True

            has_add_access = False
            if f'add_{model_name}' in s['permissions']:
                has_add_access = True

            # Initialize app section if it doesn't exist
            if app_label not in accessible_models_by_app:
                app_config_obj = apps.get_app_config(app_label)
                accessible_models_by_app[app_label] = {
                    'app_name': app_config_obj.verbose_name or app_label.title(),
                    'models': []
                }

            if has_rud_access:
                try:
                    model_url = reverse(f'{app_label}:view_{model_name}')
                    accessible_models_by_app[app_label]['models'].append({
                        'name': verbose_name_plural,
                        'url': model_url,
                    })
                except NoReverseMatch:
                    pass 
            elif has_add_access: # If no RUD access, check if user can add
                try:
                    model_url = reverse(f'{app_label}:add_{model_name}')
                    accessible_models_by_app[app_label]['models'].append({
                        'name': f'Add {verbose_name_plural}',
                        'url': model_url,
                    })
                except NoReverseMatch:
                    pass

    # Remove apps with no accessible models
    context = {'accessible_models_by_app': {
        app_label: app_data 
        for app_label, app_data in accessible_models_by_app.items() 
        if app_data['models']
    }}
    return render(request, 'core/home.html', context)

@require_POST
def set_faculty(request):
    """
    Set the selected faculty for the user.
    """    
    faculty_id = request.POST.get('faculty_id')
    s = request.session
    try:
        faculty_id = int(faculty_id)
        user = request.user
        authorized = 'access_global' in s['permissions']
        if not authorized and faculty_id not in user.faculties.values_list('id', flat=True):
            return JsonResponse({'error': 'Unauthorized faculty'}, status=403)
        s['selected_faculty'] = faculty_id

        # now set the program automatically
        if authorized:
            new_program = Program.objects.filter(faculty=faculty_id).first()
        else:
            new_program = user.programs.filter(faculty=faculty_id).first()
        s['selected_program'] = new_program.id
    except:
        s['selected_faculty'] = "None"
        s['selected_program'] = "None"

    return redirect(request.META.get('HTTP_REFERER', '/'))

@require_POST
def set_program(request):
    """
    Set the selected program for the user.
    """
    program_id = request.POST.get('program_id')
    s = request.session
    try:
        program_id = int(program_id)
        user = request.user
        authorized = 'access_global' in s['permissions'] or 'access_faculty_wide' in s['permissions']
        if not authorized and program_id not in user.programs.values_list('id', flat=True):
            return JsonResponse({'error': 'Unauthorized program'}, status=403)
        s['selected_program'] = program_id
    except:
        s['selected_program'] = "None"
    return redirect(request.META.get('HTTP_REFERER', '/'))

@require_POST
def set_group(request):
    """
    Set the selected group for the user.
    """
    group_id = request.POST.get('group_id')
    s = request.session
    try:
        group_id = int(group_id)
        user = request.user
        if group_id not in user.groups.values_list('id', flat=True):
            return JsonResponse({'error': 'Unauthorized group'}, status=403)
        s['selected_group'] = group_id
        s['permissions'] = list(Group.objects.get(id=group_id).permissions.all().values_list('codename', flat=True))
    except:
        s['selected_group'] = "None"
        s['permissions'] = []
    return redirect(request.META.get('HTTP_REFERER', '/'))