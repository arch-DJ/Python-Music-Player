import gi
import time
import vlc
from mutagen.mp3 import MP3
from manager import Manager

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GdkX11, GObject


class Handler:
    def __init__(self):
        self.manager = Manager(self)
        self.vlcInstance = vlc.Instance()
        self.player = self.vlcInstance.media_player_new()
        self.playing = False
        self.song_length = 0
        self.slider = builder.get_object("slider_id")
        self.volume_slider = builder.get_object("volume_slider_id")
        self.song = "f.mp3"
        self.playlist = 0

    def get_player_status(self):
        return self.playing

    def set_player_status(self, status):
        self.playing = status

    def close_app_handler(self, *args):
        Gtk.main_quit(*args)

    def about_clicked_handler(self, about):
        about_app = builder.get_object("about_app")
        about_app.show()

    def about_close_handler(self, about):
        about_app = builder.get_object("about_app")
        about_app.hide()

    def play_handler(self, button):
        label = button.get_label()

        if label == "Play":
            button.set_label("Pause")
            if self.get_player_status():
                self.player.play()


            else:
                self.set_player_status(True)
                song = MP3(self.song)
                self.song_length = song.info.length
                self.player.set_mrl(self.song)
                self.player.play()
                builder.get_object("currently_playing_id").set_label(
                    "Currently playing - " + self.manager.get_song_title(self.song))
                self.player.audio_set_volume(100)
                self.volume_slider.set_value(1)


        else:
            button.set_label("Play")
            self.player.pause()

    def stop_handler(self, button):
        play_button = builder.get_object("play_button_id")
        play_button.set_label("Play")
        self.set_player_status(False)
        self.player.stop()
        self.slider.set_value(0)

    def background(self):
        if (str(self.player.get_state()) == "State.Ended"):
            play_button = builder.get_object("play_button_id")
            play_button.set_label("Play")
            self.set_player_status(False)
            self.player.stop()
            self.slider.set_value(0)

        if (str(self.player.get_state()) == "State.Playing"):
            current_time = self.player.get_time() / 1000
            ratio = (current_time / self.song_length)
            self.slider.set_value(ratio * 100)

        return True

    def slider_handler(self, widget):
        current_time = widget.get_value()
        vlc_time = self.player.get_time() / (self.song_length * 10)

        if abs(current_time - vlc_time) > 0.1:
            self.player.set_time(int((current_time * 10) * self.song_length))

    def volume_handler(self, widget, status):
        self.player.audio_set_volume(int(widget.get_value() * 100))

    def open_file_handler(self, widget):
        file_opener = builder.get_object("file_opener_id")
        file_opener.show()

    def close_file_opener_handler(self, widget):
        file_opener = builder.get_object("file_opener_id")
        file_opener.hide()

    def open_file_button_handler(self, widget):
        file_opener = builder.get_object("file_opener_id")
        self.song = file_opener.get_filename()
        file_opener.hide()
        self.set_player_status(True)
        song = MP3(self.song)
        self.song_length = song.info.length
        self.player.set_mrl(self.song)
        self.player.play()
        builder.get_object("play_button_id").set_label("Pause")
        builder.get_object("currently_playing_id").set_label(
            "Currently playing - " + self.manager.get_song_title(self.song))


builder = Gtk.Builder()
builder.add_from_file("my.glade")
handler = Handler()
GObject.idle_add(handler.background)
builder.connect_signals(handler)
window = builder.get_object("main_window")
window.connect("delete-event", Gtk.main_quit)
window.show_all()
Gtk.main()
