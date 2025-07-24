def user_profile_path(instance, filename):
    # You can customize this path
    return f'user_profiles/{instance.user.id}/{filename}'