from django.urls import reverse
from django.shortcuts import redirect


class BaseAuthView:
    success_url = 'profile:profile'
    fallback_url_name = 'users:login'

    def _get_profile_url(self, user):
        """Generate the profile URL based on the user."""
        return reverse(self.success_url, kwargs={'username': user.username, 'user_id': user.id})

    def dispatch(self, request, *args, **kwargs):
        """Redirect authenticated users to their profile."""
        if request.user.is_authenticated:
            return redirect(self._get_profile_url(request.user))
        # Вызов dispatch из следующего класса в цепочке наследования
        return super().dispatch(request, *args, **kwargs) #