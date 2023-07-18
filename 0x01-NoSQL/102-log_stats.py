#!/usr/bin/env python3
"""
Script that provides stats about Nginx logs stored in MongoDB
"""

from pymongo import MongoClient


def log_stats():
    """
    Provides stats about Nginx logs stored in MongoDB
    """
    client = MongoClient('mongodb://localhost:27017')
    logs_collection = client.logs.nginx

    # Total number of logs
    total_logs = logs_collection.count_documents({})

    print(f"{total_logs} logs")

    # Count of different HTTP methods
    methods = logs_collection.aggregate([
        {"$group": {"_id": "$method", "count": {"$sum": 1}}}
    ])

    print("Methods:")
    for method in methods:
        print(f"    method {method['_id']}: {method['count']}")

    # Count of status checks
    status_check_count = logs_collection.count_documents({"method": "GET", "path": "/status"})

    print(f"{status_check_count} status check")

    # Top 10 most present IPs
    top_ips = logs_collection.aggregate([
        {"$group": {"_id": "$ip", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 10}
    ])

    print("IPs:")
    for ip in top_ips:
        print(f"    {ip['_id']}: {ip['count']}")


if __name__ == '__main__':
    log_stats()

