# Reproducible Mock Demos

Run:

```bash
python3 -B -m trust_layer.demo_runner
```

## Email

- Draft to `example.com`: `ALLOW_WITH_LOG`
- Send to approved recipient without confirmation: `REQUIRE_CONFIRMATION`
- Send to unapproved domain: `BLOCK` in tests

## Travel

- Search: allowed by contract.
- Purchase under limit: `REQUIRE_CONFIRMATION`
- Purchase over USD 500: `BLOCK`

## File Management

- Rename inside `/workspace/demo`: `ALLOW_WITH_LOG`
- Delete: `BLOCK`
- Upload: `BLOCK`
- Path escape: `BLOCK` in tests
