
from media_release_scrap__functions import *


# ACCC | Australian Competition and Consumer Commission
def init_reg_AU_ACCC(is_db_accessible, is_display):
    screen_name = "ACCC"

    # Media Release
    try:
        type_of_media = "Media Release"
        html_link = "https://www.accc.gov.au/media/media-releases"
        scrap_reg_AU_ACCC(screen_name, type_of_media, html_link, is_db_accessible, is_display)
    except Exception as e:
        print(screen_name, "-", type_of_media, "-", "Error:", e)



def scrap_reg_AU_ACCC(screen_name, type_of_media, link_html, is_db_accessible, is_display):
    access_granted = True

    month_dict = {"Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4, "May": 5, "Jun": 6,
                  "Jul": 7, "Aug": 8, "Sep": 9, "Oct": 10, "Nov": 11, "Dec": 12}

    try:
        html = requests.get(link_html, proxies=get_proxies(), timeout=10).text
    except Exception as e:
        try:
            sleep(5)
            html = requests.get(link_html, proxies=get_proxies(), timeout=50).text
        except Exception as e:
            access_granted = False
            if is_display:
                print(screen_name, " - Error:", e)



    if access_granted:  
        old_medias = get_old_media(screen_name, is_db_accessible)
        html = requests.get(link_html).text
        soup = BeautifulSoup(html, "html.parser").find('div', {'class': 'view-content'})
        regs = soup.select("div[class^=views-row]")

        for reg in regs:
            is_data = True
            link = "https://www.accc.gov.au" + reg.find('a').get('href')
            title = reg.find('a').text.strip()
            title = text_format(title)
            
            
            date_str = str(reg.find('span').text.strip())
            date_str = str(date_str).split(' ')
            date = datetime(int(date_str[2]), month_dict[date_str[1]], int(date_str[0]))
            date_to_id = date.strftime('%y%m%d')
            id = text_format(link, date=date_to_id, is_id=True)
            html = requests.get(link).text
            try:
                html = requests.get(link, proxies=get_proxies(), timeout=10).text
            except Exception as e:
                access_granted = False
                print(screen_name, " - Error:", e)

            description = ""
            if access_granted:
                soup = BeautifulSoup(html, "html.parser")
                soup = soup.find_all('div', {'class': 'field-item even'})

                if soup != []:
                    description = soup[1].find('p').getText(separator='\t')
                    description = text_format(description, is_description=True)
            link = text_format(link)


            generate_new_media(screen_name, id, date, title, description, link, type_of_media, old_medias,
                               is_db_accessible, is_display)
            
            
if __name__ == "__main__":
    init_reg_AU_ACCC(True, True)
    

    