class DataManager:
    @classmethod
    def process_data(cls, data):
        # Simulate some processing
        return f"Processed {data}"

async def async_function():
    # Call a synchronous class method within an async function
    result = DataManager.process_data("some data")
    print(result)
    # Perform additional async operations here if needed

import asyncio

# Running the async function
asyncio.run(async_function())
