# Argument Graph

Recommended claim IDs:

- `MC-01`: main claim.
- `SC-01...`: supporting claims.
- `BC-01...`: boundary/limitation claims.
- `EC-01...`: engineering consequence claims.

Represent dependencies explicitly:

```text
GAP-01 -> RQ-01 -> SC-01 -> SC-02 -> MC-01 -> EC-01
                           \-> BC-01
```

For each edge, state why the downstream node depends on the upstream node.

A main claim should not depend on a purely decorative figure or an unverified assumption.
