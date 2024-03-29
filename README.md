## Updating the OpenAPI

The process of updating the OpenAPI is mostly automated, you only need to run a
few scripts. First determine the version you want for OpenAPI spec from the
BCGov agent docker images
(https://hub.docker.com/r/bcgovimages/aries-cloudagent/). Currently the default
for the `retrieve-openapi.sh` script is "py3.9-0.10.1".

After that you can run the following commands to update the `openapi.yml`
file.

```sh
cd acapy-openapi

# Retrieve the open api file, change py3.9-0.10.1 if you want another version
./scripts/retrieve-openapi.sh py3.9-0.10.1

# transform to OpenAPI V3
./scripts/convert-to-openapi3.sh

# Fix the openapi file (add missing operation ids from data/operation-id-map.yml)
./scripts/process-openapi.sh

# Apply manual patches to the openapi file
./scripts/apply-patch.sh
```
