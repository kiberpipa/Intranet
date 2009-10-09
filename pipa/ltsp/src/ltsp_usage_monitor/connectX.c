/* connectX.c koda za komunikacijo s streznikom X */
#include <stdlib.h>
#include <stdio.h>
#include <X11/Xlib.h>   /* /usr/include/X11, /usr/local/include/X11 */
#include <X11/Xutil.h>

/* program - wide globals */
Display *theDisplay;            /* kazalec na strukturo prikazovalnika */
int     theScreen;              /* kateri zaslon na prikazovalniku */
int     theDepth;               /* stevilo bitnih ravnin */
                                /* globina barvne ravnine */
unsigned long theBlackPixel;    /* sistemska crna barva */
unsigned long theWhitePixel;    /* sistemska bela barva */

/*
** initx(): vzpostavi zvezo s streznikom X
** (na mrezi) in shrani informacijo o okolju
*/

void initX()
{
    theDisplay = XOpenDisplay(NULL); /* ime prikazovalnika */
                                     /* kam gre izhod streznika X */
    if (theDisplay == NULL) {        /* preveri povezavo */
    fprintf(stderr,
                "Error: Cannot connect to the X server %s\n",
                 XDisplayName(NULL));
       exit(1);
   }

   theScreen = DefaultScreen(theDisplay);
                       /* kateri zaslon je v uporabi */
   theDepth  = DefaultDepth(theDisplay, theScreen);
                       /* 1: monokromatski zaslon */
   theBlackPixel = BlackPixel(theDisplay, theScreen);
   theWhitePixel = WhitePixel(theDisplay, theScreen);
}

/*
** Prekine zvezo s streznikom X
*/
void quitX()
  {
   XCloseDisplay(theDisplay);
 }

