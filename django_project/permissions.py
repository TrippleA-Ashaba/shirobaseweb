PERMISSIONS = {
    "*": (
        "add",
        "change",
        "delete",
        "view",
    ),
}

GROUP_PERMISSIONS = {
    "cs_user": (
        # "users.profile.*",
        # "organization.organization.*",
        # "organization.organizationsettings.*",
        # "organization.branch.*",
    ),
}

GROUP_PERMISSIONS["cs_admin"] = GROUP_PERMISSIONS["cs_user"] + (
    "auth.user.*",
    "auth.group.*",
)
