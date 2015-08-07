import curses


def env():
    stdscr = curses.initscr()
    curses.noecho() # Turn off echoing of keys to screen
    curses.cbreak() # Initialise curses cbreak mode
    stdscr.keypad(1)

    # set player's starting coordinates
    hero_x_pos = 1
    hero_y_pos = 1


    while 1:
    #    game(stdscr)

    #curses.nocbreak()
    #curses.echo()
    #curses.endwin()

    #def game():
        c = stdscr.getch()
    # set level map
        map = ['################', 
           '#    #    #    #',
           '#    #    #    #',
           '#              #',
           '###### #####  ##',
           '#         #    #',
           '#         #    #',
           '#         #    #',
           '#              #',
           '################',
           ]

        # render map
        for y_pos in range(10):
            for x_pos in range(16):
                stdscr.addch(y_pos, x_pos, map[y_pos][x_pos])

        if c == curses.KEY_UP and map[hero_y_pos-1][hero_x_pos]==' ':
            hero_y_pos = hero_y_pos - 1
        if c == curses.KEY_DOWN and map[hero_y_pos+1][hero_x_pos]==' ':
            hero_y_pos = hero_y_pos + 1
        if c == curses.KEY_LEFT and map[hero_y_pos][hero_x_pos-1]==' ':
            hero_x_pos = hero_x_pos - 1
        if c == curses.KEY_RIGHT and map[hero_y_pos][hero_x_pos+1]==' ':
            hero_x_pos = hero_x_pos + 1

        stdscr.addch(hero_y_pos, hero_x_pos, '@') # draw hero
        stdscr.refresh() # refresh screen, reflect changes

    curses.nocbreak()
    curses.echo()
    curses.endwin()


if __name__ == '__main__':
    env()
