from media_release_scrap__functions import *



#  -------------- SCRAPING AMERICA



# ABA | American Bankers Association
def scrap_reg_US_ABA(screen_name, type_of_media, link_html, is_db_accessible, is_display):
    access_granted = True

    proxy = urllib.request.ProxyHandler(get_proxies())

    try:
        feed = feedparser.parse(link_html, handlers=[proxy])
    except Exception as e:
        try:
            sleep(5)
            feed = feedparser.parse(link_html, handlers=[proxy])
        except Exception as e:
            access_granted = False
            if is_display:
                print(screen_name, " - Error:", e)

    if access_granted:
        old_medias = get_old_media(screen_name, is_db_accessible)

        for post in feed.entries:
            date = datetime.fromtimestamp(mktime(post.updated_parsed))
            title = post.title
            title = text_format(title)

            link = post.link

            description = ""

            try:
                html = requests.get(link, proxies=get_proxies(), timeout=10).text
            except Exception as e:
                access_granted = False
                print("Error:", e)

            if access_granted:
                soup = BeautifulSoup(html, "html.parser").find_all('div', {'class': 'aba-field page-content'})

                if soup != []:
                    content = soup[0].find_all('div', {'class': 'ms-rtestate-field'})

                    if content != []:
                        description = content[0].getText(separator='\t')
                        description = text_format(description, is_description=True)

                    link = text_format(link)
                    date_to_id = date.strftime('%y%m%d')
                    id = text_format(link, date=date_to_id, is_id=True)

                    generate_new_media(screen_name, id, date, title, description, link, type_of_media, old_medias,
                                       is_db_accessible, is_display)


# FRB | Federal Reserve Board
def scrap_reg_US_FRB(screen_name, type_of_media, link_html, is_db_accessible, is_display):
    access_granted = True

    proxy = urllib.request.ProxyHandler(get_proxies())

    try:
        feed = feedparser.parse(link_html, handlers=[proxy])
    except Exception as e:
        try:
            sleep(5)
            feed = feedparser.parse(link_html, handlers=[proxy])
        except Exception as e:
            access_granted = False
            if is_display:
                print(screen_name, " - Error:", e)

    if access_granted:
        old_medias = get_old_media(screen_name, is_db_accessible)

        for post in feed.entries:
            date = datetime.fromtimestamp(mktime(post.updated_parsed))

            title = post.title
            title = text_format(title)

            link = post.link
            link = text_format(link)

            date_to_id = date.strftime('%y%m%d')
            id = text_format(link, date=date_to_id, is_id=True)

            if hasattr(post, 'dcterms_abstract'):
                description = post.dcterms_abstract
            else:
                description = post.summary

            description = text_format(description, is_description=True)

            generate_new_media(screen_name, id, date, title, description, link, type_of_media, old_medias,
                               is_db_accessible, is_display)


# OCC | Office of the Comptroller of the Currency
def scrap_reg_US_OCC(screen_name, type_of_media, link_html, is_db_accessible, is_display):
    access_granted = True

    proxy = urllib.request.ProxyHandler(get_proxies())

    try:
        feed = feedparser.parse(link_html, handlers=[proxy])
    except Exception as e:
        try:
            sleep(5)
            feed = feedparser.parse(link_html, handlers=[proxy])
        except Exception as e:
            access_granted = False
            if is_display:
                print(screen_name, " - Error:", e)

    if access_granted:
        old_medias = get_old_media(screen_name, is_db_accessible)

        for post in feed.entries:
            date = datetime.fromtimestamp(mktime(post.updated_parsed))

            title = post.title
            title = text_format(title)

            link = post.link
            link = link.replace("?utm_source=RSS_feed&utm_medium=RSS", '')
            link = text_format(link)

            date_to_id = date.strftime('%y%m%d')
            id = text_format(link, date=date_to_id, is_id=True)

            if hasattr(post, 'dcterms_abstract'):
                description = post.dcterms_abstract
            else:
                description = post.summary

            description = text_format(description, is_description=True)

            generate_new_media(screen_name, id, date, title, description, link, type_of_media, old_medias,
                               is_db_accessible, is_display)


