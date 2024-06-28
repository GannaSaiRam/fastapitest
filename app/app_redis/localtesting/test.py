import redis

# Initialize the Redis connection
r = redis.Redis(host='localhost', port='26379', db=0)

def process_keys_in_batches(prefix, batch_size):
    cursor = 0
    while True:
        cursor, keys = r.scan(cursor=cursor, match=prefix + '*', count=batch_size)
        if not keys:
            break
        # Sort keys to simulate order of insertion
        keys = sorted(keys)
        for key in keys:
            # Process the key (placeholder for actual processing logic)
            print(f"Processing {key}")
            # Remove the key after processing
            r.delete(key)
        # If cursor is 0, we have completed the iteration
        if cursor == 0:
            break

# Example usage
PREFIX = 'key'
BATCH_SIZE = 10000
process_keys_in_batches(PREFIX, BATCH_SIZE)
