import rpy2.robjects as robjects
from rpy2.robjects.packages import importr

importr("rvest")
read_html = robjects.r("read_html")
html_nodes = robjects.r("html_nodes")
html_attr = robjects.r("html_attr")
as_character = robjects.r("as.character")
paste0 = robjects.r("paste0")


def scrape_course_url_to_exercise_urls(course_url):
    exercise_urls = html_attr(
        html_nodes(read_html(course_url), xpath='//div[@class="css-1k6or5q"]//a'),
        "href",
    )
    return exercise_urls


def scrape_exercise_url_to_html(exercise_url):
    sections = html_nodes(
        read_html(exercise_url), xpath='//div[@class="listview__content"]'
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
    exercise_content = ", ".join(
        list(paste0(section1, instructions_heading, section2, solutions_heading))
    )

    return exercise_content


course = "https://www.datacamp.com/courses/introduction-to-python"

exercises = scrape_course_url_to_exercise_urls(course)
print(scrape_exercise_url_to_html(exercises[2]))
