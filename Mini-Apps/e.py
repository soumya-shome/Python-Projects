from ascii_magic import AsciiArt, Back

my_art = AsciiArt.from_image('images/image.png')
my_art.to_html_file('ascii_art.html', columns=200, width_ratio=2)