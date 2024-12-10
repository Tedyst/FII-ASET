from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required


def documents_approved_required(view_func):
    @login_required
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_verified:
            return HttpResponseForbidden(
                "Account not verified. Please wait for admin approval."
            )
        return view_func(request, *args, **kwargs)

    return _wrapped_view
