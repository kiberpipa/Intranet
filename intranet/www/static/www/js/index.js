/* 
    custom javascript for the frontpage
        - mailing list subscription
        - event carousel
*/
$(document).ready(function() {

    function zero_pad(num, places) {
      var zero = places - num.toString().length + 1;
      return Array(+(zero > 0 && zero)).join("0") + num;
    }

    $('#subscribe_mailinglist').keypress(function (e) {
        var self = $(this);
        $('.response').text("Prosim pritisnite Enter za potrditev vnosa")
        if (e.which === 13) {
            e.preventDefault();
            $.ajax({
                type: "POST",
                data: self.serialize(),
                url: self.attr('action'),
                success: function (text) {
                    self.find('i').text(text);
                },
                error: function (text) {
                    self.find('i').text("Nekaj je slo narobe, poskusite znova kasneje!");
                }
            });
        }
     });

    var render_events = function (url) {
      $.getJSON(url, function(o) {
        var i,
            event_,
            events_container = $('#events_content'),
            num_of_events,
            el;

        // add links to menu arrows
        $('#events_menu .prev').data('href', o.prev_url);
        $('#events_menu .next').data('href', o.next_url);

        // clear all events for display
        events_container.empty();

        for (i = 0; i < 7; i++) {
          var event_ = o.events[i],
              num_of_events = event_.events.length,
              el = $('#events_menu .day' + i);
              el.html('<span class="visible-tablet">' + event_.short_date + '</span><span class="hidden-tablet">' + event_.date + '</span>');
          if (event_.is_today === true && $('#events_menu .btn-inverse').length === 0) {
            el.addClass('btn-inverse');
          }
          if (num_of_events > 0) {
            el.prepend('<span class="badge">' + num_of_events + '</span>&nbsp;');
          }

          // render events divs
          $.each(event_.events, function(index, value) {
            var hide = $('#events_menu .day' + i + '.btn-inverse').length ? '' : 'hide';
            events_container.append([
              '<div class="pipa-event row-fluid ' + hide + ' day' + i + '" style="margin-bottom: 20px">',
                '<div class="span5 ac">',
                  '<a href="'+ value.url + '" style="display: inline-block">',
                    '<img class="span5 img-rounded visible-desktop" src="' + value.image + '" style="height: 200px; width: 385px" />',
                    '<img class="span5 img-rounded hidden-desktop" src="' + value.image + '" style="height: 130px; width: 250px" />',
                  '</a>',
                '</div>',
                '<div class="span7">',
                  '<h4><a href="'+ value.url + '">' + value.project + ': ' + value.title + '</a></h4>',
                  '<span class="badge badge-inverse">ob ' + moment(value.start_date).format('HH:mm') + ', ' + value.place + '</span>',
                  '<br /><br />',
                  '<p>' + value.announce + '</p>',
                '</div>',
              '</div>'
            ].join('\n'));

            if (value.is_streaming) {
              $('.hero-unit').prepend([
                 '<p class="alert alert-success ac">',
                 'Trenutno prenašamo v živo dogodek <a href="' + livestream + '">' + value.title + '</a>.',
                 '</p>',
              ].join('\n'));
            }
          });
          noevents();
        }
      });
    };

    render_events('/ajax/index/events/');

    $('#events_menu .navigation').click(function (e) {
      var that = $(this),
          href;
      e.preventDefault();
      href = that.data('href');
      render_events(href);
    });

    // map day buttons to actions
    $('#events_menu .day').click(function (e) {
      var day = $(this).data('day');
      $('.pipa-event').addClass('hide');
      $('.pipa-event.day' + day).removeClass('hide');
      $('#events_menu .day').removeClass('btn-inverse');
      $('#events_menu .day' + day).addClass('btn-inverse');
      noevents();
    });

    // if we have no events on selected day, say so
    function noevents() {
      $('#noevents').remove();
      if ($('.pipa-event').not('.hide').length === 0) {
        $('#events_content').prepend([
         '<h4 id="noevents" class="ac">',
           noevents_msg,
         '</h4>',
        ].join('\n'));
      }
    }
 });

