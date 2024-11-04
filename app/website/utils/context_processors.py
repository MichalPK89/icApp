from website.models import Item, UserSettings
from website.utils_file import get_translation

def global_variables(request):
    user = request.user
    user_profile = get_translation('user_profile')
    logout = get_translation('logout')
    add_record = get_translation('add_record')
    submit = get_translation('submit')
    back = get_translation('back')

    return {
        'user': user,
        'user_profile': user_profile,
        'logout': logout, 
        'add_record': add_record, 
        'submit': submit, 
        'back': back
    }