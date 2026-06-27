from paper2slides.parser import PaperParser

parser = PaperParser()

paper = parser.parse("examples/sample.pdf")

print("Title:", paper.title)
print("Abstract:", paper.abstract[:500])