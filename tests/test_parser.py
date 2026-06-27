from paper2slides.parser import PaperParser

parser = PaperParser()
doc = parser.load_pdf("examples/sample.pdf")

layout = parser.extract_layout(doc)

for page in layout[:1]:
    print("Page:", page["page"])
    for block in page["blocks"][:20]:
        print(
            f'{block["size"]:>5} | {block["font"]:<30} | {block["text"]}'
        )