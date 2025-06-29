import re
import sys


"""

How this python script works?

You pass an argument to it, where you specify path to your README.md text.
Then it looks at words (just splits initial text by spaces) and looks at 
all the links that occur in the text. So, your links should be separated with spaces.
Then it replaces with template that looks like so: 
[<sup>[ind-link-of-occurrence]</sup>](#reference-same-ind).
This creates an anchor to the element that is located in References section.
All links are stored in array and after text is processed, they are used to
create anchors at the bottom of the file.

How references section looks like(example)?
## 7. References

<a id="reference-1"></a>
1. [**^**](https://en.wikipedia.org/wiki/Ray_casting) Wikipedia raycasting page

<a id="reference-2"></a>
2. [**^**](https://proglib.io/p/raycasting-for-the-smallest) Article in Russian about raycasting

<a id="reference-3"></a>
3. [**^**](https://en.wikipedia.org/wiki/2.5D) What's a 2.5D, wiki page.

So, it's basically an enumeration of all used links in the README, with a proper name.

"""


RESULT_FILE_NAME          = "READMEwithRefs.md"
BEGINNING_OF_LINK         = "https:"
HTML_CODES_FOLDER         = "htmlCodes"
HTML_INSERT_CHECK_MESSAGE = "INSERT_HTML_CODE_HERE:"
MARKDOWN_COMMENT_START    = "<!--"

linksDescriptions = [
    "ASCII art, wiki page",
    "ANSI escape codes, wiki page",
    "Numeral systems",
    "How to print colored text in terminal, stack overflow question",
    "Double buffering technique",
    "BFS algorithm",
    "BFS algorithm pseudocode",
    "Python dictionary structure",
    "Hash table",
    "Bidirectional BFS description",
    "A* search algorithm",
    "Linear combination",
]


def getListOfWordsFromFile(fileName) -> list[str]:
    with open(fileName, "r") as file:
        # contains words on even indexes
        # and delimiters on  odd indexes
        parts = re.split(r"([ \n])", file.read())
        return parts
    

def isWordLink(word) -> bool:
    return word.startswith(BEGINNING_OF_LINK)


def getResultTextAndListOfLinks(parts) -> tuple[str, list[str]]:
    resultText = ""
    links      = []

    linkInd = 0
    for i, part in enumerate(parts):
        # if this is delimiter than we add it
        # however, we don't want to add space before link
        if i % 2 == 1:
            # if next word doesn't exist or it's not a link
            if i + 1 >= len(parts) or not isWordLink(parts[i + 1]):
                resultText += part
            continue

        if not isWordLink(part):
            resultText += part
            continue

        linkInd += 1
        resultText += f"[<sup>[{linkInd}]</sup>](#reference-{linkInd})"
        links.append(part)
        print(i, part, linkInd)

    return resultText, links


def addReferencesSection(resultText, links) -> str:
    assert(len(links) == len(linksDescriptions))

    resultText += "\n## References\n\n"
    for linkInd, link in enumerate(links, start=1):
        print(linkInd, link, linksDescriptions[linkInd-1])
        # print(linkInd, link)
        resultText += f"""
<a id="reference-{linkInd}"></a>
{linkInd}. [**^**]({link}) {linksDescriptions[linkInd-1]}."""
#         resultText += f"""
# <a id="reference-{linkInd}"></a>
# {linkInd}. [**^**]({link}) text."""

    return resultText


def addHTMLexamples(resultText) -> str:
    i     = 0
    res   = ""
    parts = re.split(r"([ \n])", resultText)
    while i < len(parts):
        # this is separator, we just add it and continue
        if i % 2 == 1:
            res += parts[i]
            i += 1
            continue

        # in case if this is simple word, not a comment with 
        # html example file path
        if i + 4 >= len(parts)                    or \
           parts[i]     != MARKDOWN_COMMENT_START or \
           parts[i + 2] != HTML_INSERT_CHECK_MESSAGE:
            res += parts[i]
            i += 1
            continue
        
        fileName = parts[i + 4]
        # print("fileName : ", fileName)
        with open(fileName, "r") as f:
            htmlCode = f.read()
            res += f"\n\n{htmlCode}\n\n"
        i += 7

    return res


def saveResult2File(resultText) -> None:
    with open(RESULT_FILE_NAME, "w") as resultFile:
        resultFile.write(resultText)
    print("done...\n")


if __name__ == "__main__":
    if (len(sys.argv) != 2):
        print("This script takes only one argument: \n" \
        "path to the README, that is going to be processed")
        exit(1)

    path2README = sys.argv[1]
    print("path to README: ", path2README)
    parts = getListOfWordsFromFile(path2README)

    resultText, links = getResultTextAndListOfLinks(parts)

    resultText = addReferencesSection(resultText, links)
    resultText = addHTMLexamples(resultText)
    saveResult2File(resultText)
