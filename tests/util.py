import yaml

def fetch_config(filename="esc.yaml"):
    with open(filename, 'r') as stream:
        try:
            conf = yaml.safe_load(stream)
            return conf
            steering = (conf['steering']['center'], conf['steering']['left'], conf['steering']['right'])
            throttle = (conf['throttle']['neutral'], conf['throttle']['reverse'], conf['throttle']['forward'])
        except yaml.YAMLError as exc:
            print(exc)

