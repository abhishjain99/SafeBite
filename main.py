from taipy.gui import Gui

# cover image
bg = "/images/photo.jpeg"

# path of images to be uploaded (qr + ingredients)
path1 = None
path2 = None

# image data blob (qr + ingredients)
data1 = None
data2 = None

# page markdown
md = """
<|layout|columns="1 1"
# SafeByte
<|{bg}|image|>
#### SafeByte is an innovative application designed to promote healthier eating habits. By simply scanning the ingredients of a food item, SafeByte swiftly analyzes its nutritional content and alerts users to its health status. Through a user-friendly interface, it provides clear indications of whether the food is healthy or not, empowering individuals to make informed dietary choices on the go.
<|{path1}|file_selector|label=Upload QR code|on_action=load_qr|extensions=.jpg,.jpeg,.png|>

<|{path2}|file_selector|label=Upload Ingredients|on_action=load_ingredients|extensions=.jpg,.jpeg,.png|>

<|content|>
This application was created with [Taipy](https://www.taipy.io/).
>
"""

# load qr image into memory
def load_qr(state):
    with open(state.path1, "rb") as f:
      state.data1 = f.read()
      # do whatever has to be done with the qr image here
      print(state.data1)

# load ingredients image into memory
def load_ingredients(state):
    with open(state.path2, "rb") as f:
      state.data2 = f.read()
      # do whatever has to be done with the ingredients image here
      print(state.data2)

# invokes taipy
Gui(md).run()