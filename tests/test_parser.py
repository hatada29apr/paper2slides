from paper2slides.exporter import export_paper_json
from paper2slides.parser import PaperParser

parser = PaperParser()
paper = parser.parse("examples/sample.pdf")

output_path = export_paper_json(paper, "output/paper.json")

print("Title:", paper.title)
print("Abstract:", paper.abstract[:300])
print("Sections:", len(paper.sections))
print("Exported:", output_path)