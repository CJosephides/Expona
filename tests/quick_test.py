import requests

s = requests.Session()
req = "http://localhost:8080/user/christos"
js = {"pass": "banana"}
r = s.get(req, json=js)
print(r.text)

req = "http://localhost:8080/user/christos/expona"
js = {"exponents": [0, 3]}
r = s.post(req, json=js)
print(r.text)

req = "http://localhost:8080/user/christos/expona"
js = {"numbers": [1, 2, 3]}
r = s.get(req, json=js)
print(r.text)

req = "http://localhost:8080/user/christos/expona"
js = {"numbers": [1, 2, 3]}
r = s.get(req, json=js)
print(r.text)

req = "http://localhost:8080/user/christos/expona"
js = {"exponents": [1, 2]}
r = s.post(req, json=js)
print(r.text)

req = "http://localhost:8080/user/christos/expona"
js = {"numbers": [1, 2, 3]}
r = s.get(req, json=js)
print(r.text)

req = "http://localhost:8080/user/christos/expona"
js = {"numbers": [1, 2, 3]}
r = s.get(req, json=js)
print(r.text)

req = "http://localhost:8080/user/christos/expona"
js = {"exponents": [0]}
r = s.put(req, json=js)
print(r.text)

req = "http://localhost:8080/user/christos/expona"
js = {"numbers": [1, 2, 3]}
r = s.get(req, json=js)
print(r.text)
