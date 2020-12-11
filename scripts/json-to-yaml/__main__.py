import sys, yaml, json

sys.stdout.write(yaml.dump(json.load(sys.stdin)))
