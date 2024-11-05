def get_theme_from_cookie(request):
    theme = request.COOKIES.get("theme", "light")
    return {"theme": theme}
