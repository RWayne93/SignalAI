import browser_cookie3
import json


def extract_cookie(domain_name: str, *cookie_names: str):
    browsers = [
        browser_cookie3.chrome,
        browser_cookie3.chromium,
        browser_cookie3.opera,
        browser_cookie3.opera_gx,
        browser_cookie3.brave,
        browser_cookie3.edge,
        browser_cookie3.vivaldi,
        # browser_cookie3.firefox,
        browser_cookie3.librewolf,
        browser_cookie3.safari,
    ]

    cookie_values = [None] * len(cookie_names)

    for browser_fn in browsers:
        try:
            cj = browser_fn(domain_name=domain_name)
            for cookie in cj:
                for i, cookie_name in enumerate(cookie_names):
                    if cookie.name == cookie_name:
                        cookie_values[i] = cookie.value
                        if all(cookie_values):
                            return cookie_values[0] if len(cookie_values) == 1 else tuple(cookie_values)
        except:
            continue

    return cookie_values[0] if len(cookie_values) == 1 else tuple(cookie_values)



def extract_bard_cookie():
    return extract_cookie(".google.com", "__Secure-1PSID", "__Secure-1PSIDTS")


def extract_claude_cookie():
    return extract_cookie("claude.ai", "sessionKey")

# def extract_bard_cookie():
#     """
#     Extract token cookie from browser.
#     Supports all modern web browsers and OS

#     Returns:
#         Tuple[str, str]: __Secure-1PSID and __Secure-1PSIDTS cookie values
#     """

#     # browser_cookie3.load is similar function but it's broken
#     # So here we manually search accross all browsers
#     browsers = [
#         browser_cookie3.chrome,
#         browser_cookie3.chromium,
#         browser_cookie3.opera,
#         browser_cookie3.opera_gx,
#         browser_cookie3.brave,
#         browser_cookie3.edge,
#         browser_cookie3.vivaldi,
#        # browser_cookie3.firefox,
#         browser_cookie3.librewolf,
#         browser_cookie3.safari,
#     ]

#     cookie_psid = None
#     cookie_psidts = None

#     for browser_fn in browsers:
#         # if browser isn't installed browser_cookie3 raises exception
#         # hence we need to ignore it and try to find the right one
#         try:
#             cj = browser_fn(domain_name=".google.com")
#             for cookie in cj:
#                 if cookie.name == "__Secure-1PSID" and cookie.value.endswith("."):
#                     cookie_psid = cookie.value
#                 if cookie.name == '__Secure-1PSIDTS':
#                     cookie_psidts = cookie.value
#                 if cookie_psid and cookie_psidts:
#                     return cookie_psid, cookie_psidts
#         except:
#             continue
#     return cookie_psid, cookie_psidts


# def extract_claude_cookie():

#     browsers = [
#         browser_cookie3.chrome,
#         browser_cookie3.chromium,
#         browser_cookie3.opera,
#         browser_cookie3.opera_gx,
#         browser_cookie3.brave,
#         browser_cookie3.edge,
#         browser_cookie3.vivaldi,
#         browser_cookie3.firefox,
#         browser_cookie3.librewolf,
#         browser_cookie3.safari,
#     ]

#     session_key = None

#     for browser_fn in browsers:
#         try:
#             cj = browser_fn(domain_name="claude.ai")
#             for cookie in cj:
#                 if cookie.name == "sessionKey":
#                     session_key = cookie.value
#                     return session_key
#         except:
#             continue

#     return session_key

def get_group_info(group_name):
    with open('groups.json') as f:
        groups = json.load(f)

    for group in groups:
        if group['name'] == group_name:
            return group['id'], group['internal_id']

    return None, None

# print(extract_bard_cookie())
# print(extract_claude_cookie())