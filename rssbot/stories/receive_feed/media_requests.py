import aiohttp
from botstory.integrations import commonhttp


async def upload_podcast(url, ctx, story):
    try:
        await story.start_typing(
            user=ctx['user'],
        )

        await story.send_audio(url=url,
                               user=ctx['user'])
    except commonhttp.errors.HttpRequestError as err:
        new_location = await where_is_located(url)
        if new_location and new_location != url:
            await upload_podcast(new_location, ctx, story)
        else:
            raise err

async def where_is_located(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url, allow_redirects=False) as resp:
            # TODO: should store redirected links
            print('-'*80)
            print('resp.status: {}'.format(resp.status))
            print('resp.headers {}'.format(resp.headers))
            print('-'*80)
            if resp.status == 302:
                return resp.headers['Location']
            else:
                return None
