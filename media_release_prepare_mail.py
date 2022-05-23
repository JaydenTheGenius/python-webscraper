from send_mail import *
from media_release_scrap import *


def retrieve_regulatory_update(screen_name, name_to_display, from_date, is_display_date=False):
    db = init_database()
    mail_content = ""

    sql_query = "SELECT id, title, release_date, description, link, short_link, type_of_media " \
                "FROM regulation_media " \
                "WHERE screen_name = '" + screen_name + "' " \
                "AND release_date >= '" + from_date + "' " \
                "ORDER BY release_date DESC, title DESC;"

    sql_result = db.execute(sql_query)
    records = sql_result.fetchall()

    id_pos = 0
    title_pos = 1
    release_date_pos = 2
    description_pos = 3
    link_pos = 4
    short_link_pos = 5
    type_of_media = 6

    if records:
        mail_content += html_deloitte_begin_block(name_to_display)

        for record in records:
            if record[short_link_pos] != "":
                link = str(record[short_link_pos])
            else:
                link = str(record[link_pos])

            mail_content += "<a href='" + link + "'>" + str(record[title_pos]) + "</a><br>"
            mail_content += "<p><i>"

            if is_display_date:
                mail_content += (record[release_date_pos]).strftime('%d/%m') + " "

            mail_content += str(record[type_of_media]) + "</i>"

            if str(record[description_pos]) != "":
                mail_content += " - " + str(record[description_pos])

            mail_content += "</p>"

        # mail_content += html_deloitte_end_block()

    return mail_content



def prepare_regulatory_update(from_date, is_australia_only=False, is_display_date=False, type_of_subscriber="Internal"):
    mail_content = ""

# ---- AUSTRALIA
    mail_content += prepare_regulatory_update_AU(from_date, is_display_date=is_display_date, type_of_subscriber=type_of_subscriber)

    if not is_australia_only:
# ---- INTERNATIONAL
        mail_content += prepare_regulatory_update_INT(from_date, type_of_subscriber=type_of_subscriber)

# ---- United States
        mail_content += prepare_regulatory_update_US(from_date, type_of_subscriber=type_of_subscriber)

# ---- EUROPE
        mail_content += prepare_regulatory_update_EUR(from_date, type_of_subscriber=type_of_subscriber)

# ---- ASIA
        mail_content += prepare_regulatory_update_ASIA(from_date, type_of_subscriber=type_of_subscriber)


# ---- HONG KONG







    return mail_content