# SEC | Securities and Exchange Commission
def scrap_reg_US_SEC(screen_name, type_of_media, link_html, is_db_accessible, is_display):
    access_granted = True

    proxy = urllib.request.ProxyHandler(get_proxies())

    try:
        feed = feedparser.parse(link_html, handlers=[proxy])
    except Exception as e:
        try:
            sleep(5)
            feed = feedparser.parse(link_html, handlers=[proxy])
        except Exception as e:
            access_granted = False
            if is_display:
                print(screen_name, " - Error:", e)

    if access_granted:
        old_medias = get_old_media(screen_name, is_db_accessible)

        for post in feed.entries:
            date = datetime.fromtimestamp(mktime(post.published_parsed))

            title = post.title
            title = text_format(title)

            link = post.link
            link = text_format(link)

            date_to_id = date.strftime('%y%m%d')
            id = text_format(link, date=date_to_id, is_id=True)

            description = BeautifulSoup(post.summary, "html.parser").get_text()
            description = text_format(description, is_description=True)

            generate_new_media(screen_name, id, date, title, description, link, type_of_media, old_medias,
                               is_db_accessible, is_display)



#  -------------- INIT AMERICA



# ABA | American Bankers Association
def init_reg_US_ABA(is_db_accessible, is_display):
    screen_name = "ABA"

    # News Release
    try:
        type_of_media = "News Release"
        html_link = "http://www.aba.com/Rss/PressRssXml.aspx"
        scrap_reg_US_ABA(screen_name, type_of_media, html_link, is_db_accessible, is_display)
    except Exception as e:
        print(screen_name, "-", type_of_media, "-", "Error:", e)


# FRB | Federal Reserve Board
def init_reg_US_FRB(is_db_accessible, is_display):
    screen_name = "FRB"

    # Banking and Consumer Regulatory Policy"
    try:
        type_of_media = "Banking and Consumer Regulatory Policy"
        html_link = "https://www.federalreserve.gov/feeds/press_bcreg.xml"
        scrap_reg_US_FRB(screen_name, type_of_media, html_link, is_db_accessible, is_display)
    except Exception as e:
        print(screen_name, "-", type_of_media, "-", "Error:", e)

    # Enforcement Actions
    try:
        type_of_media = "Enforcement Actions"
        html_link = "https://www.federalreserve.gov/feeds/press_enforcement.xml"
        scrap_reg_US_FRB(screen_name, type_of_media, html_link, is_db_accessible, is_display)
    except Exception as e:
        print(screen_name, "-", type_of_media, "-", "Error:", e)

    # Monetary Policy
    try:
        type_of_media = "Monetary Policy"
        html_link = "https://www.federalreserve.gov/feeds/press_monetary.xml"
        scrap_reg_US_FRB(screen_name, type_of_media, html_link, is_db_accessible, is_display)
    except Exception as e:
        print(screen_name, "-", type_of_media, "-", "Error:", e)

    # Research Paper
    try:
        type_of_media = "Research Paper"
        html_link = "https://www.federalreserve.gov/feeds/working_papers.xml"
        scrap_reg_US_FRB(screen_name, type_of_media, html_link, is_db_accessible, is_display)
    except Exception as e:
        print(screen_name, "-", type_of_media, "-", "Error:", e)


# OCC | Office of the Comptroller of the Currency
def init_reg_US_OCC(is_db_accessible, is_display):
    screen_name = "OCC"

    # News Release
    try:
        type_of_media = "News Release"
        html_link = "https://www.occ.gov/rss/occ_news.xml"
        scrap_reg_US_OCC(screen_name, type_of_media, html_link, is_db_accessible, is_display)
    except Exception as e:
        print(screen_name, "-", type_of_media, "-", "Error:", e)


# SEC | Securities and Exchange Commission
def init_reg_US_SEC(is_db_accessible, is_display):
    screen_name = "SEC"

    # Press Release
    try:
        type_of_media = "Press Release"
        html_link = "https://www.sec.gov/news/pressreleases.rss"
        scrap_reg_US_SEC(screen_name, type_of_media, html_link, is_db_accessible, is_display)
    except Exception as e:
        print(screen_name, "-", type_of_media, "-", "Error:", e)



#  -------------- LAUNCH AMERICA



def launch_scrap_US(is_db_accessible, is_display):
    init_reg_US_FRB(is_db_accessible, is_display)
    init_reg_US_OCC(is_db_accessible, is_display)
    init_reg_US_SEC(is_db_accessible, is_display)


#  -------------- MAIN AMERICA



if __name__ == '__main__':
    # CONNECTION TO SANDYEDGE
    # is_db_accessible = True
    is_db_accessible = False

    # DISPLAY CONSOLE
    # is_display = True
    is_display = False

    #init_reg_US_FRB(is_db_accessible, is_display)
    #init_reg_US_OCC(is_db_accessible, is_display)
    #init_reg_US_SEC(is_db_accessible, is_display)

    #OLD
    #init_reg_US_ABA(is_db_accessible, is_display)
