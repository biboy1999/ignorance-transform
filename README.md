# ignorance-transform
A utility package for writing ignorance transform 

# Getting Started
Pair with any web server you preferred

flask
```python3
from ignorance_transform.transform import Transform

# ignorance send elements json via POST
@app.route("/user/items", methods=["POST"])
def get_user():
    # dump json in, That's is.
    transform = Transform(request.json)
    # any add or change code, node, edge...
    
    # all change will be json and send back to ignorance
    return transform.to_dict()
```

# API

TODO
