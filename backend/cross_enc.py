from sentence_transformers import CrossEncoder

model = CrossEncoder(
    "cross-encoder/ms-marco-MiniLM-L6-v2",
    backend="openvino",
    model_kwargs={"file_name": "openvino/openvino_model_qint8_quantized.xml"},
)

# 2. Predict scores for a pair of sentences
scores = model.predict(
    [
        (
            "How many people live in Berlin?",
            "Berlin had a population of 3,520,031 registered inhabitants in an area of 891.82 square kilometers.",
        ),
        ("How many people live in Berlin?", "Berlin is well known for its museums."),
    ]
)
# => array([ 8.607138 , -4.3200774], dtype=float32)

# 3. Rank a list of passages for a query
query = "How many people live in Berlin?"
passages = [
    "Berlin had a population of 3,520,031 registered inhabitants in an area of 891.82 square kilometers.",
    "Berlin is well known for its museums.",
    "In 2014, the city state Berlin had 37,368 live births (+6.6%), a record number since 1991.",
    "The urban area of Berlin comprised about 4.1 million people in 2014, making it the seventh most populous urban area in the European Union.",
    "The city of Paris had a population of 2,165,423 people within its administrative city limits as of January 1, 2019",
    "An estimated 300,000-420,000 Muslims reside in Berlin, making up about 8-11 percent of the population.",
    "Berlin is subdivided into 12 boroughs or districts (Bezirke).",
    "In 2015, the total labour force in Berlin was 1.85 million.",
    "In 2013 around 600,000 Berliners were registered in one of the more than 2,300 sport and fitness clubs.",
    "Berlin has a yearly total of about 135 million day visitors, which puts it in third place among the most-visited city destinations in the European Union.",
]
ranks = model.rank(query, passages)

# Print the scores
print("Query:", query)
for rank in ranks:
    print(f"{rank['score']:.2f}\t{passages[rank['corpus_id']]}")
