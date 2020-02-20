- Update `requirements.nix`:

```sh
pypi2nix -V python3 -r requirements.txt -E 'pkgconfig libffi libxml2 libxslt openssl'
```

- Generate interpreter:

```sh
nix build -f requirements.nix interpreter
```
