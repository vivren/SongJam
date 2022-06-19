var socket;

            $(document).ready(function(){
                socket = io.connect('http://' + document.domain + ':' + location.port + '/chat');

                var player;
                var tag = document.createElement('script');
                tag.src = "https://www.youtube.com/iframe_api";
                var scriptTag = document.getElementsByTagName('script')[0];
                scriptTag.parentNode.insertBefore(tag, scriptTag);

                // function onYouTubeIframeAPIReady() {}

                function onPlayerReady(event) {
                    event.target.playVideo();
                }

                function onPlayerStateChange(event) {
                    $('#current').text(player.getCurrentTime());
                    playVideo()
                    socket.emit('timeUpdate', {time: player.getCurrentTime()});
                }

                function playVideo() {
                    player.playVideo();
                }

                function pauseVideo() {
                    player.pauseVideo();
                }

                function seekTo() {
                    player.seekTo(6, true);
                }

                socket.on('connect', function(client) {
                    socket.emit('joined', {});
                    socket.emit('displayPlaylist');
                    socket.emit('pause');
                    socket.emit('displayVideo');
                    socket.emit('updateVideo');
                });

                socket.on('status', function(data) {
                    $('#activityLog').val($('#activityLog').val() + '<' + data.msg + '>\n');
                    $('#activityLog').scrollTop($('#activityLog')[0].scrollHeight);
                });

                socket.on('playlist', function(data) {
                     $('#videos').empty();
                     for (let i=0; i<data.msg.length; i++){
                         $('#videos').append('<li>' + data.msg[i].split(",")[0] + '</li>');
                     }
                });

                socket.on('pauseVideo', function() {
                    pauseVideo();
                });

                socket.on('updatedVideo', function() {
                    seekTo();
                });

                var first = true;
                socket.on('video', function(data) {
                    if (first) {
                        // first = false;
                        // var currTime = $('#activityLog').val().split(">\n<")[length($('#activityLog').val().split(">\n<"))-1]
                        player = new YT.Player('player', {
                            width: '100%',
                            videoId: data.video,
                            playerVars: {
                                'autoplay': 1,
                                'mute': 1,
                                'controls': 0,
                                'origin': "https://www.youtube.com"},
                                'rel': 0,
                                'showinfo': 0,
                            allow: 'autoplay',
                            events: {
                                'onReady': onPlayerReady,
                                'onStateChange': onPlayerStateChange
                            }
                        });
                    } else {
                        // player.loadVideoById({videoId: data.video, startSeconds: data.time});
                    //     player.loadVideoById({videoId: data.video, startSeconds: 6.32});
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
                   }});
            });
            function leave_room() {
                socket.emit('left', {}, function() {
                    socket.disconnect();
                    window.location.href = "{{ url_for('index') }}";
                });
            }
