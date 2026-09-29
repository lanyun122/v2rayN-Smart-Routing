# v2rayN Smart Routing

[![License](https://img.shields.io/github/license/lanyun122/v2rayN-Smart-Routing)](LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/lanyun122/v2rayN-Smart-Routing?style=social)](https://github.com/lanyun122/v2rayN-Smart-Routing/stargazers)

A maintainable routing-rules project for v2rayN, focused on predictable traffic separation, documented outbound bindings, versioned releases, and reproducible validation.

面向 v2rayN 用户的可维护智能分流规则集，提供局域网直连、广告过滤、AI 与流媒体专用出口、交易所固定出口、国内直连和最终代理等规则。

> [!IMPORTANT]
> 本项目只提供路由规则和使用文档，不提供节点、订阅、住宅代理、账号或任何认证信息。

## 项目状态

> [!NOTE]
> 项目正在准备首个公开版本。规则文件、导入链接和完整安装文档将在测试完成后发布。

当前版本基于 **v2rayN v7.20.4（Windows x64）** 制作并完成测试。其他版本可能因界面、路由字段或核心行为不同而存在差异，具体兼容情况将记录在每个 Release 的说明中。

## 项目目标

本项目希望解决以下问题：

- 让局域网设备、打印机和私有地址保持直连。
- 拦截常见广告域名。
- 让 ChatGPT、Gemini 等 AI 服务使用指定的美国出口。
- 让常用流媒体使用指定的美国出口。
- 让交易所使用单独且固定的香港节点，减少频繁切换出口 IP。
- 让中国大陆网站和 IP 保持直连。
- 让未命中特殊规则的境外流量使用默认代理。
- 提供清晰、可验证、可版本化的导入方案。

## 规则顺序

路由规则按照从上到下的顺序匹配，先命中的规则优先生效。

| 优先级 | 规则 | 预期出口 |
|---:|---|---|
| 1 | 局域网直连 | `direct` |
| 2 | 广告过滤 | `block` |
| 3 | ChatGPT | 美国 AI/流媒体出口 |
| 4 | Gemini | 美国 AI/流媒体出口 |
| 5 | 流媒体 | 美国 AI/流媒体出口 |
| 6 | 交易所 | 固定香港节点 |
| 7 | UDP 443 阻断 | `block`，可选 |
| 8 | 国内直连 | `direct` |
| 9 | 最终代理 | `proxy` |

## 设计原则

### AI 与流媒体

ChatGPT、Gemini 和流媒体可以绑定到同一个美国出口或美国策略组。用户可以根据自己的节点情况完成本地绑定。

### 交易所

交易所规则建议绑定到一个固定的香港节点，不建议使用自动测速或频繁切换的策略组，以减少出口 IP 变化。

### 局域网

私有地址和局域网域名保持直连，避免代理影响打印机、路由器管理页面和其他本地设备。

### 可移植性

公开规则中不会写入维护者的私人节点名称、UUID、订阅地址、代理密码或住宅 IP 凭据。

## 快速开始

首个稳定版本发布后，本节将提供：

1. GitHub Release 下载方式。
2. Raw 订阅地址。
3. v2rayN 从 URL 导入规则的方法。
4. 专用 `outboundTag` 的本地绑定方法。
5. 导入后的验证步骤。
6. 常见错误和排查方法。

## 安全与隐私

公开提交前，请确认内容不包含：

- 节点分享链接
- 机场订阅地址
- UUID 或密码
- VPS 登录信息
- SSH 私钥
- 住宅代理凭据
- API Key
- 其他个人敏感信息

如果发现潜在的敏感信息或安全问题，请通过仓库 Issue 联系维护者，不要在公开 Issue 中直接粘贴密码或凭据。

## 反馈与贡献

如果你发现域名分流错误、规则冲突或版本兼容问题，可以前往：

- [提交 Issue](https://github.com/lanyun122/v2rayN-Smart-Routing/issues)
- [查看项目更新](https://github.com/lanyun122/v2rayN-Smart-Routing/commits/main)

提交问题时，请提供：

- v2rayN 版本
- 使用的核心及版本
- 相关规则名称
- 可公开的错误日志
- 预期结果和实际结果

请在提交前删除节点、UUID、订阅和代理认证信息。

## English Summary

This repository provides a maintainable routing-rules project for v2rayN users. Its planned scope includes LAN bypass, ad blocking, dedicated AI and media routing, stable exchange egress, China-direct routing, and a default proxy fallback.

The repository contains routing rules and documentation only. It does not provide proxy nodes, subscription services, residential proxies, user accounts, or credentials.

## License

本项目采用 [MIT License](LICENSE) 开源。

## Disclaimer

本项目是非官方社区项目，与 v2rayN、2dust、OpenAI 及任何代理服务商不存在隶属、授权或赞助关系。

请根据所在地法律法规以及相关服务条款合理使用本项目。维护者不对第三方服务的可用性、账号状态或网络质量作出保证。

如果这个项目确实帮助到了你，欢迎点一个 Star，方便以后找到更新，也能让维护者了解项目是否值得继续完善。
