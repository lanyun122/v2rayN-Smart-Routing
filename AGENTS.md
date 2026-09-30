# Repository Instructions

## Project purpose

This repository maintains public, auditable routing rules for v2rayN.

It provides routing rules and documentation only. It does not provide proxy nodes, subscriptions, residential proxies, accounts, passwords or authentication credentials.

## Repository scope

- The canonical public ruleset is `rules/v2rayn-routing-rules.json`.
- User-facing instructions belong in `README.md`.
- Published changes must be recorded in `CHANGELOG.md`.
- Contribution and security requirements are defined in `CONTRIBUTING.md` and `SECURITY.md`.
- Keep changes focused and avoid unrelated rewrites.

## Privacy and security

Never add or expose:

- Proxy node sharing links.
- Subscription URLs.
- UUIDs, passwords or authentication tokens.
- API keys, cookies or SSH private keys.
- Residential proxy credentials.
- Private service endpoints.
- Personally identifying IP addresses or unredacted logs.

Treat `美国住宅策略集` and `香港固定节点` as documented placeholder outbound names. Do not replace them with a maintainer's or contributor's private node names, addresses or credentials.

Never claim that a rule or version was tested unless that validation was actually performed.

## Routing behavior

Routing order is functional behavior. Rules are matched from top to bottom.

Unless a requested change explicitly modifies the design, preserve this order:

1. LAN direct access.
2. Ad blocking.
3. GPT custom outbound.
4. Gemini custom outbound.
5. Streaming custom outbound.
6. Exchange custom outbound.
7. UDP 443 blocking.
8. China direct access.
9. Final proxy fallback.

Preserve these public defaults unless a change explicitly documents otherwise:

- GPT is disabled by default.
- Gemini is disabled by default.
- Streaming is disabled by default.
- Exchange routing is disabled by default.
- LAN direct access is enabled.
- Ad blocking is enabled.
- UDP 443 blocking is enabled.
- China direct access is enabled.
- Final proxy fallback is enabled.

The final proxy fallback must remain last.

## Rule changes

When adding or changing a rule:

- Prefer established `geosite` and `geoip` categories over long manually maintained domain lists.
- Verify that referenced categories exist in the intended Geo data source.
- Document why the rule is needed and which outbound behavior is expected.
- Keep user-specific outbound rules disabled until the user binds an appropriate node or strategy group.
- Avoid broad matches when a narrower, verifiable match is available.
- Do not silently change default enablement, routing order or fallback behavior.
- Avoid reformatting the entire JSON file for a small change.

When behavior changes, update the README and CHANGELOG in the same change.

Published version tags are immutable snapshots. Do not modify or recreate an existing release tag. Use `main` for the continuously updated ruleset and a new version tag for each release.

## Validation

Before completing a ruleset change:

- Confirm the file is valid JSON.
- Confirm the root value is an array.
- Confirm every rule has a meaningful `remarks` value.
- Confirm every rule has a valid `outboundTag`.
- Confirm every `enabled` value is a JSON boolean.
- Confirm the final proxy fallback is present and remains last.
- Confirm custom outbound rules remain disabled unless the change explicitly requires otherwise.
- Check for duplicate or conflicting domain, IP, port and network matches.
- Check that no credentials or private connection details were introduced.
- Update documented rule counts and default states when they change.
- Test importing through the GitHub Raw URL in the documented v2rayN version when practical.

If an import test was not performed, state that clearly in the change description.

## Commit conventions

Use concise commit prefixes:

- `feat:` for new routing behavior.
- `fix:` for rule corrections.
- `docs:` for documentation-only changes.
- `test:` for validation coverage.
- `chore:` for repository maintenance.

Commit messages must describe the actual change. Do not create empty changes or version bumps only to generate activity.
