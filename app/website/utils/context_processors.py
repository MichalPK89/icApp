from website.models import Item, UserSettings
from website.utils_file import get_translation

def global_variables(request):
    user = request.user
    home = get_translation('home')
    user_profile = get_translation('user_profile')
    logout = get_translation('logout')
    reports = get_translation('reports')
    add_record = get_translation('add_record')
    submit = get_translation('submit')
    back = get_translation('back')
    delete = get_translation('delete')
    update = get_translation('update')
    update_record = get_translation('update_record')

    return {
        'user': user,
        'home': home,
        'user_profile': user_profile,
        'logout': logout,
        'reports': reports,
        'add_record': add_record, 
        'submit': submit, 
        'back': back,
        'delete': delete,
        'update': update,
        'update_record': update_record
    }