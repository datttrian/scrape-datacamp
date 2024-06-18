import pytest
import rpy2.robjects as robjects
from rpy2.robjects.packages import importr

from project import scrape_exercise_url_to_html, convert_html_to_markdown

# utils = importr("utils")
# utils.install_packages("tidyverse")
# utils.install_packages("httr")
# utils.install_packages("rvest")

importr("rvest")
read_html = robjects.r("read_html")
html_nodes = robjects.r("html_nodes")
html_attr = robjects.r("html_attr")
as_character = robjects.r("as.character")
paste0 = robjects.r("paste0")

urls_successful = [
    "https://campus.datacamp.com/courses/intro-to-python-for-data-science/chapter-1-python-basics?ex=3",
    "https://campus.datacamp.com/courses/intro-to-python-for-data-science/chapter-1-python-basics?ex=4",
    "https://campus.datacamp.com/courses/intro-to-python-for-data-science/chapter-1-python-basics?ex=5",
    "https://campus.datacamp.com/courses/intro-to-python-for-data-science/chapter-1-python-basics?ex=7",
    "https://campus.datacamp.com/courses/intro-to-python-for-data-science/chapter-1-python-basics?ex=8",
    "https://campus.datacamp.com/courses/intro-to-python-for-data-science/chapter-1-python-basics?ex=9",
    "https://campus.datacamp.com/courses/intro-to-python-for-data-science/chapter-1-python-basics?ex=11",
    "https://campus.datacamp.com/courses/intro-to-python-for-data-science/chapter-1-python-basics?ex=12",
]


@pytest.mark.parametrize("urls_successful", urls_successful)
def test_scrape_exercise_url_to_html_successful(urls_successful):
    result = scrape_exercise_url_to_html(urls_successful)
    assert result is not None
    assert '<div class="listview__content">' in result
    assert '<div class="exercise--instructions__content">' in result
    assert "<strong>Instructions</strong>" in result
    assert "<strong>Answer</strong>" in result


urls_unsuccessful = [
    "https://campus.datacamp.com/courses/intro-to-python-for-data-science/chapter-1-python-basics?ex=1",
    "https://campus.datacamp.com/courses/intro-to-python-for-data-science/chapter-1-python-basics?ex=2",
    "https://campus.datacamp.com/courses/intro-to-python-for-data-science/chapter-1-python-basics?ex=6",
    "https://example.com/",
    "https://www.youtube.com/",
]


@pytest.mark.parametrize("urls_unsuccessful", urls_unsuccessful)
def test_scrape_exercise_url_to_html_unsuccessful(urls_unsuccessful):
    result = scrape_exercise_url_to_html(urls_unsuccessful)
    assert result is None


@pytest.mark.parametrize(
    "html, expected_markdown",
    [
        (
            '<div class="css-fsa3o0">Heading</div><p>Paragraph with <code>code</code> snippet.</p>',
            "# Heading\n\nParagraph with `code` snippet.",
        ),
        (
            '<div class="css-fsa3o0">Title</div><p>Another paragraph.</p><ul><li>Step 1</li><li>Step 2</li></ul>',
            "# Title\n\nAnother paragraph.\n\n## Instructions\n\n- Step 1\n\n- Step 2",
        ),
        (
            '<div class="css-fsa3o0">Sample</div><p>Test paragraph.</p><strong>Answer</strong><div><li>Answer 1</li><li>Answer 2</li></div>',
            "# Sample\n\nTest paragraph.\n\n## Answer\n\n- Answer 1\n\n- Answer 2",
        ),
        (
            '<div class="css-fsa3o0">Example</div><p>Mixed content with <code>inline code</code> and normal text.</p>',
            "# Example\n\nMixed content with `inline code` and normal text.",
        ),
        (
            '<div class="css-fsa3o0">No Instructions</div><p>Just a paragraph.</p>',
            "# No Instructions\n\nJust a paragraph.",
        ),
        (
            '<div class="css-fsa3o0">Complex Case</div><p>Complex paragraph with <code>multiple</code> code <code>snippets</code>.</p><ul><li>First instruction</li><li>Second instruction</li></ul><strong>Answer</strong><div><li>First answer</li><li>Second answer</li></div>',
            "# Complex Case\n\nComplex paragraph with `multiple` code `snippets`.\n\n## Instructions\n\n- First instruction\n\n- Second instruction\n\n## Answer\n\n- First answer\n\n- Second answer",
        ),
    ],
)
def test_convert_html_to_markdown(html, expected_markdown):
    assert convert_html_to_markdown(html) == expected_markdown
