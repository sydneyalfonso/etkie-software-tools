#!/usr/bin/env python3

# %%
from jinja2 import Template
import pandas as pd
import wget
import ssl
import urllib


df = pd.read_csv("linesheet.csv")


start = r""" \documentclass[a4paper,landscape]{article}
\usepackage{graphicx} 
\usepackage{caption,subcaption}
\usepackage[default]{raleway}
\usepackage[textwidth=28cm,textheight=20cm]{geometry}
\begin{document}

"""

end = r""" 
\end{document}

"""


def get_image_template(image_file, caption1, caption2):
    return (
        r"""\begin{subfigure}{0.25\textwidth}
    \includegraphics[width=\linewidth]{"""
        + image_file
        + r"""}
    \center{"""
        + caption1
        + r"""}
    \center{"""
        + caption2
        + r"""}
    \end{subfigure}\hfil % <-- added
  """
    )


# %%


def get_one_photo(src, title):
    wget.download(url=src, out=f"photos/{title}.jpg")


get_one_photo(
    "https://cdn.shopify.com/s/files/1/0824/5717/files/Etkie_22_05_1.jpg?v=1665421442",
    "Esme Silver Large",
)

# %%


def get_photo_files():
    # download all files
    for i, row in list(df.iterrows()):
        print(f"Download for photos/{row['Title']}.jpg")
        print(f"{row['Image Src']}")
        wget.download(url=row["Image Src"], out=f"photos/{row['Title']}.jpg")


# %%
# get_photo_files()
# %%
def wholesale_price(retail):
    if retail == 225:
        return "102"
    elif retail == 238:
        return "108"
    elif retail == 255:
        return "116"
    elif retail == 268:
        return "121"
    elif retail == 285:
        return "129"
    elif retail == 298:
        return "135"
    else:
        return "265"


df["wholesale"] = df["Variant Price"].map(wholesale_price)
df["file"] = '"photos/' + df["Title"] + '"'
df["caption"] = (
    "USD " + df["wholesale"] + " / " + df["Variant Price"].astype("str") + " MSRP "
)

tags = set(df["Tags"])


def get_page(l):
    return Template(
        """
  \\begin{figure}[htb]
      \centering % <-- added
    {{t2}}
  \medskip
    {{t1}}
  \end{figure}
  """
    ).render(t1="".join(l[0:3]), t2="".join(l[3:6]))


def get_linesheet_pages(df, tag):

    img_templates = []
    for i, row in df[df["Tags"] == tag].iterrows():
        img_file = row["file"]
        caption = row["caption"]
        title = row["Title"]
        img_templates.append(get_image_template(img_file, title, caption))

    render = start
    for i, _ in enumerate(img_templates):
        if i % 6 == 0:
            render += get_page(img_templates[i : i + 6])
    render += end
    return render


templates = [(tag, get_linesheet_pages(df, tag)) for tag in tags]

for tag, t in templates:
    with open(f"output/{tag}.tex", "w") as f:
        f.write(t)

# %%

# %%

# %%
