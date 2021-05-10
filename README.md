# Notes

## External-DNS

External DNS requires `external-dns-secret` secret to exist on the target cluster:

```json
{
    "tenantId": "AAAAA",
    "subscriptionId": "BBBBB",
    "aadClientId": "CCCCC",
    "aadClientSecret": "DDDDD",
    "resourceGroup": "EEEEE"
}
```

## Chartmuseum

Chartmuseum requires `chartmuseum-secret` to exist on the target cluster:

```yaml
AZURE_STORAGE_ACCESS_KEY: AAAAA
AZURE_STORAGE_ACCOUNT: BBBBB
BASIC_AUTH_PASS: CCCCC
BASIC_AUTH_USER: DDDDD
```

Temp workaround:

```bash
kubectl create secret generic chartmuseum-secret \
    --from-literal="AZURE_STORAGE_ACCESS_KEY=AAAAA" \
    --from-literal="AZURE_STORAGE_ACCOUNT=BBBBB" \
    --from-literal="BASIC_AUTH_PASS=CCCCC" \
    --from-literal="BASIC_AUTH_USER=DDDDD"
```
