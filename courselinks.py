import logging
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

logger = logging.getLogger('uvic')

UVIC_HOME = "https://www.uvic.ca"
UVIC_SIGN_IN_LINK_SELECTOR = (
        '#glbl > div >'
        'a.glbl__lnk.glbl__lnk'
        '--signin.glbl__lnk--icon.'
        'glbl__lnk--unauth')

UVIC_COURSESPACES_SELECTOR = """#content > 
div:nth-child(3) > div.third.col 
> ul > li.moodle > a"""


def login(web, username, password):
    """login to uvic.ca on the webdriver instance"""
    # go to uvic login page
    logger.debug('getting uvic homepage')
    web.get(UVIC_HOME)
    signinbutton = chrome.find_element_by_css_selector(
            UVIC_SIGN_IN_LINK_SELECTOR)
    logger.debug('navigating to login page')
    web.get(signinbutton.get_attribute('href'))
    # type in username and password
    logger.debug('enter username and password for %s' % username)
    username_in = web.find_element_by_id('username')
    pass_in = web.find_element_by_id('password')
    for key in username:
        username_in.send_keys(key)
    for key in password:
        pass_in.send_keys(key)

    # hit enter to login
    pass_in.send_keys(Keys.ENTER)
    logger.debug('logged in to uvic.ca as %s' %username)

def get_course_pages(web):
    """Get the course links from the coursespaces main page"""
    logger.debug('navigating to coursespaces site')
    cs_link = web.find_element_by_css_selector(
            UVIC_COURSESPACES_SELECTOR).get_attribute('href')
    web.get(cs_link)
    logger.debug('looking for courses')
    courses = web.find_elements_by_class_name("course-info-container")
    course_links = [course.find_element_by_css_selector(
        'a').get_attribute('href') for course in courses]
    logger.debug(f'found {len(course_links)} courses')
    # there are some duplicate urls
    return list(set(course_links))

def pull_links_from_coursepage(web, link_to_coursepage):
    """grab all the links from the main body of the course webpage"""
    logger.debug(f'opening {link_to_coursepage}')
    web.get(link_to_coursepage)
    logger.debug(f'looking for links')
    main = web.find_elements_by_class_name('course-content')[0]
    atags = main.find_elements_by_css_selector('a')
    hrefs = [a.get_attribute('href') for a in atags]
    logger.debug(f'found {len(hrefs)} links')
    return list(set(hrefs))

options = webdriver.chrome.options.Options()
# options.add_argument('--headless')
chrome = webdriver.Chrome(options=options)
    
login(chrome, 'blakeas', '*****')
links = []
for course in get_course_pages(chrome):
    links.extend(pull_links_from_coursepage(chrome, course))
for link in links:
    print(link)
# chrome.quit()

