import curses
import colorama

from .storage import ArticleDb

def display_ui_base(stdscr,mode_str : str):
    stdscr.clear()
    mx,my = stdscr.getmaxyx()

    #frame draw
    stdscr.addstr(0,0,"ArxivReader : "+mode_str,curses.color_pair(1))
    stdscr.addstr(1,0,'-'*(my-1))
    stdscr.addstr(mx-1,0,'-'*(my-1))
    stdscr.addstr(mx-3,0,'-'*(my-1))

    stdscr.addstr(mx-2,1,">",curses.color_pair(1))





def ui_main():
    colorama.init()

    stdscr = curses.initscr()
    curses.start_color()

    curses.init_color(curses.COLOR_WHITE, 1000, 1000, 1000);


    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)


    #curses.noecho()
    curses.cbreak()


    adb = ArticleDb()



    current_mode = "help menu"

    last_in = ""
    st = {}



    modes_list = [
        "Unread articles",
        "Unread articles (alert)",
        "Favorite articles",
        "Saved articles",
        "All articles"]

    while True:

        mx,my = stdscr.getmaxyx()
        display_ui_base(stdscr,current_mode)


        if current_mode in modes_list:
            art = st["artlst"][st["index"]]
            
            

            str_auth = ""
            for a in art["authors"][:-1]:
                str_auth += a + ", "
            str_auth += art["authors"][-1]

            str_cnt = "("+str(st["index"]+1)+","+str(len(st["artlst"]))+")"

            stdscr.addstr(2,my - 10,str_cnt)

            stdscr.addstr(4,2,art["title"],curses.color_pair(2))
            stdscr.addstr(7,2,str_auth,curses.color_pair(3))
            stdscr.addstr(10,2,art["abstract"].replace("\n","\n  "),curses.color_pair(1))

            #stdscr.addstr(4,2,get_article_string(art))


        
        stdscr.move(mx-2,4)
        last_in = stdscr.getstr()

        if last_in in [b'exit',b'quit'] :
            break
        if last_in == b'fetch':
            adb.fetch_articles()



        if last_in == b'show all':
            current_mode = "All articles"
            st["artlst"] = adb.get_all_arts()
            st["index"] = 0

        if last_in == b'show saved':
            current_mode = "Saved articles"
            st["artlst"] = adb.get_saved_arts()
            st["index"] = 0
        
        if last_in == b'show fav':
            current_mode = "Favorite articles"
            st["artlst"] = adb.get_favorites_arts()
            st["index"] = 0

        if last_in == b'show unread':
            current_mode = "Unread articles"
            st["artlst"] = adb.get_unread_arts()
            st["index"] = 0

        if last_in == b'show unread alert':
            current_mode = "Unread articles (alert)"
            st["artlst"] = adb.get_unread_alert_arts()
            st["index"] = 0



        if current_mode in modes_list:
            if last_in == b'':
                st["index"] += 1

            if last_in in [b'r',b'read']:
                art = st["artlst"][st["index"]]

                adb.set_read(art["hash"])
                st["artlst"].remove(art)

                if st["index"] > len(st["artlst"]) - 1:
                    st["index"] = len(st["artlst"]) - 1

            if last_in == b'save':
                art = st["artlst"][st["index"]]
                adb.save_art(art["hash"])

            if last_in == b'star':
                art = st["artlst"][st["index"]]
                adb.swicth_favorite(art["hash"])

            if last_in == b'open':
                art = st["artlst"][st["index"]]
                adb.save_art(art["hash"])
                adb.open_art(art["hash"])

                








        


        
        

    curses.nocbreak()
    #stdscr.keypad(True)
    #curses.echo()
    curses.endwin()

