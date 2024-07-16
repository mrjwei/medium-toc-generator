# medium-toc-generator
Table-of-contents generator for [Medium](https://medium.com/).

## How to Use

### Step 1: Clone this repo
```
git clone git@github.com:mrjwei/medium-toc-generator.git
cd medium-toc-generator
```

### Step 2: Create venv and install dependencies
```
python3 -m venv app-env
source app-env/bin/activate
pip install -r requirements.txt
```

### Step 3: Run programme
```
python main.py
```
This will open a GUI.

### Step 4: Get the toc
Copy your **published** posts' urls and paste them into the GUI's inputs.
To add more input fields, hit *Add*.
Then, hit *Generate* and the generated html will be opened in your browser.
Finally, in the opened browser tab, press Cmd + A (Mac) or Ctrl + A (Windows) to select everything and copy it into your post.


