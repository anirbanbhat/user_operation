register_schema = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "email": {"type": "string"},
        "password": {"type": "string"}
    },
    "required": ["name", "email", "password"]
}

update_schema = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "password": {"type": "string"}
    },
    "anyOf": [
        {"required": ["name"]},
        {"required": ["password"]}
    ]
}

login_schema = {
    "type": "object",
    "properties": {
        "email": {"type": "string"},
        "password": {"type": "string"}
    },
    "required": ["email", "password"]
}
