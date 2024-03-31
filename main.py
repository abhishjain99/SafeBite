from taipy.gui import Gui

# cover image
bg = "/images/photo.jpeg"

# path of image to be uploaded
path = None
# image data blob
data = None

# page markdown
md = """
<|layout|columns="1 1"
# SafeByte
<|{bg}|image|>
#### SafeByte is an innovative application designed to promote healthier eating habits. By simply scanning the ingredients of a food item, SafeByte swiftly analyzes its nutritional content and alerts users to its health status. Through a user-friendly interface, it provides clear indications of whether the food is healthy or not, empowering individuals to make informed dietary choices on the go.
<|{path}|file_selector|label=Upload QR code|on_action=load_qr|extensions=.jpg,.jpeg,.png|>

<|content|>
This application was created with [Taipy](https://www.taipy.io/).
>
"""

# load_qr into memory
def load_qr(state):
    with open(state.path, "rb") as f:
      state.data = f.read()
      # do whatever has to be done with the qr image here
      print(state.data)

# invokes taipy
Gui(md).run()