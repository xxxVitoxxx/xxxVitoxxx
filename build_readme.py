import pathlib
import feedparser
import re

def fetch_blog_entries():
    entries = feedparser.parse("https://xxxvitoxxx.github.io/index.xml")["entries"]
    return [
        {
            "title": entry["title"],
            "url": entry["link"].split("#")[0],
        }
        for entry in entries
    ]

def replace_chunk(content, chunk, inline=False):
    r = re.compile(
        r"<!\-\- blog starts \-\->.*<!\-\- blog ends \-\->",
        re.DOTALL,
    )
    
    if not inline:
        chunk = "\n{}\n".format(chunk)
    chunk = "<!-- blog starts -->{}<!-- blog ends -->".format(chunk)
    return r.sub(chunk, content)

if __name__ == '__main__':
    root = pathlib.Path(__file__).parent.resolve()
    readme = root / "README.md"
    contents = readme.open().read()

    entries = fetch_blog_entries()[:3]
    entries_md = "\n".join(
        ["- [{title}]({url})".format(**entry) for entry in entries]
    )

    rewrite = replace_chunk(contents, entries_md)
    readme.open("w").write(rewrite)

