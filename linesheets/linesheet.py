#%%
#!/usr/bin/env python3

from jinja2 import Template
import pandas as pd
import wget
import ssl
import urllib


df = pd.read_csv('products.csv')


start = r""" \documentclass[a4paper,landscape]{article}
\usepackage{graphicx} 
\usepackage{caption,subcaption}
\usepackage[default]{raleway}
\usepackage[textwidth=28cm,textheight=5cm]{geometry}
\begin{document}

"""

end = """ 
\end{document}

"""

#%%
template = Template("""

\begin{figure}[htb]
    \centering % <-- added
\begin{subfigure}{0.25\textwidth}
  \includegraphics[width=\linewidth]{example-image-a}
  \center{Hello}
  \label{fig:1}
\end{subfigure}\hfil % <-- added
\begin{subfigure}{0.25\textwidth}
  \includegraphics[width=\linewidth]{example-image-b}
  \caption{image2}
  \label{fig:2}
\end{subfigure}\hfil % <-- added
\begin{subfigure}{0.25\textwidth}
  \includegraphics[width=\linewidth]{example-image-c}
  \caption{image3}
  \label{fig:3}
\end{subfigure}

\medskip
\begin{subfigure}{0.25\textwidth}
  \includegraphics[width=\linewidth]{example-image-a}
  \caption{image4}
  \label{fig:4}
\end{subfigure}\hfil % <-- added
\begin{subfigure}{0.25\textwidth}
  \includegraphics[width=\linewidth]{example-image-b}
  \caption{image5}
  \label{fig:5}
\end{subfigure}\hfil % <-- added
\begin{subfigure}{0.25\textwidth}
  \includegraphics[width=\linewidth]{example-image-c}
  \caption{image6}
  \label{fig:6}
\end{subfigure}

\end{figure}


""")

# %%

# This restores the same behavior as before.
context = ssl._create_unverified_context()
# %%
#wget.download()

img = list(df[['Image Src']].values)
# %%
img
# %%
img[0][0]
# %%
wget.download(img[0][0])
# %%
import ssl
import certifi

#urlopen(request, context=ssl.create_default_context(cafile=certifi.where()))
wget.download?
# %%
import os
# %%
os.system('cd /home/clement/src/etkie/photos & wget https://cdn.shopify.com/s/files/1/0824/5717/files/col2021_Cami_Large.jpg?v=1614533604 --no-check-certificate')
# %%

with open('output_tex.tex') as f:
    f.write(start + template + end)