#!/usr/bin/env python3

import json
import re
import sys
from pathlib import Path


EXPECTED_RULES = [
    {
        "remarks": "局域网直连",
        "outboundTag": "direct",
        "enabled": True,
    },
    {
        "remarks": "广告过滤",
        "outboundTag": "block",
        "enabled": True,
    },
    {
        "remarks": "GPT",
        "outboundTag": "美国住宅策略集",
        "enabled": False,
    },
    {
        "remarks": "Gemini",
        "outboundTag": "美国住宅策略集",
        "enabled": False,
    },
    {
        "remarks": "流媒体",
        "outboundTag": "美国住宅策略集",
        "enabled": False,
    },
    {
        "remarks": "交易所",
        "outboundTag": "香港固定节点",
        "enabled": False,
    },
    {
        "remarks": "UDP 443阻断",
        "outboundTag": "block",
        "enabled": False,
    },
    {
        "remarks": "国内直连",
        "outboundTag": "direct",
        "enabled": True,
    },
    {
        "remarks": "最终代理",
        "outboundTag": "proxy",
        "enabled": True,
    },
]

SENSITIVE_FIELD_NAMES = {
    "password",
    "passwd",
    "uuid",
    "token",
    "apikey",
    "secret",
    "secretkey",
    "privatekey",
    "subscription",
    "subscriptionurl",
    "username",
    "serveraddress",
}

PROXY_LINK_RE = re.compile(
    r"\b(?:vmess|vless|trojan|ss|ssr)://",
    re.IGNORECASE,
)

HTTP_URL_RE = re.compile(
    r"https?://",
    re.IGNORECASE,
)

UUID_RE = re.compile(
    r"\b[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-"
    r"[89ab][0-9a-f]{3}-[0-9a-f]{12}\b",
    re.IGNORECASE,
)


def normalize_field_name(name):
    return name.replace("-", "").replace("_", "").lower()


def scan_sensitive_values(value, location, errors):
    if isinstance(value, dict):
        for key, child in value.items():
            normalized_key = normalize_field_name(str(key))

            if (
                normalized_key in SENSITIVE_FIELD_NAMES
                and child not in (None, "", [], {})
            ):
                errors.append(
                    f"{location}.{key}: contains a field that may expose "
                    "private credentials"
                )

            scan_sensitive_values(
                child,
                f"{location}.{key}",
                errors,
            )

    elif isinstance(value, list):
        for index, child in enumerate(value):
            scan_sensitive_values(
                child,
                f"{location}[{index}]",
                errors,
            )

    elif isinstance(value, str):
        if PROXY_LINK_RE.search(value):
            errors.append(
                f"{location}: contains a proxy sharing link"
            )

        if HTTP_URL_RE.search(value):
            errors.append(
                f"{location}: contains an unexpected HTTP or HTTPS URL"
            )

        if UUID_RE.search(value):
            errors.append(
                f"{location}: contains a UUID-like credential"
            )


def validate_string_list(rule, field, position, errors):
    if field not in rule:
        return

    value = rule[field]

    if not isinstance(value, list):
        errors.append(
            f"Rule {position} field '{field}' must be a list"
        )
        return

    valid_values = []

    for item_index, item in enumerate(value, start=1):
        if not isinstance(item, str) or not item.strip():
            errors.append(
                f"Rule {position} field '{field}' item "
                f"{item_index} must be a non-empty string"
            )
        else:
            valid_values.append(item)

    if len(valid_values) != len(set(valid_values)):
        errors.append(
            f"Rule {position} field '{field}' contains duplicates"
        )


