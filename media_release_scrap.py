from media_release_scrap_AU import *
from media_release_scrap_EU import *
from media_release_scrap_HK import *
# from media_release_scrap_ID import *
# from media_release_scrap_IN import *
from media_release_scrap_INT import *
# from media_release_scrap_JP import *
# from media_release_scrap_KR import *
# from media_release_scrap_MY import *
# from media_release_scrap_SG import *
from media_release_scrap_US import *



#  -------------- MAIN WORLDWIDE



if __name__ == '__main__':
    # CONNECTION TO SANDYEDGE
    db_accessible = True
    # db_accessible = False

    # DISPLAY CONSOLE
    # display = True
    display = False

    launch_scrap_AU(db_accessible, display)

    launch_scrap_INT(db_accessible, display)

    launch_scrap_EU(db_accessible, display)
    launch_scrap_HK(db_accessible, display)
    launch_scrap_US(db_accessible, display)

    # Todo
    # launch_scrap_ID(db_accessible, display)
    # launch_scrap_IN(db_accessible, display)
    # launch_scrap_JP(db_accessible, display)
    # launch_scrap_KR(db_accessible, display)
    # launch_scrap_MY(db_accessible, display)
    # launch_scrap_SG(db_accessible, display)



