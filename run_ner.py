from lxml import etree
import spacy
import os
import glob
import tqdm
import shutil
import time
from concurrent.futures import ProcessPoolExecutor

# XML Namespaces
TEI_NS = "http://www.tei-c.org/ns/1.0"
ns = {'tei': TEI_NS}

# Load spaCy NER model
tagger_path = os.path.join("models", "ck-model-best-cnn")
tagger = spacy.load(tagger_path)

# Pre-load the XSLT transformation
xslt_path = 'XSLT/clean_NER.xsl'
xslt_tree = etree.parse(xslt_path)
transform = etree.XSLT(xslt_tree)


def insert_xml_tags(text, entities):
    """
    Inserts XML tags around named entities in a text.
    Entities must be inserted from the end to avoid index shifting.
    """
    entities_sorted = sorted(entities, key=lambda x: x['start'], reverse=True)
    for ent in entities_sorted:
        start, end, label = ent['start'], ent['end'], ent['label']
        tagged_text = f"<{label}>{text[start:end]}</{label}>"
        text = text[:start] + tagged_text + text[end:]
    return text


def recognize(xml_doc, debug: bool = True):
    """
    Applies NER to all <reg> elements in a TEI XML document.
    Tags are inserted inside a new <reg> node with TEI namespace.
    """
    regs = xml_doc.xpath('//tei:reg', namespaces=ns)
    valid_regs = [reg for reg in regs if reg.text and reg.text.strip()]
    reg_texts = [reg.text.strip() for reg in valid_regs]

    # Remove tqdm here

    # Batch process with spaCy
    docs = tagger.pipe(reg_texts, batch_size=1, disable=["parser", "tagger"])

    for reg, doc in zip(valid_regs, docs):
        try:
            entities = [
                {"text": ent.text, "start": ent.start_char, "end": ent.end_char, "label": ent.label_}
                for ent in doc.ents
            ]
            tagged_text = insert_xml_tags(doc.text, entities)

            new_reg = etree.Element(f"{{{TEI_NS}}}reg")
            fragment = etree.fromstring(f"<wrapper xmlns='{TEI_NS}'>{tagged_text}</wrapper>")

            new_reg.text = fragment.text
            for child in fragment:
                new_reg.append(child)

            reg.getparent().replace(reg, new_reg)

        except Exception as e:
            if debug:
                print(f"⚠️ Error processing <reg>: {reg.text}")
                print(e)

    return xml_doc


def TEIsation(xml_doc, original_file_path):
    """
    Applies an XSLT transformation to a TEI document and saves it.
    """
    transformed = transform(xml_doc)
    output_path = original_file_path.replace(".xml", "_ner.xml")
    transformed.write(output_path, pretty_print=True, encoding="utf-8", method="xml", xml_declaration=True)


def process_file(file_path):
    """
    Parses and processes a single XML file:
    - Parses the file
    - Applies NER
    - Applies XSLT transformation
    - Saves the result
    """
    try:
        parser = etree.XMLParser(remove_blank_text=True)
        doc = etree.parse(file_path, parser)
        recognize(doc, debug=False)
        TEIsation(doc, file_path)
        return f"✅ {file_path}"
    except Exception as e:
        return f"❌ {file_path} — ERROR: {e}"


if __name__ == "__main__":
    start_time = time.time()

    input_files = glob.glob("origReg/**/*.xml", recursive=True)
    print(f"🔍 Found {len(input_files)} XML files.")

    # Parallel processing
    with ProcessPoolExecutor(max_workers=1) as executor:
        results = executor.map(process_file, input_files)
        for result in tqdm.tqdm(results, total=len(input_files), desc="Global Progress"):
            print(result)

    # Move transformed files to output directory
    output_dir = "NER"
    os.makedirs(output_dir, exist_ok=True)
    for file in glob.glob("origReg/**/*_ner.xml", recursive=True):
        if os.path.isfile(file):
            shutil.move(file, os.path.join(output_dir, os.path.basename(file)))

    elapsed = time.time() - start_time
    print(f"\n✅ Finished in {elapsed:.2f} seconds ({elapsed/60:.2f} minutes)")