def validate_rules(rules):
    errors = []

    if not isinstance(rules, list):
        return ["The root JSON value must be an array"]

    if len(rules) != len(EXPECTED_RULES):
        errors.append(
            f"Expected {len(EXPECTED_RULES)} rules, "
            f"but found {len(rules)}"
        )

    seen_remarks = set()

    for index, rule in enumerate(rules):
        position = index + 1

        if not isinstance(rule, dict):
            errors.append(
                f"Rule {position} must be a JSON object"
            )
            continue

        for required_field in (
            "remarks",
            "outboundTag",
            "enabled",
        ):
            if required_field not in rule:
                errors.append(
                    f"Rule {position} is missing "
                    f"'{required_field}'"
                )

        remarks = rule.get("remarks")

        if not isinstance(remarks, str) or not remarks.strip():
            errors.append(
                f"Rule {position} must have a non-empty remarks value"
            )
        elif remarks in seen_remarks:
            errors.append(
                f"Rule {position} duplicates remarks '{remarks}'"
            )
        else:
            seen_remarks.add(remarks)

        outbound_tag = rule.get("outboundTag")

        if (
            not isinstance(outbound_tag, str)
            or not outbound_tag.strip()
        ):
            errors.append(
                f"Rule {position} must have a non-empty outboundTag"
            )

        if "enabled" in rule and not isinstance(
            rule["enabled"],
            bool,
        ):
            errors.append(
                f"Rule {position} field 'enabled' must be true or false"
            )

        if "port" in rule and not isinstance(rule["port"], str):
            errors.append(
                f"Rule {position} field 'port' must be a string"
            )

        if "network" in rule:
            network = rule["network"]

            if not isinstance(network, str):
                errors.append(
                    f"Rule {position} field 'network' must be a string"
                )
            else:
                protocols = {
                    item.strip()
                    for item in network.split(",")
                    if item.strip()
                }

                if not protocols:
                    errors.append(
                        f"Rule {position} has an empty network value"
                    )
                elif not protocols.issubset({"tcp", "udp"}):
                    errors.append(
                        f"Rule {position} has unsupported network "
                        f"value '{network}'"
                    )

        validate_string_list(
            rule,
            "domain",
            position,
            errors,
        )
        validate_string_list(
            rule,
            "ip",
            position,
            errors,
        )

        if index < len(EXPECTED_RULES):
            expected = EXPECTED_RULES[index]

            for field, expected_value in expected.items():
                actual_value = rule.get(field)

                if actual_value != expected_value:
                    errors.append(
                        f"Rule {position} field '{field}' must be "
                        f"{expected_value!r}, found {actual_value!r}"
                    )

    valid_rule_objects = [
        rule for rule in rules if isinstance(rule, dict)
    ]

    udp_rules = [
        rule
        for rule in valid_rule_objects
        if rule.get("remarks") == "UDP 443阻断"
    ]

    if len(udp_rules) == 1:
        udp_rule = udp_rules[0]

        if udp_rule.get("port") != "443":
            errors.append(
                "UDP 443阻断 must use port '443'"
            )

        if udp_rule.get("network") != "udp":
            errors.append(
                "UDP 443阻断 must use network 'udp'"
            )

    final_rules = [
        rule
        for rule in valid_rule_objects
        if rule.get("remarks") == "最终代理"
    ]

    if len(final_rules) != 1:
        errors.append(
            "Exactly one 最终代理 rule must exist"
        )

    if rules and isinstance(rules[-1], dict):
        final_rule = rules[-1]

        if final_rule.get("remarks") != "最终代理":
            errors.append(
                "The final rule must be 最终代理"
            )

        final_network = final_rule.get("network", "")
        final_protocols = {
            item.strip()
            for item in final_network.split(",")
            if item.strip()
        }

        if final_protocols != {"tcp", "udp"}:
            errors.append(
                "最终代理 must cover both tcp and udp"
            )

    scan_sensitive_values(
        rules,
        "$",
        errors,
    )

    return errors


def main():
    if len(sys.argv) > 2:
        print(
            "Usage: python scripts/validate_rules.py "
            "[path-to-rules.json]"
        )
        return 2

    default_path = (
        Path(__file__).resolve().parents[1]
        / "rules"
        / "v2rayn-routing-rules.json"
    )

    rules_path = (
        Path(sys.argv[1])
        if len(sys.argv) == 2
        else default_path
    )

    try:
        with rules_path.open(
            "r",
            encoding="utf-8-sig",
        ) as file:
            rules = json.load(file)
    except FileNotFoundError:
        print(f"ERROR: Rules file not found: {rules_path}")
        return 1
    except json.JSONDecodeError as error:
        print(
            "ERROR: Invalid JSON at "
            f"line {error.lineno}, column {error.colno}: "
            f"{error.msg}"
        )
        return 1
    except OSError as error:
        print(f"ERROR: Unable to read {rules_path}: {error}")
        return 1

    errors = validate_rules(rules)

    if errors:
        print(
            f"ERROR: Ruleset validation failed with "
            f"{len(errors)} problem(s):"
        )

        for error in errors:
            print(f"- {error}")

        return 1

    print(
        f"OK: validated {len(rules)} routing rules "
        f"in {rules_path}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
