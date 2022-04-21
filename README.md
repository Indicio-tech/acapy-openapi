## Updating the OpenAPI

The process of updating the OpenAPI is mostly automated, you only need to run a
few scripts. First determine the version you want for OpenAPI spec from the
BCGov agent docker images
(https://hub.docker.com/r/bcgovimages/aries-cloudagent/). Currently the default
for the `retrieve-openapi.sh` script is "py36-1.16-1_0.7.4".

After that you can run the following commands to update the `openapi.yml`
file.

```sh
cd acapy-openapi

# Retrieve the open api file, change py36-1.16-1_0.7.4 if you want another version
./scripts/retrieve-openapi.sh py36-1.16-1_0.7.4

# transform to OpenAPI V3
./scripts/convert-to-openapi3.sh

# Fix the openapi file (add missing operation ids from data/operation-id-map.yml)
./scripts/process-openapi.sh

# Apply manual patches to the openapi file
./scripts/apply-patch.sh
```
