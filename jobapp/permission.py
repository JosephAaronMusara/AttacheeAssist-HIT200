from django.core.exceptions import PermissionDenied

def user_is_employer(function):
    def wrap(request, *args, **kwargs):   
        if request.user.role == 'employer':
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied
    return wrap

def user_is_employee(function):
    def wrap(request, *args, **kwargs):    
        if request.user.role == 'employee':
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied
    return wrap

def user_is_coordinator(function):
    def wrap(request, *args, **kwargs):    
        if request.user.role == 'coordinator':
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied
    return wrap

def user_is_supervisor(function):
    def wrap(request, *args, **kwargs):    
        if request.user.role == 'supervisor':
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied
    return wrap

def user_is_worksupervisor(function):
    def wrap(request, *args, **kwargs):    
        if request.user.role == 'worksupervisor':
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied
    return wrap