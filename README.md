<!-- omit in toc -->
# JPEG Compressor

Yet another simple JPEG compressor in Python.

<!-- omit in toc -->
## Table of Contents

- [Context](#context)
- [Installation](#installation)
- [Usage](#usage)
- [License](#license)

## Context

This project is one of the assignments of the course *Fundamental Topics
in Multimedia Systems* at the [Alpen-Adria-Universität](https://www.aau.at/en/) in Klagenfurt, Austria.
The goal of this project is to implement a JPEG compression algorithm in Python.

[PDF Report](https://aau.spont.me/mmf/jpeg/report.pdf)

**Why Python?**

It is imposed by our teacher. I would have preferred to use C++, so it would be
faster, but more complex to implement.

## Installation

```bash
git clone https://github.com/seba1204/jpeg-compressor
cd jpeg-compressor
pip3 install -r requirements.txt
```

## Usage

```bash
python3 ./main.py -r 0.5 -i ./assets/lena.png -o ./out/lena_compressed.png
```

## License

This project is licensed under the terms of the MIT license.