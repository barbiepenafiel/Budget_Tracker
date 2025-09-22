from django.contrib.auth import login
from django.contrib.auth.models import User

class VercelSessionPersistenceMiddleware:
    """
    Custom middleware to help with session persistence on Vercel.
    Since Vercel has ephemeral storage, this helps restore sessions.
    """
    
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if user is not authenticated but has valid session data
        if not request.user.is_authenticated:
            user_id = request.session.get('user_id')
            username = request.session.get('username')
            is_authenticated = request.session.get('is_authenticated')
            
            if user_id and username and is_authenticated:
                # Try to restore the user's session
                try:
                    user = User.objects.get(id=user_id, username=username)
                    login(request, user)
                    # Refresh session flags
                    request.session['user_id'] = user.id
                    request.session['username'] = user.username
                    request.session['is_authenticated'] = True
                    request.session.modified = True
                except User.DoesNotExist:
                    # Clear invalid session data
                    if 'user_id' in request.session:
                        del request.session['user_id']
                    if 'username' in request.session:
                        del request.session['username']
                    if 'is_authenticated' in request.session:
                        del request.session['is_authenticated']
                    request.session.modified = True
        
        response = self.get_response(request)
        return response
