from media_release_scrap__functions import *



#  -------------- SCRAPING JAPAN



#     scrap_reg_JP_BOJ(screen_name, type_of_media, link_html, is_db_accessible, is_display)
#     scrap_reg_JP_FSA(screen_name, type_of_media, link_html, is_db_accessible, is_display)


def scrap_reg_JP_FSA(screen_name, type_of_media, link_html, is_db_accessible, is_display):
    access_granted = True
    
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
    
    if not access_granted:
        return
    old_medias = get_old_media(screen_name, is_db_accessible)
    html = requests.get(link_html).text
    first_result = BeautifulSoup(html, "html.parser").find('div', id='main').find('div', class_="inner").find_all('ul')
    # we retrieve all the articles from the latest month
    regs = first_result[1].find_all('li')
    for reg in regs:
        link_2nd_part = str(reg.find('a').get('href'))
        # only get the news if contains "/en/news"
        if not link_2nd_part.startswith("/en/news"):
            continue
        
        link = "https://www.fsa.go.jp/" + link_2nd_part
        
        article_html = requests.get(link).text
        article_soup = BeautifulSoup(article_html, "html.parser")
        title = article_soup.find('h1', class_="a-center").text
        date = article_soup.find_all('p', class_="a-right")[1].text
        date_string = date.split(" Financial Services Agency")[0]
        date_str = date_string.replace(',','').split(' ')
        # date in the format year-month-day
        date = datetime(int(date_str[2]),int(month_dict[date_str[0]]), int(date_str[1]))
        date_to_id = date.strftime('%y%m%d')
        id = text_format(title.lower(), date=date_to_id, is_id=True).replace(' ', '')
        description = article_soup.find('p', class_="indent").text
        first_sentence = ""
        for char in description:
            first_sentence += char
            if char == '.' or char == '!' or char == '?':
                break
        first_sentence = text_format(first_sentence, is_description=True)
        generate_new_media(screen_name, id, date, title, first_sentence, link, type_of_media, old_medias,
               is_db_accessible, is_display)


#  -------------- INIT JAPAN



#     init_reg_JP_BOJ(is_db_accessible, is_display)
#     init_reg_JP_FSA(is_db_accessible, is_display)
# FSA | Financial Services Agency 
def init_reg_JP_FSA(is_db_accessible, is_display):
    screen_name = "FSA"
    
    # Press release
    type_of_media = "Press Release"
    html_link = "https://www.fsa.go.jp/en/news/index.html"
    try:
        scrap_reg_JP_FSA(screen_name, type_of_media, html_link, is_db_accessible, is_display)
    except Exception as e:
        print(screen_name, "-", type_of_media, "-", "Error:", e)


#  -------------- LAUNCH JAPAN



# def launch_scrap_HK(is_db_accessible, is_display):
    # init_reg_HK_HKMA(is_db_accessible, is_display)
    # init_reg_HK_SFC(is_db_accessible, is_display)



#  -------------- MAIN JAPAN



if __name__ == '__main__':
    # CONNECTION TO SANDYEDGE
    db_accessible = True
    # db_accessible = False

    # DISPLAY CONSOLE
    # display = True
    display = False

    # launch_scrap_JP(db_accessible, display)

