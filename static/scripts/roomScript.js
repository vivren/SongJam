// CLEINT SIDE

var socket;
    $(document).ready(function(){
        socket = io.connect('http://' + document.domain + ':' + location.port + '/chat');

        var player;
        var tag = document.createElement('script');
        tag.src = "https://www.youtube.com/iframe_api";
        var scriptTag = document.getElementsByTagName('script')[0];
        scriptTag.parentNode.insertBefore(tag, scriptTag);


        function onPlayerReady(event) {
            event.target.playVideo();
        }

        function onPlayerStateChange(event) {
            playVideo()
            //     socket.emit('timeUpdate', {time: player.getCurrentTime()});
        }

        function playVideo() {
            player.playVideo();
        }

        function update() {
            socket.emit('timeUpdate', {time: player.getCurrentTime()});
        }

        socket.on('connect', function() {
            socket.emit('joined', {});
        });

        socket.on('status', function(data) {
            $('#activityLog').val($('#activityLog').val() + '<' + data.msg + '>\n');
            $('#activityLog').scrollTop($('#activityLog')[0].scrollHeight);
        });

        socket.on('time', function(data) {
            // $('#current').val($('#current').val() + ' ' + data.time + ' ');
            $('#current').append(`<option id="${data.time}" value="${data.time}">${data.time}</option>`);
            $('#' + data.time).attr('selected', 'selected').parent().focus();
            $("#3").parent().change();
            $('#activityLog').val($('#activityLog').val() + '< time updated >\n');
        });

        // function newOption() {
        //     $('#activityLog').val($('#activityLog').val() + '< time updated >\n');
        //     $("#3").attr('selected', 'selected').parent().focus();
        //     $("#3").parent().change();
        // }

        socket.on('playlist', function(data) {
             $('#videos').empty();
             for (let i=0; i<data.playlist.length; i++){
                 $('#videos').append('<li>' + data.playlist[i].split(",")[0].toString() + '</li>');
             }
        });

        socket.on('update', function() {
            update();
        });

       // socket.on('newOption', function() {
       //      $('#activityLog').val($('#activityLog').val() + '< time updated >\n');
       //      $('#current').val("0");
       //  });

        var first = true;
        socket.on('video', function(data) {
            if (first) {
                var currTime = $('#current').val()
                currTime = currTime.split(" ");
                currTime = currTime.sort(function(a, b) {
                    return a - b;
                });
                player = new YT.Player('player', {
                    width: '100%',
                    videoId: data.video,
                    playerVars: {
                        'start': Math.round(currTime[currTime.length-1]),
                        'autoplay': 1,
                        'mute': 1,
                        'controls': 0,
                        'origin': "https://www.youtube.com",
                        'rel': 0,
                        'showinfo': 0},
                    allow: 'autoplay',
                    events: {
                        'onReady': onPlayerReady,
                        'onStateChange': onPlayerStateChange
                    }
                });
            $('#activityLog').val($('#activityLog').val() + '< player loaded >\n');
            }
        });

        $('#text').keypress(function(e) {
           var code = e.keyCode || e.which;
           if (code == 13) {
               text = $('#text').val();
               $('#text').val('');
               socket.emit('addSong', {song: text});
               socket.emit('displayPlaylist');
               socket.emit('displayVideo')
           }
        });

        $('#current').change(function() {
            $('#activityLog').val($('#activityLog').val() + '< function called >\n');
            socket.emit('displayVideo');
        });

    });
    function leave_room() {
        socket.emit('left', {}, function() {
            socket.disconnect();
            window.location.href = "{{ url_for('index') }}";
        });
    }
