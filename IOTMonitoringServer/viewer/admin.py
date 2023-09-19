from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from receiver.models import City, State, Country, Location, Station, Measurement, Data

# ----------------------------------------------------------------------------------------

@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    actions_on_top = True
    actions_on_bottom = True
    actions_selection_counter = True
    list_max_show_all = 200
    list_per_page = 100
    list_select_related = True
    preserve_filters = True
    save_as = True
    save_as_continue = True
    save_on_top = False
    show_full_result_count = True
    view_on_site = False

    fieldsets = [
        (_("Identification"), {
            "description": _("City information"),
            # "classes": ("collapse", "expanded"),
            "fields": ["name", "code", ],
        },
        ),
    ]

    list_display = ("name", "code", )
    list_display_links = ("name", )
    list_filter = ("name", "code", )
    ordering = ("name", "code", )
    search_fields = ["name", "code", ]

# ----------------------------------------------------------------------------------------

@admin.register(State)
class StateAdmin(admin.ModelAdmin):
    actions_on_top = True
    actions_on_bottom = True
    actions_selection_counter = True
    list_max_show_all = 200
    list_per_page = 100
    list_select_related = True
    preserve_filters = True
    save_as = True
    save_as_continue = True
    save_on_top = False
    show_full_result_count = True
    view_on_site = False

    fieldsets = [
        (_("Identification"), {
            "description": _("State information"),
            # "classes": ("collapse", "expanded"),
            "fields": ["name", "code", ],
        },
        ),
    ]

    list_display = ("name", "code", )
    list_display_links = ("name", )
    list_filter = ("name", "code", )
    ordering = ("name", "code", )
    search_fields = ["name", "code", ]

# ----------------------------------------------------------------------------------------

@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    actions_on_top = True
    actions_on_bottom = True
    actions_selection_counter = True
    list_max_show_all = 200
    list_per_page = 100
    list_select_related = True
    preserve_filters = True
    save_as = True
    save_as_continue = True
    save_on_top = False
    show_full_result_count = True
    view_on_site = False

    fieldsets = [
        (_("Identification"), {
            "description": _("Country information"),
            # "classes": ("collapse", "expanded"),
            "fields": ["name", "code", ],
        },
        ),
    ]

    list_display = ("name", "code", )
    list_display_links = ("name", )
    list_filter = ("name", "code", )
    ordering = ("name", "code", )
    search_fields = ["name", "code", ]

# ----------------------------------------------------------------------------------------

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    actions_on_top = True
    actions_on_bottom = True
    actions_selection_counter = True
    list_max_show_all = 200
    list_per_page = 100
    list_select_related = True
    preserve_filters = True
    save_as = True
    save_as_continue = True
    save_on_top = False
    show_full_result_count = True
    view_on_site = False

    fieldsets = [
        (_("Identification"), {
            "description": _("Location information"),
            # "classes": ("collapse", "expanded"),
            "fields": ["description", ],
        },
        ),
        (_("Ubication"), {
            "description": _("Ubication information"),
            # "classes": ("collapse", "expanded"),
            "fields": ["country", "state", "city", "lat", "lng" ],
        },
        ),
        (_("Status"), {
            "description": _("Status information"),
            # "classes": ("collapse", "expanded"),
            "fields": ["active", ],
        },
        ),
    ]

    list_display = ("country", "state", "city", "active")
    list_display_links = ("country", )
    list_editable = ("active", )
    list_filter = ("country", "state", "city", "active", )
    ordering = ("country", "state", "city", "active", )
    search_fields = ["country", "state", "city", ]

# ----------------------------------------------------------------------------------------

@admin.register(Measurement)
class MeasurementAdmin(admin.ModelAdmin):
    actions_on_top = True
    actions_on_bottom = True
    actions_selection_counter = True
    list_max_show_all = 200
    list_per_page = 100
    list_select_related = True
    preserve_filters = True
    save_as = True
    save_as_continue = True
    save_on_top = False
    show_full_result_count = True
    view_on_site = False

    fieldsets = [
        (_("Identification"), {
            "description": _("Measurement information"),
            # "classes": ("collapse", "expanded"),
            "fields": ["name", "unit", ],
        },
        ),
        (_("Flags"), {
            "description": _("Flags information"),
            # "classes": ("collapse", "expanded"),
            "fields": ["min_value", "max_value" ],
        },
        ),
        (_("Status"), {
            "description": _("Status information"),
            # "classes": ("collapse", "expanded"),
            "fields": ["active", ],
        },
        ),
    ]

    list_display = ("name", "unit", "active")
    list_display_links = ("name", )
    list_editable = ("active", )
    list_filter = ("name", "unit", "active", )
    ordering = ("name", "unit", "active", )
    search_fields = ["name", "unit", ]

# ----------------------------------------------------------------------------------------

@admin.register(Station)
class StationAdmin(admin.ModelAdmin):
    actions_on_top = True
    actions_on_bottom = True
    actions_selection_counter = True
    list_max_show_all = 200
    list_per_page = 100
    list_select_related = True
    preserve_filters = True
    save_as = True
    save_as_continue = True
    save_on_top = False
    show_full_result_count = True
    view_on_site = False

    fieldsets = [
        (_("Identification"), {
            "description": _("Station information"),
            # "classes": ("collapse", "expanded"),
            "fields": ["user", "location", ],
        },
        ),
        (_("Status"), {
            "description": _("Status information"),
            # "classes": ("collapse", "expanded"),
            "fields": ["active", ],
        },
        ),
    ]

    list_display = ("user", "location", "active")
    list_display_links = ("user", )
    list_editable = ("active", )
    list_filter = ("user", "location", "active", )
    ordering = ("user", "location", "active", )
    search_fields = ["user", "location", ]

# ----------------------------------------------------------------------------------------

@admin.register(Data)
class DataAdmin(admin.ModelAdmin):
    actions_on_top = True
    actions_on_bottom = True
    actions_selection_counter = True
    list_max_show_all = 200
    list_per_page = 100
    list_select_related = True
    preserve_filters = True
    save_as = True
    save_as_continue = True
    save_on_top = False
    show_full_result_count = True
    view_on_site = False

    fieldsets = [
        (_("Time"), {
            "description": _("Time information"),
            # "classes": ("collapse", "expanded"),
            "fields": ["time", "base_time", ],
        },
        ),
        (_("Context"), {
            "description": _("Context information"),
            # "classes": ("collapse", "expanded"),
            "fields": ["station", "measurement", ],
        },
        ),
        (_("Values"), {
            "description": _("Values information"),
            # "classes": ("collapse", "expanded"),
            "fields": ["min_value", "max_value", "length", "avg_value", ],
        },
        ),
        (_("Raw"), {
            "description": _("Raw data"),
            # "classes": ("collapse", "expanded"),
            "fields": ["times", "values", ],
        },
        ),
    ]

    list_display = ("time", "station", "measurement", "min_value", "max_value", "length", "avg_value", )
    list_display_links = ("time", )
    list_filter = ("station", "measurement", )
    ordering = ("time", "station", "measurement", )
    search_fields = ["station", "measurement", ]

# ----------------------------------------------------------------------------------------
