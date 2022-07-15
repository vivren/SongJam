// CLEINT SIDE

var socket;
    $(document).ready(function(){
        socket = io.connect('http://' + document.domain + ':' + location.port + '/chat');

        var player;
        var playerState;
        var tag = document.createElement('script');
        tag.src = "https://www.youtube.com/iframe_api";
        var scriptTag = document.getElementsByTagName('script')[0];
        scriptTag.parentNode.insertBefore(tag, scriptTag);


        function onPlayerReady(event) {
            event.target.playVideo();
        }

        function onPlayerStateChange(event) {
            playerState = event.data;
            if (event.data == YT.PlayerState.PAUSED) {
                playVideo()
            }
            if (event.data == YT.PlayerState.ENDED) {
                socket.emit('end');
                socket.emit('displayPlaylist');
            }
        }

        function playVideo() {
            player.playVideo();
        }

        // function unmute() {
        //     player.unMute();
        // }

        function update() {
            socket.emit('timeUpdate', {time: player.getCurrentTime()});
        }

        socket.on('connect', function() {
            socket.emit('joined', {});
            socket.emit('displayPlaylist');
        });

        socket.on('status', function(data) {
            $('#activityLog').val($('#activityLog').val() + '<' + data.msg + '>\n');
            $('#activityLog').scrollTop($('#activityLog')[0].scrollHeight);
        });

        socket.on('playlist', function(data) {
             if (data.playlist.length == 0) {
                 $("#videos").append('<h5>Play a song using the search bar.</h5>');
             } else {
                 $("#videos").empty();
                 for (let i=0; i<data.playlist.length; i++) {
                     $('#videos').append('<li>' + data.playlist[i].split(",")[0].toString() + '</li>');
                 }
             }
        });

        socket.on('update', function() {
            update();
        });

        socket.on('time', function(data) {
            $('#current').append(`<option id="${Math.round(data.time)}" value="${data.time}">${data.time}</option>`);
            $('#' + Math.round(data.time)).attr('selected', 'selected').parent().focus();
            $('#' + Math.round(data.time)).parent().change();
        });

        socket.on("searchResults", function(data) {
            if (data.results === false) {
                $('#searchResults').append('<h3>No results for "' + data.search + '".</h3>')
                $('#searchResults').append('<p>Check your spelling or try a different search term.</p>')
            } else {
                $('#searchResults').empty();
            }
        });

        var first = true;
        socket.on('video', function(data) {
            if (first) {
                first = false;
                var currTime = $('#current').val()
                player = new YT.Player('player', {
                    width: '100%',
                    videoId: data.id,
                    playerVars: {
                        'start': Math.round(currTime),
                        'autoplay': 1,
                        'mute': 1,
                        'controls': 0,
                        'origin': "https://www.youtube.com",
                        'rel': 0,
                        'showinfo': 0
                    },
                    allow: 'autoplay',
                    events: {
                        'onReady': onPlayerReady,
                        'onStateChange': onPlayerStateChange
                    }
                });
            } else {
                player.loadVideoById(data.id);
            }
        });

        // socket.on('unmute', function() {
        //     unmute();
        // });

        $('#text').keypress(function(e) {
           var code = e.keyCode || e.which;
           if (code == 13) {
               text = $('#text').val();
               $('#text').val('');
               socket.emit('addSong', {song: text});
               socket.emit('displayPlaylist');
               if ((playerState == YT.PlayerState.ENDED) || (typeof player == 'undefined')) {
                   socket.emit('displayVideo');
               }
           }
        });

        $('#current').change(function() {
            socket.emit('displayVideo');
        });
    });

    function leave_room() {
        socket.emit('left', {}, function() {
            socket.disconnect();
            window.location.href = "{{ url_for('index') }}";
        });
    }
