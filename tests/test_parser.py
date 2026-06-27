from paper2slides.parser import PaperParser

parser = PaperParser()
paper = parser.parse("examples/sample.pdf")

print("Title:", paper.title)
print("Abstract:", paper.abstract[:500])
print("Sections:", len(paper.sections))

for section in paper.sections[:5]:
    print("-", section.title)