from media_release_scrap__functions import *



#  -------------- SCRAPING HONG-KONG



# HKMA | Hong Kong Monetary Authority
def scrap_reg_HK_HKMA(screen_name, type_of_media, link_html, is_db_accessible, is_display):
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
            title = post.title
            title = text_format(title)

            if "Tender Results" in title:
                continue

            date = datetime.fromtimestamp(mktime(post.updated_parsed))
            date = date + timedelta(days=1)

            link = post.link

            # Take the first line
            html = requests.get(link, proxies=get_proxies(), timeout=10).text
            soup_desc = BeautifulSoup(html, "html.parser")
            description = soup_desc.find('div', {"class": re.compile( r'template-content-area')})
            description = str(description.get_text().strip())
            description = ' '.join(re.split(r'(?<=[.:;])\s', description)[:1])
            try:
                html = requests.get(link, proxies=get_proxies(), timeout=10).text
            except Exception as e:
                access_granted = False
                print(screen_name, " - Error:", e)

            if access_granted:
                soup = BeautifulSoup(html, "html.parser").find_all('div', {'id': 'content'})
                if len(soup):
                    if len(soup[0].find_all('p')[0].text) > 20:
                        description = soup[0].find_all('p')[0].text.strip()
                    else:
                        description = soup[0].find_all('p')[1].text.strip()

                    description = text_format(description, is_description=True)

            link = text_format(link)

            date_to_id = date.strftime('%y%m%d')
            id = text_format(link, date=date_to_id, is_id=True)

            generate_new_media(screen_name, id, date, title, description, link, type_of_media, old_medias,
                               is_db_accessible, is_display)



#  -------------- INIT HONG-KONG



# HKMA | Hong Kong Monetary Authority
def init_reg_HK_HKMA(is_db_accessible, is_display):
    screen_name = "HKMA"

    # Press Release
    try:
        type_of_media = "Press Release"
        html_link = "http://www.hkma.gov.hk/eng/other-information/rss/rss_press-release.xml"
        scrap_reg_HK_HKMA(screen_name, type_of_media, html_link, is_db_accessible, is_display)
    except Exception as e:
        print(screen_name, "-", type_of_media, "-", "Error:", e)


# def init_reg_HK_SFC(is_db_accessible, is_display):
#     screen_name = "HKMA"

#     scrap_reg_HK_SFC(screen_name, type_of_media, link_html, is_db_accessible, is_display)


#  -------------- LAUNCH HONG-KONG



def launch_scrap_HK(is_db_accessible, is_display):
    init_reg_HK_HKMA(is_db_accessible, is_display)



#  -------------- MAIN HONG-KONG



if __name__ == '__main__':
    # CONNECTION TO SANDYEDGE
    # is_db_accessible = True
    is_db_accessible = False

    # DISPLAY CONSOLE
    is_display = True
    # is_display = False

   # init_reg_HK_HKMA(is_db_accessible, is_display)
   #init_reg_HK_SFC(is_db_accessible, is_display)