def prepare_regulatory_update_AU(from_date, is_display_date=False, type_of_subscriber="Internal"):
    mail_content = ""

    # ---- AUSTRALIA
    regulation_content = ""

    if type_of_subscriber == "Super":
        regulation_content += retrieve_regulatory_update("AASB", "AASB | Australian Accounting Standards Board", from_date, is_display_date)
    regulation_content += retrieve_regulatory_update("ACCC", "ACCC | Australian Competition and Consumer Commission", from_date, is_display_date)
    regulation_content += retrieve_regulatory_update("AEMO", "AEMO | Australian Energy Market Operator", from_date, is_display_date)
    if type_of_subscriber == "Super":
        regulation_content += retrieve_regulatory_update("AFSA", "AFSA | Australian Financial Security Authority", from_date, is_display_date)
    regulation_content += retrieve_regulatory_update("AIST", "AIST | Australian Institute of Superannuation Trustees", from_date, is_display_date)
    regulation_content += retrieve_regulatory_update("APRA", "APRA | Australian Prudential Regulation Authority", from_date, is_display_date)
    regulation_content += retrieve_regulatory_update("ARENA", "ARENA | Australian Renewable Energy Agency", from_date, is_display_date)
    regulation_content += retrieve_regulatory_update("ASIC", "ASIC | Australian Securities and Investments Commission", from_date, is_display_date)
    if type_of_subscriber == "Super":
        regulation_content += retrieve_regulatory_update("ASX", "ASX | Australian Securities Exchange", from_date, is_display_date)
    regulation_content += retrieve_regulatory_update("ATO", "ATO | Australian Taxation Authority", from_date, is_display_date)
    regulation_content += retrieve_regulatory_update("AUSTRAC", "AUSTRAC | Australian Transaction Reports and Analysis Centre", from_date, is_display_date)
    regulation_content += retrieve_regulatory_update("Treasury_AU", "Australian Government | The Treasury", from_date)
    regulation_content += retrieve_regulatory_update("Minister_for_Finance_AU", "Australian Government | Minister for Finance", from_date)
    if type_of_subscriber == "Super":
        regulation_content += retrieve_regulatory_update("CBA", "CBA | Commonwealth Bank of Australia", from_date)
        regulation_content += retrieve_regulatory_update("CFR", "CFR | Council of Financial Regulators", from_date)
    if type_of_subscriber == "Super":
        regulation_content += retrieve_regulatory_update("CIO", "CIO | Credit & Investments Ombudsman", from_date)
    regulation_content += retrieve_regulatory_update("FIRB", "FIRB | Foreign Investment Review Board", from_date)
    if type_of_subscriber == "Super":
        regulation_content += retrieve_regulatory_update("FOS", "FOS | Financial Ombudsman Service Australia", from_date)
    regulation_content += retrieve_regulatory_update("FSC", "FSC | Financial Services Council", from_date)
    regulation_content += retrieve_regulatory_update("FSI", "FSI | Financial System Inquiry", from_date)
    regulation_content += retrieve_regulatory_update("NSW_Industry", "NSW Industry | State of New South Wales through The NSW Department of Industry", from_date)
    regulation_content += retrieve_regulatory_update("RBA", "RBA | Reserve Bank of Australia", from_date)
    if type_of_subscriber == "Super":
        regulation_content += retrieve_regulatory_update("WBC", "WBC | Westpac", from_date)

    if regulation_content != "":
        mail_content += html_deloitte_block_country("Australia")
        mail_content += regulation_content

    return mail_content



def prepare_regulatory_update_INT(from_date, type_of_subscriber="Internal"):
    mail_content = ""

    # ---- INTERNATIONAL
    regulation_content = ""

    regulation_content += retrieve_regulatory_update("BIS", "BIS | Bank for International Settlements", from_date)
    if type_of_subscriber == "Super":
        regulation_content += retrieve_regulatory_update("CREDITSUISSE", "Credit Suisse | Research Institute", from_date)
    regulation_content += retrieve_regulatory_update("FSB", "FSB | Financial Stability Board", from_date)
    regulation_content += retrieve_regulatory_update("IFRS", "IFRS | International Financial Reporting Standards", from_date)
    if type_of_subscriber == "Super":
        regulation_content += retrieve_regulatory_update("IOSCO", "IOSCO | International Organization of Securities Commissions", from_date)
        regulation_content += retrieve_regulatory_update("KWM", "KWM | King & Wood Mallesons", from_date)
        regulation_content += retrieve_regulatory_update("MS", "MS | Morgan Stanley", from_date)
        regulation_content += retrieve_regulatory_update("PIMCO", "PIMCO", from_date)
        regulation_content += retrieve_regulatory_update("ROBECO", "ROBECO | The Investment Engineers", from_date)

    if regulation_content != "":
        mail_content += html_deloitte_block_country("International")
        mail_content += regulation_content

    return mail_content





def prepare_regulatory_update_US(from_date, type_of_subscriber="Internal"):
    mail_content = ""

    # ---- UNITED STATES
    regulation_content = ""

    regulation_content += retrieve_regulatory_update("ABA", "ABA | American Bankers Association", from_date)
    regulation_content += retrieve_regulatory_update("FRB", "FRB | Federal Reserve Board", from_date)
    regulation_content += retrieve_regulatory_update("OCC", "OCC | Office of the Comptroller of the Currency", from_date)
    regulation_content += retrieve_regulatory_update("SEC", "SEC | Securities and Exchange Commission", from_date)

    if regulation_content != "":
        mail_content += html_deloitte_block_country("United States")
        mail_content += regulation_content

    return mail_content





