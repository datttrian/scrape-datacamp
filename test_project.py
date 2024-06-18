import pytest
from rpy2.robjects.packages import importr
from project import scrape_exercise_url_to_html
import rpy2.robjects as robjects

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


urls_no_content = [
    "https://campus.datacamp.com/courses/intro-to-python-for-data-science/chapter-1-python-basics?ex=1",
    "https://campus.datacamp.com/courses/intro-to-python-for-data-science/chapter-1-python-basics?ex=2",
    "https://campus.datacamp.com/courses/intro-to-python-for-data-science/chapter-1-python-basics?ex=6",
]


@pytest.mark.parametrize("urls_no_content", urls_no_content)
def test_scrape_no_content(urls_no_content):
    result = scrape_exercise_url_to_html(urls_no_content)
    assert result is None


urls_unsuccessful = [
    "https://example.com/",
    "https://www.youtube.com/",
]


@pytest.mark.parametrize("urls_unsuccessful", urls_unsuccessful)
def test_scrape_exercise_url_to_html_unsuccessful(urls_unsuccessful):
    result = scrape_exercise_url_to_html(urls_unsuccessful)
    assert result is None
