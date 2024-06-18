import rpy2.robjects as robjects
from rpy2.robjects.packages import importr

importr("rvest")
read_html = robjects.r("read_html")
html_nodes = robjects.r("html_nodes")
html_attr = robjects.r("html_attr")
as_character = robjects.r("as.character")
paste0 = robjects.r("paste0")


def scrape_chapter_url_to_html(exercise):
    sections = html_nodes(
        read_html(exercise), xpath='//div[@class="listview__content"]'
    )
    if len(sections) == 0:
        return None

    section1 = as_character(sections)[0]
    section2 = paste0(
        html_nodes(
            read_html(as_character(sections)[1]),
            xpath='//div[@class="exercise--instructions__content"]',
        )
    )

    instructions_heading = "<strong>Instructions</strong>"
    solutions_heading = "<strong>Answer</strong>"
    chapter_content = ", ".join(
        list(paste0(section1, instructions_heading, section2, solutions_heading))
    )

    return chapter_content


exercises = "https://campus.datacamp.com/courses/intro-to-python-for-data-science/chapter-1-python-basics?ex=3"

exercise = scrape_chapter_url_to_html(exercises)

print(type(exercise))
print(exercise)
