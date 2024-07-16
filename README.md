# medium-toc-generator
Table-of-contents generator for [Medium](https://medium.com/).

## Features

- Building TOCs with one click
- Generating TOCs in bulk for multiple blog posts
- Supporting up to 2 levels of lists
- User-friendly GUI & even non-programmers can set up and get go in minutes
- Opening browser tabs containing rendered, ready-for-copying TOCs, one tab for a TOC

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
Copy your **published** posts' urls and paste them into the GUI's inputs, one input for a url.
To add more input fields, hit *Add*.
Then, hit *Generate* and the generated TOCs will be opened in your browser, one tab for a TOC, and they are ready to be copied.
Just go over each of the tabs, copying and pasted the TOC into its corresponding post.


