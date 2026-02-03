import locale

def get_system_language():
    lang, _ = locale.getdefaultlocale()
    if not lang:
        return "es" # Default to Spanish if locale is not detected
    return lang.split("_")[0]
