import json
import os
import urllib.request
from pathlib import Path

from PIL import Image, ImageOps

USERNAME = "Hephzibahbehulah"

PHOTO = Path("profile.jpg")
DARK_SVG = Path("dark_mode.svg")
LIGHT_SVG = Path("light_mode.svg")

ASCII_CHARS = "@%#*+=-:. "
ASCII_WIDTH = 54
ASCII_HEIGHT = 54

CARD_WIDTH = 1200
CARD_HEIGHT = 650

def github_api(url):
token = os.environ.get("GITHUB_TOKEN", "")

```
headers = {
    "Accept": "application/vnd.github+json",
    "User-Agent": "Hephzibahbehulah-GitHub-Profile",
}

if token:
    headers["Authorization"] = f"Bearer {token}"

request = urllib.request.Request(url, headers=headers)

with urllib.request.urlopen(request, timeout=30) as response:
    return json.loads(response.read().decode("utf-8"))
```

def get_github_stats():
user = github_api(
f"https://api.github.com/users/{USERNAME}"
)

```
repositories = []

page = 1

while True:
    data = github_api(
        f"https://api.github.com/users/{USERNAME}/repos"
        f"?per_page=100&page={page}&type=owner"
    )

    repositories.extend(data)

    if len(data) < 100:
        break

    page += 1

total_stars = sum(
    repository.get("stargazers_count", 0)
    for repository in repositories
)

total_forks = sum(
    repository.get("forks_count", 0)
    for repository in repositories
)

languages = {}

for repository in repositories:
    language = repository.get("language")

    if language:
        languages[language] = languages.get(language, 0) + 1

top_languages = sorted(
    languages.items(),
    key=lambda item: item[1],
    reverse=True,
)[:4]

language_text = " • ".join(
    language for language, _ in top_languages
)

if not language_text:
    language_text = "Python"

return {
    "repos": user.get("public_repos", 0),
    "followers": user.get("followers", 0),
    "following": user.get("following", 0),
    "stars": total_stars,
    "forks": total_forks,
    "languages": language_text,
}
```

