"""
MongoDB Document Database Client with seamless in-memory fallback.
Ensures the system works in full production with live MongoDB (mongodb://localhost:27017)
or in-memory mock storage without requiring external daemon startup.
"""

import os
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime, timezone
import pymongo
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError

logger = logging.getLogger("fraudshield.mongo")

class InMemoryCollection:
    """High-performance in-memory document store matching MongoDB API semantics."""
    def __init__(self, name: str):
        self.name = name
        self._documents: List[Dict[str, Any]] = []
        self._indexes: Dict[str, bool] = {}

    def create_index(self, key_or_list, **kwargs):
        index_name = str(key_or_list)
        self._indexes[index_name] = True
        return index_name

    def insert_one(self, doc: Dict[str, Any]):
        doc_copy = dict(doc)
        if "_id" not in doc_copy:
            doc_copy["_id"] = doc_copy.get("id") or str(len(self._documents) + 1)
        self._documents.append(doc_copy)
        class InsertResult:
            def __init__(self, inserted_id):
                self.inserted_id = inserted_id
        return InsertResult(doc_copy["_id"])

    def insert_many(self, docs: List[Dict[str, Any]]):
        inserted_ids = []
        for d in docs:
            res = self.insert_one(d)
            inserted_ids.append(res.inserted_id)
        class InsertManyResult:
            def __init__(self, ids):
                self.inserted_ids = ids
        return InsertManyResult(inserted_ids)

    def _matches_filter(self, doc: Dict[str, Any], filter_query: Dict[str, Any]) -> bool:
        if not filter_query:
            return True
        for k, v in filter_query.items():
            doc_val = doc.get(k)
            if isinstance(v, dict):
                for op, op_val in v.items():
                    if op == "$gte":
                        if doc_val is None or doc_val < op_val:
                            return False
                    elif op == "$lte":
                        if doc_val is None or doc_val > op_val:
                            return False
                    elif op == "$gt":
                        if doc_val is None or doc_val <= op_val:
                            return False
                    elif op == "$lt":
                        if doc_val is None or doc_val >= op_val:
                            return False
                    elif op == "$in":
                        if doc_val not in op_val:
                            return False
                    elif op == "$ne":
                        if doc_val == op_val:
                            return False
            else:
                if doc_val != v:
                    return False
        return True

    def find(self, filter_query: Optional[Dict[str, Any]] = None, limit: int = 0, sort: Optional[List] = None) -> List[Dict[str, Any]]:
        filter_query = filter_query or {}
        matches = [d for d in self._documents if self._matches_filter(d, filter_query)]
        
        if sort:
            for field, order in reversed(sort):
                matches.sort(key=lambda x: x.get(field, 0), reverse=(order == -1 or order == pymongo.DESCENDING))
        
        if limit > 0:
            return matches[:limit]
        return matches

    def find_one(self, filter_query: Optional[Dict[str, Any]] = None) -> Optional[Dict[str, Any]]:
        res = self.find(filter_query, limit=1)
        return res[0] if res else None

    def count_documents(self, filter_query: Optional[Dict[str, Any]] = None) -> int:
        return len(self.find(filter_query))

    def update_one(self, filter_query: Dict[str, Any], update_doc: Dict[str, Any], upsert: bool = False):
        doc = self.find_one(filter_query)
        if doc:
            if "$set" in update_doc:
                doc.update(update_doc["$set"])
            if "$inc" in update_doc:
                for k, v in update_doc["$inc"].items():
                    doc[k] = doc.get(k, 0) + v
            if "$push" in update_doc:
                for k, v in update_doc["$push"].items():
                    if k not in doc or not isinstance(doc[k], list):
                        doc[k] = []
                    doc[k].append(v)
            return True
        elif upsert:
            new_doc = dict(filter_query)
            if "$set" in update_doc:
                new_doc.update(update_doc["$set"])
            self.insert_one(new_doc)
            return True
        return False

    def delete_many(self, filter_query: Optional[Dict[str, Any]] = None):
        filter_query = filter_query or {}
        self._documents = [d for d in self._documents if not self._matches_filter(d, filter_query)]

class NoSQLDocumentStore:
    def __init__(self, uri: Optional[str] = None):
        self.uri = uri or os.getenv("MONGODB_URI", "mongodb://localhost:27017")
        self.db_name = "fraudshield_db"
        self.is_connected_to_live_mongo = False
        self._client = None
        self._db = None
        self._mock_collections: Dict[str, InMemoryCollection] = {}
        self._init_connection()

    def _init_connection(self):
        try:
            client = pymongo.MongoClient(self.uri, serverSelectionTimeoutMS=1000)
            client.admin.command('ping')
            self._client = client
            self._db = client[self.db_name]
            self.is_connected_to_live_mongo = True
            self._setup_indexes()
            logger.info("Connected to live MongoDB instance at %s", self.uri)
        except (ConnectionFailure, ServerSelectionTimeoutError, Exception) as e:
            self.is_connected_to_live_mongo = False
            logger.info("Live MongoDB not reachable. Initializing high-speed In-Memory NoSQL Document Store. (%s)", e)

    def _setup_indexes(self):
        if self.is_connected_to_live_mongo:
            self._db.transactions.create_index([("transaction_id", pymongo.ASCENDING)], unique=True)
            self._db.transactions.create_index([("sender_account", pymongo.ASCENDING)])
            self._db.transactions.create_index([("receiver_account", pymongo.ASCENDING)])
            self._db.transactions.create_index([("timestamp", pymongo.DESCENDING)])
            self._db.accounts.create_index([("account_id", pymongo.ASCENDING)], unique=True)
            self._db.alerts.create_index([("risk_score", pymongo.DESCENDING)])

    def get_collection(self, name: str):
        if self.is_connected_to_live_mongo:
            return self._db[name]
        if name not in self._mock_collections:
            self._mock_collections[name] = InMemoryCollection(name)
        return self._mock_collections[name]

    @property
    def transactions(self):
        return self.get_collection("transactions")

    @property
    def accounts(self):
        return self.get_collection("accounts")

    @property
    def alerts(self):
        return self.get_collection("alerts")

    def get_status(self) -> Dict[str, Any]:
        return {
            "engine": "Live MongoDB Cluster" if self.is_connected_to_live_mongo else "In-Memory Document NoSQL Engine",
            "connected_live": self.is_connected_to_live_mongo,
            "database": self.db_name,
            "collections": {
                "transactions": self.transactions.count_documents(),
                "accounts": self.accounts.count_documents(),
                "alerts": self.alerts.count_documents(),
            }
        }

# Global singleton instance
doc_store = NoSQLDocumentStore()
