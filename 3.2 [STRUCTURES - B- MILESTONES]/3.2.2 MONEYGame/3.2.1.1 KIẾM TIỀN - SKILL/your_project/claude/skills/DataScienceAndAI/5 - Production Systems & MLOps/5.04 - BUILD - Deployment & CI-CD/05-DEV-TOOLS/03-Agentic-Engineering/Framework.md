Để em nghiên cứu BMAD Method rồi so sánh với gstack cho anh.Em đã nghiên cứu xong cả hai. Đây là phân tích so sánh chi tiết:

---

## Điểm giống nhau cốt lõi

Cả gstack và BMAD đều xuất phát từ cùng một insight: **một AI agent chung chung cho ra kết quả tầm thường — tách thành nhiều vai trò chuyên biệt thì tốt hơn hẳn**. Cụ thể, cả hai đều dùng role-based personas (CEO, PM, Architect, QA...), đều cover full lifecycle từ planning đến shipping, đều open-source và free, và đều hướng tới việc AI là "collaborator" chứ không phải làm thay hoàn toàn.

## Khác nhau — và đây mới là phần quan trọng

**1. Triết lý: "Dao mổ" vs "Bệnh viện"**

gstack là con dao mổ — 8 skill, mỗi cái làm đúng một việc, gọi bằng slash command. Không có workflow engine, không có YAML config, không có dependency graph. Anh gõ `/review` thì nó review, `/ship` thì nó ship. Triết lý của Garry Tan là: "Tôi không cần framework, tôi cần tools sắc bén mà tôi điều khiển."

BMAD là cả bệnh viện — 12+ agents, 34+ workflows, có YAML-based blueprints định nghĩa sequence, dependencies, handoff points giữa các agent. Có "Party Mode" cho nhiều personas thảo luận trong một session. Triết lý: "Framework hướng dẫn bạn qua quy trình có cấu trúc để ra quyết định tốt hơn."

**2. Đối tượng người dùng**

gstack nhắm vào **founder/solo dev muốn ship nhanh**. Garry Tan dùng nó để cá nhân ông ship 100 PRs/tuần. Nó giả định người dùng đã biết mình muốn gì, chỉ cần AI thực thi theo đúng "cognitive mode."

BMAD nhắm vào **team dev cần quy trình chặt chẽ**, đặc biệt phù hợp với brownfield projects (codebase có sẵn). Nó guide người dùng qua từng bước, hỏi ngược lại, buộc suy nghĩ kỹ trước khi hành động.

**3. Orchestration: Manual vs Automated**

gstack dùng **Conductor pattern** — chạy 10+ Claude Code sessions song song, mỗi cái isolated workspace riêng, nhưng **con người quyết định** session nào làm gì. Không có auto-handoff.

BMAD có **workflow engine thực sự** — định nghĩa task sequence, dependencies, auto-handoff giữa agents. PM agent xong thì tự chuyển sang Architect agent, rồi sang Developer agent. Tuy nhiên, trong thực tế developers phản hồi rằng auto-handoff [vẫn còn nhiều vấn đề](https://github.com/bmad-code-org/BMAD-METHOD/issues/446) — agent bỏ qua documents quan trọng, không follow links.

**4. Platform support**

gstack: **chỉ Claude Code**. Đây là thiết kế có chủ đích — tận dụng sâu Claude Code's skill system.

BMAD: **cross-platform** — Claude Code, Cursor, Windsurf, GitHub Copilot. Dùng Markdown-based prompts làm "universal interface" nên chạy được trên nhiều AI IDE.

**5. Scope và complexity**

gstack: ~8 files markdown, cài bằng một dòng lệnh, chạy ngay. Repo có 5 commits.

BMAD: ecosystem lớn với extensions (BMad Builder, Test Architect, Game Dev Studio, Creative Intelligence Suite), 40.6K stars, 124 contributors, documentation site riêng. Cài qua NPM, cần Node.js v20+.

**6. Điểm yếu đã biết**

gstack: context window có thể bị đầy khi chain nhiều skills liên tiếp. Không có automated workflow — mọi thứ manual.

BMAD: code review workflow [ép tìm tối thiểu 3 issues](https://github.com/bmad-code-org/BMAD-METHOD/issues/1332) ngay cả khi code tốt, gây "review fatigue." Dev agent đôi khi ignore documents quan trọng. Framework nặng hơn nên learning curve cao hơn.

## Tóm lại

|Tiêu chí|gstack|BMAD|
|---|---|---|
|Triết lý|Tools sắc bén, người dùng điều khiển|Framework có cấu trúc, AI hướng dẫn|
|Agents|8 skills|12+ agents + 34+ workflows|
|Orchestration|Manual (Conductor)|Semi-automated (YAML workflows)|
|Platform|Claude Code only|Cross-platform|
|Cài đặt|1 dòng paste|NPM install + config|
|Phù hợp với|Solo founder, ship nhanh|Team, quy trình agile chặt|
|Community|4K stars, 3 contributors|40.6K stars, 124 contributors|

**Nhận định của em:** Nếu anh là founder/solo dev muốn tốc độ và kiểm soát trực tiếp, gstack phù hợp hơn. Nếu anh cần orchestrate một team hoặc project phức tạp cần quy trình rõ ràng từ ideation đến deployment, BMAD mạnh hơn ở mặt structure. Hai cái không loại trừ nhau — có thể lấy ý tưởng role-based của gstack kết hợp workflow discipline của BMAD.

---

Sources:

- [gstack GitHub](https://github.com/garrytan/gstack)
- [BMAD Method GitHub](https://github.com/bmad-code-org/BMAD-METHOD)
- [BMAD Documentation](https://docs.bmad-method.org/)
- [BMAD Issue #446 - Agent coordination feedback](https://github.com/bmad-code-org/BMAD-METHOD/issues/446)
- [BMAD Issue #1332 - Code review forces minimum 3 issues](https://github.com/bmad-code-org/BMAD-METHOD/issues/1332)
- [SitePoint: gstack analysis](https://www.sitepoint.com/gstack-garry-tan-claude-code/)
- [Augment Code: Best Spec-Driven Development Tools 2026](https://www.augmentcode.com/tools/best-spec-driven-development-tools)
- [Comparative Analysis: BMAD vs GitHub Spec Kit](https://medium.com/@mariussabaliauskas/a-comparative-analysis-of-ai-agentic-frameworks-bmad-method-vs-github-spec-kit-edd8a9c65c5e)