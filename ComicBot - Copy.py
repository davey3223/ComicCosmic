import discord
import requests
import asyncio


client = discord.Client()

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

@client.event
async def on_message(message):
    if message.content.startswith('comic'):
        # Get the name of the comic book series from the user's message
        series_name = message.content[5:]

        # Use the Comic Vine API to search for the comic book series
        api_key = "YOUR_API_KEY_HERE"
        response = requests.get(f"https://comicvine.gamespot.com/api/search/?api_key={api_key}&format=json&query={series_name}&resources=volume")
        results = response.json()
        if len(results["results"]) == 0:
            await message.channel.send(f"No results found for '{series_name}'.")
            return

        # Create a list of options for the user to choose from
        options = []
        for result in results["results"]:
            name = result["name"]
            option = discord.MessageAction(name=name, value=name)
            options.append(option)

        # Create a message with a list of options for the user to choose from
        prompt = "Please select a comic book series from the list below:"
        message = await message.channel.send(prompt, embed=discord.Embed(title="Comic Book Series", fields=[discord.Embed.Field(name="Options", value="\n".join(options))]))

        # Add a reaction to the message for each option
        for option in options:
            await message.add_reaction(option.emoji)

        # Wait for the user to select an option
        def check(reaction, user):
            return reaction.message.id == message.id and user == message.author
        try:
            reaction, user = await client.wait_for("reaction_add", check=check, timeout=30.0)
        except asyncio.TimeoutError:
            await message.channel.send("Timed out.")
            return

        # Get the selected option
        selected_option = reaction.emoji
        for option in options:
            if option.emoji == selected_option:
                series_name = option.value
                break

        # Use the Comic Vine API to search for the selected comic book series
        response = requests.get(f"https://comicvine.gamespot.com/api/search/?api_key={api_key}&format=json&query={series_name}&resources=volume")
        results = response.json()
        if len(results["results"]) == 0:
            await message.channel.send(f"No results found for '{series_name}'.")
            return

        # Get the first result from the search
        series = results["results"][0]

        # Get the name and ID of the series
        series_name = series["name"]
        series_id = series["id"]

        # Use the Comic Vine API to get the list of issues in the series
        response = requests.get(f"https://comicvine.gamespot.com/api/volume/4050-{series_id}/?api_key={api_key}&format=json&field_list=name,issue_number,store_date,price")
        series_info = response.json()

        # Create a list of options for the user to choose from
        options = []
        for issue in series_info["results"]["issues"]:
            name = f"{issue['name']} #{issue['issue_number']}"
            option = discord.MessageAction(name=name, value=name)
            options.append(option)

        # Create a message with a list of options for the user to choose from
        prompt = f"Please select an issue from the '{series_name}' series:"
        message = await message.channel.send(prompt, embed=discord.Embed(title="Comic Book Issues", fields=[discord.Embed.Field(name="Options", value="\n".join(options))]))

        # Add a reaction to the message for each option
        for option in options:
            await message.add_reaction(option.emoji)

        # Wait for the user to select an option
        def check(reaction, user):
            return reaction.message.id == message.id and user == message.author
        try:
            reaction, user = await client.wait_for("reaction_add", check=check, timeout=30.0)
        except asyncio.TimeoutError:
            await message.channel.send("Timed out.")
            return

        # Get the selected option
        selected_option = reaction.emoji
        for option in options:
            if option.emoji == selected_option:
                issue_name = option.value
                break

        # Get the release date and price of the selected issue
        for issue in series_info["results"]["issues"]:
            if f"{issue['name']} #{issue['issue_number']}" == issue_name:
                release_date = issue["store_date"]
                price = issue["price"]
                break

        # Send the information back to the user
        await message.channel.send(f"{issue_name} will be released on {release_date} and will cost ${price}.")
        
        for option in options:
            if option.emoji == selected_option:
                series_name = option.value
                break


        # Search for the selected issue in the list of issues
        for issue in series_info["results"]["issues"]:
            if f"{issue['name']} #{issue['issue_number']}" == issue_name:
                release_date = issue["store_date"]
                price = issue["price"]
                break

        # Send the information back to the user
        await message.channel.send(f"{issue_name} will be released on {release_date} and will cost ${price}.")

    client.run('YOUR_BOT_TOKEN_HERE')