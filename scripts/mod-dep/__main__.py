# git friendly yaml modification

import sys, yaml, io, argparse
from yaml.events import MappingStartEvent, MappingEndEvent, ScalarEvent

parser = argparse.ArgumentParser()
parser.add_argument("--request-cpu", help="modifiy cpu requests")
parser.add_argument("--request-memory", help="modifiy memory requests")
parser.add_argument("--limit-cpu", help="modifiy cpu limits")
parser.add_argument("--limit-memory", help="modifiy memory limits")

args = parser.parse_args()

document = sys.stdin.read()
events = yaml.parse(io.StringIO(document))
lines = document.splitlines()

last_value = None
in_resources = False
in_requests = False
in_limits = False

request_memory = None
request_cpu = None
limit_memory = None
limit_cpu = None

for event in events:
    if last_value == 'resources' and isinstance(event, MappingStartEvent):
        in_resources = True

    elif in_resources and last_value == 'requests' and isinstance(event, MappingStartEvent):
        in_requests = True

    elif in_resources and last_value == 'limits' and isinstance(event, MappingStartEvent):
        in_limits = True

    elif in_requests and last_value == 'cpu' and isinstance(event, ScalarEvent):
        request_cpu = event

    elif in_requests and last_value == 'memory' and isinstance(event, ScalarEvent):
        request_memory = event

    elif in_limits and last_value == 'cpu' and isinstance(event, ScalarEvent):
        limit_cpu = event

    elif in_limits and last_value == 'memory' and isinstance(event, ScalarEvent):
        limit_memory = event

    elif in_requests and isinstance(event, MappingEndEvent):
        in_requests = False

    elif in_limits and isinstance(event, MappingEndEvent):
        in_limits = False

    elif in_resources and isinstance(event, MappingEndEvent):
        in_resources = False

    if isinstance(event, ScalarEvent):
        last_value = event.value
    else:
        last_value = None

found_events = [request_memory, request_cpu, limit_cpu, limit_memory]

def replace(event, doc, value, events):
    result = doc[:event.start_mark.index] + value + doc[event.end_mark.index:]
    diff = len(value) - (event.end_mark.index - event.start_mark.index)
    for e in events:
        if e.start_mark.index > event.end_mark.index:
            e.start_mark.index += diff
            e.end_mark.index += diff
    return result

if args.request_cpu is not None:
    document = replace(request_cpu, document, args.request_cpu, found_events)
if args.request_memory is not None:
    document = replace(request_memory, document, args.request_memory, found_events)
if args.limit_cpu is not None:
    document = replace(limit_cpu, document, args.limit_cpu, found_events)
if args.limit_memory is not None:
    document = replace(limit_memory, document, args.limit_memory, found_events)

sys.stdout.write(document)
