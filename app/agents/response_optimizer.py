import re


class ResponseOptimizer:

    def __init__(
        self,
        max_chunks=4,
        max_chunk_chars=1200
    ):
        self.max_chunks = max_chunks
        self.max_chunk_chars = max_chunk_chars

    def remove_duplicates(
        self,
        chunks
    ):

        seen = set()
        unique = []

        for chunk in chunks:

            text = chunk["text"]

            key = text[:300].lower()

            if key in seen:
                continue

            seen.add(key)

            unique.append(chunk)

        return unique

    def remove_short_chunks(
        self,
        chunks
    ):

        filtered = []

        for chunk in chunks:

            if len(
                chunk["text"].split()
            ) < 40:
                continue

            filtered.append(chunk)

        return filtered

    def score_chunk(
        self,
        chunk,
        query
    ):

        text = chunk["text"].lower()

        query_words = set(
            query.lower().split()
        )

        score = 0

        for word in query_words:

            if word in text:
                score += 1

        return score

    def rank_chunks(
        self,
        chunks,
        query
    ):

        ranked = sorted(
            chunks,
            key=lambda x: self.score_chunk(
                x,
                query
            ),
            reverse=True
        )

        return ranked

    def trim_chunk(
        self,
        text
    ):

        return text[
            :self.max_chunk_chars
        ]

    def optimize(
        self,
        chunks,
        query
    ):

        chunks = self.remove_duplicates(
            chunks
        )

        chunks = self.remove_short_chunks(
            chunks
        )

        chunks = self.rank_chunks(
            chunks,
            query
        )

        chunks = chunks[
            :self.max_chunks
        ]

        optimized = []

        for chunk in chunks:

            optimized.append(
                {
                    **chunk,
                    "text": self.trim_chunk(
                        chunk["text"]
                    )
                }
            )

        return optimized


optimizer = ResponseOptimizer()