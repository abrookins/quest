

def auth_token(token):
    """
    A token stored for a user.

    Format: token:[token]
    """
    return f"token:{token}"


def admin_goals_dashboard():
    """
    The rendered Admin Goals Dashboard.

    Format: admin:goals-dashboard
    """
    return "admin:goals-dashboard"


def task():
    """
    Task data.

    Format: task:[id]
    """
