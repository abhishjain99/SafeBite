from taipy.gui import Gui
import json

json_data = '''
{
  "items":[
    {
      "facts":"You shouldn't use it",
      "description":"I dont like it",
      "id":"5e711e64-ef05-11ee-be60-56e977dbd9ed",
      "name":"Sugsar"
    },
    {
      "facts":"You shouldn't use it",
      "description":"I dont like it",
      "id":"5e711e64-ef05-11ee-be60-56e977dbd9ed",
      "name":"Sugaaaar"
    },
    {
      "facts":"You shouldn't use it",
      "description":"I dont like it",
      "id":"5e711e64-ef05-11ee-be60-56e977dbd9ed",
      "name":"Sugar"
    }
  ]
}
'''

# cover image
bg = "/images/photo.jpeg"

# path of images to be uploaded (qr + ingredients)
path1 = None
path2 = None

# image data blob (qr + ingredients)
data1 = None
data2 = None

# table data
table_info = {}

# page markdown
md = """
<|layout|columns="1 1"
# SafeByte
<|{bg}|image|>
#### SafeByte is an innovative application designed to promote healthier eating habits. By simply scanning the ingredients of a food item, SafeByte swiftly analyzes its nutritional content and alerts users to its health status. Through a user-friendly interface, it provides clear indications of whether the food is healthy or not, empowering individuals to make informed dietary choices on the go.
<|{path1}|file_selector|label=Upload QR code|on_action=load_qr|extensions=.jpg,.jpeg,.png|>

<|{path2}|file_selector|label=Upload Ingredients|on_action=load_ingredients|extensions=.jpg,.jpeg,.png|>

<|{table_info}|table|show_all|rebuild|>
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
    global table_info
    with open(state.path2, "rb") as f:
      state.data2 = f.read()
      # do whatever has to be done with the ingredients image here

    # ******* Table creation -- need to decide where/how this will be invoked *******
    # Parse JSON data and make dictionary
    parsed_data = json.loads(json_data)
    columns = parsed_data["items"][0].keys()
    result_dict = {col: [] for col in columns}
    for item in parsed_data["items"]:
        for col, value in item.items():
            result_dict[col].append(value)
    state.table_info = result_dict

# invokes taipy
Gui(md).run()