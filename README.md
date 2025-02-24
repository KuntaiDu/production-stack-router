# production-stack-router


## Usage:

Run
```pip install -r requirements.txt```
to install python dependencies, and then run
```python test_router.py```
to test the router.



## Benchmarking results:

Example:
```
INFO:test_router:Nreq distribution: [400 200   0 400   0 400   0 400   0 400]
INFO:test_router:Cache-miss length: mean: 382.99, std: 368.24
INFO:test_router:142 out of 424 share-prefix requests were routed to the same endpoint
```

## Abstractions

### Prefix Matcher

The prefix matcher matches the request to a set of endpoints.

- `match(text: str, unavailable_endpoints: Set[str]) -> str`: Routes a request text to an available endpoint
- `update(text: str, endpoint: str) -> None`: Updates the matcher state after a request is routed
- `add_endpoints(endpoints: Set[str]) -> None`: Adds new endpoints to the matcher
- `remove_endpoints(endpoints: Set[str]) -> None`: Removes endpoints from the matcher

### Unavailable Endpoints Detector 

The unavailable endpoints detector identifies overloaded endpoints that should not receive new requests. It has:

- `detect(endpoints_to_status: Dict[str, EndpointStatus]) -> Set[str]`: Returns set of endpoints that are currently unavailable



## Hyper-parameters


- `router_class`: can be `LCPMatcher` (longest common prefix matcher) or `SimhashMatcher`.
- `dataset_size`: Number of requests to generate for testing (default: 2200)
- `num_running_requests_threshold`: Maximum number of concurrent requests an endpoint can handle before being marked as unavailable (default: 400)  
- `minimum_endpoints`: Minimum number of endpoints needed based on dataset size and request threshold
- `num_endpoints`: Total number of endpoints to create, set to 2x minimum required (default: 2 * minimum_endpoints)
- `continue_chat_probability`: Probability that a new request continues an existing conversation (default: 0.2)
- `tokens_typed_by_user_per_request`: Number of tokens in each simulated user request (default: 100)

