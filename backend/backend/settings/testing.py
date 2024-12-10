from .common import *

DEBUG = True

MIDDLEWARE = ["debug_toolbar.middleware.DebugToolbarMiddleware"] + MIDDLEWARE

INSTALLED_APPS += ["debug_toolbar", "template_profiler_panel", "pyflame"]

INTERNAL_IPS = [
    "127.0.0.1",
]

DEBUG_TOOLBAR_PANELS = [
    "debug_toolbar.panels.history.HistoryPanel",
    "debug_toolbar.panels.versions.VersionsPanel",
    "debug_toolbar.panels.timer.TimerPanel",
    "debug_toolbar.panels.settings.SettingsPanel",
    "debug_toolbar.panels.headers.HeadersPanel",
    "debug_toolbar.panels.request.RequestPanel",
    "debug_toolbar.panels.sql.SQLPanel",
    "debug_toolbar.panels.staticfiles.StaticFilesPanel",
    "debug_toolbar.panels.templates.TemplatesPanel",
    "debug_toolbar.panels.alerts.AlertsPanel",
    "debug_toolbar.panels.cache.CachePanel",
    "debug_toolbar.panels.signals.SignalsPanel",
    "debug_toolbar.panels.redirects.RedirectsPanel",
    "debug_toolbar.panels.profiling.ProfilingPanel",
    "template_profiler_panel.panels.template.TemplateProfilerPanel",
    "cachalot.panels.CachalotPanel",
    "pyflame.djdt.panel.FlamegraphPanel",
]

CSP_SCRIPT_SRC = "'self' 'unsafe-inline' 'unsafe-eval'"

CSP_INCLUDE_NONCE_IN = []
