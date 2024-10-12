# Supported URL for `repo_uri`

## GitHub Repo URLs

Supported GitHub URLs:

- `https://github.com/<repo_owner>/<repo_name>/tree/<repo_branch>/<repo_directory>`
  - In this case, make sure branch name doesn't contain `/`. This only works without `repo_branch` parameter.
  - e.g., https://github.com/swanchain/awesome-swanchain/tree/main/Llama3-8B-LLM-Chat
- `https://github.com/<repo_owner>/<repo_name>/tree/<repo_branch>`
  - e.g., https://github.com/alphaflows/hello/tree/test
- `⁠https://github.com/<repo_owner>/<repo_name>` (branch default to `main`)
  - e.g., https://github.com/alphaflows/hello
- `https://github.com/<repo_owner>/<repo_name>.git`  (branch default to `main`)
  - e.g., https://github.com/alphaflows/hello.git
- `git@github.com:<repo_owner>/<repo_name>.git`  (branch default to `main`)
  - e.g., git@github.com:alphaflows/hello.git

Note:
- If your branch name contains `/`, please use `repo_branch` to provide the branch name. `repo_branch` is prioritized for GitHub repo's branch name.
  - Example:
    - `repo_uri='https://github.com/alphaflows/hello'`
    - `repo_branch='feature/feature-branch-name-01'`

### Requirements for GitHub Repository

#### File Requirements

1. Your repository **must** include one of the following:
   - `Dockerfile`
   - `deploy.yaml`

2. **Priority**: If both files are present, `deploy.yaml` takes precedence.

#### deploy.yaml Specifications

If using `deploy.yaml`:
- **Mandatory**: Adhere to [LDL (Lagrange Definition Language) specifications](https://docs.lagrangedao.org/spaces/intro/lagrange-definition-language-ldl).


## Lagrange Space URLs

Lagrange space URLs containing : `spaces/<space_owner>/<space_name>`

e.g., 

- https://lagrange.computer/spaces/0x231fe9090f4d45413474BDE53a1a0A3Bd5C0ef03/chainnode-rpc/app
- https://lagrange.computer/spaces/0x231fe9090f4d45413474BDE53a1a0A3Bd5C0ef03/chainnode-rpc/card
- https://lagrange.computer/spaces/0x231fe9090f4d45413474BDE53a1a0A3Bd5C0ef03/chainnode-rpc/files

NOTE: Lagrange Space URL should match its environment, i.e., mainnet space url can be only used in mainnet and testnet space url can be only used in testnet.