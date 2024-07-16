from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox
import requests
from bs4 import BeautifulSoup
from jinja2 import Template
import webbrowser
from pathlib import Path

class TOCGenerator(Frame):
  def __init__(self, root):
    super().__init__(root)
    self.root = root
    self.root.title('Generate TOC for Medium')
    # Initially, there are 4 rows:
    # Row 1: label for first url entry
    # Row 2: first url entry
    # Row 3: frame containing add button, generate and quit buttons
    self.total_rows = 3

    self.main_frame = Frame(self.root)
    self.main_frame.grid(padx=20, pady=20, sticky='we')
    self.main_frame.columnconfigure(0, minsize=150, weight=1)
    self.main_frame.columnconfigure(1, minsize=150, weight=1)

    self.init_url_label = Label(self.main_frame, text='URL')
    self.init_url_label.grid(row=0, column=0, sticky=W)

    init_url_entry = Entry(self.main_frame)
    init_url_entry.grid(row=1, column=0, sticky='we', columnspan=2)

    self.url_entries = [init_url_entry]

    self.frame = Frame(self.main_frame)
    self.frame.grid(row=self.total_rows - 1, column=0, sticky='we', columnspan=2)
    self.frame.columnconfigure(0, minsize=150, weight=1)
    self.frame.columnconfigure(1, minsize=150, weight=1)

    self.add_btn = Button(self.frame, text='+ Add', command=self.add_url_group)
    self.add_btn.grid(row=0, column=0, sticky='we', columnspan=2)

    self.gen_btn = Button(self.frame, text='Generate', command=self.generate_toc)
    self.gen_btn.grid(row=1, column=0, sticky='we')

    self.quit_btn = Button(self.frame, text='Quit', command=lambda: self.root.quit())
    self.quit_btn.grid(row=1, column=1, sticky='we')

  def update_frame_position(self):
    self.frame.grid(row=self.total_rows, column=0, sticky='we')

  def update_init_url_label(self):
    self.init_url_label.configure(text='URL 1')

  def add_url_group(self):
    # Here, index is 1-based
    index = len(self.url_entries) + 1
    Label(self.main_frame, text=f'URL {index}').grid(row=self.total_rows, column=0, sticky=W)
    entry = Entry(self.main_frame)
    entry.grid(row=self.total_rows + 1, column=0, sticky='we', columnspan=2)

    self.url_entries.append(entry)

    self.total_rows += 2
    self.update_init_url_label()
    self.update_frame_position()

  def fetch_html(self, url):
    try:
      response = requests.get(url)
      # Raise an HTTPError for bad responses
      response.raise_for_status()
      html_content = response.text
      return html_content
    except requests.RequestException as e:
      print(f"Error fetching the URL: {e}")
      return None

  def create_soup(self, html_content):
    return BeautifulSoup(html_content, 'html.parser')

  def _has_unwanted_class(self, element):
    unwanted_classes = [
      'pw-author-name',
      'pw-post-title',
      'pw-subtitle-paragraph'
    ]
    return any(class_name in element.get('class', []) for class_name in unwanted_classes)

  def _has_unwanted_text(self, element):
    unwanted_text = 'Table of Contents'
    return unwanted_text in element.text

  def get_target_headings(self, soup):
    headings = soup.find_all(['h1', 'h2'])
    filtered_headings = [
      h for h in headings if
      not (
        self._has_unwanted_class(h) or
        self._has_unwanted_text(h)
      )
    ]
    return filtered_headings

  def generate_toc(self):
    try:
      for i, entry in enumerate(self.url_entries):
        url = entry.get()
        if not url:
          continue
        html_content = self.fetch_html(url)
        if not html_content:
          continue
        soup = self.create_soup(html_content)

        headings = self.get_target_headings(soup)

        context = {
          'h1s': []
        }
        current_h1 = None

        for h in headings:
          path = '#' + h.get('id', '')
          text = h.text.strip()
          if h.name == 'h1':
            current_h1 = {'path': path, 'text': text, 'children': []}
            context['h1s'].append(current_h1)
          elif h.name == 'h2' and current_h1 is not None:
            current_h1['children'].append({'path': path, 'text': text})

        template = Template('''
          <h2>Table of Contents</h2>
          <ul>
            {% for h1 in h1s %}
              <li>
                <a href={{h1.path}}>{{h1.text}}</a>
                {% for child in h1.children %}
                  <br>
                  - <a href={{child.path}}>{{child.text}}</a>
                {% endfor %}
              </li>
            {% endfor %}
          </ul>
        ''')

        Path("outputs").mkdir(parents=True, exist_ok=True)
        file_name = f'outputs/output_{i+1}.html'

        with open(file_name, 'w', encoding='utf-8') as f:
          f.write(template.render(context))
        webbrowser.open(f'file:///{Path(file_name).absolute()}')
    except Exception as e:
      messagebox.showerror(title='Error', message=f'{e}')

if __name__ == "__main__":
  root = Tk()
  app = TOCGenerator(root)
  app.mainloop()
