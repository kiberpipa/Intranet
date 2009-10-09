
all:
	gcc ltsp_usage_monitor.c connectX.c -I/usr/include -I/usr/local/include -I/usr/X11R6/include -L/usr/lib -L/usr/local/lib -L/usr/X11R6/lib -lX11 -Wall -o ltsp_usage_monitor

clean:
	rm ltsp_usage_monitor

install:
	install -o root -g root -m 755 ltsp_usage_monitor /usr/local/bin/ltsp_usage_monitor
	install -o root -g root -m 755 ltsp_monitor_dispatcher /usr/local/bin/ltsp_monitor_dispatcher
	for u in t1 t2 t3 t4 t5 t6 t7 t8 t9 t10; do install -d /home/ltsp/$${u}/.config ; install -d /home/ltsp/$${u}/.config/autostart ; install -o $${u} -g dezurni -m 644 ltsp_usage_monitor.desktop /home/ltsp/$${u}/.config/autostart/ltsp_usage_monitor.desktop ; done
