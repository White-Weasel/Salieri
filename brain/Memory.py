import logging
import queue
import threading
import traceback
import uuid
from qdrant_client import QdrantClient
from qdrant_client.http import models, exceptions
from .models.ChatGPT import embed

logger = logging.getLogger(__name__)

SHORT_MEM_LENGTH = 3
MIN_SCORE = 0.75


class LongTermMemory:
    def __init__(self, host="localhost", port=6333, collection_name="Salieri_conversation_memory"):
        self.client = QdrantClient(host, port=port)
        self.collection_name = collection_name
        try:
            self.client.get_collection(collection_name=self.collection_name)
        except exceptions.UnexpectedResponse:
            logger.warning(f"Collection {self.collection_name} not existed, creating collection")
            self.client.recreate_collection(
                collection_name=self.collection_name,
                vectors_config={
                    "embedded_vector": models.VectorParams(size=1536, distance=models.Distance.DOT),
                }
            )
        pass

    def conversation_search(self, message, limit=3):
        vector = embed(message)
        result = self.client.search(
            collection_name=self.collection_name,
            query_vector=("embedded_vector", vector),
            score_threshold=MIN_SCORE,
            limit=limit,
        )
        return '\n'.join([r.payload['conversation'] for r in result])

    def save_conversation(self, conversation, vector):
        self.client.upsert(
            collection_name=self.collection_name,
            points=[
                models.PointStruct(
                    id=str(uuid.uuid4()),
                    vector={"embedded_vector": vector},
                    payload={
                        "conversation": conversation,
                    }
                )
            ]
        )

    def clear_memory(self):
        self.client.delete_collection(collection_name=self.collection_name)
        self.client.recreate_collection(
            collection_name=self.collection_name,
            vectors_config={
                "embedded_vector": models.VectorParams(size=1536, distance=models.Distance.DOT),
            }
        )


class ShortTermMemory(queue.Queue):
    def __init__(self, host="localhost", port=6333, collection_name="Salieri_conversation_memory", *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._conversation_count = 0
        self.long_term_memory = LongTermMemory(host, port, collection_name)

    def put(self, *args, **kwargs):
        super().put(*args, **kwargs)
        self._conversation_count += 1
        if self._conversation_count >= SHORT_MEM_LENGTH:
            self._conversation_count = 0
            logger.warning("Saving conversation")
            threading.Thread(target=self.convert_to_long_term).start()

    def convert_to_long_term(self):
        """Empty the queue and save them into LongTermMemory. This method should run on another thread."""
        conver = []
        while not self.empty():
            conver.append(self.get())
        if not conver:
            return
        if isinstance(conver[0], dict):
            convo_text = ''.join(
                [f"{'User' if line['role'] == 'user' else 'Marv'}: {line['content']}\n" for line in conver])
        else:
            convo_text = '\n'.join([line for line in conver])
        vector = embed(convo_text)
        self.long_term_memory.save_conversation(convo_text, vector)


if __name__ == '__main__':
    COLLECTION_NAME = "1st_collection"

    client = QdrantClient("localhost", port=6333)

    try:
        client.get_collection(collection_name=COLLECTION_NAME)
    except exceptions.UnexpectedResponse as e:
        logger.warning("Creating collection")
        client.recreate_collection(
            collection_name="1st_collection",
            vectors_config={
                "text": models.VectorParams(size=4, distance=models.Distance.DOT),
            }
        )

    a = client.upsert(
        collection_name="1st_collection",
        points=[
            models.PointStruct(
                id=str(uuid.uuid4()),
                vector={"text": [0.05, 0.61, 0.76, 0.74]},
                payload={
                    "city": "Berlin",
                    "price": 1.99,
                },
            ),
        ]
    )

    # client.search(
    #     collection_name=COLLECTION_NAME,
    #     query_filter=models.Filter(
    #         must=[
    #             models.FieldCondition(
    #                 key="city",
    #                 match=models.MatchValue(
    #                     value="London",
    #                 ),
    #             )
    #         ]
    #     ),
    #     search_params=models.SearchParams(
    #         hnsw_ef=128,
    #         exact=False
    #     ),
    #     query_vector=[0.2, 0.1, 0.9, 0.7],
    #     limit=3,
    # )

    res = client.search(
        collection_name=COLLECTION_NAME,
        query_vector=("text", [0.2, 0.1, 0.9, 0.7]),
        # limit=3,
    )

    print([r.payload for r in res])

    client.delete(
        collection_name=COLLECTION_NAME,
        points_selector=models.PointIdsList(
            points=[r.id for r in res],
        ),
    )
