# YaK collection

## Inventory plugin

### db

You can overwrite the default behavior of the inventory using these environment variables:

- `DEBUG`: Display more information for debugging purpose.
  - Valid options: [`true`, `1`, `yes`, `false`, `0`, `no`].
- `YAK_ANSIBLE_TRANSPORT_URL`: The YAK backend entry point.
  - Valid option: `<URL TO BACKEND ENTRYPOINT>`.
- `YAK_SSL_VERIFY_CERTIFICATE`: If you need to bypass the certificate validation, enable this.
  - Valid options: [`true`, `1`, `yes`, `false`, `0`, `no`].
- `HTTPS_PROXY`, `HTTP_PROXY`: To instruct the inventory to use an HTTPS or HTTP proxy.
  - Valid option: `https://<proxy-hostname>:<port-number>`.
