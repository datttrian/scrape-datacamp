from rpy2 import robjects
from rpy2.robjects.packages import importr
from bs4 import BeautifulSoup


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


def convert_html_to_markdown(html):

    soup = BeautifulSoup(html, "html.parser")

    markdown = []

    if soup.find(class_="css-fsa3o0"):
        heading = soup.find(class_="css-fsa3o0").text.strip()
        markdown.append(f"# {heading}")

    for para in soup.find_all("p"):
        text = para.text.strip()
        for code in para.find_all("code"):
            text = text.replace(code.text, f"`{code.text}`")
        markdown.append(text)

    instructions = soup.find_all("ul")
    if instructions:
        markdown.append("## Instructions")
        for li in instructions[0].find_all("li"):
            markdown.append(f"- {li.text.strip()}")

    answer = soup.find_all("strong", string="Answer")
    if answer:
        markdown.append("## Answer")

        for sibling in answer[0].next_siblings:
            if sibling.name == "div":
                for li in sibling.find_all("li"):
                    markdown.append(f"- {li.text.strip()}")

    return "\n\n".join(markdown)


def main():
    COURSE = "https://www.datacamp.com/courses/introduction-to-python"
    exercises = scrape_course_url_to_exercise_urls(COURSE)
    html_exercise = scrape_exercise_url_to_html(exercises[7])
    markdown_exercise = convert_html_to_markdown(html_exercise)
    print(markdown_exercise)


if __name__ == "__main__":
    main()
