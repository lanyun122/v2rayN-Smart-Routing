# Changelog

本文件记录 v2rayN Smart Routing 的重要版本变化。

版本号遵循语义化版本规则：

- 补丁与兼容性修复：`v0.1.1`
- 新增功能或规则：`v0.2.0`
- 经过充分验证的稳定版本：`v1.0.0`

## [Unreleased]

### Added

- 新增 `CONTRIBUTING.md`，说明问题报告、规则设计、隐私保护和 Pull Request 要求。
- 新增 `SECURITY.md` 和 GitHub 私密漏洞报告入口。
- 新增兼容性故障与规则调整两类 Issue 表单。
- 新增仓库级 `AGENTS.md`，约束编程代理的修改范围和验证要求。
- 新增 `scripts/validate_rules.py` 规则验证脚本。
- 新增 GitHub Actions 自动验证工作流。

### Changed

- README 新增自动验证说明和工作流状态徽章。

## [0.1.0] - 2026-09-30

### Added

- 发布首个公开的 v2rayN 智能分流规则集。
- 提供局域网直连和私有地址直连。
- 提供常见广告域名过滤。
- 提供 GPT、Gemini 和流媒体自定义出口规则。
- 提供交易所固定出口规则。
- 提供可选的 UDP 443 阻断规则。
- 提供中国大陆域名和 IP 直连。
- 提供未命中特殊规则时的最终代理。
- 提供 GitHub Raw URL 导入方式。
- 提供持续更新地址和固定版本地址。

### Defaults

- GPT、Gemini、流媒体和交易所规则默认关闭。
- 局域网直连、广告过滤、UDP 443阻断、国内直连和最终代理默认启用。
- 自定义出口名称仅作为占位符，不包含任何节点、订阅或认证信息。

### Verified

- 基于 v2rayN v7.20.4（Windows x64）制作。
- GitHub Raw URL 可以正常访问。
- 已完成 v2rayN URL 导入测试。
- 导入后可以正确显示 9 条规则。

[Unreleased]: https://github.com/lanyun122/v2rayN-Smart-Routing/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/lanyun122/v2rayN-Smart-Routing/releases/tag/v0.1.0
