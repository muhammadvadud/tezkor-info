from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

PAGES = [
    {
        "seperator": False,
        "items": [
            {
                "title": _("Home page"),
                "icon": "home",
                "link": reverse_lazy("admin:index"),
            }
        ],
    },
    {
        "title": _("Authentication & Users"),
        "separator": True,
        "items": [
            {
                "title": _("Users"),
                "icon": "person",
                "link": reverse_lazy("admin:accounts_user_changelist"),
            },
            {
                "title": _("Groups"),
                "icon": "groups",
                "link": reverse_lazy("admin:auth_group_changelist"),
            },
            {
                "title": _("Permissions"),
                "icon": "lock",
                "link": reverse_lazy("admin:auth_permission_changelist"),
            },
            {
                "title": _("SMS Confirmations"),
                "icon": "sms",
                "link": reverse_lazy("admin:django_core_smsconfirm_changelist"),
            },
            {
                "title": _("Signup Bonus"),
                "icon": "card_giftcard",
                "link": reverse_lazy("admin:accounts_signupbonusmodel_changelist"),
            },
        ],
    },
    {
        "title": _("Locations"),
        "separator": True,
        "items": [
            {
                "title": _("Countries"),
                "icon": "public",
                "link": reverse_lazy("admin:accounts_country_changelist"),
            },
            {
                "title": _("Regions"),
                "icon": "location_on",
                "link": reverse_lazy("admin:accounts_region_changelist"),
            },
            {
                "title": _("Districts"),
                "icon": "location_city",
                "link": reverse_lazy("admin:accounts_district_changelist"),
            },
        ],
    },
    {
        "title": _("Telegram"),
        "separator": True,
        "items": [
            {
                "title": _("User Telegram IDs"),
                "icon": "chat",
                "link": reverse_lazy("admin:accounts_usertgids_changelist"),
            },
        ],
    },
    {
        "title": _("Main Content"),
        "separator": True,
        "items": [
            {
                "title": _("Categories"),
                "icon": "category",
                "link": reverse_lazy("admin:main_categorymodel_changelist"),
            },
            {
                "title": _("Company Selections"),
                "icon": "business",
                "link": reverse_lazy("admin:main_companyselectionmodel_changelist"),
            },
            {
                "title": _("Ads"),
                "icon": "campaign",
                "link": reverse_lazy("admin:main_admodel_changelist"),
            },
            {
                "title": _("Product & Services"),
                "icon": "inventory",
                "link": reverse_lazy("admin:main_productservicemodel_changelist"),
            },
            {
                "title": _("Notifications"),
                "icon": "notifications",
                "link": reverse_lazy("admin:main_notificationmodel_changelist"),
            },
        ],
    },
    {
        "title": _("Pricing"),
        "separator": True,
        "items": [
            {
                "title": _("Price Brackets"),
                "icon": "attach_money",
                "link": reverse_lazy("admin:main_pricebracket_changelist"),
            },
            {
                "title": _("Price by Country"),
                "icon": "flag",
                "link": reverse_lazy("admin:main_pricecountrymodel_changelist"),
            },
        ],
    },
    {
        "title": _("Legal & Documents"),
        "separator": True,
        "items": [
            {
                "title": _("Legal Documents"),
                "icon": "description",
                "link": reverse_lazy("admin:main_legaldocumentsmodels_changelist"),
            },
        ],
    },
    {
        "title": _("Referral System"),
        "separator": True,
        "items": [
            {
                "title": _("Referrals"),
                "icon": "people",
                "link": reverse_lazy("admin:referral_referralmodel_changelist"),
            },
            {
                "title": _("Referral Users"),
                "icon": "person_add",
                "link": reverse_lazy("admin:referral_referralusersmodel_changelist"),
            },
            {
                "title": _("Referral History"),
                "icon": "history",
                "link": reverse_lazy("admin:referral_referralhistorymodel_changelist"),
            },
        ],
    },
    {
        "title": _("Cashback"),
        "separator": True,
        "items": [
            {
                "title": _("Cashbacks"),
                "icon": "monetization_on",
                "link": reverse_lazy("admin:payments_cashbackmodel_changelist"),
            },
            {
                "title": _("Cashback Percent"),
                "icon": "percent",
                "link": reverse_lazy("admin:payments_cashbackpercentmodel_changelist"),

            },
        ]
    },
    {
        "title": _("Settings"),
        "separator": True,
        "items": [
            {
                "title": _("Settings"),
                "icon": "settings",
                "link": reverse_lazy("admin:shared_settingsmodel_changelist"),
            },
        ],
    },
]
