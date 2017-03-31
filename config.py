import yaml

def getConfig():
    with open("config.yaml", 'r') as yamlfile:
        config = yaml.load(yamlfile)
        return config

def getConfigForGuild(guild):
    config = getConfig()
    guildc = config['guilds'][guild]
    return