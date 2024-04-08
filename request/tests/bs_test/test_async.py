import aiohttp
import asyncio


async def fetch(session, url):
    try:
        async with session.get(url) as response:
            # Optionally, check response status to handle errors (e.g., 404, 500)
            if response.status == 200:
                print(response)
                return await response.text(), response.status
            else:
                return f"Error: {response.status}", response.status
    except aiohttp.ClientError as e:
        return f"Request failed: {e}", 0


async def fetch_all(urls):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for url in urls:
            task = asyncio.create_task(fetch(session, url))
            tasks.append(task)
        responses = await asyncio.gather(*tasks)
        return responses


def run_test(file_path):
    # Read URLs from file
    with open(file_path, 'r') as file:
        urls = [line.strip() for line in file.readlines()]

    # Run the async event loop
    responses = asyncio.run(fetch_all(urls))

    # Print the responses (or do something else with them)
    for response in responses:
        print(response)


# Assuming your URLs are stored in 'urls.txt'
run_test('urls.txt')
