from app.menu.user_menu import UserMenu
from app.utils.log_handler import log_app

log_app("application_started","main")
UserMenu.show_user_menu()
# from app.dashboard.admin.admin_dashboard import AdminDashboard

# AdminDashboard.show_dashboard()