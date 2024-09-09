# Supported URL for `repo_uri`

## GitHub Repo URLs

Supported GitHub URLs:

- `https://github.com/<repo_owner>/<repo_name>/tree/<repo_branch>/<repo_directory>`
  - e.g., https://github.com/swanchain/awesome-swanchain/tree/main/Llama3-8B-LLM-Chat
- `https://github.com/<repo_owner>/<repo_name>/tree/<repo_branch>`
  - e.g., https://github.com/alphaflows/hello/tree/test
- `⁠https://github.com/<repo_owner>/<repo_name>` (branch default to `main`)
  - e.g., https://github.com/alphaflows/hello
- `https://github.com/<repo_owner>/<repo_name>.git`  (branch default to `main`)
  - e.g., https://github.com/alphaflows/hello.git
- `git@github.com:<repo_owner>/<repo_name>.git`  (branch default to `main`)
  - e.g., git@github.com:alphaflows/hello.git

## Lagrange Space URLs

Lagrange space URLs containing : `spaces/<space_owner>/<space_name>`

e.g., 

- https://lagrange.computer/spaces/0x231fe9090f4d45413474BDE53a1a0A3Bd5C0ef03/chainnode-rpc/app
- https://lagrange.computer/spaces/0x231fe9090f4d45413474BDE53a1a0A3Bd5C0ef03/chainnode-rpc/card
- https://lagrange.computer/spaces/0x231fe9090f4d45413474BDE53a1a0A3Bd5C0ef03/chainnode-rpc/files

NOTE: Lagrange Space URL should match its environment, i.e., mainnet space url can be only used in mainnet and testnet space url can be only used in testnet.