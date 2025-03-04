import tkinter as tk
from tkinter import ttk, messagebox
from models.album import Album
from models.song import Song
from models.song_format import SongFormat

class MusicManagerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Quản lý Âm nhạc")
        self.root.geometry("800x600")
        
        # Tạo notebook để chứa các tab
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(expand=True, fill='both', padx=10, pady=5)
        
        # Tab Albums
        self.albums_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.albums_frame, text='Albums')
        self.setup_albums_tab()
        
        # Tab Songs
        self.songs_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.songs_frame, text='Bài hát')
        self.setup_songs_tab()

    def setup_albums_tab(self):
        # Frame cho danh sách albums
        list_frame = ttk.Frame(self.albums_frame)
        list_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Treeview cho albums
        self.albums_tree = ttk.Treeview(list_frame, columns=('ID', 'Name', 'Type', 'Artist'), show='headings')
        self.albums_tree.heading('ID', text='ID')
        self.albums_tree.heading('Name', text='Tên Album')
        self.albums_tree.heading('Type', text='Loại')
        self.albums_tree.heading('Artist', text='Nghệ sĩ')
        
        self.albums_tree.column('ID', width=50)
        self.albums_tree.column('Name', width=150)
        self.albums_tree.column('Type', width=100)
        self.albums_tree.column('Artist', width=150)
        
        self.albums_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Scrollbar cho albums
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.albums_tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.albums_tree.configure(yscrollcommand=scrollbar.set)
        
        # Frame cho các nút điều khiển
        control_frame = ttk.Frame(self.albums_frame)
        control_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=5, pady=5)
        
        ttk.Button(control_frame, text="Thêm Album", command=self.add_album_dialog).pack(fill=tk.X, pady=2)
        ttk.Button(control_frame, text="Sửa Album", command=self.edit_album_dialog).pack(fill=tk.X, pady=2)
        ttk.Button(control_frame, text="Xóa Album", command=self.delete_album).pack(fill=tk.X, pady=2)
        ttk.Button(control_frame, text="Làm mới", command=self.refresh_albums).pack(fill=tk.X, pady=2)

    def setup_songs_tab(self):
        # Frame cho tìm kiếm
        search_frame = ttk.Frame(self.songs_frame)
        search_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(search_frame, text="Tìm kiếm:").pack(side=tk.LEFT)
        self.search_var = tk.StringVar()
        self.search_var.trace('w', lambda *args: self.search_songs())
        ttk.Entry(search_frame, textvariable=self.search_var).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        # Frame cho danh sách bài hát
        list_frame = ttk.Frame(self.songs_frame)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Treeview cho bài hát
        self.songs_tree = ttk.Treeview(list_frame, 
                                     columns=('ID', 'Title', 'Artist', 'Duration', 'Album'),
                                     show='headings')
        self.songs_tree.heading('ID', text='ID')
        self.songs_tree.heading('Title', text='Tên bài hát')
        self.songs_tree.heading('Artist', text='Nghệ sĩ')
        self.songs_tree.heading('Duration', text='Thời lượng')
        self.songs_tree.heading('Album', text='Album')
        
        self.songs_tree.column('ID', width=50)
        self.songs_tree.column('Title', width=200)
        self.songs_tree.column('Artist', width=150)
        self.songs_tree.column('Duration', width=100)
        self.songs_tree.column('Album', width=150)
        
        self.songs_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Scrollbar cho bài hát
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.songs_tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.songs_tree.configure(yscrollcommand=scrollbar.set)
        
        # Frame cho các nút điều khiển
        control_frame = ttk.Frame(self.songs_frame)
        control_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(control_frame, text="Thêm bài hát", command=self.add_song_dialog).pack(side=tk.LEFT, padx=2)
        ttk.Button(control_frame, text="Sửa bài hát", command=self.edit_song_dialog).pack(side=tk.LEFT, padx=2)
        ttk.Button(control_frame, text="Xóa bài hát", command=self.delete_song).pack(side=tk.LEFT, padx=2)
        ttk.Button(control_frame, text="Quản lý định dạng", command=self.manage_formats_dialog).pack(side=tk.LEFT, padx=2)
        ttk.Button(control_frame, text="Làm mới", command=self.refresh_songs).pack(side=tk.LEFT, padx=2)

    def refresh_albums(self):
        for item in self.albums_tree.get_children():
            self.albums_tree.delete(item)
        
        albums = Album.get_all()
        for album in albums:
            self.albums_tree.insert('', 'end', values=(
                album.id,
                album.name,
                album.type,
                album.artist
            ))

    def refresh_songs(self):
        for item in self.songs_tree.get_children():
            self.songs_tree.delete(item)
        
        search_term = self.search_var.get()
        if search_term:
            songs = Song.search_by_title(search_term)
        else:
            songs = []
            albums = Album.get_all()
            for album in albums:
                songs.extend(album.get_songs())
        
        for song in songs:
            album = Album.get_by_id(song.album_id) if song.album_id else None
            self.songs_tree.insert('', 'end', values=(
                song.id,
                song.title,
                song.artist,
                f"{song.duration//60}:{song.duration%60:02d}",
                album.name if album else 'N/A'
            ))

    def search_songs(self):
        self.refresh_songs()

    def add_album_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Thêm Album")
        dialog.geometry("300x200")
        
        ttk.Label(dialog, text="Tên Album:").pack(pady=5)
        name_var = tk.StringVar()
        ttk.Entry(dialog, textvariable=name_var).pack(pady=5)
        
        ttk.Label(dialog, text="Loại:").pack(pady=5)
        type_var = tk.StringVar(value="album")
        ttk.Combobox(dialog, textvariable=type_var, values=['album', 'mini_album']).pack(pady=5)
        
        ttk.Label(dialog, text="Nghệ sĩ:").pack(pady=5)
        artist_var = tk.StringVar()
        ttk.Entry(dialog, textvariable=artist_var).pack(pady=5)
        
        def save():
            try:
                Album.create(
                    name=name_var.get(),
                    type=type_var.get(),
                    artist=artist_var.get()
                )
                self.refresh_albums()
                dialog.destroy()
            except Exception as e:
                messagebox.showerror("Lỗi", str(e))
        
        ttk.Button(dialog, text="Lưu", command=save).pack(pady=10)

    def edit_album_dialog(self):
        selected = self.albums_tree.selection()
        if not selected:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn một album để sửa")
            return
        
        item = self.albums_tree.item(selected[0])
        album_id = item['values'][0]
        album = Album.get_by_id(album_id)
        
        dialog = tk.Toplevel(self.root)
        dialog.title("Sửa Album")
        dialog.geometry("300x200")
        
        ttk.Label(dialog, text="Tên Album:").pack(pady=5)
        name_var = tk.StringVar(value=album.name)
        ttk.Entry(dialog, textvariable=name_var).pack(pady=5)
        
        ttk.Label(dialog, text="Loại:").pack(pady=5)
        type_var = tk.StringVar(value=album.type)
        ttk.Combobox(dialog, textvariable=type_var, values=['album', 'mini_album']).pack(pady=5)
        
        ttk.Label(dialog, text="Nghệ sĩ:").pack(pady=5)
        artist_var = tk.StringVar(value=album.artist)
        ttk.Entry(dialog, textvariable=artist_var).pack(pady=5)
        
        def save():
            try:
                album.name = name_var.get()
                album.type = type_var.get()
                album.artist = artist_var.get()
                album.update()
                self.refresh_albums()
                dialog.destroy()
            except Exception as e:
                messagebox.showerror("Lỗi", str(e))
        
        ttk.Button(dialog, text="Lưu", command=save).pack(pady=10)

    def delete_album(self):
        selected = self.albums_tree.selection()
        if not selected:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn một album để xóa")
            return
        
        if messagebox.askyesno("Xác nhận", "Bạn có chắc muốn xóa album này?"):
            item = self.albums_tree.item(selected[0])
            album_id = item['values'][0]
            album = Album.get_by_id(album_id)
            album.delete()
            self.refresh_albums()
            self.refresh_songs()

    def add_song_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Thêm bài hát")
        dialog.geometry("300x300")
        
        ttk.Label(dialog, text="Tên bài hát:").pack(pady=5)
        title_var = tk.StringVar()
        ttk.Entry(dialog, textvariable=title_var).pack(pady=5)
        
        ttk.Label(dialog, text="Nghệ sĩ:").pack(pady=5)
        artist_var = tk.StringVar()
        ttk.Entry(dialog, textvariable=artist_var).pack(pady=5)
        
        ttk.Label(dialog, text="Thời lượng (giây):").pack(pady=5)
        duration_var = tk.StringVar()
        ttk.Entry(dialog, textvariable=duration_var).pack(pady=5)
        
        ttk.Label(dialog, text="Album:").pack(pady=5)
        albums = Album.get_all()
        album_choices = {f"{a.name} ({a.artist})": a.id for a in albums}
        album_var = tk.StringVar()
        ttk.Combobox(dialog, textvariable=album_var, values=list(album_choices.keys())).pack(pady=5)
        
        def save():
            try:
                duration = int(duration_var.get())
                album_id = album_choices.get(album_var.get())
                Song.create(title_var.get(), artist_var.get(), duration, album_id)
                self.refresh_songs()
                dialog.destroy()
            except Exception as e:
                messagebox.showerror("Lỗi", str(e))
        
        ttk.Button(dialog, text="Lưu", command=save).pack(pady=10)

    def edit_song_dialog(self):
        selected = self.songs_tree.selection()
        if not selected:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn một bài hát để sửa")
            return
        
        item = self.songs_tree.item(selected[0])
        song_id = item['values'][0]
        song = Song.get_by_id(song_id)
        
        dialog = tk.Toplevel(self.root)
        dialog.title("Sửa bài hát")
        dialog.geometry("300x300")
        
        ttk.Label(dialog, text="Tên bài hát:").pack(pady=5)
        title_var = tk.StringVar(value=song.title)
        ttk.Entry(dialog, textvariable=title_var).pack(pady=5)
        
        ttk.Label(dialog, text="Nghệ sĩ:").pack(pady=5)
        artist_var = tk.StringVar(value=song.artist)
        ttk.Entry(dialog, textvariable=artist_var).pack(pady=5)
        
        ttk.Label(dialog, text="Thời lượng (giây):").pack(pady=5)
        duration_var = tk.StringVar(value=str(song.duration))
        ttk.Entry(dialog, textvariable=duration_var).pack(pady=5)
        
        ttk.Label(dialog, text="Album:").pack(pady=5)
        albums = Album.get_all()
        album_choices = {f"{a.name} ({a.artist})": a.id for a in albums}
        album_var = tk.StringVar()
        if song.album_id:
            current_album = Album.get_by_id(song.album_id)
            album_var.set(f"{current_album.name} ({current_album.artist})")
        ttk.Combobox(dialog, textvariable=album_var, values=list(album_choices.keys())).pack(pady=5)
        
        def save():
            try:
                song.title = title_var.get()
                song.artist = artist_var.get()
                song.duration = int(duration_var.get())
                song.album_id = album_choices.get(album_var.get())
                song.update()
                self.refresh_songs()
                dialog.destroy()
            except Exception as e:
                messagebox.showerror("Lỗi", str(e))
        
        ttk.Button(dialog, text="Lưu", command=save).pack(pady=10)

    def delete_song(self):
        selected = self.songs_tree.selection()
        if not selected:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn một bài hát để xóa")
            return
        
        if messagebox.askyesno("Xác nhận", "Bạn có chắc muốn xóa bài hát này?"):
            item = self.songs_tree.item(selected[0])
            song_id = item['values'][0]
            song = Song.get_by_id(song_id)
            song.delete()
            self.refresh_songs()

    def manage_formats_dialog(self):
        selected = self.songs_tree.selection()
        if not selected:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn một bài hát để quản lý định dạng")
            return
        
        item = self.songs_tree.item(selected[0])
        song_id = item['values'][0]
        song = Song.get_by_id(song_id)
        
        dialog = tk.Toplevel(self.root)
        dialog.title(f"Quản lý định dạng - {song.title}")
        dialog.geometry("400x300")
        
        # Treeview cho các định dạng
        formats_tree = ttk.Treeview(dialog, columns=('ID', 'Format', 'Path', 'Bitrate', 'Size'), show='headings')
        formats_tree.heading('ID', text='ID')
        formats_tree.heading('Format', text='Định dạng')
        formats_tree.heading('Path', text='Đường dẫn')
        formats_tree.heading('Bitrate', text='Bitrate')
        formats_tree.heading('Size', text='Kích thước')
        
        formats_tree.column('ID', width=50)
        formats_tree.column('Format', width=70)
        formats_tree.column('Path', width=150)
        formats_tree.column('Bitrate', width=70)
        formats_tree.column('Size', width=70)
        
        formats_tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        def refresh_formats():
            for item in formats_tree.get_children():
                formats_tree.delete(item)
            
            formats = SongFormat.get_by_song_id(song_id)
            for fmt in formats:
                formats_tree.insert('', 'end', values=(
                    fmt.id,
                    fmt.format,
                    fmt.file_path,
                    f"{fmt.bitrate}kbps",
                    f"{fmt.size//1024}KB"
                ))
        
        def add_format():
            format_dialog = tk.Toplevel(dialog)
            format_dialog.title("Thêm định dạng")
            format_dialog.geometry("300x250")
            
            ttk.Label(format_dialog, text="Định dạng:").pack(pady=5)
            format_var = tk.StringVar(value="MP3")
            ttk.Combobox(format_dialog, textvariable=format_var, 
                        values=['MP3', 'FLAC', 'WAV', 'AAC']).pack(pady=5)
            
            ttk.Label(format_dialog, text="Đường dẫn:").pack(pady=5)
            path_var = tk.StringVar()
            ttk.Entry(format_dialog, textvariable=path_var).pack(pady=5)
            
            ttk.Label(format_dialog, text="Bitrate (kbps):").pack(pady=5)
            bitrate_var = tk.StringVar()
            ttk.Entry(format_dialog, textvariable=bitrate_var).pack(pady=5)
            
            ttk.Label(format_dialog, text="Kích thước (bytes):").pack(pady=5)
            size_var = tk.StringVar()
            ttk.Entry(format_dialog, textvariable=size_var).pack(pady=5)
            
            def save_format():
                try:
                    SongFormat.create(
                        song_id,
                        format_var.get(),
                        path_var.get(),
                        int(bitrate_var.get()),
                        int(size_var.get())
                    )
                    refresh_formats()
                    format_dialog.destroy()
                except Exception as e:
                    messagebox.showerror("Lỗi", str(e))
            
            ttk.Button(format_dialog, text="Lưu", command=save_format).pack(pady=10)
        
        def delete_format():
            selected = formats_tree.selection()
            if not selected:
                messagebox.showwarning("Cảnh báo", "Vui lòng chọn một định dạng để xóa")
                return
            
            if messagebox.askyesno("Xác nhận", "Bạn có chắc muốn xóa định dạng này?"):
                item = formats_tree.item(selected[0])
                format_id = item['values'][0]
                fmt = SongFormat(id=format_id)
                fmt.delete()
                refresh_formats()
        
        button_frame = ttk.Frame(dialog)
        button_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(button_frame, text="Thêm định dạng", command=add_format).pack(side=tk.LEFT, padx=2)
        ttk.Button(button_frame, text="Xóa định dạng", command=delete_format).pack(side=tk.LEFT, padx=2)
        
        refresh_formats()

def gui():
    root = tk.Tk()
    app = MusicManagerGUI(root)
    root.mainloop()