def escape_xml(value):
return (
str(value)
.replace("&", "&")
.replace("<", "<")
.replace(">", ">")
.replace('"', """)
.replace("'", "'")
)

def image_to_ascii():
if not PHOTO.exists():
return [
"PROFILE IMAGE NOT FOUND",
"",
"Add your photo as:",
"profile.jpg",
]

```
image = Image.open(PHOTO).convert("L")

image = ImageOps.fit(
    image,
    (ASCII_WIDTH, ASCII_HEIGHT),
    method=Image.Resampling.LANCZOS,
)

pixels = list(image.getdata())

rows = []

for y in range(image.height):
    row = []

    for x in range(image.width):
        brightness = pixels[y * image.width + x]

        index = int(
            (255 - brightness)
            / 255
            * (len(ASCII_CHARS) - 1)
        )

        row.append(ASCII_CHARS[index])

    rows.append("".join(row))

return rows
```

def make_svg(stats, dark=False):
if dark:
background = "#0d1117"
panel = "#161b22"
foreground = "#f0f6fc"
muted = "#8b949e"
accent = "#58a6ff"
border = "#30363d"
portrait_background = "#010409"
else:
background = "#ffffff"
panel = "#f6f8fa"
foreground = "#24292f"
muted = "#57606a"
accent = "#0969da"
border = "#d0d7de"
portrait_background = "#ffffff"

```
portrait = image_to_ascii()

svg = []

svg.append(
    f'<svg xmlns="http://www.w3.org/2000/svg" '
    f'width="{CARD_WIDTH}" height="{CARD_HEIGHT}" '
    f'viewBox="0 0 {CARD_WIDTH} {CARD_HEIGHT}">'
)

svg.append(
    f'<rect width="{CARD_WIDTH}" height="{CARD_HEIGHT}" '
    f'rx="28" fill="{background}"/>'
)

svg.append(
    f'<rect x="16" y="16" width="{CARD_WIDTH - 32}" '
    f'height="{CARD_HEIGHT - 32}" rx="24" '
    f'fill="{panel}" stroke="{border}" stroke-width="2"/>'
)

svg.append(
    f'<text x="48" y="54" '
    f'font-family="monospace" font-size="14" '
    f'fill="{muted}">'
    f'HEPHZIBAHBEHULAH@GITHUB:~$ ./profile'
    f'</text>'
)

svg.append(
    f'<line x1="48" y1="76" x2="{CARD_WIDTH - 48}" y2="76" '
    f'stroke="{border}" stroke-width="1"/>'
)

portrait_x = 42
portrait_y = 100
portrait_width = 570
portrait_height = 500

svg.append(
    f'<rect x="{portrait_x}" y="{portrait_y}" '
    f'width="{portrait_width}" height="{portrait_height}" '
    f'rx="18" fill="{portrait_background}" '
    f'stroke="{border}" stroke-width="1"/>'
)

character_width = 9
character_height = 8.2

start_x = portrait_x + 35
start_y = portrait_y + 30

for row_index, row in enumerate(portrait):
    y = start_y + row_index * character_height

    svg.append(
        f'<text x="{start_x}" y="{y:.1f}" '
        f'font-family="monospace" '
        f'font-size="9px" '
        f'font-weight="700" '
        f'fill="{foreground}" '
        f'xml:space="preserve">'
        f'{escape_xml(row)}'
        f'</text>'
    )

information_x = 670

svg.append(
    f'<text x="{information_x}" y="128" '
    f'font-family="sans-serif" '
    f'font-size="38" font-weight="700" '
    f'fill="{foreground}">'
    f'Hephzibah Behulah'
    f'</text>'
)

svg.append(
    f'<text x="{information_x}" y="163" '
    f'font-family="monospace" '
    f'font-size="16" '
    f'fill="{accent}">'
    f'Elektroniker → Automation → Technology'
    f'</text>'
)

svg.append(
    f'<text x="{information_x}" y="198" '
    f'font-family="sans-serif" '
    f'font-size="18" '
    f'fill="{muted}">'
    f'Cybersecurity &amp; Data Analytics'
    f'</text>'
)

svg.append(
    f'<text x="{information_x}" y="228" '
    f'font-family="sans-serif" '
    f'font-size="15" '
    f'fill="{muted}">'
    f'Hamburg, Germany'
    f'</text>'
)

svg.append(
    f'<line x1="{information_x}" y1="252" '
    f'x2="{CARD_WIDTH - 48}" y2="252" '
    f'stroke="{border}" stroke-width="1"/>'
)

stat_items = [
    ("PUBLIC REPOSITORIES", stats["repos"]),
    ("FOLLOWERS", stats["followers"]),
    ("FOLLOWING", stats["following"]),
    ("TOTAL STARS", stats["stars"]),
    ("TOTAL FORKS", stats["forks"]),
]

stat_y = 292

for label, value in stat_items:
    svg.append(
        f'<text x="{information_x}" y="{stat_y}" '
        f'font-family="monospace" '
        f'font-size="12" '
        f'fill="{muted}">'
        f'{label}'
        f'</text>'
    )

    svg.append(
        f'<text x="{information_x + 250}" y="{stat_y}" '
        f'font-family="monospace" '
        f'font-size="17" '
        f'font-weight="700" '
        f'fill="{foreground}">'
        f'{escape_xml(value)}'
        f'</text>'
    )

    stat_y += 48

svg.append(
    f'<text x="{information_x}" y="545" '
    f'font-family="monospace" '
    f'font-size="12" '
    f'fill="{muted}">'
    f'LANGUAGES'
    f'</text>'
)

svg.append(
    f'<text x="{information_x + 110}" y="545" '
    f'font-family="monospace" '
    f'font-size="12" '
    f'fill="{accent}">'
    f'{escape_xml(stats["languages"])}'
    f'</text>'
)

svg.append(
    f'<text x="48" y="628" '
    f'font-family="monospace" '
    f'font-size="12" '
    f'fill="{muted}">'
    f'Building practical skills in Python, data, cybersecurity, '
    f'software and automation.'
    f'</text>'
)

svg.append("</svg>")

return "\n".join(svg)
```

def main():
stats = get_github_stats()

```
light_svg = make_svg(stats, dark=False)
dark_svg = make_svg(stats, dark=True)

LIGHT_SVG.write_text(
    light_svg,
    encoding="utf-8",
)

DARK_SVG.write_text(
    dark_svg,
    encoding="utf-8",
)

print("GitHub profile SVGs generated successfully.")
```

if **name** == "**main**":
main()
