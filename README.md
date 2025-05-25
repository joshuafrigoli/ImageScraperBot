# ImageScraperBot

**ImageScraperBot** is a Python bot that, given a URL and a CSS selector, automatically downloads all images matching the specified rule.

---

## 🛠️ Technologies & Libraries

- **Python 3.7+**
- **Selenium**: for browser automation
- **webdriver-manager**: automatic management of browser drivers (Chrome, Firefox, Edge)
- **Requests**: for downloading images
- **argparse**: parsing command-line arguments

---

## 🚀 Core Features

1. **Multi-browser support**: Chrome, Firefox, Edge, Safari (macOS only).
2. **Incognito/private mode**: activate with `--incognito`.
3. **Dynamic content handling**: waits for elements and scrolls for lazy-loaded images.
4. **Flexible attribute selection**: specify image attribute (e.g., `src`, `data-src`) via `--attribute`.
5. **Configurable output format**: save as `jpg` or `png` with `--saving_format`.
6. **Custom output directory**: set with `--folder_path`.

---

## 📋 Prerequisites

Install required packages with:

```bash
pip install selenium webdriver-manager requests
```

## ⚙️ Installation

### Clone the repository:

```bash
git clone https://github.com/joshuafrigoli/ImageScraperBot.git
cd ImageScraperBot
```

### (Optional) Create and activate a virtual environment:

#### On Windows

```sh
.venv\Scripts\activate
```

#### On MacOS/Linux

```sh
source .venv/bin/activate
```

### Install dependencies:

```bash
pip install -r requirements.txt
```

## 🎯 Usage

### Arguments

```bash
python image_scraper.py <URL> <CSS_SELECTOR> [--attribute ATTRIBUTE] [--driver DRIVER] [--incognito] [--saving_format FORMAT] [--folder_path PATH]
```

### Example

```bash
python image_scraper.py 'https://example.com' 'img.my-class' --attribute data-src --driver chrome --incognito --saving_format png --folder_path images
```

### To deactivate virtual environment

```sh
deactivate
```

**Tip:** if the `python` command doesn’t work, try `python3` instead!

## 🔒 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
