from base_settings import *
    
TELNET_PORTS = [4000]
#WEBSERVER_PORTS = [(4001, 4005)]
SERVERNAME = "Ithir"
GAME_SLOGAN = "The Return to Glory"
USE_TZ = True

# try:
#    from server.conf.secret_settings import *
# except ImportError:
#    print("secret_settings.py file not found or failed to import.")


######################################################################
# Contrib config
######################################################################
# if SEND_GAME_INDEX:
#     GAME_INDEX_LISTING = {
#         'game_status': 'beta',
#         # Optional, comment out or remove if N/A.
#         'game_website': 'http://ithirmush.org',
#         'short_description': 'High fantasy MUSH in an original setting',
#         # Optional but highly recommended. Markdown is supported.
#         'long_description': (
#             "Ithir is a MUX-style game in an original high-fantasy setting, "
#             "inspired by Tolkien and set in an Elven society at odds. "
#         ),
#         'listing_contact': 'admin@ithirmush.org',
#         # At minimum, specify this or the web_client_url options. Both is fine, too.
#         'telnet_hostname': 'ithirmush.org',
#         'telnet_port': 4000,
#         # At minimum, specify this or the telnet_* options. Both is fine, too.
#         'web_client_url': 'http://ithirmush.org/webclient/',
#     }
