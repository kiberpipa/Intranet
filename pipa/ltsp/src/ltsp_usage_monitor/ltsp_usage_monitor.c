/* draw.c - glavni program */
#include <X11/Xlib.h>
#include <stdio.h>  /* printf */
#include <stdlib.h>
#include <unistd.h> /* getuid */
#include <time.h>   /* time, ctime */
#include <string.h> /* strncpy */
#include <sys/socket.h>
#include <sys/types.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <sys/un.h>

#include "config.h"


extern Display *theDisplay;
Bool mouse_changed = False; /* if mouse position changed */
Window theWindow;           /* root window */

/* v connectX.c */
void initX();
void quitX();

/* 
 * detect_mouse()
 *
 * Detects mouse movement by comparing current values with 
 * previously measured ones.
 */
Bool detect_mouse()
{
    static int prev_X, prev_Y;
    int root_x, root_y, win_x, win_y;
    Window root_return, child_return;
    unsigned int mask;

    XQueryPointer(theDisplay, theWindow, &root_return, &child_return,
            &root_x, &root_y, &win_x, &win_y, &mask);
    
    if (prev_X != root_x || prev_Y != root_y) {
        prev_X = root_x;
        prev_Y = root_y;
        return True;   
    } else {
        return False;
    }
}


int main(int argc, char *argv[], char *envp[])
{
    uid_t     uid;
    time_t  current_time;
    char    printable_time[30] = "\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0";

    struct sockaddr_un si_me;
    int s, slen;
    char buf[BUFLEN];


    uid = getuid(); /* zapomnimo si pid */

    initX(); /* Vzpostavi zvezo s streznikom X */
    theWindow = RootWindow(theDisplay, 0); /* Odpri root okno */
    mouse_changed = detect_mouse(); /* "Kalibracija" */

    /* Loop kjer gledamo, ce se miska premika */
    while (1) {
        
        #ifdef SLEEP_TIME
        sleep(SLEEP_TIME);
        #endif

        mouse_changed = detect_mouse();
        time(&current_time);
        /* 24 je dolzina stringa, ki ga izpljune ctime */
        strncpy(printable_time, ctime(&current_time), 24);
        sprintf(buf, "%s uid %d mousemoved %d                  ", printable_time, uid, (int)mouse_changed);

        /* vsakic nova povezava, ker je server tipa select */
        if ((s=socket(AF_UNIX, SOCK_STREAM, 0))==-1)
            perror("client: socket");
        si_me.sun_family = AF_UNIX;
        strcpy(si_me.sun_path, STATS_SOCKET);
        slen = sizeof(si_me.sun_family) + strlen(si_me.sun_path);
        if (connect(s, &si_me, slen) < 0) 
            perror("client: connect");
        if (send(s, buf, BUFLEN, 0)==-1)
            perror("client: send");
        close(s);
    }
    /* Prekini povezavo streznikom X */
    quitX();
    return 0;
}

