#!/usr/bin/env python3

import docker
import json

client = docker.from_env()

inventory = {
    "linux": {
        "hosts": []
    },
    "_meta": {
        "hostvars": {}
    }
}

containers = client.containers.list()

for container in containers:
    name = container.name

    # Only pick linux containers (you can refine later with labels)
    if "linux" in name:
        ports = container.attrs['NetworkSettings']['Ports']

        ssh_port = None
        if "22/tcp" in ports and ports["22/tcp"]:
            ssh_port = ports["22/tcp"][0]["HostPort"]

        if ssh_port:
            inventory["linux"]["hosts"].append(name)

            inventory["_meta"]["hostvars"][name] = {
                "ansible_host": "127.0.0.1",
                "ansible_port": ssh_port,
                "ansible_user": "ansible",
                "ansible_ssh_private_key_file": "~/.ssh/id_ed25519",
                "ansible_ssh_common_args": "-o StrictHostKeyChecking=no"
            }

print(json.dumps(inventory, indent=4))