import os

import sqlalchemy
import pandas as pd

QUERY = """\
WITH theme_documents AS (
    SELECT DISTINCT document_id
    FROM themes
    WHERE theme = 'Внешняя политика'
),
metadata AS (
    SELECT
        dm.id,
        dm.title,
        dm.date AS date_published,
        dm.url AS source
    FROM documents_metadata dm
    INNER JOIN theme_documents td ON dm.id = td.document_id
),
relevant_sentences AS (
    SELECT
        s.document_id,
        string_agg(s.text::TEXT, E'\n' ORDER BY s.document_id, s.paragraph_id, s.sentence_id) AS "text"
    FROM sentences s
    INNER JOIN theme_documents td ON s.document_id = td.document_id
    GROUP BY s.document_id
)
SELECT
    m.id,
    m.title,
    m.date_published,
    m.source,
    rs.text
FROM metadata m
LEFT JOIN relevant_sentences rs ON m.id = rs.document_id
ORDER BY m.date_published DESC;"""

if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(current_dir, "rls", "input", "data.csv")

    engine = sqlalchemy.create_engine(os.environ["DATABASE_URI"])
    pd.read_sql(QUERY, con=engine).to_csv(output_path, index=False)
