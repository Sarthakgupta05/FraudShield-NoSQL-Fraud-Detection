"""
Unit tests for Document NoSQL Storage (MongoDB client & in-memory engine).
"""

import pytest
from src.backend.database.mongo_client import NoSQLDocumentStore

def test_document_crud_operations():
    store = NoSQLDocumentStore()
    col = store.get_collection("test_transactions")
    col.delete_many({})

    # 1. Insert One
    doc1 = {
        "transaction_id": "TX_TEST_01",
        "sender_account": "ACC_101",
        "receiver_account": "ACC_202",
        "amount": 1500.0,
        "payment_type": "UPI_INSTANT",
        "tags": ["retail", "fast"]
    }
    res = col.insert_one(doc1)
    assert res.inserted_id is not None

    # 2. Count Documents
    assert col.count_documents() == 1
    assert col.count_documents({"sender_account": "ACC_101"}) == 1
    assert col.count_documents({"sender_account": "ACC_999"}) == 0

    # 3. Insert Many
    docs = [
        {"transaction_id": f"TX_TEST_{i}", "sender_account": "ACC_101", "amount": i * 1000.0}
        for i in range(2, 6)
    ]
    col.insert_many(docs)
    assert col.count_documents({"sender_account": "ACC_101"}) == 5

    # 4. Filter Queries ($gte, $lte)
    high_amt = col.find({"amount": {"$gte": 3000.0}})
    assert len(high_amt) == 3

    # 5. Update Operations ($set, $inc)
    col.update_one({"transaction_id": "TX_TEST_01"}, {"$set": {"status": "FLAGGED"}, "$inc": {"amount": 500.0}})
    updated = col.find_one({"transaction_id": "TX_TEST_01"})
    assert updated["status"] == "FLAGGED"
    assert updated["amount"] == 2000.0

    # Cleanup
    col.delete_many({})
    assert col.count_documents() == 0