def prepare_regulatory_update_EUR(from_date, type_of_subscriber="Internal"):
    mail_content = ""

    # ---- EUROPE
    regulation_content = ""

    regulation_content += retrieve_regulatory_update("EBA", "EBA | European Banking Authority", from_date)
    regulation_content += retrieve_regulatory_update("ECB", "ECB | European Central Bank", from_date)
    if type_of_subscriber == "Super":
        regulation_content += retrieve_regulatory_update("ECB_BS", "EBS | European Banking Supervision", from_date)

    if regulation_content != "":
        mail_content += html_deloitte_block_country("Europe")
        mail_content += regulation_content


    # ---- ENGLAND
    regulation_content = ""

    if type_of_subscriber == "Super":
        regulation_content += retrieve_regulatory_update("BOE", "BoE | Bank of England", from_date)
        regulation_content += retrieve_regulatory_update("BOE_PRA", "PRA | Prudential Regulation Authority | Bank of England", from_date)

    if regulation_content != "":
        mail_content += html_deloitte_block_country("England", is_sub_country=True)
        mail_content += regulation_content


    # ---- FRANCE
    regulation_content = ""

    if type_of_subscriber == "Super":
        regulation_content += retrieve_regulatory_update("BdF", "BdF | Banque de France", from_date)
        regulation_content += retrieve_regulatory_update("BNP", "BNP Paribas | Economic Research", from_date)
        regulation_content += retrieve_regulatory_update("CACIB", "CA-CIB | Credit Agricole CIB", from_date)
        regulation_content += retrieve_regulatory_update("NGAM", "NGAM | Natixis Global Asset Management", from_date)

    if regulation_content != "":
        mail_content += html_deloitte_block_country("France", is_sub_country=True)
        mail_content += regulation_content


    # ---- GERMANY
    regulation_content = ""

    if type_of_subscriber == "Super":
        regulation_content += retrieve_regulatory_update("??", "DB | Deutsche Bundesbank", from_date)

    if regulation_content != "":
        mail_content += html_deloitte_block_country("Germany", is_sub_country=True)
        mail_content += regulation_content


    # ---- ITALY
    regulation_content = ""

    if type_of_subscriber == "Super":
        regulation_content += retrieve_regulatory_update("BOI", "BoI | Bank of Italy", from_date)

    if regulation_content != "":
        mail_content += html_deloitte_block_country("Italy", is_sub_country=True)
        mail_content += regulation_content

    return mail_content





def prepare_regulatory_update_ASIA(from_date, type_of_subscriber="Internal"):
    mail_content = ""

    # ---- HONG KONG
    regulation_content = ""

    regulation_content += retrieve_regulatory_update("HKMA", "HKMA | Hong Kong Monetary Authority", from_date)
    if type_of_subscriber == "Super":
        regulation_content += retrieve_regulatory_update("SFC", "SFC | Securities and Futures Commission", from_date)


    if regulation_content != "":
        mail_content += html_deloitte_block_country("Hong Kong")
        mail_content += regulation_content


    return mail_content





def prepare_regulatory_update_OTHER(from_date, type_of_subscriber="Internal"):
    regulation_content = ""
    mail_content = ""

    # ---- INDIA
    regulation_content = ""

    if regulation_content != "":
        mail_content += html_deloitte_block_country("India")
        mail_content += regulation_content



        # ---- INDONESIA
    regulation_content = ""

    if regulation_content != "":
        mail_content += html_deloitte_block_country("Indonesia")
        mail_content += regulation_content



        # ---- JAPAN
    regulation_content = ""

    if regulation_content != "":
        mail_content += html_deloitte_block_country("Japan")
        mail_content += regulation_content



        # ---- MALAYSIA
    regulation_content = ""

    if regulation_content != "":
        mail_content += html_deloitte_block_country("Malaysia")
        mail_content += regulation_content



        # ---- SINGAPORE
    regulation_content = ""

    if regulation_content != "":
        mail_content += html_deloitte_block_country("Singapore")
        mail_content += regulation_content

    return mail_content